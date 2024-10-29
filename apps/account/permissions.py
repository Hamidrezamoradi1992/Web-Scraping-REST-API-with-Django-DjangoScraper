from rest_framework.permissions import BasePermission
from.models import User

class VipPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated :
            print('vip permission')
            user=User.objects.get(id=request.user.id)
            return  bool(True if user.permissions_vip else False)
        return bool(False)
