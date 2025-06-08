from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404
from . import models
from . import serializers
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from django.db.models import Q


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


@api_view(['GET'])
def get_user_games(request: Request, pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = pk)
    except models.UserProfile.DoesNotExist:
        raise Http404()
    
    games = models.Game.objects.filter(
        Q(player_x=user) | Q(player_o=user)
    ).order_by("-id")
    serializer = serializers.GameSerializer(games, many = True)

    return Response(serializer.data, status = HTTP_200_OK)

@api_view(['POST'])
def create_game(request: Request, pk_player_x, pk_player_o, format = None):
    try:
        player_o = models.UserProfile.objects.get(pk = pk_player_o)
        player_x = models.UserProfile.objects.get(pk = pk_player_x)
    except:
        raise Http404()
    
    data = request.data.copy()
    data['player_o'] = player_o.pk
    data['player_x'] = player_x.pk

    
    serializer = serializers.GameSerializer(data = data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)