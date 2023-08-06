# Setup tools
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from distutils.util import get_platform
from subprocess import run, CalledProcessError, TimeoutExpired

# Misc
import re
import os


with open('./README.rst', encoding='utf-8') as f:
    readme = f.read()

is_raspberry = True if (get_platform() == 'linux-armv7l') else False
requires = [i.strip() for i in open("./requirements.txt").readlines()] + (['GPIOEmu'] if not is_raspberry else [])


class PostDevelopCommand(develop):
    """Develop command for setuptools

    """
    def run(self):
        # Pre install
        develop.run(self)
        # Post install


class PostInstallCommand(install):
    """Install command for setuptools

    """
    def _exec_sql_file(self, cursor, sql_file):
        from pymysql.err import ProgrammingError, OperationalError
        print("\n[INFO] Executing SQL script file: {}".format(sql_file))
        statement = ""

        for line in open(sql_file):
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                print("\n\n[DEBUG] Executing SQL statement:\n{}".format(statement))
                try:
                    cursor.execute(statement)
                except (OperationalError, ProgrammingError) as e:
                    print("\n[WARN] MySQLError during execute statement \n\tArgs: {}".format(str(e.args)))

                statement = ""

    def _pre_install(self):
        args = ['apt', 'install', '-y', 'libsystemd-dev', 'lm-sensors', 'libffi-dev', 'libssl-dev']

        if not is_raspberry:
            args.append('libsdl2-dev')
        print('Installing external dependencies')

        try:
            result = run(args, timeout=200)
        except Exception as e:
            print('Error installing dependencies: '.format(e))
        else:
            if result.returncode == 0:
                print('Happy')

        if not os.path.exists('/etc/modis'):
            try:
                os.mkdir('/etc/modis', mode=0o755)
            except Exception as e:
                print('Could not create directory: '.format(e))

    def _post_install(self):
        from pymysql import connect
        from pymysql.cursors import DictCursor
        from pymysql.err import InternalError, OperationalError

        connection = None

        try:
            connection = connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='modislock',
                                 charset='utf8mb4',
                                 cursorclass=DictCursor)
        except (InternalError, OperationalError):
            try:
                connection = connect(host='localhost', user='root', password='')
                self._exec_sql_file(connection.cursor(), '/etc/modis/modislock_init.sql')
            except (InternalError, OperationalError):
                print('Database not available')
        finally:
            if connection is not None:
                connection.close()

        try:
            args = ['supervisorctl', 'reread']
            run(args, timeout=30)
        except (CalledProcessError, TimeoutExpired):
            pass

        try:
            args = ['supervisorctl', 'restart', 'monitor:*']
            run(args, timeout=50)
        except (CalledProcessError, TimeoutExpired):
            pass

    def run(self):
        # Pre-install
        self._pre_install()
        # Install
        install.run(self)
        # Post-install
        self._post_install()


setup(
    name='modislock-monitor',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.13',

    description='Monitors slave status, door sensors, and provides validation to slave requests',

    long_description=readme,

    # The project's main homepage.
    url='https://github.com/Modis-GmbH/ModisLock-Monitor',

    # Choose your license
    license='GPL',

    # Author details
    author='Richard Lowe',
    author_email='richard@modislab.com',

    # What does your project relate to?
    keywords=['modis', 'raspberry pi', 'lock', 'serial monitor'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security"
    ],

    platforms=['Linux', 'Raspberry Pi'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requires,

    # If your project only runs on certain Python versions, setting the python_requires argument to the appropriate
    # PEP 440 version specifier string will prevent pip from installing the project on other Python versions.
    python_requires='>=3.5',

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,

    zip_safe=False,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('/etc/supervisor/conf.d', ['deploy/modis_monitor.conf']),
                ('/etc/modis', ['deploy/modislock_init.sql', 'deploy/interfaces.bu'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'modis_monitor = modislock_monitor.run_monitor:main',
            'modis_monitor_worker = modislock_monitor.celery_worker:main'
        ]
    },

    cmdclass={'develop': PostDevelopCommand,
              'install': PostInstallCommand}
)
