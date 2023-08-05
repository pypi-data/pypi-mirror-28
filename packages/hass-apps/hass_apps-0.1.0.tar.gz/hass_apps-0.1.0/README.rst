hass-apps
=========

Some useful apps and snippets to empower Home Assistant and AppDaemon
even more.


Apps
----

All apps for AppDaemon can be found inside the ``hass_apps`` directory
of this repository. Each includes a sample configuration in the file
``doc/apps.yaml.example``.

Currently, the following apps are included:

* `heaty`_:  A highly-configurable, comfortable to use Home Assistant /
  appdaemon app that controls thermostats based on a schedule while still
  facilitating manual intervention at any time.
* **motion_light**:  This app can turn devices on/off according to the
  state of sensors.
  The most obvious use case is controlling lights when motion sensors
  report motion, but other scenarios are imaginable as well. Delays and
  constraints can be configured freely for each individual sensor.

.. _heaty: hass_apps/heaty/doc/README.rst


Installation
------------

In order to use one or more of the apps provided here, please install
the whole ``hass_apps`` package. Don't worry, only the apps you configure
will be loaded.

Install from PyPi:

::

    pip3 install hass-apps

Or clone the GitHub repository to get even the latest changes:

::

    git clone https://github.com/efficiosoft/hass-apps
    cd hass-apps
    pip3 install . --upgrade


A note for hass.io users
~~~~~~~~~~~~~~~~~~~~~~~~

As far as I know, it's not possible to create a plug & play add-on for
hass.io containing hass-apps, because it needs to be installed into
AppDaemon's container.

Even though it's untested, the only actions needed in order to install
under hass.io should be:

1. Install the appdaemon add-on.
2. Copy the ``hass_apps`` folder and the file ``hass_apps_loader.py`` into
   the ``apps`` directory of your AppDaemon container. This is also the
   only thing you need to do when upgrading to a newer version of hass-apps.
3. Continue with the configuration as normal.


Configuration
-------------

1. Get yourself a nice cup of coffee or tea. You'll surely need it.
2. Copy the file ``hass_apps_loader.py`` to your AppDaemon's ``apps``
   directory. This is just a stub that imports the real app's code.
3. Pick one or more apps you want to use.
4. Copy the contents of ``hass_apps/some_app/doc/apps.yaml.example``
   to your ``apps.yaml`` file and adapt it as necessary. The example
   files also contain documentation comments explaining what the
   different settings mean.
5. AppDaemon should have noticed the changes made to ``apps.yaml`` and
   restart its apps automatically.

You're done!


Upgrade
-------

Simply pull upgrades from PyPi:

::

    pip3 install --upgrade hass-apps

Or, if you installed from the git repository:

::

    cd /path/to/your/clone/of/the/repository
    git pull
    pip3 install . --upgrade

Note that AppDaemon doesn't detect changes in the imported modules
automatically and needs to be restarted manually after an upgrade.
