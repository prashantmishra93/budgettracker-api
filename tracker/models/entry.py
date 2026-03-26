from django.db import models
from django.utils import timezone
from .category import Category
from django.contrib.auth.models import User

# Entry is a database table name.
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=100, blank=True)


    CREATED_CHOICES = [('manual','manual'), ('import','import')]


    def is_income(self):
        return self.category.type == Category.INCOME


    def __str__(self):
        t = 'income' if self.is_income() else 'expense'
        return f"{t} {self.amount} on {self.date} -> {self.category.name}"
    
    class Meta:
        db_table = 'entries'