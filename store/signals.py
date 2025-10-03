from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from .models import DailyRecord, Debt, PaidDebt, Purchase, WorkerWage, Expense


def update_daily_record(user, date):
    """Recalculate all sums for a given user+date and update/create DailyRecord"""
    daily_record, _ = DailyRecord.objects.get_or_create(user=user, date=date)

    daily_record.customer_debts = (
        Debt.objects.filter(user=user, date=date).aggregate(total=Sum("amount"))["total"] or 0
    )
    daily_record.debts_paid = (
        PaidDebt.objects.filter(user=user, date=date).aggregate(total=Sum("amount"))["total"] or 0
    )
    daily_record.purchases = (
        Purchase.objects.filter(user=user, date=date).aggregate(total=Sum("price"))["total"] or 0
    )
    daily_record.workers_wages = (
        WorkerWage.objects.filter(user=user, date=date).aggregate(total=Sum("amount"))["total"] or 0
    )
    daily_record.expenses = (
        Expense.objects.filter(user=user, date=date).aggregate(total=Sum("amount"))["total"] or 0
    )

    daily_record.save()


# 🔹 Debt
@receiver([post_save, post_delete], sender=Debt)
def update_on_debt_change(sender, instance, **kwargs):
    update_daily_record(instance.user, instance.date)


# 🔹 PaidDebt
@receiver([post_save, post_delete], sender=PaidDebt)
def update_on_paiddebt_change(sender, instance, **kwargs):
    update_daily_record(instance.user, instance.date)


# 🔹 Purchase
@receiver([post_save, post_delete], sender=Purchase)
def update_on_purchase_change(sender, instance, **kwargs):
    update_daily_record(instance.user, instance.date)


# 🔹 WorkerWage
@receiver([post_save, post_delete], sender=WorkerWage)
def update_on_workerwage_change(sender, instance, **kwargs):
    update_daily_record(instance.user, instance.date)


# 🔹 Expense
@receiver([post_save, post_delete], sender=Expense)
def update_on_expense_change(sender, instance, **kwargs):
    update_daily_record(instance.user, instance.date)
