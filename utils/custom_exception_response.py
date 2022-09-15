# this file designs every error that is going out into one a well strucutre response


from rest_framework.views import exception_handler
from .custom_response import structure_responseDict


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    ExceptionClassNameThatRaisingTheError =exc.__class__.__name__

    DictOfErrorHandlers = {
            "ValidationError":_ValidationError,
            "AuthenticationFailed":_AuthenticationFailed,
            "Http404":_Http404,
            "NotAuthenticated":_NotAuthenticated,
            'ValueError':_ValueError
    }   
    # Now add the HTTP status code to the response.
    "this gives Us Control of the Error Class Response to Alter"
    if response is not None and DictOfErrorHandlers.get(ExceptionClassNameThatRaisingTheError,None) is not None:
        response.data= DictOfErrorHandlers[ExceptionClassNameThatRaisingTheError](exc,context,response)

    return response

def _ValueError(exc,context,response):
    return structure_responseDict(
        msg="Value Error",data=response.data,
        status_code=response.status_code,success=False)
def _ValidationError(exc,context,response):
    # return {**response.data,'status_code':response.status_code,'success':False}
    return structure_responseDict(
        msg="Validation Error",data=response.data,
        status_code=response.status_code,success=False)
    
def _NotAuthenticated(exc,context,response):
    return structure_responseDict(
        msg="Please Login",
        data=response.data,
         status_code=response.status_code,success=False
        
    )

def _AuthenticationFailed(exc,context,response):
    return structure_responseDict(
        msg=response.data['detail'],status_code=response.status_code,success=False)
    
def _Http404(exc,context,response):

    return structure_responseDict(
        msg=response.data['detail'],status_code=response.status_code,success=False)
    