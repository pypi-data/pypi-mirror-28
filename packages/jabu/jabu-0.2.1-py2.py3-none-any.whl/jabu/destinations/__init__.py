import logging

handlers = {}


def backupdestination(id):
    def register(handler_class):
        logging.debug("Adding destination '%s' as '%s'" % (handler_class, id))
        handlers[id] = handler_class
        return handler_class

    return register
