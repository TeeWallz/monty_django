from django.http import HttpResponse


class HealthCheckMiddleware:
    """Answer /health before any host validation runs.

    The special yoink proxy sends a probe with the container name as the Host header,
    which would otherwise fail ALLOWED_HOSTS and return 4XX.
    This returns success early so we don't hit any of that other middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health":
            return HttpResponse("ok")
        return self.get_response(request)
