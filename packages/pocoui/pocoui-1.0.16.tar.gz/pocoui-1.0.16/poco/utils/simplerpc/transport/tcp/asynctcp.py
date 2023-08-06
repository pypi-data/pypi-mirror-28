from __future__ import print_function

import asyncore
import collections
import socket


LOOP_THREAD = None
MAX_MESSAGE_LENGTH = 4096


class BaseClient(asyncore.dispatcher):

    """base class for both local/remote client socket."""

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.outbox = collections.deque()
        self.inbox = ""
        self.closed = False

    def say(self, message):
        self.outbox.append(message)

    def writable(self):
        if self.connecting:  # is it a bug in asynccore? handle_connect_event triggered only when writable is True
            return True
        return bool(self.outbox)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        self.send(message)

    def handle_read(self):
        message = self.recv(MAX_MESSAGE_LENGTH)
        if message == b"":
            return
        self.inbox += message

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        print("Closed", self)
        self.closed = True

    def read_message(self, length=None):
        if length is None:
            message, self.inbox = self.inbox, ""
        else:
            message, self.inbox = self.inbox[:length], self.inbox[length:]
        return message


class RemoteClient(BaseClient):

    """Wraps a remote client socket."""

    def __init__(self, host, socket, address, cid=None):
        BaseClient.__init__(self)
        self.host = host
        self.cid = cid
        self.set_socket(socket)

    def handle_close(self):
        BaseClient.handle_close(self)
        self.host.close_client(self.cid)


class Host(asyncore.dispatcher):

    CLIENT_ID_COUNTER = 1
    CLIENT_MAX_COUNT = 10

    def __init__(self, address=('0.0.0.0', 5001)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(self.CLIENT_MAX_COUNT)
        print('server listening at', address)
        self.remote_clients = {}
        self.msg_queue = []

    def handle_accept(self):
        socket, addr = self.accept()  # For the remote client.
        print('Accepted client at %s', addr)
        client_id = self.__class__.CLIENT_ID_COUNTER
        self.__class__.CLIENT_ID_COUNTER += 1
        client = RemoteClient(self, socket, addr, client_id)
        self.remote_clients[client_id] = client
        print('connected clients', self.remote_clients)
        return client

    def swap_msg_queue(self):
        for client in self.remote_clients.values():
            message = client.read_message()
            self.msg_queue.append(message)

        msg_queue = self.msg_queue
        self.msg_queue = []
        return msg_queue

    def broadcast(self, message):
        print('Broadcasting message: %s' % len(message))
        for remote_client in self.remote_clients.values():
            remote_client.say(message)

    def say(self, client_id, message):
        self.remote_clients[client_id].say(message)

    def close_client(self, client_id):
        print('Closing client:', client_id, self.remote_clients)
        client = self.remote_clients.pop(client_id)
        return client


class Client(BaseClient):

    def __init__(self, host_address):
        BaseClient.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Connecting to host at:', host_address)
        self.connect(host_address)

    def handle_connect(self):
        print(self, " is connected")


def start_thread(target, *args, **kwargs):
    import threading
    t = threading.Thread(target=target, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    return t


def init_loop():
    global LOOP_THREAD
    if LOOP_THREAD and LOOP_THREAD.is_alive():
        print("LOOP_THREAD ALREADY STARTED: %s" % LOOP_THREAD)
    else:
        LOOP_THREAD = start_thread(asyncore.loop, timeout=0.001)


if __name__ == '__main__':
    h = Host()
    asyncore.loop()
