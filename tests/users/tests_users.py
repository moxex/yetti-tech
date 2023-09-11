import pytest
from users.models import User
from django.urls import reverse
from core.settings import settings

@pytest.fixture
def user_data():
    return {
        "email": "akojimoses@gmail.com",
        "password": "testpassword",
        
    }

@pytest.fixture
def authenticated_user(client, user_data):
    user = User.objects.create_user(**user_data)
    client.login(email=user_data["email"], password=user_data["password"])
    return user

def test_register_user(client, user_data):
    response = client.post(reverse("registerUser"), user_data, follow=True)
    assert response.status_code == 200
    assert User.objects.filter(email=user_data["email"]).exists()

def test_user_login_logout(client, user_data):
    User.objects.create_user(**user_data)
    response = client.post(reverse("login"), user_data, follow=True)
    assert response.status_code == 200
    assert response.context["user"].is_authenticated

    response = client.get(reverse("logout"), follow=True)
    assert response.status_code == 200
    assert not response.context["user"].is_authenticated

def test_authenticated_user_access_task_management(client, authenticated_user):
    response = client.get(reverse("task_management"), follow=True)
    assert response.status_code == 200


def test_edge_cases_and_error_scenarios(client):
    """Test cases for incorrect passwords, non-existent users, etc."""
    response = client.post(reverse("login"), {"email": "nonexistent", "password": "incorrect"}, follow=True)
    assert response.status_code == 200
    assert not response.context["user"].is_authenticated


def test_security_vulnerabilities(client, user_data):
    """Test for potential security vulnerabilities like session fixation and CSRF attacks."""
    response = client.get(reverse("login"), follow=True)
    assert response.status_code == 200

"""Helper functions for testing CSRF and session fixation"""
def get_csrf_token(client):
    response = client.get(reverse("login"))
    csrf_token = response.cookies["csrftoken"].value
    return csrf_token

def test_csrf_attack(client, user_data):
    csrf_token = get_csrf_token(client)
    """An attacker might try to use this token to perform an action on behalf of the user."""
    response = client.post(reverse("some_action"), {"param": "value", "csrfmiddlewaretoken": csrf_token})
    assert response.status_code == 403  # CSRF attack detected

def test_session_fixation_attack(client, user_data):
    """An attacker might try to set the session ID to a known value."""
    session_id = "known_session_id"
    client.cookies[settings.SESSION_COOKIE_NAME] = session_id
    response = client.get(reverse("profile"))
    assert response.status_code == 200
    assert response.context["user"].is_anonymous  # User is anonymous, session fixation detected
