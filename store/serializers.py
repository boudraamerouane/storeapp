from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Debt, PaidDebt, Purchase, Worker, WorkerWage,Expense, DailyRecord

# store/serializers.py

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class CustomerSerializer(serializers.ModelSerializer):
    total_debts = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    remaining_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'total_debts', 'total_paid', 'remaining_balance']


class DebtSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Debt
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}  # ✅ mark as read-only
        }


class PaidDebtSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = PaidDebt
        fields = '__all__'
        extra_kwargs = {
                'user': {'read_only': True}  # ✅ mark as read-only
            }

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
        extra_kwargs = {
                'user': {'read_only': True}  # ✅ mark as read-only
            }

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
        extra_kwargs = {
                'user': {'read_only': True}  # ✅ mark as read-only
            }

class WorkerWageSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source="worker.name", read_only=True)

    class Meta:
        model = WorkerWage
        fields = '__all__'
        extra_kwargs = {
                'user': {'read_only': True}  # ✅ mark as read-only
            }


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        extra_kwargs = {
                'user': {'read_only': True}  # ✅ mark as read-only
            }



class DailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecord
        fields = [
            'id', 'date', 'depart', 'bn', 'pc', 'liquide', 'sarf',
            'purchases', 'customer_debts', 'workers_wages',
            'expenses', 'debts_paid', 'total'
        ]
        read_only_fields = [
            'purchases', 'customer_debts', 'workers_wages',
            'expenses', 'debts_paid', 'total'
        ]

    def create(self, validated_data):
        # Automatically set the user from the request
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
