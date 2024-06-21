import uuid
from django.db import models
from django.contrib.auth.models import User


class user(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=30)


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open_date = models.CharField(max_length=12)
    city = models.CharField(max_length=25)
    type = models.CharField(max_length=20)
    break_point_1 = models.IntegerField()
    break_point_2 = models.IntegerField()
    break_point_3 = models.IntegerField()
    break_point_4 = models.IntegerField()
    break_point_5 = models.IntegerField()
    break_point_6 = models.IntegerField()
    break_point_7 = models.IntegerField()
    break_point_8 = models.IntegerField()
    break_point_9 = models.IntegerField()
    break_point_10 = models.IntegerField()
    break_point_11 = models.IntegerField()
    break_point_12 = models.IntegerField()
    predicted_revenue = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.user} on {self.open_date}"