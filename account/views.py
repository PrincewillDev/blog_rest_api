from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResgisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


 
# Create your views here.

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            

            
            res = Response()
            res.data = {'success':True}
            
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            print(access_token)
            return res
        
        except Exception as e:
            return Response({
                'success':False,
                "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            res = Response()
            res.data = {'refreshed':True}
            
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res

        except InvalidToken as e:
            return Response({
                'message':'Invalid Token',
                "refreshed": "Failed",
                'detail': str(e),
                'status': status.HTTP_401_UNAUTHORIZED,
            }, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            return Response({
                "message": str(e),
                "refreshed": "Failed",
                "status": status.HTTP_401_UNAUTHORIZED,
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "message": "Unexpected Error",
                "refreshed": "Failed",
                "detail": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

@api_view(['POST'])
def logout(request):
    try:
        res = Response()
        res.data = {'success':True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except:
        return Response({'success':False})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = ResgisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'messages': 'Error occured when registering user'
                }, status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            
            return Response({
                'message': 'Account Created Successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error':str(e),
                'message': 'Error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

#  Just to check if the user is authenticated or not (Temporary View function)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated':True})
