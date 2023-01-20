from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, GenresViewSet, TitleViewSet

router = DefaultRouter()

router.register('category', CategoriesViewSet, basename='category')
router.register('genre', GenresViewSet, basename='genre')
router.register('title', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
]
