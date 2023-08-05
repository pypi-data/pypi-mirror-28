import json as json_handler
import traceback
from balebot.utils.logger import Logger

from balebot.filters import DefaultFilter
from balebot.handlers import Handler, CommandHandler, MessageHandler
from balebot.models.base_models import Response
from balebot.models.base_models.fat_seq_update import FatSeqUpdate
from balebot.models.factories import server_update_factory


class Dispatcher:
    def __init__(self, bot, bale_futures, timeout, incoming_queue=None, outgoing_queue=None):

        self.logger = Logger.get_logger()

        self.bot = bot
        self._bale_futures = bale_futures
        self.timeout = timeout

        self.incoming_queue = incoming_queue
        self.outgoing_queue = outgoing_queue

        self.message_handlers = []
        self.error_handlers = []
        self.read_handler_object = None
        self.default_handler_object = None

        self.conversation_next_step_handlers = {}
        self.conversation_data = {}

        self.running = False

    async def run(self):

        self.running = True

        while self.running:
            try:
                update_message = await self.incoming_queue.get()
                update_message_data = update_message.data
                update_message_json = json_handler.loads(update_message_data)

                self.process_update(update_message_json)

            except Exception as ex:
                self.logger.error(ex)

                traceback.print_exc()
                bot_timeout_json = {"body": {"tag": "CLIENT_INTERNAL_ERROR"}}
                error_response = Response(bot_timeout_json)
                self.dispatch_error(error_response, ex)

    def stop(self):
        self.running = False

    def process_update(self, update_json):

        update = server_update_factory.ServerUpdateFactory.create_update(update_json)

        if isinstance(update, Response):
            response_id = update.id
            bale_future = self.find_future(response_id)

            if not bale_future:
                return

            update.create_body(bale_future.response_body_module, bale_future.response_body_class)
            if update.is_bot_error():
                bale_future.reject(update)
                return
            bale_future.resolve(update)
            return

        elif isinstance(update, FatSeqUpdate):
            if update.is_message_update():
                user_peer = update.get_effective_user()
                user_id = user_peer.peer_id

                message_handled = False

                if (user_id in self.conversation_next_step_handlers) and self.conversation_next_step_handlers.get(
                        user_id, None):

                    default_conversation_handler = None

                    for handler in self.conversation_next_step_handlers.get(user_id, None):

                        if not handler.is_default_handler():
                            try:
                                if handler.check_update(update):
                                    handler.handle_update(self, update)
                                    message_handled = True
                                    break
                            except Exception as ex:
                                self.logger.error(ex)
                                traceback.print_exc()

                                try:
                                    bot_timeout_json = {"body": {"tag": "CLIENT_INTERNAL_ERROR"}}
                                    error_response = Response(bot_timeout_json)
                                    self.dispatch_error(error_response, ex)
                                except Exception as ex:
                                    self.logger.error(ex)
                                    traceback.print_exc()
                        else:
                            default_conversation_handler = handler

                    if (not message_handled) and default_conversation_handler:
                        if default_conversation_handler.check_update(update):
                            default_conversation_handler.handle_update(self, update)

                else:

                    for handler in self.message_handlers:
                        try:
                            if handler.check_update(update):
                                handler.handle_update(self, update)
                                message_handled = True
                                break
                        except Exception as ex:
                            self.logger.error(ex)
                            traceback.print_exc()

                            try:
                                bot_timeout_json = {"body": {"tag": "CLIENT_INTERNAL_ERROR"}}
                                error_response = Response(bot_timeout_json)
                                self.dispatch_error(error_response, ex)
                            except Exception as ex:
                                self.logger.error(ex)
                                traceback.print_exc()

                    if (not message_handled) and self.default_handler_object:
                        if self.default_handler_object.check_update(update):
                            self.default_handler_object.handle_update(self, update)
                return

            elif update.is_read_update():
                if self.read_handler_object:
                    try:
                        if self.read_handler_object.check_update(update):
                            self.read_handler_object.handle_update(self, update)
                    except Exception as ex:
                        self.logger.error(ex)
                        traceback.print_exc()

                        try:
                            bot_timeout_json = {"body": {"tag": "CLIENT_INTERNAL_ERROR"}}
                            error_response = Response(bot_timeout_json)
                            self.dispatch_error(error_response, ex)
                        except Exception as ex:
                            self.logger.error(ex)
                            traceback.print_exc()

    def add_handler(self, handler):
        if isinstance(handler, Handler):
            if handler.is_default_handler():
                self.default_handler_object = handler
            else:
                self.message_handlers.append(handler)

    def add_handlers(self, handlers):
        if isinstance(handlers, list):
            for handler in handlers:
                self.add_handler(handler)
        else:
            self.add_handler(handlers)

    def remove_handler(self, handler):
        self.message_handlers.remove(handler)

    def add_error_handler(self, handler):
        self.error_handlers.append(handler)

    def add_error_handlers(self, handlers):
        if isinstance(handlers, list):
            self.error_handlers += handlers
        else:
            self.error_handlers.append(handlers)

    def remove_error_handler(self, handler):
        self.error_handlers.remove(handler)

    def dispatch_error(self, update, error):
        for error_handler in self.error_handlers:
            error_handler(self.bot, update, error)

    def find_future(self, response_id):
        for i in range(len(self._bale_futures)):
            if self._bale_futures[i].request_id == response_id:
                return self._bale_futures.pop(i)

    def message_handler(self, filters):
        def decorator(callback_func):
            handler = MessageHandler(filters, callback_func)
            self.add_handler(handler)

            return callback_func

        return decorator

    def command_handler(self, commands, include_template_response=False):
        def decorator(callback_func):
            handler = CommandHandler(commands, callback_func, include_template_response)
            self.add_handler(handler)

            return callback_func

        return decorator

    def default_handler(self):
        def decorator(callback_func):
            handler = MessageHandler(DefaultFilter(), callback_func)
            self.add_handler(handler)

            return callback_func

        return decorator

    def error_handler(self):
        def decorator(callback_func):
            self.add_error_handler(callback_func)

            return callback_func

        return decorator

    def register_conversation_next_step_handler(self, update, handlers):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():

            next_step_handlers = []

            if isinstance(handlers, list):
                for handler in handlers:
                    if isinstance(handler, Handler):
                        next_step_handlers.append(handler)
            elif isinstance(handlers, Handler):
                next_step_handlers.append(handlers)

            user_peer = update.get_effective_user()
            user_id = user_peer.peer_id

            if user_id in self.conversation_next_step_handlers:
                self.conversation_next_step_handlers[user_id].clear()
                self.conversation_next_step_handlers[user_id] += next_step_handlers
            else:
                self.conversation_next_step_handlers[user_id] = next_step_handlers

    def conversation_finished(self, update):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            user_peer = update.get_effective_user()
            user_id = user_peer.peer_id
            return user_id not in self.conversation_next_step_handlers and user_id not in self.conversation_data

    def finish_conversation(self, update):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            user_peer = update.get_effective_user()
            user_id = user_peer.peer_id

            if user_id in self.conversation_next_step_handlers:
                self.conversation_next_step_handlers.pop(user_id)

            if user_id in self.conversation_data:
                self.conversation_data.pop(user_id)

    def set_conversation_data(self, update, key, value):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            user_peer = update.get_effective_user()
            user_id = user_peer.peer_id

            if user_id in self.conversation_data:
                new_dict_element = {key: value}
                if isinstance(self.conversation_data[user_id], dict):
                    self.conversation_data[user_id].update(new_dict_element)
            else:
                self.conversation_data[user_id] = {key: value}

    def get_conversation_data(self, update, key):
        if isinstance(update, FatSeqUpdate) and update.is_message_update():
            user_peer = update.get_effective_user()
            user_id = user_peer.peer_id

            if user_id in self.conversation_data:
                if isinstance(self.conversation_data[user_id], dict):
                    return self.conversation_data[user_id].get(key, None)
            else:
                return None
