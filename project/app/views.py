from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404
from . import models
from . import serializers
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_403_FORBIDDEN
from django.db.models import Q
from .utils import calculate_winner
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def get_users(request: Request):
    users = models.UserProfile.objects.all()
    serializer = serializers.UserSerializer(users, many = True)
    return Response(serializer.data)


@api_view(['POST'])
def create_user(request : Request, format = None):
    serializer = serializers.UserSerializer(data = request.data , many = False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = HTTP_201_CREATED)
    return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user(request: Request, pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = pk)
    except models.UserProfile.DoesNotExist:
        raise Http404()
    
    if request.user.profile.pk != user.pk:
        return Response(status=HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = serializers.UserSerializer(user, many = False)
        return Response(serializer.data, status = HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = serializers.UserSerializer(user, data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_200_OK)
        return Response(serializer.errors, stauts = HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    return Response(serializer.errors, stauts = HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_games(request: Request, pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = pk)
    except models.UserProfile.DoesNotExist:
        raise Http404()
    
    if request.method != 'GET':
        return Response(HTTP_400_BAD_REQUEST)
    
    if request.user.profile.pk != user.pk:
        return Response(status = HTTP_403_FORBIDDEN)
    
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
    except models.UserProfile.DoesNotExist:
        raise Http404()
    
    if request.method != 'POST':
        return Response(status=HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    data['player_o'] = player_o.pk
    data['player_x'] = player_x.pk

    
    serializer = serializers.GameSerializer(data = data, many = False)

    if serializer.is_valid():
        moves = data.get('moves', [])
        winner = calculate_winner(moves)
        serializer.validated_data['winner'] = winner


        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request: Request, pk_sent_to ,format = None):
    try:
        from_user = request.user.profile
        to_user = models.UserProfile.objects.get(pk = pk_sent_to)
    except models.UserProfile.DoesNotExist:
        raise Http404()\
    
    if from_user == to_user:
        return Response({"detail": "You can't send a friend request to yourself."}, status=HTTP_400_BAD_REQUEST)
    
    if models.FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({"detail": "Friend request already sent."}, status=HTTP_400_BAD_REQUEST)
    
    if to_user in from_user.friends.all():
        return Response({"detail": "You are already friends with this user"}, status=HTTP_400_BAD_REQUEST)
    

    data = {
        "from_user": from_user.pk,
        "to_user": to_user.pk
    }

    serializer = serializers.FriendRequestSerializer(data = data)
    
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(status=HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def respond_friend_request(request: Request, pk_frequest ,format = None):
    try:
        user = request.user.profile
        friend_request = models.FriendRequest.objects.get(pk = pk_frequest)
    except (models.UserProfile.DoesNotExist or  models.FriendRequest.DoesNotExist):
        raise Http404()
    
    if friend_request.to_user.pk != user.pk:
        return Response(status=HTTP_403_FORBIDDEN)

    if request.method == 'POST':

        user.friends.add(friend_request.from_user)
        friend_request.delete()

        return Response(status = HTTP_201_CREATED)
    
    elif request.method == 'DELETE':

        friend_request.delete()
        return Response(status = HTTP_204_NO_CONTENT)

    return Response(status = HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request: Request, format = None):
    user = request.user.profile

    friend_requests = models.FriendRequest.objects.filter(to_user=user).order_by('-id')

    serializer = serializers.FriendRequestSerializer(friend_requests, many=True)

    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request: Request, user_pk, friend_pk, format = None):
    try:
        user = models.UserProfile.objects.get(pk = user_pk)
        friend = models.UserProfile.objects.get(pk = friend_pk)
    except models.UserProfile.DoesNotExist:
        Http404()

    if request.user.profile.pk != user.pk:
        return Response(status=HTTP_403_FORBIDDEN)

    user.friends.remove(friend)
    userSerializer = serializers.UserSerializer(user)

    return Response(userSerializer.data, status = HTTP_204_NO_CONTENT)