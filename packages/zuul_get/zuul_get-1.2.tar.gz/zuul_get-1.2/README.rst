========
zuul_get
========

The ``zuul_get`` script retrieves status updates from OpenStack's Zuul
deployment and returns the status of a particular CI job. The script now
supports version 2 and 3 of Zuul.

Installation
------------

The easiest method is to use pip:

.. code-block:: console

   pip install zuul_get


Running the script
------------------

Provide a six-digit gerrit review number as an argument to retrieve the CI job
URLs from Zuul's JSON status file. Here's an example:

.. code-block:: console

    $ zuul_get 510588
    +---------------------------------------------------+---------+----------------------+
    | Zuulv2 Jobs for 510588                            |         |                      |
    +---------------------------------------------------+---------+----------------------+
    | gate-ansible-hardening-docs-ubuntu-xenial         | Queued  |                      |
    | gate-ansible-hardening-linters-ubuntu-xenial      | Queued  |                      |
    | gate-ansible-hardening-ansible-func-centos-7      | Success | https://is.gd/ifQc2I |
    | gate-ansible-hardening-ansible-func-ubuntu-xenial | Queued  |                      |
    | gate-ansible-hardening-ansible-func-opensuse-423  | Success | https://is.gd/RiiZFW |
    | gate-ansible-hardening-ansible-func-debian-jessie | Success | https://is.gd/gQ0izk |
    | gate-ansible-hardening-ansible-func-fedora-26     | Success | https://is.gd/w9zTCa |
    +---------------------------------------------------+---------+----------------------+
    +-----------------------------------------------------+--------+--+
    | Zuulv3 Jobs for 510588                              |        |  |
    +-----------------------------------------------------+--------+--+
    | build-openstack-sphinx-docs                         | Queued |  |
    | openstack-tox-linters                               | Queued |  |
    | legacy-ansible-func-centos-7                        | Queued |  |
    | legacy-ansible-func                                 | Queued |  |
    | legacy-ansible-func-opensuse-423                    | Queued |  |
    | legacy-ansible-hardening-ansible-func-debian-jessie | Queued |  |
    | legacy-ansible-hardening-ansible-func-fedora-26     | Queued |  |
    +-----------------------------------------------------+--------+--+


Currently running jobs will have a link displayed which allows you to view
the progress of a particular job. Zuulv2 uses ``telnet://`` links while
Zuulv3 has a continuously updating page in your browser.

Completed jobs will have a link to the job results.

Contributing
------------

Pull requests and GitHub issues are always welcome!
