=====
Useragents
=====

Useragents is a simple app to track the user agents, ips and other info
of the various visitors of your django site. The information is stored in
the database for easy reference and exporting.

Quick start
-----------

1. Add "ct_useragents" and "ipware" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ipware',
        'ct_useragents',
    ]
    
2. Add useragents to the middleware:
make sure you add this after 'django.contrib.auth.middleware.AuthenticationMiddleware'
of you will get errors
	MIDDLEWARE_CLASSES = [
		...
		'useragents.utils.UserAgentsMiddleware',
		...
	]

3. Add ipware helpers to settings:
# you can provide your own meta precedence order by
# including IPWARE_META_PRECEDENCE_ORDER in your project's
# settings.py. The check is done from top to bottom
IPWARE_META_PRECEDENCE_ORDER = (
	'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',  # client, proxy1, proxy2
	'HTTP_CLIENT_IP',
	'HTTP_X_REAL_IP',
	'HTTP_X_FORWARDED',
	'HTTP_X_CLUSTER_CLIENT_IP',
	'HTTP_FORWARDED_FOR',
	'HTTP_FORWARDED',
	'HTTP_VIA',
	'REMOTE_ADDR',
)

# you can provide your own private IP prefixes by
# including IPWARE_PRIVATE_IP_PREFIX in your project's setting.py
# IPs that start with items listed below are ignored
# and are not considered a `real` IP address
IPWARE_PRIVATE_IP_PREFIX = (
	'0.',  # externally non-routable
	'10.',  # class A private block
	'169.254.',  # link-local block
	'172.16.', '172.17.', '172.18.', '172.19.',
	'172.20.', '172.21.', '172.22.', '172.23.',
	'172.24.', '172.25.', '172.26.', '172.27.',
	'172.28.', '172.29.', '172.30.', '172.31.',  # class B private blocks
	'192.0.2.',  # reserved for documentation and example code
	'192.168.',  # class C private block
	'255.255.255.',  # IPv4 broadcast address
) + (
	'2001:db8:',  # reserved for documentation and example code
	'fc00:',  # IPv6 private block
	'fe80:',  # link-local unicast
	'ff00:',  # IPv6 multicast
)

for more info check django-ipware git repo: https://github.com/un33k/django-ipware

3. Run `python manage.py migrate ct_useragents` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   see the info on your visitors

