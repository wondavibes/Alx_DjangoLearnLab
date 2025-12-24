# posts/urls.py
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView
from django.urls import path

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("feed/", FeedView.as_view(), name="post-feed"),
    path("posts/<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("posts/<int:pk>/unlike/", UnlikePostView.as_view(), name="unlike-post"),
]

urlpatterns += router.urls
