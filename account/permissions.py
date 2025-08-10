from rest_framework.permissions import BasePermission

class BaseRolePermission(BasePermission):
    """Base class for checking if a user's role has a specific permission."""
    required_permission = None  

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'role') or not user.role:
            return False
        return user.role.permissions.filter(permission_type=self.required_permission).exists()


# ===== Specific Permission Classes =====

class CanCreateTicket(BaseRolePermission):
    required_permission = "can_create_ticket"


class CanEditTicket(BaseRolePermission):
    required_permission = "can_edit_ticket"


class CanViewTicket(BaseRolePermission):
    required_permission = "can_view_ticket"


class CanDeleteTicket(BaseRolePermission):
    required_permission = "can_delete_ticket"


class CanManageStatus(BaseRolePermission):
    required_permission = "can_manage_status"


class CanManagePriority(BaseRolePermission):
    required_permission = "can_manage_priority"


class CanManageMenu(BaseRolePermission):
    required_permission = "can_manage_menu"
    

class CanManageRoles(BaseRolePermission):
    required_permission = "can_manage_roles"

class CanManagePermissions(BaseRolePermission):
    required_permission = "can_manage_permissions"


class IsAdminOrSupervisor(BasePermission):
    """
    Allows access only to users with role Admin or Supervisor.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        role = getattr(user, 'role', None)
        if role and role.name in ['Admin', 'Supervisor']:
            return True
        return False
    
    
class IsSelfOrAdminSupervisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role and user.role.name in ['Admin', 'Supervisor']:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role and user.role.name in ['Admin', 'Supervisor']:
            return True
        return obj == user