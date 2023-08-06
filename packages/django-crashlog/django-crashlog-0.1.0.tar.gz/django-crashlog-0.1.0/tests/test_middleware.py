# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

from crashlog.middleware import CrashLogMiddleware, process_exception
from crashlog.models import Error


@pytest.mark.django_db
def test_return_value():
    m = CrashLogMiddleware()
    factory = RequestFactory()
    request = factory.get("/my/home/url")
    ret = m.process_exception(request, PermissionDenied())
    assert isinstance(ret, HttpResponse) or ret is None


@pytest.mark.django_db
def test_log():
    m = CrashLogMiddleware()
    factory = RequestFactory()
    request = factory.get("/my/home/url")
    request.user = AnonymousUser()
    request.session = {}
    m.process_exception(request, PermissionDenied())
    assert Error.objects.filter(class_name='PermissionDenied').exists()


@pytest.mark.django_db
def test_log_user():
    m = CrashLogMiddleware()
    factory = RequestFactory()
    request = factory.get("/my/home/url")
    request.user = User.objects.create(username='sax')
    request.session = {}
    m.process_exception(request, PermissionDenied())
    assert Error.objects.filter(class_name='PermissionDenied', username='sax').exists()


@pytest.mark.django_db
def test_ignore_class():
    m = CrashLogMiddleware()
    factory = RequestFactory()
    request = factory.get("/my/home/url")
    request.session = {}

    with override_settings(CRASHLOG_IGNORE_EXCEPTIONS=['django.core.exceptions.PermissionDenied']):
        m.process_exception(request, PermissionDenied())
        assert not Error.objects.filter(class_name='PermissionDenied').exists()


@pytest.mark.django_db
def test_view(django_app, admin_user):
    url = reverse('raise-error')
    with pytest.raises(IndexError):
        res = django_app.get(url, user=admin_user)
        assert res.status_code == 500

    assert Error.objects.filter(class_name='IndexError').exists()


@pytest.mark.django_db
def test_message_user(django_app, admin_user):
    url = reverse('raise_with_message_user')
    res = django_app.get(url, user=admin_user.username)
    assert res.status_code == 200

    assert Error.objects.filter(class_name='IndexError').exists()

@pytest.mark.django_db
def test_simple(rf, django_app, admin_user):
    request = rf.get("/my/home/url")
    error = process_exception(PermissionDenied())
    assert error.pk
