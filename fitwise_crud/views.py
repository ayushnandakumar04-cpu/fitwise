from django.shortcuts import render
from django.contrib.auth.models import User
from fitwise_crud.models import Foodlog
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from fitwise_crud.serializers import UserSerializer,FoodSerializer
from rest_framework import authentication,permissions
from rest_framework.response import Response
from django.db.models import Sum,Count
from fitwise_crud.permissions import IsFoodlogOwner
# Create your views here.
class SignupRegisterView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            qs=User.objects.create_user(**cleaned_data)
            serializer_instant=UserSerializer(qs)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
class GetMeView(APIView):
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user

        qs=User.objects.get(username=auth_user)

        serializer_instance=UserSerializer(qs)

        return Response(data=serializer_instance.data)
    
class FoodListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        qs=Foodlog.objects.filter(owner=request.user)
        serializer_instance=FoodSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=FoodSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class FoodListRetrieveView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsFoodlogOwner]

    def get(self,request,pk=None):
        qs=get_object_or_404(Foodlog,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance=FoodSerializer(qs)
        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):
         instance=get_object_or_404(Foodlog,id=pk)
         self.check_object_permissions(request,instance)
         form_data=request.data
         serializer_instance=FoodSerializer(data=form_data,instance=instance)
         if serializer_instance.is_valid(): 
             serializer_instance.save()
             return Response(
                 serializer_instance.data)
         else:
            return Response(serializer_instance.errors)
          

    def delete(self,request,pk=None):
         instance=get_object_or_404(Foodlog,id=pk)
         self.check_object_permissions(request,instance)
         instance.delete()
         return Response({"message": "Expense deleted successfully"})



class FoodSummaryView(APIView):

    def get(self, request):

        food_logs = Foodlog.objects.filter(
            owner=request.user
        )

        total_calories = food_logs.aggregate(
            total=Sum("calories")
        )["total"] or 0

        total_meals = food_logs.count()

        meal_summary = food_logs.values(
            "meal_type"
        ).annotate(
            total_calories=Sum("calories"),count=Count("id")
        )

        return Response({
            "total_calories": total_calories,
            "total_meals": total_meals,
            "meal_summary": meal_summary
        })   

