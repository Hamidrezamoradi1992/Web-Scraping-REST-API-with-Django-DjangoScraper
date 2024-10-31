from django.utils import timezone

from apps.core.models import DailyVisit


class DailyVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_client_ip(request):
        return _.split(',')[0] if (_ := request.META.get('HTTP_X_FORWARDED_FOR')) else request.META.get('REMOTE_ADDR')

    @staticmethod
    def get_user(request):
        return (request.user.is_authenticated and request.user) or None
    def __call__(self, request):
        today = timezone.now().date()
        # ignore admin path:
        if "/admin" not in request.path:
            ips=request.META['REMOTE_ADDR']
            users=request.user
            visit= DailyVisit.objects.create(date=today,url=request.path,ip_address=self.get_client_ip(request),user=self.get_user(request))
        return self.get_response(request)