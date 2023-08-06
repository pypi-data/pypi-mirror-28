"""
Radicale extension unit tests.
"""
import os
import tempfile

try:
    from configparser import ConfigParser
except ImportError:
    # SafeConfigParser (py2) == ConfigParser (py3)
    from ConfigParser import SafeConfigParser as ConfigParser

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import six
from django.core import management

from modoboa.lib import exceptions as lib_exceptions
from modoboa.lib.tests import ModoTestCase

from modoboa.admin.factories import (
    MailboxFactory, populate_database
)
from modoboa.admin.models import (
    Domain, Mailbox
)

from .factories import (
    UserCalendarFactory, SharedCalendarFactory, AccessRuleFactory
)
from .models import UserCalendar, SharedCalendar, AccessRule
from .modo_extension import Radicale


class UserCalendarTestCase(ModoTestCase):

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(UserCalendarTestCase, cls).setUpTestData()
        populate_database()

    def assertRuleEqual(self, calname, username, read=False, write=False):
        acr = AccessRule.objects.get(
            mailbox__user__username=username,
            calendar__name=calname)
        self.assertEqual(acr.read, read)
        self.assertEqual(acr.write, write)

    def test_model(self):
        """Check few things about the model."""
        Radicale().load()
        mbox = Mailbox.objects.get(address="admin", domain__name="test.com")
        cal = UserCalendarFactory(name="MyCal", mailbox=mbox)
        with self.assertRaises(lib_exceptions.InternalError) as cm:
            url = cal.url
        self.assertEqual(
            str(cm.exception), "Server location is not set, please fix it.")
        self.set_global_parameter(
            "server_location", "http://localhost", app="modoboa_radicale")
        self.assertEqual(cal.url, "http://localhost/test.com/user/admin/MyCal")

    def test_add_calendar(self):
        MailboxFactory(
            address="polo", domain__name="test.com",
            user__username="polo@test.com")

        # As a super administrator
        mbox = Mailbox.objects.get(address='user', domain__name='test.com')
        values = {
            "name": "Test calendar",
            "mailbox": mbox.pk,
            "username": "admin@test.com",
            "read_access": 1,
            "stepid": "step2"
        }
        self.ajax_post(
            reverse("modoboa_radicale:user_calendar_add"), values)
        self.client.logout()
        self.assertRuleEqual("Test calendar", "admin@test.com", read=True)

        # As a domain administrator
        self.client.login(username="admin@test.com", password="toto")
        values = {
            "name": "Test calendar 2",
            "mailbox": mbox.pk,
            "username": "admin@test.com",
            "read_access": 1,
            "write_access": 1,
            "stepid": "step2"
        }
        self.ajax_post(
            reverse("modoboa_radicale:user_calendar_add"), values)
        self.client.logout()
        self.assertRuleEqual(
            "Test calendar 2", "admin@test.com", read=True, write=True
        )

        # As a user
        self.client.login(username="user@test.com", password="toto")
        values = {
            "name": "My calendar",
            "username": "admin@test.com",
            "read_access": 1,
            "write_access": 1,
            "username_1": "polo@test.com",
            "write_access_1": 1,
            "stepid": "step2"
        }
        self.ajax_post(
            reverse("modoboa_radicale:user_calendar_add"), values)
        UserCalendar.objects.get(name="My calendar")
        self.assertRuleEqual(
            "My calendar", "admin@test.com", read=True, write=True)
        self.assertRuleEqual("My calendar", "polo@test.com", write=True)

    def test_edit_calendar(self):
        cal = UserCalendarFactory(
            mailbox__user__username='test@modoboa.org',
            mailbox__address='test', mailbox__domain__name='modoboa.org')
        values = {
            "name": "Modified", "mailbox": cal.mailbox.pk
        }
        self.ajax_post(
            reverse("modoboa_radicale:user_calendar", args=[cal.pk]), values
        )

    def test_del_calendar(self):
        cal = UserCalendarFactory(
            mailbox__user__username='test@modoboa.org',
            mailbox__address='test', mailbox__domain__name='modoboa.org')
        self.ajax_delete(
            reverse("modoboa_radicale:user_calendar", args=[cal.pk])
        )
        with self.assertRaises(ObjectDoesNotExist):
            UserCalendar.objects.get(pk=cal.pk)

    def test_del_calendar_denied(self):
        cal = UserCalendarFactory(
            mailbox__user__username='test@modoboa.org',
            mailbox__address='test', mailbox__domain__name='modoboa.org')
        self.client.logout()
        self.client.login(username="admin@test.com", password="toto")
        self.ajax_delete(
            reverse("modoboa_radicale:user_calendar", args=[cal.pk]),
            status=403
        )

    def test_add_calendar_denied(self):
        self.client.logout()
        self.client.login(username="admin@test.com", password="toto")
        values = {
            "name": "Test calendar",
            "mailbox": Mailbox.objects.get(
                address="user", domain__name="test2.com").pk,
            "stepid": "step2"
        }
        self.ajax_post(
            reverse("modoboa_radicale:user_calendar_add"), values, status=400)


class SharedCalendarTestCase(ModoTestCase):

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(SharedCalendarTestCase, cls).setUpTestData()
        populate_database()

    def test_add_calendar(self):
        # As a super administrator
        domain = Domain.objects.get(name="test.com")
        values = {
            "name": "Test calendar",
            "domain": domain.pk,
        }
        self.ajax_post(
            reverse("modoboa_radicale:shared_calendar_add"), values)
        self.client.logout()

        # As a domain administrator
        self.client.login(username="admin@test.com", password="toto")
        values = {
            "name": "Test calendar 2",
            "domain": domain.pk
        }
        self.ajax_post(
            reverse("modoboa_radicale:shared_calendar_add"), values)
        self.client.logout()

    def test_add_calendar_denied(self):
        self.client.logout()
        self.client.login(username="admin@test.com", password="toto")
        values = {
            "name": "Test calendar",
            "domain": Domain.objects.get(name="test2.com")
        }
        self.ajax_post(
            reverse("modoboa_radicale:shared_calendar_add"), values,
            status=400)

    def test_edit_calendar(self):
        cal = SharedCalendarFactory(
            domain__name='modoboa.org')
        values = {
            "name": "Modified", "domain": cal.domain.pk
        }
        self.ajax_post(
            reverse("modoboa_radicale:shared_calendar", args=[cal.pk]), values
        )
        cal = SharedCalendar.objects.get(pk=cal.pk)
        self.assertEqual(cal.name, "Modified")

    def test_del_calendar(self):
        cal = SharedCalendarFactory(domain__name='modoboa.org')
        self.ajax_delete(
            reverse("modoboa_radicale:shared_calendar", args=[cal.pk])
        )
        with self.assertRaises(ObjectDoesNotExist):
            SharedCalendar.objects.get(pk=cal.pk)

    def test_del_calendar_denied(self):
        cal = SharedCalendarFactory(domain__name='modoboa.org')
        self.client.logout()
        self.client.login(username="admin@test.com", password="toto")
        self.ajax_delete(
            reverse("modoboa_radicale:shared_calendar", args=[cal.pk]),
            status=403
        )


class AccessRuleTestCase(ModoTestCase):

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(AccessRuleTestCase, cls).setUpTestData()
        populate_database()

    def setUp(self):
        """Initialize tests."""
        super(AccessRuleTestCase, self).setUp()
        self.rights_file_path = tempfile.mktemp()
        self.set_global_parameter(
            "rights_file_path", self.rights_file_path, app="modoboa_radicale")

    def tearDown(self):
        os.unlink(self.rights_file_path)

    def test_rights_file_generation(self):
        mbox = Mailbox.objects.get(address="admin", domain__name="test.com")
        cal = UserCalendarFactory(mailbox=mbox)

        AccessRuleFactory(
            mailbox=Mailbox.objects.get(
                address="user", domain__name="test.com"),
            calendar=cal, read=True)
        management.call_command("generate_rights", verbosity=False)

        cfg = ConfigParser()
        with open(self.rights_file_path) as fpo:
            if six.PY3:
                cfg.read_file(fpo)
            else:
                cfg.readfp(fpo)

        # Check mandatory rules
        self.assertTrue(cfg.has_section("domain-shared-calendars"))
        self.assertTrue(cfg.has_section("owners-access"))

        # Check user-defined rules
        section = "user@test.com-to-User calendar 0-acr"
        self.assertTrue(cfg.has_section(section))
        self.assertEqual(cfg.get(section, "user"), "user@test.com")
        self.assertEqual(
            cfg.get(section, "collection"),
            "test.com/user/admin/User calendar 0"
        )
        self.assertEqual(cfg.get(section, "permission"), "r")

        # Call a second time
        management.call_command("generate_rights", verbosity=False)

    def test_rights_file_generation_with_admin(self):
        self.set_global_parameter(
            "allow_calendars_administration", True, app="modoboa_radicale")
        management.call_command("generate_rights", verbosity=False)
        cfg = ConfigParser()
        with open(self.rights_file_path) as fpo:
            if six.PY3:
                cfg.read_file(fpo)
            else:
                cfg.readfp(fpo)

        # Check mandatory rules
        self.assertTrue(cfg.has_section("domain-shared-calendars"))
        self.assertTrue(cfg.has_section("owners-access"))

        # Super admin rules
        section = "sa-admin-acr"
        self.assertTrue(cfg.has_section(section))

        # Domain admin rules
        for section in ["da-admin@test.com-to-test.com-acr",
                        "da-admin@test2.com-to-test2.com-acr"]:
            self.assertTrue(cfg.has_section(section))
