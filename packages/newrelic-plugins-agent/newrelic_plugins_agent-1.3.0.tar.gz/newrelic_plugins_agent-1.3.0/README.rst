NewRelic Plugins Agent
=====================

An agent that polls supported backend systems and submits the results to the
NewRelic platform. Currently supported backend systems are:

- MongoDB

Base Requirements
-----------------
The agent requires Python 2.6 or 2.7 and ``pip`` for installation. Individual plugins backends may require additional libraries and are detailed below.

Configuration File Note
-----------------------
The configuration file uses YAML as its format. Most tickets for non-working installs are due to configuration file formatting errors. Please make sure you are properly formatting your configuration file prior to submitting a ticket. YAML is a whitespace dependent markup format. More information on writing proper YAML can be found at http://yaml.org.

Installation Instructions
-------------------------
1. Install via ``pip`` *:

::

    $ pip install newrelic-plugins-agent

* See ``pip`` installation instructions at http://www.pip-installer.org/en/latest/installing.html

2. Copy the configuration file example from ``/opt/newrelic-plugins-agent/newrelic-plugins-agent.cfg`` to ``/etc/newrelic/newrelic-plugins-agent.cfg`` and edit the configuration in that file.

3. Make a ``/var/log/newrelic`` directory and make sure it is writable by the user specified in the configuration file

4. Make a ``/var/run/newrelic`` directory and make sure it is writable by the user specified in the configuration file

5. Run the app:

::

    $ newrelic-plugins-agent -c PATH-TO-CONF-FILE [-f]

Where ``-f`` is to run it in the foreground instead of as a daemon.

Sample configuration and init.d scripts are installed to ``/opt/newrelic-plugins-agent`` in addition to a PHP script required for APC monitoring.

Installing Additional Requirements
----------------------------------

To use the MongoDB the ``mongodb`` library is required. To easily do
this, make sure you have the latest version of ``pip`` installed (http://www.pip-installer.org/). This should be done after installing the agent itself:

::

    $ pip install newrelic-plugins-agent[mongodb]

If this does not work for you, make sure you are running a recent copy of ``pip`` (>= 1.3).

Plugin Configuration Stanzas
----------------------------
Each plugin can support gathering data from a single or multiple targets. To support multiple targets for a plugin, you create a list of target stanzas:

::

    plugin_name:
      - name: target_name
        host: localhost
        foo: bar
      - name: target_name
        host: localhost
        foo: bar

While you can use the multi-target format for a plugin's configuration stanza like:

::

    plugin_name:
      - name: target_name
        host: localhost
        foo: bar

You can also use a single mapping like follows:

::

    plugin_name:
      name: target_name
      host: localhost
      foo: bar

The fields for plugin configurations can vary due to a plugin's configuration requirements. The name value in each stanza is only required when using multiple targets in a plugin. If it is only a single target, the name will be taken from the server's hostname.

MongoDB Installation Notes
--------------------------
You need to install the pymongo driver, either by running ``pip install pymongo`` or by following the "`Installing Additional Requirements`_" above. Each database you wish to collect metrics for must be enumerated in the configuration.

There are two configuration stanza formats for MongoDB. You must use one or the other, they can not be mixed. For non-authenticated polling, you can simply enumate the databases you would like stats from as a list:

::

      mongodb:
        name: hostname
        host: localhost
        port: 27017
        #admin_username: foo
        #admin_password: bar
        #ssl: False
        #ssl_keyfile: /path/to/keyfile
        #ssl_certfile: /path/to/certfile
        #ssl_cert_reqs: 0  # Should be 0 for ssl.CERT_NONE, 1 for ssl.CERT_OPTIONAL, 2 for ssl.CERT_REQUIRED
        #ssl_ca_certs: /path/to/cacerts file
        databases:
          - database_name_1
          - database_name_2

If your MongoDB server requires authentication, you must provide both admin credentials and database level credentials and the stanza is formatted as a nested array:

::

      mongodb:
        name: hostname
        host: localhost
        port: 27017
        #admin_username: foo
        #admin_password: bar
        #ssl: False
        #ssl_keyfile: /path/to/keyfile
        #ssl_certfile: /path/to/certfile
        #ssl_cert_reqs: 0  # Should be 0 for ssl.CERT_NONE, 1 for ssl.CERT_OPTIONAL, 2 for ssl.CERT_REQUIRED
        #ssl_ca_certs: /path/to/cacerts file
        databases:
          database_name_1:
            username: foo
            password: bar
          database_name_2:
            username: foo
            password: bar

Configuration Example
---------------------

::

    %YAML 1.2
    ---
    Application:
      license_key: REPLACE_WITH_REAL_KEY
      poll_interval: 60
      #newrelic_api_timeout: 10
      #proxy: http://localhost:8080

      mongodb:
        name: hostname
        host: localhost
        port: 27017
        admin_username: foo
        admin_password: bar
        databases:
          database_name_1:
            username: foo
            password: bar
          database_name_2:
            username: foo
            password: bar

    Daemon:
      user: newrelic
      pidfile: /var/run/newrelic/newrelic-plugin-agent.pid

    Logging:
      formatters:
        verbose:
          format: '%(levelname) -10s %(asctime)s %(process)-6d %(processName) -15s %(threadName)-10s %(name) -25s %(funcName) -25s L%(lineno)-6d: %(message)s'
      handlers:
        file:
          class : logging.handlers.RotatingFileHandler
          formatter: verbose
          filename: /var/log/newrelic/newrelic-plugin-agent.log
          maxBytes: 10485760
          backupCount: 3
      loggers:
        newrelic-plugin-agent:
          level: INFO
          propagate: True
          handlers: [console, file]
        requests:
          level: ERROR
          propagate: True
          handlers: [console, file]

Troubleshooting
---------------
- If the installation does not install the ``newrelic-plugin-agent`` application in ``/usr/bin`` then it is likely that ``setuptools`` or ``distribute`` is not up to date. The following commands can be run to install ``distribute`` and ``pip`` for installing the application:

::

    $ curl http://python-distribute.org/distribute_setup.py | python
    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

- If the application installs but doesn't seem to be submitting status, check the logfile which at ``/tmp/newrelic-plugin-agent.log`` if the default example logging configuration is used.
- If the agent starts but dies shortly after ensure that ``/var/log/newrelic`` and ``/var/run/newrelic`` are writable by the same user specified in the daemon section of the configuration file.
- If the agent has died and won't restart, remove any files found in ``/var/run/newrelic/``
