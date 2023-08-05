import functools
import logging
import signal


def handle_signal(server, ioloop, signum, frame):
    logging.info("Received signal {}; shutting down...".format(signum))

    def stop_ioloop():
        logging.info("Stopping IOLoop")
        ioloop.stop()

    def stop_server():
        logging.info("Stopping HTTPServer")
        server.stop()
        ioloop.call_later(2, stop_ioloop)

    ioloop.add_callback_from_signal(stop_server)


def on_sigterm(server, ioloop):
    signal.signal(signal.SIGTERM, functools.partial(handle_signal, server, ioloop))
