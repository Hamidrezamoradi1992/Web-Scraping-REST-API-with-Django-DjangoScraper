from django.utils import timezone

from apps.core.models import DailyVisit


class DailyVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        today = timezone.now().date()
        # ignore admin path:
        if "/admin" not in request.path:
            ips=request.META['REMOTE_ADDR']
            users=request.user
            visit= DailyVisit.objects.create(date=today,url=request.path,ip_address=ips,user=users)
        return self.get_response(request)