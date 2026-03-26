from django.db import models

class StockPrice(models.Model):
    symbol = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stock_prices'
        ordering = ['-fetched_at']
        indexes = [
            models.Index(fields=['symbol']),
        ]
        
    def __str__(self):
        return f"{self.symbol} - {self.price}"
    
    