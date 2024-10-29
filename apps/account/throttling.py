from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle


class VipThrottling(UserRateThrottle):
    scope = 'vip'

    def get_cache_key(self, request, view):

        if request.user and request.user.is_authenticated and request.user.is_superuser:
            ident = request.user.pk
        else:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class UsersThrottle(UserRateThrottle):
    scope = 'users'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and not request.user.is_superuser:
            ident = request.user.pk
        else:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
