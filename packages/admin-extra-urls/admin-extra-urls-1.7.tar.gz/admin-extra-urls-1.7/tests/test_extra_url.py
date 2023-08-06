# -*- coding: utf-8 -*-
import logging

import pytest
from django.contrib.auth.models import Permission
from admin_extra_urls.extras import reverse

logger = logging.getLogger(__name__)


def test_link(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['add_demomodel1', 'change_demomodel1'])
    staff_user.user_permissions.add(*perms)
    url = reverse('admin:demo_demomodel1_changelist')
    res = django_app.get(url, user=staff_user)
    res = res.click('Refresh').follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'refresh called'


def test_link_reverse(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['add_demomodel1', 'change_demomodel1'])
    staff_user.user_permissions.add(*perms)
    url = reverse('admin:demo_demomodel1_refresh')
    res = django_app.get(url, user=staff_user).follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'refresh called'


def test_link_custom_path_reverse(django_app, admin_user):
    url = reverse('admin:demo_demomodel1_custom_path')
    assert url == '/admin/demo/demomodel1/a/b/'


@pytest.mark.django_db
def test_action(app, demomodel2, admin_user):
    url = reverse('admin:demo_demomodel2_change', args=[demomodel2.pk])
    res = app.get(url, user=admin_user)
    res = res.click(r'Update', index=1).follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'action called'


def test_default_httpresponseaction(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('No Response').follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'No_response'


def test_upload(app, admin_user):
    url = reverse('admin:demo_demomodel4_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('Upload')
    form = res.forms[0]
    form.submit()
