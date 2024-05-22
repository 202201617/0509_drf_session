from django.urls import path, include
from .views import *

# 정해진 방식
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('viewsets', PostModelViewSet)
                # url 주소

app_name = 'posts'

urlpatterns = [
    path('post/', PostAPIView.as_view()),
    # path('post/', PostAPIView2.as_view()),
    # path('post/', PostAPI_FBV),
    # path('list/', PostListAPIView.as_view()),
    # path('createOrlist/byMixin/', PostListCreateMixin.as_view()),
    # path('createOrlist/byGeneric/', PostListCreateGeneric.as_view()),
    path('', include(router.urls)),
    path('list/', PostList.as_view()),
    path('comment/', PostComment.as_view()),
]