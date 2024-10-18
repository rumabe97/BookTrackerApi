import uuid

from django.db import models


class ApiErrorLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    error_message = models.TextField()
    error_traceback = models.TextField(blank=True, null=True)
    url = models.URLField()
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    request_data = models.TextField(blank=True, null=True)
    query_params = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referer = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
