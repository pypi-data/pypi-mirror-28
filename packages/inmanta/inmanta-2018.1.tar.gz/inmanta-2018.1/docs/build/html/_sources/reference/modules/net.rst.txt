Module net
==========

 * License: Apache 2.0
 * Version: 0.5.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/net.git

Typedefs
--------

.. inmanta:typedef:: net::mac_addr

   * Base type ``string``
   * Type constraint ``(self regex re.compile('^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}|$'))``

.. inmanta:typedef:: net::vlan_id

   * Base type ``number``
   * Type constraint ``((self >= 0) and (self < 4096))``


Entities
--------

.. inmanta:entity:: net::Interface

   Parents: :inmanta:entity:`std::Entity`

   This interface models an ethernet network interface.
   

   .. inmanta:attribute:: string net::Interface.name


   .. inmanta:attribute:: number net::Interface.mtu=1500


   .. inmanta:attribute:: net::mac_addr net::Interface.mac=''


   .. inmanta:attribute:: bool net::Interface.vlan=False


   .. inmanta:relation:: std::Host net::Interface.host [1]

      other end: :inmanta:relation:`std::Host.ifaces [0:\*]<std::Host.ifaces>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`

