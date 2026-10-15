from django.shortcuts import render
from django.contrib.auth.models import User
from fitwise_crud.models import Foodlog
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from fitwise_crud.serializers import UserSerializer,FoodSerializer
from rest_framework import authentication,permissions
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from fitwise_crud.ai_program import get_budget_plan
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
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):

        response_data={
            "total_today":0
        }
    
        cur_date=datetime.now().date()
        cur_month=datetime.now().month
        cur_year=datetime.now().year

        monthly_transactions=Foodlog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        if monthly_transactions:
            monthly_total=monthly_transactions.values("calories").aggregate(total=Sum("calories")).get("total")
            response_data["monthly_total"]=monthly_total

        todays_calorie=Foodlog.objects.filter(owner=request.user,created_at__date=cur_date)
        if todays_calorie:
            total_today=todays_calorie.values("calories").aggregate(total=Sum("calories")).get("total")
            #todays meal_type
            total_meal=todays_calorie.values("meal_type").annotate(total=Sum("calories"))
            response_data={"total_today":total_today}
            response_data={"total_meal_type":total_meal}
            #monthly

        return Response(data=response_data)

class DietPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get (self,request):
        user=request.user
        #monthly total

        curr_month=datetime.now().month
        curr_year=datetime.now().year
        response_data={"monthly_Expense_total":0}
        monthly_calories=Foodlog.objects.filter(owner=request.user,created_at__month=curr_month,created_at__year=curr_year)
        if monthly_calories:
            monthly_total=monthly_calories.values("calories").aggregate(total=Sum("calories")).get("total")
            response_data["monthly_total"]=monthly_total
            meal_type_summary=monthly_calories.values("meal_type").annotate(total=Sum("calories"))
            response_data["meal_type_summary"]=meal_type_summary  
            diet_plan=get_budget_plan(response_data) 
            response_data["plan"]=diet_plan
        return Response(response_data)
