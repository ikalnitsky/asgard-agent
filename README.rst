============
Asgard Agent
============

Asgard Agent is a small discovery toolset that provides console scripts to
do lookuping and heartbeating from node.


Requirements
------------

Despite the agent makes `IPA`_ compatible ``lookup`` request, it's indented
to be used with `Ironic Asgard Driver`_ and `Ironic Ansible Driver`_. Other
drivers may not work.

.. _IPA: https://wiki.openstack.org/wiki/Ironic-python-agent
.. _Ironic Asgard Driver: https://github.com/ikalnitsky/ironic-asgard-driver
.. _Ironic Ansible Driver: https://review.openstack.org/#/c/325974


Design Decisions
----------------

* Ironic API endpoint is passed as ``ironic_api_url`` kernel parameter in
  order to be compatible with Ironic builtin ``PXEBoot`` driver.

* Asgard Agent is not an agent. It's a set of entry points (console scripts)
  to trigger various actions. Having them as standalone scripts allows us
  to integrate them with third-party schedulers (e.g. cron), run manually
  on demand or skip implementation of auto-healing code.
