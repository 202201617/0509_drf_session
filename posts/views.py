# posts > views.py
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from .models import Post, Comment
from .serializers import *

class PostAPIView(APIView): # CBV
    def post(self, request): #post 요청 받았을 때, post, put, get 다 됨
        # request: 프론트에서 넘어오는 모든 데이터가 담아져있음
        serializer = PostBaseSerializer(data = request.data) #데이터를 통해 받음 / 번역 과정
        if serializer.is_valid(): # 유효성 검사
            if serializer.validated_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save() # save하려면 유효성 검사 필요
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostAPIView2(APIView):
    def post(self, request):
        serializer = PostSerializer(data = request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            if serializer.initial_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                print(serializer.data)
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 과제2: 전체 게시글 목록 가져오는 로직 구현하기(method: get, url: api/posts/list, CBV: APIView)
class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializers = PostSerializer(posts, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    # 405 Method Not Allowed로 인해 생성, 얘가 없어도 전체 게시글 목록이 뜨긴 함
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 과제3: 특정 Post에 Comment를 다는 로직 구현하기(method: post, url: api/posts/comment/, CBV or FBV)
class PostComment(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def PostAPI_FBV(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response({"message": "post success"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListCreateMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)

class PostListCreateGeneric(generics.ListCreateAPIView):
    queryset = Post.objects.all() # post의 모든 것을 가지고 논다...?
    serializer_class = PostSerializer # 번역기를 정해놓는다.

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)
    
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer    