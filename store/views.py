from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import generics

from .models import Customer, Debt, PaidDebt, Purchase, Worker, WorkerWage, Expense,DailyRecord
from .serializers import (
    CustomerSerializer, DebtSerializer, PaidDebtSerializer,
    PurchaseSerializer, WorkerSerializer, WorkerWageSerializer, ExpenseSerializer, DailyRecordSerializer   
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
    
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Your account has been deleted."}, status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)

class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return Debt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)

class PaidDebtViewSet(viewsets.ModelViewSet):
    queryset = PaidDebt.objects.all()
    serializer_class = PaidDebtSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return PaidDebt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return Purchase.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return Worker.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)


class WorkerWageViewSet(viewsets.ModelViewSet):
    queryset = WorkerWage.objects.all()
    serializer_class = WorkerWageSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return WorkerWage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by("-date")
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Only return expenses of the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save with the logged-in user
        serializer.save(user=self.request.user)


class DailyRecordViewSet(viewsets.ModelViewSet):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return daily records of the logged-in user
        return DailyRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Check if record already exists for this user and date
        date = serializer.validated_data["date"]
        if DailyRecord.objects.filter(user=self.request.user, date=date).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"date": "You already have a daily record for this date."})

        serializer.save(user=self.request.user)
