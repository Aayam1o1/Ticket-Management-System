import os
import django
from django.utils import timezone

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticket_management.settings") 
django.setup()

from account.models import Role, Permission, User
from menu.models import Menu

def run():
    permissions_data = [
        ("can_create_ticket", "Allows user to can create ticket"),
        ("can_edit_ticket", "Allows user to can edit ticket"),
        ("can_view_ticket", "Allows user to can view ticket"),
        ("can_delete_ticket", "Allows user to can delete ticket"),
        ("can_manage_status", "Allows user to can manage status"),
        ("can_manage_priority", "Allows user to can manage priority"),
        ("can_manage_menu", "Allows user to can manage menu"),
        ("can_create_roles", "Allow user to create new roles"),
        ("can_manage_permissions", "Allow user to manage permissions"),
        
    ]

    for ptype, desc in permissions_data:
        Permission.objects.get_or_create(permission_type=ptype, defaults={"description": desc})

    # Roles
    roles_data = [
        ("Admin", [ "can_manage_permissions", "can_create_roles", "can_manage_menu", "can_manage_priority", "can_manage_status", "can_delete_ticket", "can_view_ticket", "can_edit_ticket", "can_create_ticket" ]),
        ("Agent", ["can_create_ticket", "can_view_ticket"]),
        ("Supervisor", ["can_edit_ticket", "can_view_ticket", "can_create_ticket", "can_manage_menu"]),
        ("normal", ["can_view_ticket"]),
    ]

    role_objs = {}
    for role_name, perms in roles_data:
        role, _ = Role.objects.get_or_create(name=role_name)
        for perm_type in perms:
            perm = Permission.objects.get(permission_type=perm_type)
            role.permissions.add(perm)
        role.save()
        role_objs[role_name] = role

    # Menus
    menu1, _ = Menu.objects.get_or_create(
    name="Menu Level 1",
    parent=None,
    defaults={"created_by": None, "created_at": timezone.now()}
)

    menu2, _ = Menu.objects.get_or_create(
        name="Menu Level 2",
        parent=menu1,
        defaults={"created_by": None, "created_at": timezone.now()}
    )

    menu3, _ = Menu.objects.get_or_create(
        name="Menu Level 3",
        parent=menu2,
        defaults={"created_by": None, "created_at": timezone.now()}
    )

    # Users
    users_data = [
    {
        "username": "admin",
        "email": "aayammaharjan5@gmail.com",
        "phone_number": "+9779840000000",
        "role": role_objs["Admin"],
        "is_staff": True,        
        "is_superuser": True,     
        "is_active": True,
        "password": "pass1234",
    },
    {
        "username": "agent",
        "email": "aayamaharjan5@gmail.com",
        "phone_number": "+9779840000000",
        "role": role_objs["Agent"],
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "password": "pass1234",
    },
    {
        "username": "normal",
        "email": "nopermission@gamil.com",
        "phone_number": "+9779840000000",
        "role": role_objs["normal"],
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "password": "pass1234",
    },
    {
        "username": "supervisor",
        "email": "supervisor@gamil.com",
        "phone_number": "+9779840000000",
        "role": role_objs["Supervisor"],
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "password": "pass1234",
    },
]

    for udata in users_data:
        user, created = User.objects.get_or_create(username=udata["username"], defaults={
            "email": udata["email"],
            "phone_number": udata["phone_number"],
            "role": udata["role"],
            "is_staff": udata.get("is_staff", False),
            "is_superuser": udata.get("is_superuser", False),
            "is_active": udata["is_active"],
        })
        if created:
            user.set_password(udata["password"])
            user.save()
        else:
            updated = False
            for field in ["email", "phone_number", "role", "is_staff", "is_superuser", "is_active"]:
                if getattr(user, field) != udata.get(field, getattr(user, field)):
                    setattr(user, field, udata.get(field, getattr(user, field)))
                    updated = True
            if updated:
                user.save()

    # Create superuser
    superuser_username = "superuser"
    superuser_email = "superuser@example.com"
    superuser_password = "superpass1234"
    if not User.objects.filter(username=superuser_username).exists():
        User.objects.create_superuser(
            username=superuser_username,
            email=superuser_email,
            password=superuser_password,
            phone_number="+9779840000000",
        )
        print(f"Superuser '{superuser_username}' created with password '{superuser_password}'")
    else:
        print(f"Superuser '{superuser_username}' already exists")

    print("Seed data including users created successfully!")


if __name__ == "__main__":
    run()
