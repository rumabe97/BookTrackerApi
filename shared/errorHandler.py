from django.http import JsonResponse
import logging


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, StripeChargeError):
            logging.error(f"StripeChargeError: {exception.message}, Code: {exception.error_code}")

            return JsonResponse({
                'error': 'StripeChargeError',
                'message': exception.message,
                'status_code': exception.error_code,
                'solution': 'Please verify your card details or contact support.'
            }, status=exception.error_code)

        # logging.error(f"Unhandled exception: {str(exception)}")
        return JsonResponse({
            'error': 'UnhandledException',
            'message': str(exception),
            'status_code': 500
        }, status=500)


class StripeChargeError(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
