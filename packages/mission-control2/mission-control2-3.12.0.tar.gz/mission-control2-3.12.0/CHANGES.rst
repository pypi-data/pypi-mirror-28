CHANGE LOG
==========

3.12.0
------

- Allow specify of COMMAND health check

3.11.4
------

- Remove default nginx conf: new version of nginx ships with a default conf

3.11.3
------

- Add on_delete models protect to controller's owner and organization

3.11.2
------

- Handle task restarts gracefully, do not bubble up InfrastructureException to Sentry (#141)

3.11.1
------

- Fix HAPROXY_0_VHOST value, should be comma separated rather than space.

3.11.0
------
- allow user to request rabbitmq vhost

3.10.0
------
- Add memory-swappiness=0 docker parameter to all app definitions.

3.9.0
-----
- Allow users to register on MC

3.8.1
-----
- move version number to __init__.py
- show is_app_admin in the UI
- show org list dropdown in alphabetical order
- ensure full list of orgs is shown by default

3.8.0
-----
- change labels when external visibility disabled
- allow port to be optional (UI fix)
- add organization name to marathon labels
- (bug) fix issue with app labels not allowing multiples

3.7.3
-----
- add app_admin for SSO
- fix logging for apps with multiple instance

3.7.2
-----
- revert Font fix: need to find a better solution

3.7.1
-----
- (bug) Font css not loading properly after compress
- (bug) ensure output_field is specified for Sum

3.7.0
-----
- Added dashboard to show summary stats

3.6.1
-----
- Fix single-signon bug for Molo
- (bug) All multi-field forms can now be deleted (e.g env variables)

3.6.0
-----
- Create postgres databases through mission control
- Use org permissions to give sso access
- Allow other non-pk domains to log in to MC2

3.5.0
-----
- Allow adding additional links to an app
- Add view only for users

3.4.2
-----
- (bug) Ensure organization field is shown on docker controller edit view

3.4.1
-----
- Add sensible timeouts to external HTTP APIs.

3.4.0
-----
- Add traefik labels to app definitions
- Allow labels to contain '.' characters
- Better improved docker file
- Add clone option to docker controller
- Switch from Logdriver to Mesos API for logs
- Allow port-less containers
- Added sensible backoff values for marathon
- Show suspended apps as greyed out

3.3.3
-----
- Add marathon-lb labels to app definitions

3.3.2
-----
- ensure int values for health check timeouts

3.3.1
-----
- allow health check timeouts to be configurable

3.3.0
-----
- added description field
- ensure org change doesn't result in 404 if org permssions are good
- ensure all marathon calls are done via celery
- re-introduce log driver
- added app restart webhook
- UI improvements + tweaks
- increase graceperiod for when apps start with healthchecks
- small docker image with python:2.7.11-alpine

3.2.11
------
- add hypothesis testing
- upgrade to latest version of grappelli (fixes delete bug)

3.2.10
-----
- remove freebasics

3.2.9
-----
- add marathon labels

3.2.8
-----
- ensure cards can be clicked properly
- cleanup old settings
- remove dependency of ws4redis
- fix delete of app
- allow hub domain to be specified in ENV

3.2.7
-----
- specify user/pass env for smtp

3.2.6
-----
- expose SMPT settings as env variables

3.2.5
-----
- user json serializer for email

3.2.4
-----
- ensure bool env (DEBUG) is read correctly

3.2.3
-----
- enable restart button
- allow debug to be set using env variable

3.2.2
-----
- update UI fields on homepage
- Fix redirect issue when logging in

3.2.1
-----
- fix password reset
- add domain URLs for docker controllers
- tweaks to the UI

3.2.0
-----
- Added single-sign-on support for Molo
- Enable email login + password reset

3.1.1
-----
- Fix for marathon cmd when blank

3.1.0
-----
- Docker container now fully functional
- Use Environment variables to specify settings
- Add volume support use xylem plugin
- Allow marathon cmd to be blank for docker controller

3.0.5
-----
- ensure all static files are packaged

3.0.4
-----
- use json serialiser for celery

3.0.3
-----
- fix E402 in latest flake8 version

3.0.2
-----
- update celery to be inline with 3.1.19

3.0.1
-----
- make settings variables configurable via ENV

3.0.0
-----
- release as pip installable
- refactored namespace to use mc2
- allow deleting of app

2.0.0
-----
- Initial 2.0 release (non-backwards compatible)
- refactored code structure
- introduced controller base
- simplified model definitions

< 2.0
-----
- Mission Control for Universal Core
