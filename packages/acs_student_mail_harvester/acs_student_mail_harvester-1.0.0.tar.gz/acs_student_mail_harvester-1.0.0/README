About
=====

Console app and Python API for harvesting email addresses of our `ACS`_
students during their first week of ACS lab coursework.

.. _`ACS`: http://www.acs.uns.ac.rs/

Instructions for teaching assistants
------------------------------------

These steps should be performed with your every student group, at the very
start of their first week in the ACS labs:

#. Copy the ``examples/student-info.ini`` file into
   ``ispitni_materijaliA/.eXXXXX/`` and ``ispitni_materijaliB/.eXXXXX/``

#. Ask the administrator to switch the lab to the "exam" mode (aka "provera")

#. Wait for all of the students to login

#. Instruct the students to:

   #. Locate the ``student-info.ini`` file in their ``$HOME/$STUDENT_ID``
      directory

   #. Update the contents of the file with their own information

   #. Save the file and close the editor

   #. Logout

#. Ask the administrator to collect the exam ``.tar`` archive and switch the lab
   to the "normal" mode

Please send your collected exam archives to your professors as soon as you can.

Installation
============

To install acs_student_mail_harvester run::

    $ pip install acs_student_mail_harvester

Console app usage
=================

Quick start::

    $ acs_student_mail_harvester students.csv --tar-path=examples/

Show help::

    $ acs_student_mail_harvester --help

Python API usage
================

Quick start::

    >>> from acs_student_mail_harvester import get_student_info, store_results_to
    >>> student_info = get_student_info('examples/')
    >>> store_results_to('students.csv', student_info)


Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://bitbucket.org/petar/acs_student_mail_harvester/issues/new
.. _`the repository`: http://bitbucket.org/petar/acs_student_mail_harvester
.. _`AUTHORS`: https://bitbucket.org/petar/acs_student_mail_harvester/src/default/AUTHORS
