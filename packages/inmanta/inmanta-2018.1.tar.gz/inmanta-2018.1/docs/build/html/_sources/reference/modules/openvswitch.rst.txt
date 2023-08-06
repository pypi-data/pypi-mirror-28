Module openvswitch
==================

 * License: Apache 2.0
 * Version: 0.4
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/openvswitch.git

Entities
--------

.. inmanta:entity:: openvswitch::Bond

   Parents: :inmanta:entity:`openvswitch::OVSPort`

   .. inmanta:attribute:: number openvswitch::Bond.mtu


   .. inmanta:attribute:: string openvswitch::Bond.lacp_time='fast'


   .. inmanta:attribute:: string openvswitch::Bond.trunks


   .. inmanta:attribute:: string openvswitch::Bond.interfaces


   .. inmanta:attribute:: bool openvswitch::Bond.lacp=True


   .. inmanta:attribute:: string openvswitch::Bond.bond_mode='balance-tcp'


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openvswitch::Bridge

   Parents: :inmanta:entity:`std::Entity`

   A network bridge
   

   .. inmanta:attribute:: string openvswitch::Bridge.name


   .. inmanta:relation:: openvswitch::OVSPort openvswitch::Bridge.ports [0:\*]

      other end: :inmanta:relation:`openvswitch::OVSPort.bridge [1]<openvswitch::OVSPort.bridge>`

   .. inmanta:relation:: openvswitch::Bridge openvswitch::Bridge.patch_from [0:\*]

      other end: :inmanta:relation:`openvswitch::Bridge.patch_to [0:\*]<openvswitch::Bridge.patch_to>`

   .. inmanta:relation:: std::Host openvswitch::Bridge.host [1]

      other end: :inmanta:relation:`std::Host.bridges [0:\*]<std::Host.bridges>`

   .. inmanta:relation:: openvswitch::Bridge openvswitch::Bridge.patch_to [0:\*]

      other end: :inmanta:relation:`openvswitch::Bridge.patch_from [0:\*]<openvswitch::Bridge.patch_from>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openvswitch::bridgeUCA`
      * :inmanta:implementation:`openvswitch::bridgeRDO`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openvswitch::bridgeUCA`
        constraint ``std::familyof(host.os,'ubuntu')``
      * :inmanta:implementation:`openvswitch::bridgeRDO`
        constraint ``((std::familyof(host.os,'rhel') and (host.os.version >= 7)) or std::familyof(host.os,'fedora'))``


.. inmanta:entity:: openvswitch::Interface

   Parents: :inmanta:entity:`openvswitch::OVSPort`

   .. inmanta:attribute:: number openvswitch::Interface.tag


   .. inmanta:attribute:: ip::ip openvswitch::Interface.netmask


   .. inmanta:attribute:: number openvswitch::Interface.mtu


   .. inmanta:attribute:: ip::ip openvswitch::Interface.ip_address


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openvswitch::OVSCommon

   Parents: :inmanta:entity:`std::Entity`

   Installation and configuration of openvswitch (without adding any switches)
   

   .. inmanta:attribute:: string openvswitch::OVSCommon.sdn_controller=''


   .. inmanta:relation:: ip::Host openvswitch::OVSCommon.host [1]

      other end: :inmanta:relation:`ip::Host.ovs_common [0:1]<ip::Host.ovs_common>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openvswitch::ovsCommonUCA`
      * :inmanta:implementation:`openvswitch::ovsCommonRDO`
      * :inmanta:implementation:`openvswitch::ovsSDN`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openvswitch::ovsCommonUCA`
        constraint ``std::familyof(host.os,'ubuntu')``
      * :inmanta:implementation:`openvswitch::ovsCommonRDO`
        constraint ``((std::familyof(host.os,'rhel') and (host.os.version >= 7)) or std::familyof(host.os,'fedora'))``
      * :inmanta:implementation:`openvswitch::ovsSDN`
        constraint ``(sdn_controller != '')``


.. inmanta:entity:: openvswitch::OVSPort

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string openvswitch::OVSPort.name


   .. inmanta:relation:: openvswitch::Bridge openvswitch::OVSPort.bridge [1]

      other end: :inmanta:relation:`openvswitch::Bridge.ports [0:\*]<openvswitch::Bridge.ports>`


Implementations
---------------

.. inmanta:implementation:: openvswitch::bridgeRDO

.. inmanta:implementation:: openvswitch::bridgeUCA

.. inmanta:implementation:: openvswitch::ovsCommonRDO

.. inmanta:implementation:: openvswitch::ovsCommonUCA

.. inmanta:implementation:: openvswitch::ovsSDN
