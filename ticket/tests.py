import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from menu.models import Menu
from account.models import User, Role, Permission
from ticket.models import Ticket, TicketStatus, TicketPriority

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def ticket_status():
    return TicketStatus.objects.create(name="Open", weight=1)

@pytest.fixture
def ticket_priority():
    return TicketPriority.objects.create(name="High", weight=1)

@pytest.fixture
def menu_level_1():
    return Menu.objects.create(name="Menu Level 1")

@pytest.fixture
def menu_level_2(menu_level_1):
    return Menu.objects.create(name="Menu Level 2", parent=menu_level_1)

@pytest.fixture
def menu_level_3(menu_level_2):
    return Menu.objects.create(name="Menu Level 3", parent=menu_level_2)

@pytest.fixture
def permission_create_ticket():
    return Permission.objects.get_or_create(permission_type='can_create_ticket')[0]

@pytest.fixture
def permission_view_ticket():
    return Permission.objects.get_or_create(permission_type='can_view_ticket')[0]

@pytest.fixture
def permission_assign_ticket():
    return Permission.objects.get_or_create(permission_type='can_assign_ticket')[0]

@pytest.fixture
def role_agent(permission_create_ticket, permission_view_ticket):
    role = Role.objects.create(name="Agent")
    role.permissions.add(permission_create_ticket, permission_view_ticket)
    return role

@pytest.fixture
def role_admin(permission_assign_ticket, permission_create_ticket):
    role = Role.objects.create(name="Admin")
    role.permissions.add(permission_assign_ticket, permission_create_ticket)
    return role

@pytest.fixture
def user_admin(role_admin, menu_level_1):
    user = User.objects.create_user(username="admin", password="pass1234", role=role_admin)
    user.assigned_menus.add(menu_level_1)
    return user

@pytest.fixture
def user_regular(role_agent, menu_level_3):
    user = User.objects.create_user(username="user", password="pass1234", role=role_agent)
    user.assigned_menus.add(menu_level_3)
    return user



@pytest.mark.django_db
def test_ticket_creation(api_client, user_regular, menu_level_3, ticket_status, ticket_priority):
    api_client.force_authenticate(user=user_regular)
    data = {
        "title": "Test Ticket",
        "description": "This is a test",
        "status": ticket_status.id,
        "priority": ticket_priority.id,
        "menu": [menu_level_3.id]
    }
    url = reverse("ticket.api:ticket-create")
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Test Ticket"
    assert any(m['id'] == menu_level_3.id for m in response.data["menu_details"])

@pytest.mark.django_db
def test_ticket_list(api_client, user_admin, user_regular, menu_level_3, ticket_status, ticket_priority):
    ticket = Ticket.objects.create(
        created_by=user_admin,
        assigned_to=None,
        title="Ticket To Assign",
        description="Assign test",
        status=ticket_status,
        priority=ticket_priority,
    )
    ticket.menu.add(menu_level_3)
    user_regular.assigned_menus.add(menu_level_3)

    api_client.force_authenticate(user=user_regular)
    url = reverse("ticket.api:ticket-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert any(t["id"] == ticket.id for t in response.data)
    
@pytest.mark.django_db
def test_ticket_assign(api_client, user_admin, user_regular, ticket_status, ticket_priority, menu_level_1, menu_level_2, menu_level_3):
    user_admin.assigned_menus.add(menu_level_1, menu_level_2, menu_level_3)

    ticket = Ticket.objects.create(
        created_by=user_admin,
        title="Test Ticket",
        description="Assign test",
        status=ticket_status,
        priority=ticket_priority,
    )
    ticket.menu.add(menu_level_3)

    api_client.force_authenticate(user=user_admin)
    url = reverse("ticket.api:ticket-assign", args=[ticket.id])
    data = {"assigned_to": user_regular.id}
    response = api_client.patch(url, data, format="json")

    assert response.status_code in (200, 204)
    ticket.refresh_from_db()
    assert ticket.assigned_to == user_regular
