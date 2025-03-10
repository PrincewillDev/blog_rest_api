from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResgisterSerializer
from rest_framework.views import APIView
from rest_framework import status

 
# Create your views here.
class RegisterView(APIView):
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
            