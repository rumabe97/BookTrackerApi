import json
import traceback

from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from apiErrors.models import ApiErrorLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class ApiErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        errorMessage = str(exception)
        errorTraceback = ''.join(traceback.format_exception(None, exception, exception.__traceback__))
        ipAddress = get_client_ip(request)
        userAgent = request.META.get('HTTP_USER_AGENT', '')
        referer = request.META.get('HTTP_REFERER', '')
        method = request.method
        url = request.build_absolute_uri()
        queryParams = request.GET.dict() if request.GET else None
        statusCode = getattr(exception, 'error_code', 500)

        try:
            requestData = request.body.decode('utf-8') if request.body else None
        except Exception:
            requestData = None

        ApiErrorLog.objects.create(
            error_message=errorMessage,
            error_traceback=errorTraceback,
            url=url,
            method=method,
            ip_address=ipAddress,
            user_agent=userAgent,
            referer=referer,
            query_params=json.dumps(queryParams),
            request_data=requestData,
            status_code=statusCode,
            timestamp=now(),
        )
