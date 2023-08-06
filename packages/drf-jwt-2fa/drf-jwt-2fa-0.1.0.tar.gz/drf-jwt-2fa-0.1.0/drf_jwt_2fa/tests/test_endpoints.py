import pytest
from django.contrib.auth.backends import ModelBackend
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import get_user
from .utils import (
    check_auth_token, check_code_token, get_verification_code_from_mailbox)


@pytest.mark.django_db
def test_get_code_token_success():
    token = get_code_token()
    check_code_token(token)


def get_code_token():
    get_user(username='testuser', password='a42')
    client = get_api_client()
    result = client.post(
        reverse('get-code'),
        data={'username': 'testuser', 'password': 'a42'})
    assert sorted(result.data.keys()) == ['token']
    assert result.status_code == 200
    return result.data['token']


def test_code_token_missing_fields():
    client = get_api_client()
    # Post without username field
    result = client.post(reverse('get-code'), data={'password': 'abc'})
    assert sorted(result.data.keys()) == ['username']
    assert result.status_code == 400
    assert result.data['username'] == ['This field is required.']


@pytest.mark.django_db
def test_code_token_invalid_password():
    get_user(username='testuser', password='a42')
    client = get_api_client()
    result = client.post(
        reverse('get-code'),
        data={'username': 'testuser', 'password': 'wrong'})
    assert sorted(result.data.keys()) == ['non_field_errors']
    assert result.status_code == 400
    assert result.data['non_field_errors'] == ['Invalid credentials']


class InactiveAllowingAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True


@override_settings(AUTHENTICATION_BACKENDS=[
    __name__ + '.InactiveAllowingAuthBackend'])
@pytest.mark.django_db
def test_code_token_inactive_user():
    user = get_user(username='testuser', password='a42')
    user.is_active = False
    user.save()
    client = get_api_client()
    result = client.post(
        reverse('get-code'),
        data={'username': 'testuser', 'password': 'a42'})
    assert sorted(result.data.keys()) == ['non_field_errors']
    assert result.status_code == 400
    assert result.data['non_field_errors'] == ['Deactivated user']


@pytest.mark.django_db
def test_auth_token_success():
    code_token = get_code_token()
    code = get_verification_code_from_mailbox()
    client = get_api_client()
    result = client.post(
        reverse('auth'),
        data={'code_token': code_token, 'code': code})
    assert sorted(result.data.keys()) == ['token']
    assert result.status_code == 200
    token = result.data['token']
    check_auth_token(token)


@pytest.mark.django_db
def test_auth_token_invalid_code():
    code_token = get_code_token()
    correct_code = get_verification_code_from_mailbox()
    code = '123456' if correct_code != '123456' else '654321'
    client = get_api_client()
    result = client.post(
        reverse('auth'),
        data={'code_token': code_token, 'code': code})
    assert sorted(result.data.keys()) == ['non_field_errors']
    assert result.status_code == 400
    assert result.data['non_field_errors'] == ['Verification failed']


@pytest.mark.django_db
def test_auth_token_removed_user():
    code_token = get_code_token()
    code = get_verification_code_from_mailbox()
    user = get_user()
    user.delete()
    client = get_api_client()
    result = client.post(
        reverse('auth'),
        data={'code_token': code_token, 'code': code})
    assert sorted(result.data.keys()) == ['non_field_errors']
    assert result.status_code == 400
    assert result.data['non_field_errors'] == ['Unknown user']


def get_api_client():
    api_client = APIClient()
    api_client.default_format = 'json'
    return api_client
