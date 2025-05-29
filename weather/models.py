from django.db import models
from django.contrib.auth.models import User
from django.db.models import Index

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        indexes = [
            Index(fields=['name']),
            Index(fields=['country']),
        ]
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}, {self.country}"




class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, db_index=True)
    search_date = models.DateTimeField(auto_now_add=True, db_index=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    search_count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['search_date']
        indexes = [
            Index(fields=['-search_date']),
            Index(fields=['user', '-search_date']),
            Index(fields=['session_key', '-search_date']),
        ]
        verbose_name_plural = "search histories"

    def __str__(self):
        return f"{self.city} searched at {self.search_date}"