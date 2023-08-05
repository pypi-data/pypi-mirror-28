from zope.interface import Interface, implementer, Attribute


class IHandleExceptionEvent(Interface):
    """Event fired when handling an exception."""

    request = Attribute('The current request')


@implementer(IHandleExceptionEvent)
class HandleExceptionEvent(object):

    def __init__(self, request):
        self.request = request
