from rest_framework import serializers
from .models import Post, Comment
from accounts.models import User

# 기본 serializer
class PostBaseSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
    view_count = serializers.IntegerField()
    writer = serializers.IntegerField() # 모델에서는 foreign_key
    bad_post = serializers.BooleanField() # 모델에 없는 기능

    # 단점: creat, update가 없음
    # create 추가
    def create(self, validated_data):
        post = Post.objects.create(
            content = validated_data['content'],
            view_count = validated_data['view_count'],
            # writer = validated_data['writer'], # 값이 1,
            writer = User.objects.get(id=validated_data['writer'])
        )
        return post
        # return Post.objects.create(validated_data)

# ModelSerializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' #['id', 'content']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'