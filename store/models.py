from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')  # ✅ Each user can have "Ali"

    def __str__(self):
        return self.name

    @property
    def total_debts(self):
        return self.debts.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def total_paid(self):
        return self.paiddebts.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def remaining_balance(self):
        return self.total_debts - self.total_paid


class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    customer = models.ForeignKey(Customer, related_name='debts', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer} - {self.amount} on {self.date}"


class PaidDebt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    customer = models.ForeignKey(Customer, related_name='paiddebts', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    note = models.TextField(blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        remaining = self.customer.remaining_balance
        if self.pk:  # when updating, adjust old value
            old = PaidDebt.objects.get(pk=self.pk)
            remaining += old.amount
        if self.amount > remaining:
            raise ValidationError("Amount paid exceeds customer's remaining balance.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} paid {self.amount} on {self.date}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    item = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.item} - {self.amount} on {self.date}"


class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('user', 'name')  # ✅ Each user can have "Ahmed"

    def __str__(self):
        return self.name


class WorkerWage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    worker = models.ForeignKey(Worker, related_name='wages', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    note = models.TextField(blank=True)




class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    # User-entered values
    depart = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    liquide = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sarf = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date')
        ]

    @property
    def purchases(self):
        return Purchase.objects.filter(user=self.user, date=self.date).aggregate(total=Sum("price"))["total"] or 0

    @property
    def customer_debts(self):
        return Debt.objects.filter(user=self.user, date=self.date).aggregate(total=Sum("amount"))["total"] or 0

    @property
    def debts_paid(self):
        return PaidDebt.objects.filter(user=self.user, date=self.date).aggregate(total=Sum("amount"))["total"] or 0

    @property
    def workers_wages(self):
        return WorkerWage.objects.filter(user=self.user, date=self.date).aggregate(total=Sum("amount"))["total"] or 0

    @property
    def expenses(self):
        return Expense.objects.filter(user=self.user, date=self.date).aggregate(total=Sum("amount"))["total"] or 0

    @property
    def total(self):
        return (
            self.expenses
            + self.workers_wages
            + self.customer_debts
            + self.purchases
            + self.liquide
            + self.sarf
            - self.depart
            - self.debts_paid
        )

    def __str__(self):
        return f"Daily Record {self.date} - {self.user.username}"
