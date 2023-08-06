from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class BaseBlameModel(models.Model):
    created_by = models.ForeignKey(UserModel, related_name='+', on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(UserModel, related_name='+', on_delete=models.SET_NULL)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
