from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import CustomUser

# Create your models here.
class expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense_name} - {self.amount}"