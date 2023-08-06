import requests
import warnings
from zope import component
from zope.component.factory import Factory
from zope import interface
from zope.schema.fieldproperty import FieldProperty
from .interfaces import IRequest, IRequestResolver
from sparc.config import IConfigContainer


@interface.implementer(IRequest)
class Request(object):
    req_kwargs = FieldProperty(IRequest['req_kwargs'])
    gooble_warnings = FieldProperty(IRequest['gooble_warnings'])
    
    def __init__(self, **kwargs):
        self.req_kwargs = kwargs.get('req_kwargs', {})
        self.gooble_warnings = kwargs.get('gooble_warnings', False)
        self.requester = kwargs.get('requester', requests)
    
    def request(self, *args, **kwargs):
        kwargs_updated = self.req_kwargs.copy()
        kwargs_updated.update(kwargs)
        if self.gooble_warnings:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return self.requester.request(*args, **kwargs_updated)
        else:
            return self.requester.request(*args, **kwargs_updated)
requestFactory = Factory(Request)
SparcRequest = requestFactory()

@interface.implementer(IRequestResolver)
def request_resolver(**kwargs):
    """Resolve for a IRequest and return
    
    This will return a IRequest based on the following resolution order:
    1. 'request' is given in kwargs and provides IRequest
    2.  IRequest is available as a unnamed utility in zca
    3.  A new IRequest is created and returned
    """
    if 'request' in kwargs and IRequest.providedBy(kwargs['request']):
        return kwargs['request']
    sm = component.getSiteManager()
    return sm.queryUtility(IRequest, default=requestFactory())

@interface.implementer(IRequest)
@component.adapter(IConfigContainer)
class RequestFromConfigContainer(Request):
    """Adapts from the first RequestOptions found"""
    def __init__(self, context):
        self.context = context
        RequestOptions = context.mapping().get_value('RequestOptions', default={})
        super(RequestFromConfigContainer, self).__init__(**RequestOptions)
