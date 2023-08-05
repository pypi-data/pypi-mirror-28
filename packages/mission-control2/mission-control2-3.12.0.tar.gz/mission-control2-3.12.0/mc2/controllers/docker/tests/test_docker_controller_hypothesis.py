import json
import mock
import pytest
import responses
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from hypothesis import given, settings as hsettings
from hypothesis.extra.django import TestCase
from hypothesis.extra.django.models import models, default_value
from hypothesis.strategies import text, random_module, lists, just

from mc2.controllers.base.models import EnvVariable, MarathonLabel
from mc2.controllers.base.tests.base import ControllerBaseTestCase
from mc2.controllers.docker.models import (
    DockerController, marathon_lb_domains, traefik_domains)
from mc2.controllers.base.managers.rabbitmq import ControllerRabbitMQManager
from mc2.organizations.models import Organization


def add_envvars(controller):
    """
    Generate some EnvVariable models for the given controller.

    We discard these once we've made them because they're in the database.
    """
    envvars = lists(models(EnvVariable, controller=just(controller)))
    return envvars.map(lambda _: controller)


def add_labels(controller):
    """
    Generate some MarathonLabel models for the given controller.

    We discard these once we've made them because they're in the database.
    """
    labels = lists(models(MarathonLabel, controller=just(controller)))
    return labels.map(lambda _: controller)


def docker_controller(with_envvars=True, with_labels=True, **kw):
    """
    Generate a DockerController model with (optional) envvars and labels.
    """
    # The slug is used in places where whitespace and colons are problematic,
    # so we remove them from the generated value.
    # TODO: Build a proper SlugField strategy.
    # TODO: Figure out why the field validation isn't being applied.
    # Slugs must be domain-name friendly - used in the "generic" domain
    slug = text(string.ascii_letters + string.digits + '-')
    kw.setdefault("slug", slug)

    kw.setdefault("owner", models(User, is_active=just(True)))
    kw.setdefault("organization", models(Organization, slug=slug))

    # Prevent Hypothesis from generating domains with invalid characters
    domain_urls = text(string.ascii_letters + string.digits + '-.')
    kw.setdefault("domain_urls", domain_urls)

    # Prevent Hypothesis from generating vhosts with invalid characters
    rabbitmq_vhost_name = text(string.ascii_letters + string.digits + '-.')
    kw.setdefault("rabbitmq_vhost_name", rabbitmq_vhost_name)

    # Prevent Hypothesis from generating usernames with invalid characters
    rabbitmq_vhost_username = text(string.ascii_letters + string.digits + '-.')
    kw.setdefault("rabbitmq_vhost_username", rabbitmq_vhost_username)

    # The model generator sees `controller_ptr` (from the PolymorphicModel
    # magic) as a mandatory field and objects if we don't provide a value for
    # it.
    controller = models(DockerController, controller_ptr=default_value, **kw)
    if with_envvars:
        controller = controller.flatmap(add_envvars)
    if with_labels:
        controller = controller.flatmap(add_labels)
    return controller


def check_and_clear_appdata(appdata, controller):
    """
    Assert that appdata is correct and clear it.

    Because there are a bunch of separate checks for different parts of the
    data, we remove each thing we check as we check it. If we don't have an
    empty dict at the end, there's something unexpected in the data.

    We do it this way instead of generating a big dict to compare against so
    that we don't end up with two copies of the same logic.
    """
    assert appdata.pop("id") == controller.app_id
    assert appdata.pop("cpus") == controller.marathon_cpus
    assert appdata.pop("mem") == controller.marathon_mem
    assert appdata.pop("instances") == controller.marathon_instances
    check_and_remove_optional(appdata, "cmd", controller.marathon_cmd)
    check_and_remove_docker(appdata, controller)
    check_and_remove_health(appdata, controller)
    check_and_remove_env(appdata, controller)
    check_and_remove_labels(appdata, controller)
    check_and_remove_backoff_params(appdata)
    assert appdata == {}


def check_and_remove_docker_param(parameters, key, value):
    """
    Assert that a particular docker param is correct and remove it.
    """
    paraml = [p for p in parameters if p["key"] == key]
    assert paraml == [{"key": key, "value": value}]
    parameters.remove(paraml[0])


def check_and_remove_docker_params(docker, controller):
    """
    Assert that the docker params data is correct and remove it.
    """
    parameters = docker.pop("parameters")
    check_and_remove_docker_param(parameters, "memory-swappiness", "0")
    if controller.volume_needed:
        check_and_remove_docker_param(parameters, "volume-driver", "xylem")
        volume = u"%s_media:%s" % (
            controller.app_id,
            controller.volume_path or settings.MARATHON_DEFAULT_VOLUME_PATH)
        check_and_remove_docker_param(parameters, "volume", volume)
    assert parameters == []


def check_and_remove_docker(appdata, controller):
    """
    Assert that the docker container data is correct and remove it.
    """
    container = appdata.pop("container")
    assert container.pop("type") == "DOCKER"
    docker = container.pop("docker")
    assert docker.pop("image") == controller.docker_image
    assert docker.pop("forcePullImage") is True
    assert docker.pop("network") == "BRIDGE"
    if controller.port:
        assert docker.pop("portMappings") == [
            {"containerPort": controller.port, "hostPort": 0}]
    check_and_remove_docker_params(docker, controller)
    assert docker == {}
    assert container == {}


def check_and_remove_health(appdata, controller):
    """
    Assert that the health check data is correct and remove it.
    """
    if controller.marathon_health_check_path and \
            controller.marathon_health_check_cmd:
        assert appdata.pop("healthChecks") == [{
            "gracePeriodSeconds": 60,
            "intervalSeconds": 10,
            "maxConsecutiveFailures": 3,
            "path": controller.marathon_health_check_path,
            "portIndex": 0,
            "protocol": "HTTP",
            "timeoutSeconds": 20,
        }, {
            "gracePeriodSeconds": 60,
            "intervalSeconds": 10,
            "maxConsecutiveFailures": 3,
            "command": {"value": controller.marathon_health_check_cmd},
            "protocol": "COMMAND",
            "timeoutSeconds": 20,
        }]
        assert appdata.pop("ports") == [0]
    elif controller.marathon_health_check_path:
        assert appdata.pop("healthChecks") == [{
            "gracePeriodSeconds": 60,
            "intervalSeconds": 10,
            "maxConsecutiveFailures": 3,
            "path": controller.marathon_health_check_path,
            "portIndex": 0,
            "protocol": "HTTP",
            "timeoutSeconds": 20,
        }]
        assert appdata.pop("ports") == [0]
    elif controller.marathon_health_check_cmd:
        assert appdata.pop("healthChecks") == [{
            "gracePeriodSeconds": 60,
            "intervalSeconds": 10,
            "maxConsecutiveFailures": 3,
            "command": {"value": controller.marathon_health_check_cmd},
            "protocol": "COMMAND",
            "timeoutSeconds": 20,
        }]

    assert "ports" not in appdata
    assert "healthChecks" not in appdata


def check_and_remove_backoff_params(appdata):
    appdata.pop('backoffFactor')
    appdata.pop('backoffSeconds')


def check_and_remove_env(appdata, controller):
    """
    Assert that the correct envvars are in appdata and remove them.
    """
    env_variables = controller.env_variables.all()
    if env_variables or controller.postgres_db_needed or \
            (controller.rabbitmq_vhost_needed and
             controller.rabbitmq_vhost_name):
        envs = appdata.pop("env")

        if controller.postgres_db_needed:
            assert envs.pop(
                "DATABASE_URL") == 'postgres://trevor:1234@localhost/trevordb'

        if controller.rabbitmq_vhost_needed and controller.rabbitmq_vhost_name:
            assert envs.pop("BROKER_URL") == 'amqp://%s:%s@%s/%s' % (
                controller.rabbitmq_vhost_username,
                controller.rabbitmq_vhost_password,
                controller.rabbitmq_vhost_host,
                controller.rabbitmq_vhost_name)
        if env_variables:
            # We may have duplicate keys in here, but hopefully the database
            # always return the objects in the same order.
            assert envs == {ev.key: ev.value for ev in env_variables}

    assert "env" not in appdata


def check_and_remove_labels(appdata, controller):
    """
    Assert that the correct labels are in appdata and remove them.
    """
    labels = appdata.pop("labels")
    assert labels.pop("name") == controller.name
    assert labels.pop("org") == controller.organization.slug \
        if controller.organization else ''
    domains = [u".".join([controller.app_id, settings.HUB_DOMAIN])]
    domains.extend(controller.domain_urls.split())
    assert sorted(labels.pop("HAPROXY_0_VHOST").split(",")) == sorted(domains)

    haproxy_group = labels.pop("HAPROXY_GROUP")

    if controller.external_visibility:
        assert sorted(labels.pop("domain").split()) == sorted(domains)
        traefik_domains = labels.pop("traefik.frontend.rule")
        traefik_domains = traefik_domains.split(":", 2)[-1].split(",")
        traefik_domains = [d.strip() for d in traefik_domains]
        assert sorted(traefik_domains) == sorted(domains)
        assert haproxy_group == "external"
    else:
        assert haproxy_group == "internal"

    # We may have duplicate keys in here, but hopefully the database always
    # return the objects in the same order.
    lvs = {lv.name: lv.value for lv in controller.label_variables.all()}
    assert labels == lvs


def check_and_remove_optional(appdata, field, value):
    """
    Assert that the given field has the correct value or is missing if unset.
    """
    if value:
        assert appdata.pop(field) == value
    assert field not in appdata


def test_marathon_lb_domains_single():
    """
    When a domains string with a single domain is passed to
    marathon_lb_domains, it returns the domain unchanged.
    """
    domains = 'abc.com'
    assert marathon_lb_domains(domains) == 'abc.com'


def test_marathon_lb_domains_multiple():
    """
    When a domains string with multiple domains is passed to
    marathon_lb_domains, it returns a comma-separated list of domains.
    """
    domains = 'abc.com def.co.za   ghi.co.ng'
    assert marathon_lb_domains(domains) == 'abc.com,def.co.za,ghi.co.ng'


def test_traefik_domains_single():
    """
    When a domains string with a single domain is passed to traefik_domains,
    it returns a Host frontend rule.
    """
    domains = 'abc.com'
    assert traefik_domains(domains) == 'Host: abc.com'


def test_traefik_domains_multiple():
    """
    When a domains string with multiple domains is passed to traefik_domains,
    it returns multiple Host frontend rules joined by ';'.
    """
    domains = 'abc.com def.co.za   ghi.co.ng'
    assert (traefik_domains(domains) ==
            'Host: abc.com, def.co.za, ghi.co.ng')


def test_traefik_domains_none():
    """
    When a domains string with no domains is passed to traefik_domains, it
    returns an empty string.
    """
    domains = '  '
    assert traefik_domains(domains) == ''


@pytest.mark.django_db
class DockerControllerHypothesisTestCase(TestCase, ControllerBaseTestCase):
    """
    Hypothesis tests for the DockerController model.

    These need to have the health checks disabled because Django model
    generation is very slow and occasionally fails the slow data generation
    check.
    """
    def setUp(self):
        self.mock_create_postgres_db(200, {
            'result': {
                'name': 'trevordb',
                'user': 'trevor',
                'password': '1234',
                'host': 'localhost'}})

    @responses.activate
    @mock.patch.object(ControllerRabbitMQManager, '_create_username')
    @hsettings(perform_health_check=False)
    @given(_r=random_module(), controller=docker_controller())
    def test_get_marathon_app_data(self, _r, controller, mock_create_u):
        """
        Suitable app_data is built for any combination of model parameters.
        """
        if controller.rabbitmq_vhost_needed and controller.rabbitmq_vhost_name:
            self.mock_successful_new_vhost(
                controller.rabbitmq_vhost_name,
                controller.rabbitmq_vhost_username)
            mock_create_u.return_value = controller.rabbitmq_vhost_username

        app_data = controller.get_marathon_app_data()
        check_and_clear_appdata(app_data, controller)

    @responses.activate
    @mock.patch.object(ControllerRabbitMQManager, '_create_username')
    @hsettings(perform_health_check=False)
    @given(_r=random_module(), controller=docker_controller())
    def test_from_marathon_app_data(self, _r, controller, u):
        """
        A model imported from app_data generates the same app_data as the model
        it was imported from.
        """
        if controller.rabbitmq_vhost_needed and controller.rabbitmq_vhost_name:
            self.mock_successful_new_vhost(
                controller.rabbitmq_vhost_name,
                controller.rabbitmq_vhost_username)
            u.return_value = controller.rabbitmq_vhost_username

        app_data = controller.get_marathon_app_data()
        new_controller = DockerController.from_marathon_app_data(
            controller.owner, controller.organization, app_data)
        assert app_data == new_controller.get_marathon_app_data()

    @responses.activate
    @mock.patch.object(ControllerRabbitMQManager, '_create_username')
    @hsettings(perform_health_check=False, max_examples=50)
    @given(_r=random_module(), controller=docker_controller(), name=text())
    def test_from_marathon_app_data_with_name(self, _r, controller, name, u):
        """
        A model imported from app_data generates the same app_data as the model
        it was imported from, but with the name field overridden.

        We limit the number of examples we generate because we don't need
        hundreds of examples to verify that this behaviour is correct.
        """
        if controller.rabbitmq_vhost_needed and controller.rabbitmq_vhost_name:
            self.mock_successful_new_vhost(
                controller.rabbitmq_vhost_name,
                controller.rabbitmq_vhost_username)
            u.return_value = controller.rabbitmq_vhost_username

        app_data = controller.get_marathon_app_data()
        new_controller = DockerController.from_marathon_app_data(
            controller.owner, controller.organization, app_data, name=name)
        assert new_controller.name == name

        app_data_with_name = json.loads(json.dumps(app_data))
        app_data_with_name["labels"]["name"] = name
        assert app_data_with_name == new_controller.get_marathon_app_data()

    @responses.activate
    @mock.patch.object(ControllerRabbitMQManager, '_create_username')
    @hsettings(perform_health_check=False, max_examples=50)
    @given(_r=random_module(), controller=docker_controller(), name=text())
    def test_hidden_import_view(self, _r, controller, name, mock_create_u):
        """
        A model imported through the hidden view generates the same app_data
        as the model it was imported from, but with the name field overridden.

        We limit the number of examples we generate because we don't need
        hundreds of examples to verify that this behaviour is correct.
        """
        if controller.rabbitmq_vhost_needed and controller.rabbitmq_vhost_name:
            self.mock_successful_new_vhost(
                controller.rabbitmq_vhost_name,
                controller.rabbitmq_vhost_username)
            mock_create_u.return_value = controller.rabbitmq_vhost_username

        app_data = controller.get_marathon_app_data()
        user = controller.owner
        user.set_password("password")  # So we can log in.
        user.save()
        client = Client()
        assert client.login(username=user.username, password="password")
        with responses.RequestsMock() as rsps:
            # If the Marathon request hasn't occurred by the time this context
            # is closed then the test will fail.
            rsps.add(
                responses.POST, '%s/v2/apps' % settings.MESOS_MARATHON_HOST,
                body="{}", content_type="application/json", status=201)
            resp = client.post(
                reverse('controllers.docker:hidden_import'),
                {"name": name, "app_data": json.dumps(app_data)})
        assert resp.status_code == 302

        new_controller = DockerController.objects.exclude(
            pk=controller.pk).get()
        assert new_controller.name == name

        app_data_with_name = json.loads(json.dumps(app_data))
        app_data_with_name["labels"]["name"] = name
        assert app_data_with_name == new_controller.get_marathon_app_data()
