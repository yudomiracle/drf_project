from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Post
from .serializers import PostSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter(author=request.user.author)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method in ['PUT', 'DELETE']:
        if post.author != request.user:
            return Response({'error': f'You do not have permission to {request.method.lower()} this post.'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def authenticate_user(request):
    try:
        user = request.data
        login = user['username']
        password = user['password']
        user = authenticate(request, username=login, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            return Response({
                'refresh': str(token),
                'access': str(token.access_token)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

    except (User.DoesNotExist, KeyError) as e:
        print(e)
        return Response(status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

            login(request, user)

            return Response({'message': 'User registered and logged in successfully'})
        else:
            return Response(serializer.errors, status=400)

    return Response({'message': 'Register page'})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                'refresh': str(refresh),
                'access': str(access),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

    except KeyError as e:
        return Response({'error': f'Missing key: {str(e)}'}, status=400)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'User logged out successfully'})


