import logging
import os
import socket
import sys
import threading
import time
import traceback
from concurrent import futures
from threading import Thread

import grpc

from sdk.softfire.grpc import messages_pb2_grpc, messages_pb2
from sdk.softfire.grpc.messages_pb2 import Empty
from sdk.softfire.utils import get_config

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _receive_forever(manager_instance):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=int(manager_instance.get_config_value('system', 'server_threads', '5'))))
    messages_pb2_grpc.add_ManagerAgentServicer_to_server(_ManagerAgent(manager_instance), server)
    binding = '[::]:%s' % manager_instance.get_config_value('messaging', 'bind_port')
    logging.info("Start listening on %s" % binding)
    server.add_insecure_port(binding)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logging.info("Shutting down gRPC")
        server.stop(0)
        return
    except:
        traceback.print_exc()
        logging.warning("Did not receive ctrl-c...")
        logging.debug("Stopping server")
        server.stop(0)
        _receive_forever(manager_instance)
    finally:
        logging.info("Finished serve forever...")


def _register(config_file_path):
    time.sleep(1)
    channel = grpc.insecure_channel(
        '%s:%s' % (get_config("system", "experiment_manager_ip", config_file_path),
                   get_config("system", "experiment_manager_port", config_file_path)))
    stub = messages_pb2_grpc.RegistrationServiceStub(channel)
    response = stub.register(
        messages_pb2.RegisterMessage(name=get_config("system", "name", config_file_path),
                                     endpoint="%s:%s" % (
                                         get_config("system", "ip", config_file_path),
                                         get_config("messaging", "bind_port", config_file_path)),
                                     description=get_config("system", "description", config_file_path)))
    logging.debug("Manager received registration response: %s" % response.result)


def _unregister(config_file_path):
    channel = grpc.insecure_channel(
        '%s:%s' % (get_config("system", "experiment_manager_ip", config_file_path),
                   get_config("system", "experiment_manager_port", config_file_path)))
    stub = messages_pb2_grpc.RegistrationServiceStub(channel)
    response = stub.unregister(
        messages_pb2.UnregisterMessage(name=get_config("system", "name", config_file_path),
                                       endpoint="%s:%s" % (
                                           get_config("system", "ip", config_file_path),
                                           get_config("messaging", "bind_port", config_file_path))))
    logging.debug("Manager received unregistration response: %s" % response.result)


def handle_error(e):
    traceback.print_exc()
    if hasattr(e, "message"):
        return messages_pb2.ResponseMessage(result=messages_pb2.ERROR, error_message=e.message)
    if hasattr(e, "args"):
        return messages_pb2.ResponseMessage(result=messages_pb2.ERROR, error_message=str(e.args))
    return messages_pb2.ResponseMessage(result=messages_pb2.ERROR, error_message="No message available")


class _ManagerAgent(messages_pb2_grpc.ManagerAgentServicer):
    def delete_user(self, request, context):
        try:
            self.abstract_manager.delete_user(request)
            return Empty()
        except Exception as e:
            return handle_error(e)

    def heartbeat(self, request, context):
        return Empty()

    def __init__(self, abstract_manager):
        """
        create the ManagerAgent in charge of dealing with the dispatch of messages
        :param abstract_manager: the Implementation of AbstractManager
         :type abstract_manager: AbstractManager
        """
        self.abstract_manager = abstract_manager

    def create_user(self, request, context):
        try:
            return self.abstract_manager.create_user(request)
        except Exception as e:
            return handle_error(e)

    def refresh_resources(self, request, context):
        try:
            resources = self.abstract_manager.refresh_resources(user_info=request)
            response = messages_pb2.ListResourceResponse(resources=resources)
            return messages_pb2.ResponseMessage(result=messages_pb2.Ok, list_resource=response)
        except Exception as e:
            return handle_error(e)

    def execute(self, request, context):
        if request.method == messages_pb2.LIST_RESOURCES:
            try:
                return messages_pb2.ResponseMessage(result=messages_pb2.Ok,
                                                    list_resource=messages_pb2.ListResourceResponse(
                                                        resources=self.abstract_manager.list_resources(
                                                            user_info=request.user_info,
                                                            payload=request.payload)))
            except Exception as e:
                return handle_error(e)
        if request.method == messages_pb2.PROVIDE_RESOURCES:
            try:
                return messages_pb2.ResponseMessage(result=messages_pb2.Ok,
                                                    provide_resource=messages_pb2.ProvideResourceResponse(
                                                        resources=[messages_pb2.Resource(content=r) for r in
                                                                   self.abstract_manager.provide_resources(
                                                                       user_info=request.user_info,
                                                                       payload=request.payload)]))
            except Exception as e:
                return handle_error(e)
        if request.method == messages_pb2.RELEASE_RESOURCES:
            try:
                self.abstract_manager.release_resources(user_info=request.user_info, payload=request.payload)
                return messages_pb2.ResponseMessage(result=messages_pb2.Ok)
            except Exception as e:
                return handle_error(e)

        if request.method == messages_pb2.VALIDATE_RESOURCES:
            try:
                self.abstract_manager.validate_resources(user_info=request.user_info, payload=request.payload)
                return messages_pb2.ResponseMessage(result=messages_pb2.Ok)
            except Exception as e:
                return handle_error(e)


def _is_ex_man__running(ex_man_bind_ip, ex_man_bind_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ex_man_bind_ip, int(ex_man_bind_port)))
    sock.close()
    return result == 0


def __print_banner(banner_file_path):
    if not os.path.isfile(banner_file_path):
        logging.error('Not printing banner since the file {} does not exist.'.format(banner_file_path))
        return
    with open(banner_file_path, 'r') as banner_file:
        banner = banner_file.read()
        print(banner)


def start_manager(manager_instance):
    """
    Start the ExperimentManager
    :param manager_instance: the instance of the Manager
    """
    if manager_instance.get_config_value('system', 'banner-file', '') != '':
        __print_banner(manager_instance.get_config_value('system', 'banner-file', ''))
    logging.info("Starting %s Manager." % manager_instance.get_config_value('system', 'name'))

    if manager_instance.get_config_value("system", "wait_for_em", "true").lower() == "true":
        while not _is_ex_man__running(manager_instance.get_config_value("system", "experiment_manager_ip", "localhost"),
                                      manager_instance.get_config_value("system", "experiment_manager_port", "5051")):
            time.sleep(2)

    event = threading.Event()
    listen_thread = ExceptionHandlerThread(target=_receive_forever, args=[manager_instance], event=event)
    register_thread = ExceptionHandlerThread(target=_register, args=[manager_instance.config_file_path], event=event)

    listen_thread.start()
    register_thread.start()

    while True:
        try:
            time.sleep(30)
            continue
        except InterruptedError:
            traceback.print_exc()
            _going_down(event, listen_thread, register_thread)
            break
        except KeyboardInterrupt:
            logging.info("Received ctrl-c...")
            _unregister(manager_instance.config_file_path)
            _going_down(event, listen_thread, register_thread)
            break

    return


def _going_down(event, listen_thread, register_thread):
    logging.info("going down...")
    event.set()
    if listen_thread.is_alive():
        listen_thread.join(timeout=5)
    if register_thread.is_alive():
        register_thread.join(timeout=3)


class ExceptionHandlerThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None, event=None):

        if sys.version_info > (3, 0):
            super().__init__(group, target, name, args, kwargs, daemon=daemon)
        else:
            super(self.__class__, self).__init__(group, target, name, args, kwargs, daemon=daemon)
        self.exception = None
        self.event = event
        self._target = target
        self._args = args

    def run(self):
        while True:
            if not self.event.is_set():
                try:
                    self._target(*self._args)
                    return
                except KeyboardInterrupt:
                    logging.info("received ctrl-c")
                    return
                except:
                    logging.error("Received exception in thread")
                    traceback.print_exc()
                    logging.debug("Trying to restart...")
                    time.sleep(1)
