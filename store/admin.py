from django.contrib import admin
from .models import Customer, Debt, PaidDebt, Purchase, Worker, WorkerWage,DailyRecord

admin.site.register(Customer)
admin.site.register(Debt)
admin.site.register(PaidDebt)
admin.site.register(Purchase)
admin.site.register(Worker)
admin.site.register(WorkerWage)
admin.site.register(DailyRecord)
