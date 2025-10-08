from django.db import models

class MonthlyBudget(models.Model):
    # month in YYYY-MM format stored as string for simplicity, or use year+month ints
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        unique_together = ('year', 'month')


    def __str__(self):
        return f"Budget {self.year}-{self.month:02d}: {self.amount}"
    
    class Meta:
        db_table = 'monthly_budgets'
        