Module dns
==========

 * License: Apache 2.0
 * Version: 0.1.8
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/dns.git

Typedefs
--------

.. inmanta:typedef:: dns::hoststring

   * Base type ``string``
   * Type constraint ``(self regex re.compile('^[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*\\.?$'))``


Entities
--------

.. inmanta:entity:: dns::A

   Parents: :inmanta:entity:`dns::Record`

   An A record
   
   

   .. inmanta:attribute:: ip::ip dns::A.ipaddress

      The address to point this record to

   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::aImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::aImpl`


.. inmanta:entity:: dns::AAAA

   Parents: :inmanta:entity:`dns::Record`

   .. inmanta:attribute:: string dns::AAAA.ipaddress


   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::aaaaImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::aaaaImpl`


.. inmanta:entity:: dns::Cname

   Parents: :inmanta:entity:`dns::Record`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::cnameImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::cnameImpl`


.. inmanta:entity:: dns::DnsServer

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: ip::ip dns::DnsServer.ipaddress


   .. inmanta:relation:: dns::Zone dns::DnsServer.slave_zones [0:\*]

      other end: :inmanta:relation:`dns::Zone.slaves [0:\*]<dns::Zone.slaves>`

   .. inmanta:relation:: dns::Zone dns::DnsServer.master_zones [0:\*]

      other end: :inmanta:relation:`dns::Zone.master [1]<dns::Zone.master>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: dns::MX

   Parents: :inmanta:entity:`dns::Record`

   .. inmanta:attribute:: number dns::MX.priority=10


   .. inmanta:attribute:: dns::hoststring dns::MX.server


   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::mxImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::mxImpl`


.. inmanta:entity:: dns::NS

   Parents: :inmanta:entity:`dns::Record`

   .. inmanta:attribute:: dns::hoststring dns::NS.server


   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::nsImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::nsImpl`


.. inmanta:entity:: dns::PTR

   Parents: :inmanta:entity:`dns::Record`

   .. inmanta:attribute:: ip::ip dns::PTR.ipaddress


   .. inmanta:attribute:: string dns::PTR.name


   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::ptrImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::ptrImpl`


.. inmanta:entity:: dns::Record

   Parents: :inmanta:entity:`std::Entity`

   A generic dns resource record
   

   .. inmanta:attribute:: string dns::Record.value


   .. inmanta:attribute:: string dns::Record.resource=''


   .. inmanta:attribute:: string dns::Record.record_type


   .. inmanta:relation:: dns::Zone dns::Record.zone [1]

      other end: :inmanta:relation:`dns::Zone.records [0:\*]<dns::Zone.records>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: dns::Server

   Parents: :inmanta:entity:`ip::services::Server`, :inmanta:entity:`dns::DnsServer`

   A dns server
   

   .. inmanta:attribute:: string dns::Server.allow_recursion=''


   .. inmanta:attribute:: string dns::Server.forwarders=''


   .. inmanta:attribute:: bool dns::Server.recursive=True



.. inmanta:entity:: dns::SlaveZone

   Parents: :inmanta:entity:`dns::Zone`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: dns::TXT

   Parents: :inmanta:entity:`dns::Record`

   .. inmanta:attribute:: string dns::TXT.data


   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::txtImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`dns::txtImpl`


.. inmanta:entity:: dns::Zone

   Parents: :inmanta:entity:`std::Entity`

   A dns zone.
   
   

   .. inmanta:attribute:: string dns::Zone.domain


   .. inmanta:attribute:: number dns::Zone.refresh=7200


   .. inmanta:attribute:: string dns::Zone.hostmaster


   .. inmanta:attribute:: number dns::Zone.ttl=3600


   .. inmanta:attribute:: number dns::Zone.expiry=1209600


   .. inmanta:attribute:: number dns::Zone.retry=600


   .. inmanta:attribute:: bool dns::Zone.add_ns=False


   .. inmanta:relation:: dns::DnsServer dns::Zone.master [1]

      other end: :inmanta:relation:`dns::DnsServer.master_zones [0:\*]<dns::DnsServer.master_zones>`

   .. inmanta:relation:: dns::Record dns::Zone.records [0:\*]

      other end: :inmanta:relation:`dns::Record.zone [1]<dns::Record.zone>`

   .. inmanta:relation:: dns::DnsServer dns::Zone.slaves [0:\*]

      other end: :inmanta:relation:`dns::DnsServer.slave_zones [0:\*]<dns::DnsServer.slave_zones>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`dns::addNS`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`
      * :inmanta:implementation:`dns::addNS`
        constraint ``add_ns``


Implementations
---------------

.. inmanta:implementation:: dns::aImpl

.. inmanta:implementation:: dns::aaaaImpl

.. inmanta:implementation:: dns::addNS

.. inmanta:implementation:: dns::cnameImpl

.. inmanta:implementation:: dns::mxImpl

.. inmanta:implementation:: dns::nsImpl

.. inmanta:implementation:: dns::ptrImpl

.. inmanta:implementation:: dns::txtImpl

Plugins
-------

.. py:function:: dns.filter_record(record: std::hoststring, zone: dns::Zone) -> std::hoststring

   Filter the zone part from the record
   

.. py:function:: dns.ip_to_arpa(ip_addr: ip::ip) -> std::hoststring

   Convert an ip to the addr.arpa notation
   

.. py:function:: dns.quote(data: string) -> string
