"""
Atmosphere web helper methods..

"""

from django.contrib.auth.models import User as DjangoUser
from django.core.context_processors import csrf

from atmosphere.logger import logger
from django.contrib.auth.models import User as DjangoUser
from core.models import Provider, Identity
from core.models.euca_key import Euca_Key

def prepareDriver(request, provider_id, identity_id):
    """
    TODO: Cache driver based on specific provider
    return esh_driver
    """
    from service.api import getEshDriver
    username = extractUser(request).username
    core_provider = Provider.objects.get(id=provider_id)
    core_identity = Identity.objects.get(id=identity_id)
    esh_driver = getEshDriver(core_provider, core_identity, username)
    return esh_driver

def extractUser(request):
    if request and request.session:
        username = request.session.get('username',None)
    if not username and request and request.META:
        username = request.META.get('username',None)
    if not username:
        username='esteve'
    return DjangoUser.objects.get_or_create(username=username)[0]

def getRequestParams(request):
    """
    Extracts paramters from GET/POST in a Django Request object
    """
    if request.META['REQUEST_METHOD'] == 'GET':
        try:
            #Will only succeed if a GET method with items
            return dict(request.GET.items())
        except:
            pass
    elif request.META['REQUEST_METHOD'] == 'POST':
        try:
            #Will only succeed if a POST method with items
            return dict(request.POST.items())
        except:
            pass
    logger.debug("REQUEST_METHOD is neither GET or POST.")

def getRequestVars(request):
    """
    Extracts parameters from a Django Request object
    Expects ALL or NOTHING. You cannot mix data!
    """

    username = None
    token = None
    api_server = None
    emulate = None
    try:
        #Attempt #1 - SessionStorage - Most reliable
        logger.debug(request.session.items())
        username = request.session['username']
        token = request.session['token']
        api_server = request.session['api_server']
        emulate = request.session.get('emulate',None)
        return {'username':username, 'token':token, 'api_server':api_server, 'emulate': emulate}
    except KeyError, missing:
        pass
    try:
        #Attempt #2 - Header/META values, this is DEPRECATED as of v2!
        logger.debug(request.META.items())
        username = request.META['HTTP_X_AUTH_USER']
        token = request.META['HTTP_X_AUTH_TOKEN']
        api_server = request.META['HTTP_X_API_SERVER']
        emulate = request.META.get('HTTP_X_AUTH_EMULATE',None)
        return {'username':username, 'token':token, 'api_server':api_server, 'emulate': emulate}
    except KeyError, missing:
        pass
    try:
        #Final attempt - GET/POST values
        params = getRequestParams(request)
        logger.debug(params.items())
        username = params['HTTP_X_AUTH_USER']
        token = params['HTTP_X_AUTH_TOKEN']
        api_server = params['HTTP_X_API_SERVER']
        emulate = params.get('HTTP_X_AUTH_EMULATE',None)
        return {'username':username, 'token':token, 'api_server':api_server, 'emulate': emulate}
    except KeyError, missing:
        pass
    return None