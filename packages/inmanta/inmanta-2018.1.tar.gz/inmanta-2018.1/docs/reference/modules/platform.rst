Module platform
===============

 * License: ASL 2.0
 * Version: 0.2.0
 * Upstream project: https://github.com/inmanta/platform.git

Entities
--------

.. inmanta:entity:: platform::UserdataBootstrap

   Parents: :inmanta:entity:`std::Entity`

   Bootstrap an inmanta agent on the host by passing a shell script to the virtual machine user data.
   Setting the INMANTA_RELEASE environment variable to dev will install the agent from development snapshots.
   
   The user script will force the correct hostname and setenforce 0 to disable enforcing selinux.
   
   .. warning:: Currently this script only support centos 7 or equivalent (rhel7, aws linux, sl7, ...).
   

   .. inmanta:relation:: platform::UserdataVM platform::UserdataBootstrap.vm [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`platform::userdataBootstrap`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`platform::userdataBootstrap`


.. inmanta:entity:: platform::UserdataVM

   Parents: :inmanta:entity:`std::Entity`

   Base class for virtual machines that provide a user_data attribute through which a shell script can be injected
   at first boot of the virtual machine.
   
   

   .. inmanta:attribute:: string platform::UserdataVM.user_data

      A shell script that is executed at first boot.


Implementations
---------------

.. inmanta:implementation:: platform::userdataBootstrap
