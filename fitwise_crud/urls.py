from django.urls import path
from fitwise_crud.views import SignupRegisterView,FoodListCreateView,GetMeView,FoodListRetrieveView,FoodSummaryView
urlpatterns =[
    path('signup/',SignupRegisterView.as_view()),

    path('Me/',GetMeView.as_view()),

    path('food/',FoodListCreateView.as_view()),
    path('food/<int:pk>',FoodListRetrieveView.as_view()),
    path('summary/',FoodSummaryView.as_view())
]