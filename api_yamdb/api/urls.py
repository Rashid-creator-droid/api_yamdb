from django.urls import path
from .views import UserView, UserViewDetail, MeViewDetail, SignUp, TokenView

urlpatterns = [
    path('v1/users/', UserView.as_view()),
    path('v1/users/me/', MeViewDetail.as_view()),                                   
    path('v1/users/<username>/', UserViewDetail.as_view()),
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', TokenView.as_view())
]
