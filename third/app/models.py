from django.db import models

class LoginInfo(models.Model):
    douban_id = models.CharField(max_length=50, blank=True)
    weibo_id = models.CharField(max_length=50, blank=True)
    qzone_id = models.CharField(max_length=50, blank=True)