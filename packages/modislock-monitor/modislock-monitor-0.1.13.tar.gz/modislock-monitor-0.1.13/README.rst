|logo|_

.. image:: https://badge.fury.io/py/modislock-monitor.png
    :target: https://badge.fury.io/py/modislock-monitor

==================
Modis Lock Monitor
==================

Overview
========
Intended to run as a daemon service that monitors the incoming requests from Modis readers. The monitor also
maintains conditions of 2 door sensors as well as 4 possible readers.

Notifications are handled at the monitor but they are sent asynchronously via Redis and Celery.

- Project Homepage: https://github.com/Modis-GmbH/ModisLock-Monitor
- Releases Page: https://github.com/Modis-GmbH/ModisLock-Monitor/releases

Requirements
============
* Supervisor ``apt install supervisor``
* MySQL service is also required to be running on the same machine. ``apt install mysql-server5.5``

During installation, setup will populate the database, but a *root* account with *no password* is required
for the install to structure and populate the database.

Optional
========
For notifications and background tasks, a `redis <https://redis.io/topics/quickstart>`_ server is required.
``apt install redis``

Installation
============
The monitor was designed to run on a Raspberry Pi 3 or CM3 module. For testing you can install it
on a Linux machine and with it, the GPIO emulator `GPIOEmu <https://github.com/paly2/GPIOEmu>`_ will be
installed, which takes the place of the `RPi.GPIO <https://sourceforge.net/projects/raspberry-gpio-python/>`_
package.

.. note:: Validation requests are handled through Raspberry Pi's UART so if running on a Pi3 will need the BT module disabled and the pins configured for UART communications.

Installation can be accomplished with
-------------------------------------
During installation several files are written to areas that require elevated priviledges etc. ``/etc/supervisor/conf.d``

``sudo pip3 install modislock-monitor``

Database Population
___________________
Population of the database happens at installation but can be accomplished after the installation if you don't have a mysql instance running by executing the initialization
script found in ``/etc/modis/modislock_init.sql``

Options
-------
You can adapt the configuration of the monitor by modifying the ``config/default.py`` or ``config/development.py`` or
``config/production.py`` files based on your mode of operation.

.. |logo| image:: http://modis.io/wp-content/uploads/2017/04/logo_100.png
   :align: middle
.. _logo: https://modislab.io