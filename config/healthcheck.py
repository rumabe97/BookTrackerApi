from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
import requests

from shared.googleBookApi import healthcheckApi


def healthcheck(request):
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

    return JsonResponse(health_status, status=200 if health_status["status"] == "healthy" else 500)
