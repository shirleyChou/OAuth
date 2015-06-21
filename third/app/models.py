from django.db import models

class login_info(models.Model):
	douban_id = models.CharField(max_length=50, blank=True)
	douban_username = models.CharField(max_length=50, blank=True)
	weibo_id = models.CharField(max_length=50, blank=True)
	weibo_username = models.CharField(max_length=50, blank=True)
	qzone_id = models.CharField(max_length=50, blank=True)
	qzone_username = models.CharField(max_length=50, blank=True)