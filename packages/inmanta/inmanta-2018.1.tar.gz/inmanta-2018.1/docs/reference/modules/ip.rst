Module ip
=========

 * License: Apache 2.0
 * Version: 0.10.0
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2016.5 or higher
 * Upstream project: https://github.com/inmanta/ip.git

Typedefs
--------

.. inmanta:typedef:: ip::cidr

   * Base type ``string``
   * Type constraint ``(self regex re.compile('^([0-9]{1,3})(\\.[0-9]{1,3}){3}.[0-9]{1,2}$'))``

.. inmanta:typedef:: ip::ip

   * Base type ``string``
   * Type constraint ``(ip::is_valid_ip(self) == True)``

.. inmanta:typedef:: ip::port

   * Base type ``number``
   * Type constraint ``((self >= 0) and (self < 65536))``

.. inmanta:typedef:: ip::protocol

   * Base type ``string``
   * Type constraint ``(((((self == 'tcp') or (self == 'udp')) or (self == 'icmp')) or (self == 'sctp')) or (self == 'all'))``


Entities
--------

.. inmanta:entity:: ip::Address

   Parents: :inmanta:entity:`ip::Alias`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::Alias

   Parents: :inmanta:entity:`ip::IP`

   .. inmanta:attribute:: ip::ip ip::Alias.netmask='0.0.0.0'


   .. inmanta:attribute:: number ip::Alias.alias=0


   .. inmanta:attribute:: bool ip::Alias.dhcp=False


   .. inmanta:relation:: ip::services::Server ip::Alias.server [0:\*]

      other end: :inmanta:relation:`ip::services::Server.ips [0:\*]<ip::services::Server.ips>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::DstService

   Parents: :inmanta:entity:`ip::Service`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::Host

   Parents: :inmanta:entity:`std::Host`

   A host that has an ip attribute for easy ip address access in the configuration
   model.
   
   

   .. inmanta:attribute:: string ip::Host.remote_user='root'

      The remote user for the remote agent to login with

   .. inmanta:attribute:: ip::port ip::Host.remote_port=22

      The remote port for this remote agent to use.

   .. inmanta:attribute:: bool ip::Host.remote_agent=False

      Start the mgmt agent for this node on the server and use remote io (ssh)

   .. inmanta:attribute:: ip::ip ip::Host.ip

      The ipaddress of this node

   .. inmanta:relation:: ip::services::Client ip::Host.clients [0:\*]

      other end: :inmanta:relation:`ip::services::Client.host [1]<ip::services::Client.host>`

   .. inmanta:relation:: ip::services::Server ip::Host.servers [0:\*]

      other end: :inmanta:relation:`ip::services::Server.host [1]<ip::services::Server.host>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::hostDefaults`


.. inmanta:entity:: ip::IP

   Parents: :inmanta:entity:`std::Entity`

   Base class for all ip addresses
   

   .. inmanta:attribute:: ip::ip ip::IP.v4='0.0.0.0'


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::Network

   Parents: :inmanta:entity:`std::Entity`

   A network in this infrastructure.
   

   .. inmanta:attribute:: bool ip::Network.dhcp


   .. inmanta:attribute:: string ip::Network.netmask


   .. inmanta:attribute:: string ip::Network.name


   .. inmanta:attribute:: string ip::Network.network


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::Port

   Parents: :inmanta:entity:`ip::PortRange`

   .. inmanta:attribute:: ip::port ip::Port.high=0


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::PortRange

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: ip::port ip::PortRange.high


   .. inmanta:attribute:: ip::port ip::PortRange.low


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::Service

   Parents: :inmanta:entity:`std::Entity`

   Define a service as a protocol and a source and destination port range
   

   .. inmanta:attribute:: ip::protocol ip::Service.proto


   .. inmanta:relation:: ip::PortRange ip::Service.dst_range [0:\*]

   .. inmanta:relation:: ip::services::BaseServer ip::Service.listening_servers [0:\*]

      other end: :inmanta:relation:`ip::services::BaseServer.services [0:\*]<ip::services::BaseServer.services>`

   .. inmanta:relation:: ip::PortRange ip::Service.src_range [0:\*]

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::BaseClient

   Parents: :inmanta:entity:`std::Entity`

   Base client class that connects to a server
   

   .. inmanta:relation:: ip::services::BaseServer ip::services::BaseClient.servers [0:\*]

      other end: :inmanta:relation:`ip::services::BaseServer.clients [0:\*]<ip::services::BaseServer.clients>`


.. inmanta:entity:: ip::services::BaseServer

   Parents: :inmanta:entity:`std::Entity`

   Base class for servers that accept connections from clients
   

   .. inmanta:relation:: ip::services::BaseClient ip::services::BaseServer.clients [0:\*]

      other end: :inmanta:relation:`ip::services::BaseClient.servers [0:\*]<ip::services::BaseClient.servers>`

   .. inmanta:relation:: ip::Service ip::services::BaseServer.services [0:\*]

      other end: :inmanta:relation:`ip::Service.listening_servers [0:\*]<ip::Service.listening_servers>`


.. inmanta:entity:: ip::services::Client

   Parents: :inmanta:entity:`ip::services::BaseClient`

   This interface models a client that is linked to a host
   

   .. inmanta:relation:: ip::Host ip::services::Client.host [1]

      other end: :inmanta:relation:`ip::Host.clients [0:\*]<ip::Host.clients>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::Server

   Parents: :inmanta:entity:`ip::services::BaseServer`

   This interface models a server that accepts connections from a client
   

   .. inmanta:relation:: ip::Host ip::services::Server.host [1]

      other end: :inmanta:relation:`ip::Host.servers [0:\*]<ip::Host.servers>`

   .. inmanta:relation:: ip::Alias ip::services::Server.ips [0:\*]

      other end: :inmanta:relation:`ip::Alias.server [0:\*]<ip::Alias.server>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::VirtualClient

   Parents: :inmanta:entity:`ip::services::BaseClient`, :inmanta:entity:`ip::services::VirtualSide`

   This interface models a virtual client. It can for example represent
   all clients that exist on the internet.
   

   .. inmanta:attribute:: string ip::services::VirtualClient.name


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::VirtualHost

   Parents: :inmanta:entity:`ip::services::VirtualScope`

   An address represented by a hostname
   

   .. inmanta:attribute:: std::hoststring ip::services::VirtualHost.hostname


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::VirtualIp

   Parents: :inmanta:entity:`ip::services::VirtualScope`

   Only one ip
   

   .. inmanta:attribute:: ip::ip ip::services::VirtualIp.address



.. inmanta:entity:: ip::services::VirtualNetwork

   Parents: :inmanta:entity:`ip::services::VirtualScope`

   Define a virtual network segment
   

   .. inmanta:attribute:: ip::ip ip::services::VirtualNetwork.netmask


   .. inmanta:attribute:: ip::ip ip::services::VirtualNetwork.network



.. inmanta:entity:: ip::services::VirtualRange

   Parents: :inmanta:entity:`ip::services::VirtualScope`

   A range defined by from/to
   

   .. inmanta:attribute:: ip::ip ip::services::VirtualRange.to


   .. inmanta:attribute:: ip::ip ip::services::VirtualRange.from


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ip::services::VirtualScope

   Parents: :inmanta:entity:`std::Entity`

   This interface represents a scope to determine what a virtual client
   or server is.
   

   .. inmanta:relation:: ip::services::VirtualSide ip::services::VirtualScope.side [0:\*]

      other end: :inmanta:relation:`ip::services::VirtualSide.scope [0:\*]<ip::services::VirtualSide.scope>`


.. inmanta:entity:: ip::services::VirtualServer

   Parents: :inmanta:entity:`ip::services::BaseServer`, :inmanta:entity:`ip::services::VirtualSide`

   Same as VirtualClient but then for a server
   

   .. inmanta:attribute:: string ip::services::VirtualServer.name



.. inmanta:entity:: ip::services::VirtualSide

   Parents: :inmanta:entity:`std::Entity`

   A base class for a virtual server or client
   

   .. inmanta:relation:: ip::services::VirtualScope ip::services::VirtualSide.scope [0:\*]

      other end: :inmanta:relation:`ip::services::VirtualScope.side [0:\*]<ip::services::VirtualScope.side>`


Implementations
---------------

.. inmanta:implementation:: ip::agentConfig

Plugins
-------

.. py:function:: ip.cidr_to_network(cidr: string) -> string

   Given cidr return the network address
   

.. py:function:: ip.concat(host: std::hoststring, domain: std::hoststring) -> std::hoststring

   Concat host and domain
   

.. py:function:: ip.connect_to(scope: ip::services::VirtualScope) -> string

.. py:function:: ip.hostname(fqdn: string) -> string

   Return the hostname part of the fqdn
   

.. py:function:: ip.ipindex(addr: ip::cidr, position: number) -> string

   Return the address at position in the network.
   

.. py:function:: ip.ipnet(addr: ip::cidr, what: string) -> string

.. py:function:: ip.is_valid_ip(addr: string) -> bool

.. py:function:: ip.net_to_nm(network_addr: string) -> string

.. py:function:: ip.netmask(cidr: number) -> ip::ip

   Given the cidr, return the netmask
   

.. py:function:: ip.network(ip: ip::ip, cidr: string) -> string

   Given the ip and the cidr, return the network address
   

.. py:function:: ip.networkaddress(ip: ip::Alias) -> string

   Return the network address
   
