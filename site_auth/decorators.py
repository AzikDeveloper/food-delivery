from rest_framework.response import Response
from rest_framework import status


def login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return Response(data={
                'detail': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
