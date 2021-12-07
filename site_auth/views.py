from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .decorators import login_required


@api_view(['POST'])
@login_required
def logoutView(request):
    request.user.auth_token.delete()
    return Response(data={
        'detail': 'logged out'
    })
