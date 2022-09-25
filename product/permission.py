from rest_framework.permissions import  BasePermission, SAFE_METHODS

class UpdateOrDelete(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.shop.user == request.user


class IsShopOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        print({
            "shop owner ":obj.shop.user,
            'shop owner': request.user
        })
        # Instance must have an attribute named `owner`.
        return obj.shop.user == request.user