from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
import requests
from packaging import version
from shared.GoogleDriveVersions import get_latest_version
from shared.googleBookApi import healthcheckApi
from rest_framework.views import APIView
from shared.mixins import APIKeyPermission

class Healthcheck(APIView):
    def get_permissions(self):
        return [APIKeyPermission()]

    def get(self, request):
        userVersion = request.GET.get('version', None)

        health_status = {
            "database": "ok",
            "google_books_api": "ok",
            "status": "healthy"
        }

        try:
            db_conn = connections['default']
            db_conn.cursor()
        except OperationalError:
            health_status["database"] = "error"
            health_status["status"] = "unhealthy"

        try:
            isActive = healthcheckApi()
            if not isActive:
                health_status["google_books_api"] = "error"
                health_status["status"] = "unhealthy"
        except requests.exceptions.RequestException:
            health_status["google_books_api"] = "error"
            health_status["status"] = "unhealthy"

        if userVersion:
            latest_version, latest_file_id = get_latest_version()

            if version.parse(userVersion) < version.parse(latest_version):
                download_url = f'https://drive.google.com/uc?id={latest_file_id}'
                health_status.update({
                    'outdated': True,
                    'latest_version': latest_version,
                    'download_url': download_url
                })
            else:
                health_status.update({
                    'outdated': False,
                    'latest_version': latest_version
                })
        else:
            health_status['outdated'] = None
            health_status['latest_version'] = 'N/A'
            health_status['download_url'] = None
        return JsonResponse(health_status, status=200 if health_status["status"] == "healthy" else 500)
