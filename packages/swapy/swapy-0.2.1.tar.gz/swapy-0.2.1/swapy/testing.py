from werkzeug.wrappers import Response
from werkzeug.test import Client


def client(app):
    """
    Returns the werkzeug Client class with the Response class

    :param app: callable
        The application function
    :return: Client
    """
    return Client(app, Response)
