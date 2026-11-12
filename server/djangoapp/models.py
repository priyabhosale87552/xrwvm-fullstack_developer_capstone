from django.conf import settings
from django.db import models


class Review(models.Model):
    dealership_id = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def name(self):
        return self.user.get_full_name() or self.user.get_username()

    def __str__(self):
        return f"Review for dealer {self.dealership_id} by {self.name}"
