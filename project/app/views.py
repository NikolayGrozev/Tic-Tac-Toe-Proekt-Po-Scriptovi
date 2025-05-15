from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404
from . import models
from . import serializers
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK


@api_view(['GET'])
def get_users(request):
    users = models.UserProfile.objects.all()
    serializer = serializers.UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def add_friend(request: Request, user_pk, friend_pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = user_pk)
        friend = models.UserProfile.objects.get(pk = friend_pk)
    except models.UserProfile.DoesNotExist:
        Http404()
    

    user.friends.add(friend)
    userSerializer = serializers.UserSerializer(user, many = False)

    return Response(userSerializer.data, status = HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_friend(request: Request, user_pk, friend_pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = user_pk)
        friend = models.UserProfile.objects.get(pk = friend_pk)
    except models.UserProfile.DoesNotExist:
        Http404()

    user.friends.remove(friend)
    userSerializer = serializers.UserSerializer(user)

    return Response(userSerializer.data, status = HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user(request : Request, format = None):
    serializer = serializers.UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = HTTP_201_CREATED)
    return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def user(request: Request, pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = pk)
    except models.UserProfile.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        serializer = serializers.UserSerializer(user, many = False)
        return Response(serializer.data, status = HTTP_200_OK)
    
    
    elif request.method == 'PUT':
        serializer = serializers.UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_200_OK)
        return Response(serializer.errors, stauts = HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

# class UsersView(APIView):
#     def get_users(self, request):
#         users = models.User.objects.all()
#         serializer = serializers.UserSerializer(users, many = True)
#         return Response(serializer.data)
    
#     def get_user(self, request, pk):
#         try:
#             user = models.User.objects.get(pk = pk)
#             serializer = serializers.UserSerializer(user, many = False)
#             return Response(serializer.data)
#         except user.DoesNotExist:
#             raise Http404()
        
#     def post(self, request, format = None):
#         serializer = serializers.UserSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = HTTP_201_CREATED)
#         return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk, format = None):
#         try:
#             user = models.User.objects.get(pk = pk)
#             serializer = serializers.UserSerializer(user, data = request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, stauts = HTTP_400_BAD_REQUEST)
#         except:
#             raise Http404()
    
#     def delete(self, request, pk, format = None):
#         try:
#             user = models.User.objects.get(pk = pk)
#             user.delete()
#             return Response(status=HTTP_204_NO_CONTENT)
#         except user.DoesNotExist:
#             raise Http404()