from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, DebtViewSet, PaidDebtViewSet,
    PurchaseViewSet, WorkerViewSet, WorkerWageViewSet,
    ExpenseViewSet, DailyRecordViewSet,
    RegisterView, DeleteAccountView, UserDetailView
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'debts', DebtViewSet, basename='debts')
router.register(r'paiddebts', PaidDebtViewSet, basename='paiddebts')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'workers', WorkerViewSet, basename='workers')
router.register(r'wages', WorkerWageViewSet, basename='wages')
router.register(r'dailyrecords', DailyRecordViewSet, basename='dailyrecords')
router.register(r'expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),

    # 🔑 Auth-related endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    
]
