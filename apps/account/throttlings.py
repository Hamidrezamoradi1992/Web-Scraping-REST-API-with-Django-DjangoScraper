from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle


class VipThrottling(SimpleRateThrottle):
    scope = 'vip'
    def get_cache_key(self, request, view):
        print('throttle')
        print(request.user.name)
        if request.user and request.user.is_authenticated:
            ident = request.user.pk if request.user.is_superuser else self.get_ident(request)
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
