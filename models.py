from django.db import models

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    coin_symbol = models.CharField(max_length=10)
    scraped_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)