========
mrg_core
========

The common library for all Meteor Research Group scripts. This
library includes all metrec data interfaces, common astronomical routines,
and utility classes.

.. image:: icon.png


Requirements
============

- ``python 2.7, >=3.4``

It is recommended to work with a dedicated Python virtual environment
for this project. The sections below demonstrate how to create a virtual
environment in the user's home directory under the ``venv`` directory.

Ubuntu
------

.. code-block:: console

    sudo apt-get install virtualenv

    mkdir ~/venv
    cd ~/venv
    virtualenv -p python3 mrg_py3

Windows
-------

Download git from and Python 64-bit versions from,

* https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe

and install it taking defaults.

Create a Python virtual environment,

.. code-block:: console

    c:\Python36\Scripts\pip.exe install virtualenv
    mkdir %HOMEPATH%\venv
    cd %HOMEPATH%\venv
    c:\Python36\python.exe -m virtualenv mrg_py3

To activate and deactivate the newly created virtual environment
using the following commands,

.. code-block:: console

    %HOMEPATH%\venv\mrg_py3\Scripts\activate.bat
    deactivate


Installation
============

First activate the virtual environment before executing the following commands.

Install as end-user
-------------------

If there is no need to modify the source code, then it is recommended
to install the latest release from the official Python PyPI server.

.. code-block:: console

    pip install --upgrade mrg_core


Install from source
-------------------

For developers of this package, the project source code should be installed
using git. Then the dependencies may be installed in the virtual environment
using the ``pip install`` commands.

Windows
~~~~~~~

Download and install git from,

* https://git-scm.com/download/win

.. code-block:: console

    mkdir ~/PycharmProjects
    cd ~/PycharmProjects
    git clone https://gitlab.com/mrg-tools/mrg_test_data.git
    git clone https://gitlab.com/mrg-tools/mrg_core.git
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

Ubuntu
~~~~~~

.. code-block:: console

    sudo apt-get install git
    mkdir ~/PycharmProjects
    cd ~/PycharmProjects
    git clone https://gitlab.com/mrg-tools/mrg_test_data.git
    git clone https://gitlab.com/mrg-tools/mrg_core.git
    pip install -r requirements.txt
    pip install -r requirements-dev.txt


Developer Commands
------------------

Activate the virtual environment.

To run the unittests,

.. code-block:: console

    cd ~/PycharmProjects/mrg_core
    pytest

To run the pylint,

.. code-block:: console

    cd ~/PycharmProjects/mrg_core
    pylint --rcfile pylint.cfg mrg_core

To build the sphinx documentation,

.. code-block:: console

    cd ~/PycharmProjects/mrg_core/docs
    make html
    # ubuntu
    firefox build/html/index.html
    # windows
    start build/html/index.html

Releasing a new version to PyPI server,

Make sure the %HOMEPATH%/.pypirc file looks similar to the following,

.. code-block:: console

    [distutils]
    index-servers =
      test-pypi
      pypi

    [pypi]
    repository=https://upload.pypi.org/legacy/
    username=<user>
    password=*******

    [test-pypi]
    repository=https://test.pypi.org/legacy/
    username=<user>
    password=*******

Releasing a new version requires all changes to be committed and
a new tag to be issued,

.. code-block:: console

    cd ~/PycharmProjects/mrg_core
    git add <modified file>
    git commit -m "+REL: 0.1.1"
    git tag 0.1.1
    python setup.py bdist_wheel upload


Database Setup
==============

MariaDB is a port of mysql with essentially the same interface as that of mysql.
It is currently included in many Linux distributions.
The following commands will help you setup a MRG database.



Install MariaDB
---------------

.. code-block:: console

    # install the mysql database server
    sudo apt install mariadb-server
    sudo apt install mysql-workbench

    # set the root password
    sudo mysql_secure_installation

    # create a new root user that does not require sudo to access mysql
    sudo mysql -u root -p
    # Enter password: ********
    MariaDB [(none)]> use mysql;
    MariaDB [mysql]> GRANT ALL PRIVILEGES ON *.* TO 'root2'@'localhost' IDENTIFIED BY 'new_password' WITH GRANT OPTION;
    MariaDB [mysql]> FLUSH PRIVILEGES;
    MariaDB [mysql]> quit

    # test the new root user (no space after -p
    mysql -u root2 -pnew_password
    # or: mysql -u root2 --password=new_password


Create MRG Database
-------------------

.. code-block:: console

    # install virtual environment and mrg_core
    virtualenv ~/venv/mrg35 --python=python3.5
    source ~/venv/mrg35/bin/activate
    python --version
    # check that the output is: Python 3.5.2
    (mrg35)$ pip install mrg_core

    # create a VMO database
    (mrg35)$ mrgdbadmin --help
    (mrg35)$ mrgdbadmin create -n vmo1 -u root2
    (mrg35)$ mysql -uvmo1 -pvmo1 vmo1
    MariaDB [vmo2]> show tables;
    MariaDB [vmo2]> quit
    (mrg35)$ mrgdbadmin count -n vmo1 -u root2
    (mrg35)$ mrgdbadmin list -n vmo1 -u root2
    (mrg35)$ mrgdbadmin drop -n vmo1 -u root2

    # import VMO file system data into VMO database
    (mrg35)$ mrgdb --help
    (mrg35)$ export vmo_db="mysql://vmo1:vmo1@localhost:0/vmo1"
    (mrg35)$ export vmo_dir="/media/hsmit/B810F71810F6DC76"
    (mrg35)$ mrgdb validate -d "$vmo_dir/2015/2015????/ICC[7|9]" -db=$vmo_db
    (mrg35)$ mrgdb import   -d "$vmo_dir/2015/2015????/ICC[7|9]" -db=$vmo_db -SRC



Export to SQLite
----------------

.. code-block:: console

    # convert mysql database to sqlite
    mysqldump vmo1 -u vmo1 -p > vmo1.sql
    mrg2sqlite -i vmo1.sql -o vmo1.db

Usage
=====

This packages contains many runnable scripts. These are listed below,

* mrgdb
* mrgdbadmin
* mrg2sqlite
* mrgarchive
* mrgpasswd

TODO: describe the different scripts.

Documentation
=============

The documentation can be found at this link: https://mrg-tools.gitlab.io/mrg_core/


License
=======

ESA Software Community License - Type 3. See License File.

