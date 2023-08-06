WQt - A Qt project manager
==========================

WQt is a Qt project management tool which allows the user to create,
update, build, and run Qt projects from command line. It uses CMake to
build the project, hence making it compatible with almost any text
editor and IDE.

Prerequisites
-------------

In order for this tool to work, the user needs to make sure the
preequisites discussed below are met.

-  Install ``Qt`` for your machine
-  Add Qt’s bin folder to the path

   -  This will depend on the compiler you installed through Qt
      installer
   -  Ex: ``/usr/doge/applications/Qt/5.10.0/clang_64/bin``

-  Install ``CMake`` for your machine
-  Install ``Make`` and basic ``C/C++`` tools

Project Structure
-----------------

WQt tries to define a project structure for the user. This is done to
organize the Qt code and to make it is easier to build and compile. Any
custom structure may break the functionality of the tool and hence
should be avoided.

::

    wqt create

The command above is used to create a project structure. This will
initialize the project will add template files to get the user started.
Qt can have multiple type of applications, hence **three** of these
applications are supported: ``widgets``, ``quick`` and ``console``. The
``create`` command will take an argument of which Qt application to
create and one of the above can be specified. This will then create a
project structure for that particular application. The basic project
structure is as follow:

::

    project/
        lib/
        src/
        res/
        wqt/
            cmake/
            helper/
        .gitignore
        config.json
        CMakeLists.txt

Configurations and Updates
--------------------------

Every project needs to have some way of configuring properties and this
is why there is a ``config.json`` file in every ``WQt`` project. This
file is very important because it contains critical information need to
make the ``build``, and ``run`` possible. This configuration file is
different based on which machine the project is created on. Config
files’ templates are:

**Mac OS**

.. figure:: screenshots/config_mac.png
   :alt: Mac OS config

   config-mac

**Windows and Linux**

.. figure:: screenshots/config_others.png
   :alt: Mac OS config

   config-mac

Looking at these configuration files, you can see that the fields are
defined without user needed to change them. This is done because we
wanted to have a system where the user ``creates`` the project and then
it runs ``immediately``. The ``name-project`` field is automatically
filled with the name of the project folder. Mac OS needs a bit more
information to create a ``.app`` file and hence extra fields are
provided in the configuration file. **Note: These fields can be modified
and the project will adjust accordingly**

In order for the new configurations to take affect, ``update`` command
is used

::

    wqt update

This command updates the ``CMakeLists.txt`` file and makes necessary
changes to the project based on the ``config.json`` properties. This
command is a must run for the new configurations to be accepted. **Note:
it is useful to run his command after cloning a WQt project repo to have
it customized according to your machine**

Building the project
--------------------

WQt provides a way to build the project with just one command. All the
build files are stored in the ``wqt/build`` folder. This folder is
included in the ``.gitignore`` by default. After building the project, a
``bin`` folder is created to store the executable and all the resources
it needs. This file is also a part of ``.gitignore`` by default. In the
order to build the project, ``build`` command is used.

::

    wqt build

Important information
---------------------

As you all are reading this, you should know that all these commands
only work when you are in the project directory. If you are not in the
project directory, ``--path <PATH>`` optional command can be added to
specify the project path.

Run and Preview
---------------

Qt is mostly used for creating graphical applications, so it won’t be
fun if you couldn’t run and preview the application. WQt comes with two
such commands which can help you preview and run your project code. The
first such command is ``run``

::

    wqt run

This command will ``build`` the project and opens the ``executable``
file on your machine. This feature is supported on ``windows``,
``mac OS`` and ``linux``. This does not work on ``windows subsystem`` or
any other ``linux emulator`` running on ``windows``.

The other such command is ``preview-qml``. As the name suggest it helps
you preview the ``qml`` files in your project. For this command to work
your project application type has to be ``quick``. In order to find the
``qml`` files in your project, the tool looks into the ``res/qml``
folder and shows you a list of those files. You can then run

::

    wqt list-qml

::

    wqt preview-qml <qml file name>

As a side note the tool accepts both the full name with extention and
without extension.

Other useful commands and features
----------------------------------

``list-libs``
~~~~~~~~~~~~~

This command is useful if you want to see which ``Qt`` libraries are
included in the project. These are the ``core Qt`` libraries and not
custom libraries.

::

    wqt list-libs

``add-lib``
~~~~~~~~~~~

This command is useful if you want to add a ``core Qt`` library to the
project. The tool will add this library to the ``config.json`` file and
will update the project for the changes to take an affect. Next time
when the project builds, that library is used in the build. There are no
checks performed to see if this library being added is indeed
``core Qt`` library.

::

    wqt add-lib <library name>

``rm-lib``
~~~~~~~~~~

This command is useful if you want to remove a ``core Qt`` library from
the project. The tool will remove this library from the ``config.json``
file and will update the project for the changes to take an affect. Next
time when the project builds, that library is not used in the build.

::

    wqt add-lib <library name>

``list-types``
~~~~~~~~~~~~~~

This command is is useful to see which ``Qt`` application types are
compatible with WQt. It will show the list of those application types.

::

    wqt list-types
