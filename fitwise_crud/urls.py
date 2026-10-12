from django.urls import path
from fitwise_crud.views import SignupRegisterView,FoodListCreateView,GetMeView,FoodListRetrieveView,FoodSummaryView
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns =[
    path('signup/',SignupRegisterView.as_view()),

    path('Me/',GetMeView.as_view()),

    path('food/',FoodListCreateView.as_view()),
    path('food/<int:pk>/',FoodListRetrieveView.as_view()),
    path('summary/',FoodSummaryView.as_view()),

    path('token/',ObtainAuthToken.as_view())
]