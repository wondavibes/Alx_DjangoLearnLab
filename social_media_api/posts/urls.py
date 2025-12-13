# posts/urls.py
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.urls import path

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("feed/", PostViewSet.as_view({"get": "feed"}), name="post-feed"),
]
urlpatterns = router.urls
