from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, GenresViewSet, TitleViewSet, ReviewViewSet, CommentViewSet
from .views import UserView, UserViewDetail, MeViewDetail, SignUp, TokenView

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)
urlpatterns = [
    path('v1/users/', UserView.as_view()),
    path('v1/users/me/', MeViewDetail.as_view()),
    path('v1/users/<username>/', UserViewDetail.as_view()),
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls)),
]
