Module openstack
================

 * License: Apache 2.0
 * Version: 2.9.0
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.1 or higher
 * Upstream project: https://github.com/inmanta/openstack.git

Typedefs
--------

.. inmanta:typedef:: openstack::admin_state

   * Base type ``string``
   * Type constraint ``((self == 'up') or (self == 'down'))``

.. inmanta:typedef:: openstack::direction

   * Base type ``string``
   * Type constraint ``((self == 'ingress') or (self == 'egress'))``


Entities
--------

.. inmanta:entity:: openstack::EndPoint

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   .. inmanta:attribute:: string openstack::EndPoint.admin_url


   .. inmanta:attribute:: string openstack::EndPoint.public_url


   .. inmanta:attribute:: string openstack::EndPoint.internal_url


   .. inmanta:attribute:: string openstack::EndPoint.service_id


   .. inmanta:attribute:: string openstack::EndPoint.region


   .. inmanta:relation:: openstack::Provider openstack::EndPoint.provider [1]

      other end: :inmanta:relation:`openstack::Provider.endpoints [0:\*]<openstack::Provider.endpoints>`

   .. inmanta:relation:: openstack::Service openstack::EndPoint.service [1]

      other end: :inmanta:relation:`openstack::Service.endpoint [0:1]<openstack::Service.endpoint>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openstack::endPoint`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openstack::endPoint`


.. inmanta:entity:: openstack::FloatingIP

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   .. inmanta:attribute:: string openstack::FloatingIP.name


   .. inmanta:relation:: openstack::HostPort openstack::FloatingIP.port [1]

      other end: :inmanta:relation:`openstack::HostPort.floating_ips [0:\*]<openstack::HostPort.floating_ips>`

   .. inmanta:relation:: openstack::Network openstack::FloatingIP.external_network [1]

      other end: :inmanta:relation:`openstack::Network.floating_ips [0:\*]<openstack::Network.floating_ips>`

   .. inmanta:relation:: openstack::Project openstack::FloatingIP.project [1]

      other end: :inmanta:relation:`openstack::Project.floating_ips [0:\*]<openstack::Project.floating_ips>`

   .. inmanta:relation:: openstack::Provider openstack::FloatingIP.provider [1]

      other end: :inmanta:relation:`openstack::Provider.floating_ips [0:\*]<openstack::Provider.floating_ips>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openstack::fipName`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openstack::fipName`


.. inmanta:entity:: openstack::GroupRule

   Parents: :inmanta:entity:`openstack::SecurityRule`

   .. inmanta:relation:: openstack::SecurityGroup openstack::GroupRule.remote_group [1]

      other end: :inmanta:relation:`openstack::SecurityGroup.remote_group_rules [0:\*]<openstack::SecurityGroup.remote_group_rules>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::Host

   Parents: :inmanta:entity:`ip::Host`, :inmanta:entity:`openstack::VMAttributes`

   .. inmanta:attribute:: bool openstack::Host.purged=False


   .. inmanta:relation:: openstack::SecurityGroup openstack::Host.security_groups [0:\*]

   .. inmanta:relation:: ssh::Key openstack::Host.key_pair [1]

   .. inmanta:relation:: openstack::Subnet openstack::Host.subnet [0:1]

   .. inmanta:relation:: openstack::Provider openstack::Host.provider [1]

   .. inmanta:relation:: openstack::VirtualMachine openstack::Host.vm [1]

      other end: :inmanta:relation:`openstack::VirtualMachine.host [0:1]<openstack::VirtualMachine.host>`

   .. inmanta:relation:: openstack::Project openstack::Host.project [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openstack::eth0Port`
      * :inmanta:implementation:`openstack::openstackVM`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openstack::eth0Port`
        constraint ``subnet is defined is defined``
      * :inmanta:implementation:`std::hostDefaults`, :inmanta:implementation:`openstack::openstackVM`
      * :inmanta:implementation:`openstack::userData`
        constraint ``install_agent``


.. inmanta:entity:: openstack::HostPort

   Parents: :inmanta:entity:`openstack::Port`

   A port attached to a VM
   
   

   .. inmanta:attribute:: bool openstack::HostPort.dhcp=True

      Enable dhcp for this port or not for this port

   .. inmanta:attribute:: string openstack::HostPort.name

      The name of the host port.

   .. inmanta:attribute:: number openstack::HostPort.retries=20

      A hostport can only be attached to a VM when it is in an active state. The handler will skip this port when the VM is not ready. To speed up deployments, the handler can retry this number of times before skipping the resource.

   .. inmanta:attribute:: bool openstack::HostPort.portsecurity=True

      Enable or disable port security (security groups and spoofing filters)

   .. inmanta:attribute:: number openstack::HostPort.port_index=0

      The index of the port. This determines the order of the interfaces on the virtual machine. 0 means no specific order.

   .. inmanta:attribute:: number openstack::HostPort.wait=5

      The number of seconds to wait between retries.

   .. inmanta:relation:: openstack::VirtualMachine openstack::HostPort.vm [1]

      other end: :inmanta:relation:`openstack::VirtualMachine.ports [0:\*]<openstack::VirtualMachine.ports>`

   .. inmanta:relation:: openstack::FloatingIP openstack::HostPort.floating_ips [0:\*]

      other end: :inmanta:relation:`openstack::FloatingIP.port [1]<openstack::FloatingIP.port>`

   .. inmanta:relation:: openstack::Subnet openstack::HostPort.subnet [1]

      other end: :inmanta:relation:`openstack::Subnet.host_ports [0:\*]<openstack::Subnet.host_ports>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::IPrule

   Parents: :inmanta:entity:`openstack::SecurityRule`

   .. inmanta:attribute:: ip::cidr openstack::IPrule.remote_prefix


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::Network

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A neutron network owned by a project
   

   .. inmanta:attribute:: bool openstack::Network.external=False


   .. inmanta:attribute:: string openstack::Network.network_type=''


   .. inmanta:attribute:: string openstack::Network.physical_network=''


   .. inmanta:attribute:: number openstack::Network.segmentation_id=0


   .. inmanta:attribute:: string openstack::Network.name


   .. inmanta:relation:: openstack::Router openstack::Network.routers [0:\*]

      other end: :inmanta:relation:`openstack::Router.ext_gateway [0:1]<openstack::Router.ext_gateway>`

   .. inmanta:relation:: openstack::Subnet openstack::Network.subnets [0:\*]

      other end: :inmanta:relation:`openstack::Subnet.network [1]<openstack::Subnet.network>`

   .. inmanta:relation:: openstack::Provider openstack::Network.provider [1]

      other end: :inmanta:relation:`openstack::Provider.networks [0:\*]<openstack::Provider.networks>`

   .. inmanta:relation:: openstack::FloatingIP openstack::Network.floating_ips [0:\*]

      other end: :inmanta:relation:`openstack::FloatingIP.external_network [1]<openstack::FloatingIP.external_network>`

   .. inmanta:relation:: openstack::Project openstack::Network.project [1]

      other end: :inmanta:relation:`openstack::Project.networks [0:\*]<openstack::Project.networks>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::OpenStackResource

   Parents: :inmanta:entity:`std::PurgeableResource`, :inmanta:entity:`std::ManagedResource`


.. inmanta:entity:: openstack::Port

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A port on a network
   

   .. inmanta:attribute:: ip::ip openstack::Port.address


   .. inmanta:relation:: openstack::Project openstack::Port.project [1]

      other end: :inmanta:relation:`openstack::Project.ports [0:\*]<openstack::Project.ports>`

   .. inmanta:relation:: openstack::Provider openstack::Port.provider [1]

      other end: :inmanta:relation:`openstack::Provider.ports [0:\*]<openstack::Provider.ports>`


.. inmanta:entity:: openstack::Project

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A project / tenant in openstack
   

   .. inmanta:attribute:: bool openstack::Project.enabled=True


   .. inmanta:attribute:: string openstack::Project.name


   .. inmanta:attribute:: string openstack::Project.description=''


   .. inmanta:relation:: openstack::Router openstack::Project.routers [0:\*]

      other end: :inmanta:relation:`openstack::Router.project [1]<openstack::Router.project>`

   .. inmanta:relation:: openstack::SecurityGroup openstack::Project.security_groups [0:\*]

      other end: :inmanta:relation:`openstack::SecurityGroup.project [1]<openstack::SecurityGroup.project>`

   .. inmanta:relation:: openstack::Role openstack::Project.roles [0:\*]

      Each user can have multiple roles
      

      other end: :inmanta:relation:`openstack::Role.project [1]<openstack::Role.project>`

   .. inmanta:relation:: openstack::Network openstack::Project.networks [0:\*]

      other end: :inmanta:relation:`openstack::Network.project [1]<openstack::Network.project>`

   .. inmanta:relation:: openstack::Provider openstack::Project.provider [1]

      other end: :inmanta:relation:`openstack::Provider.projects [0:\*]<openstack::Provider.projects>`

   .. inmanta:relation:: openstack::Port openstack::Project.ports [0:\*]

      other end: :inmanta:relation:`openstack::Port.project [1]<openstack::Port.project>`

   .. inmanta:relation:: openstack::FloatingIP openstack::Project.floating_ips [0:\*]

      other end: :inmanta:relation:`openstack::FloatingIP.project [1]<openstack::FloatingIP.project>`

   .. inmanta:relation:: openstack::Subnet openstack::Project.subnets [0:\*]

      other end: :inmanta:relation:`openstack::Subnet.project [1]<openstack::Subnet.project>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::Provider

   Parents: :inmanta:entity:`std::Entity`

   The configuration for accessing an Openstack based IaaS
   

   .. inmanta:attribute:: string openstack::Provider.password


   .. inmanta:attribute:: string openstack::Provider.admin_url=''


   .. inmanta:attribute:: bool openstack::Provider.auto_agent=True


   .. inmanta:attribute:: string openstack::Provider.name


   .. inmanta:attribute:: string openstack::Provider.token=''


   .. inmanta:attribute:: string openstack::Provider.tenant


   .. inmanta:attribute:: string openstack::Provider.username


   .. inmanta:attribute:: string openstack::Provider.connection_url


   .. inmanta:relation:: openstack::Router openstack::Provider.routers [0:\*]

      other end: :inmanta:relation:`openstack::Router.provider [1]<openstack::Router.provider>`

   .. inmanta:relation:: openstack::Subnet openstack::Provider.subnets [0:\*]

      other end: :inmanta:relation:`openstack::Subnet.provider [1]<openstack::Subnet.provider>`

   .. inmanta:relation:: openstack::Project openstack::Provider.projects [0:\*]

      other end: :inmanta:relation:`openstack::Project.provider [1]<openstack::Project.provider>`

   .. inmanta:relation:: openstack::FloatingIP openstack::Provider.floating_ips [0:\*]

      other end: :inmanta:relation:`openstack::FloatingIP.provider [1]<openstack::FloatingIP.provider>`

   .. inmanta:relation:: openstack::SecurityGroup openstack::Provider.security_groups [0:\*]

      other end: :inmanta:relation:`openstack::SecurityGroup.provider [1]<openstack::SecurityGroup.provider>`

   .. inmanta:relation:: openstack::EndPoint openstack::Provider.endpoints [0:\*]

      other end: :inmanta:relation:`openstack::EndPoint.provider [1]<openstack::EndPoint.provider>`

   .. inmanta:relation:: openstack::Network openstack::Provider.networks [0:\*]

      other end: :inmanta:relation:`openstack::Network.provider [1]<openstack::Network.provider>`

   .. inmanta:relation:: openstack::Service openstack::Provider.services [0:\*]

      other end: :inmanta:relation:`openstack::Service.provider [1]<openstack::Service.provider>`

   .. inmanta:relation:: openstack::Role openstack::Provider.roles [0:\*]

      other end: :inmanta:relation:`openstack::Role.provider [1]<openstack::Role.provider>`

   .. inmanta:relation:: openstack::VirtualMachine openstack::Provider.virtual_machines [0:\*]

      other end: :inmanta:relation:`openstack::VirtualMachine.provider [1]<openstack::VirtualMachine.provider>`

   .. inmanta:relation:: openstack::User openstack::Provider.users [0:\*]

      other end: :inmanta:relation:`openstack::User.provider [1]<openstack::User.provider>`

   .. inmanta:relation:: openstack::Port openstack::Provider.ports [0:\*]

      other end: :inmanta:relation:`openstack::Port.provider [1]<openstack::Port.provider>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openstack::agentConfig`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`
      * :inmanta:implementation:`openstack::agentConfig`
        constraint ``auto_agent``


.. inmanta:entity:: openstack::Role

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A role in openstack. A role defines membership of a user in a project.
   This entity is used to connect users to projects. With this, it
   implicitly defines the role.
   
   

   .. inmanta:attribute:: string openstack::Role.role_id


   .. inmanta:attribute:: string openstack::Role.role


   .. inmanta:relation:: openstack::User openstack::Role.user [1]

      other end: :inmanta:relation:`openstack::User.roles [0:\*]<openstack::User.roles>`

   .. inmanta:relation:: openstack::Project openstack::Role.project [1]

      Each user can have multiple roles
      

      other end: :inmanta:relation:`openstack::Project.roles [0:\*]<openstack::Project.roles>`

   .. inmanta:relation:: openstack::Provider openstack::Role.provider [1]

      other end: :inmanta:relation:`openstack::Provider.roles [0:\*]<openstack::Provider.roles>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`openstack::roleImpl`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`openstack::roleImpl`


.. inmanta:entity:: openstack::Route

   Parents: :inmanta:entity:`std::Entity`

   A routing rule to add
   

   .. inmanta:attribute:: ip::cidr openstack::Route.destination


   .. inmanta:attribute:: ip::ip openstack::Route.nexthop


   .. inmanta:relation:: openstack::Router openstack::Route.router [0:1]

      other end: :inmanta:relation:`openstack::Router.routes [0:\*]<openstack::Router.routes>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::Router

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A router
   

   .. inmanta:attribute:: openstack::admin_state openstack::Router.admin_state='up'


   .. inmanta:attribute:: bool openstack::Router.ha=False


   .. inmanta:attribute:: bool openstack::Router.distributed=False


   .. inmanta:attribute:: string openstack::Router.name


   .. inmanta:relation:: openstack::Route openstack::Router.routes [0:\*]

      other end: :inmanta:relation:`openstack::Route.router [0:1]<openstack::Route.router>`

   .. inmanta:relation:: openstack::Subnet openstack::Router.subnets [0:\*]

      other end: :inmanta:relation:`openstack::Subnet.router [0:1]<openstack::Subnet.router>`

   .. inmanta:relation:: openstack::Provider openstack::Router.provider [1]

      other end: :inmanta:relation:`openstack::Provider.routers [0:\*]<openstack::Provider.routers>`

   .. inmanta:relation:: openstack::Network openstack::Router.ext_gateway [0:1]

      other end: :inmanta:relation:`openstack::Network.routers [0:\*]<openstack::Network.routers>`

   .. inmanta:relation:: openstack::RouterPort openstack::Router.ports [0:\*]

      other end: :inmanta:relation:`openstack::RouterPort.router [0:1]<openstack::RouterPort.router>`

   .. inmanta:relation:: openstack::Project openstack::Router.project [1]

      other end: :inmanta:relation:`openstack::Project.routers [0:\*]<openstack::Project.routers>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::RouterPort

   Parents: :inmanta:entity:`openstack::Port`

   A port attached to a router
   

   .. inmanta:attribute:: string openstack::RouterPort.name


   .. inmanta:relation:: openstack::Router openstack::RouterPort.router [0:1]

      other end: :inmanta:relation:`openstack::Router.ports [0:\*]<openstack::Router.ports>`

   .. inmanta:relation:: openstack::Subnet openstack::RouterPort.subnet [0:1]

      other end: :inmanta:relation:`openstack::Subnet.routers [0:\*]<openstack::Subnet.routers>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::SecurityGroup

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   

   .. inmanta:attribute:: bool openstack::SecurityGroup.manage_all=True


   .. inmanta:attribute:: string openstack::SecurityGroup.name


   .. inmanta:attribute:: number openstack::SecurityGroup.retries=10

      A security group can only be deleted when it is no longer in use. The API confirms the delete of a virtual machine for example, but it might still be in progress. This results in a failure to delete the security group. To speed up deployments, the handler can retry this number of times before skipping the resource.

   .. inmanta:attribute:: number openstack::SecurityGroup.wait=5

      The number of seconds to wait between retries.

   .. inmanta:attribute:: string openstack::SecurityGroup.description=''


   .. inmanta:relation:: openstack::GroupRule openstack::SecurityGroup.remote_group_rules [0:\*]

      other end: :inmanta:relation:`openstack::GroupRule.remote_group [1]<openstack::GroupRule.remote_group>`

   .. inmanta:relation:: openstack::Project openstack::SecurityGroup.project [1]

      other end: :inmanta:relation:`openstack::Project.security_groups [0:\*]<openstack::Project.security_groups>`

   .. inmanta:relation:: openstack::Provider openstack::SecurityGroup.provider [1]

      other end: :inmanta:relation:`openstack::Provider.security_groups [0:\*]<openstack::Provider.security_groups>`

   .. inmanta:relation:: openstack::SecurityRule openstack::SecurityGroup.rules [0:\*]

      other end: :inmanta:relation:`openstack::SecurityRule.group [1]<openstack::SecurityRule.group>`

   .. inmanta:relation:: openstack::VirtualMachine openstack::SecurityGroup.virtual_machines [0:\*]

      other end: :inmanta:relation:`openstack::VirtualMachine.security_groups [0:\*]<openstack::VirtualMachine.security_groups>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::SecurityRule

   Parents: :inmanta:entity:`std::Entity`

   A filter rule in the a security group
   
   

   .. inmanta:attribute:: ip::port openstack::SecurityRule.port_max=0


   .. inmanta:attribute:: ip::port openstack::SecurityRule.port_min=0


   .. inmanta:attribute:: openstack::direction openstack::SecurityRule.direction


   .. inmanta:attribute:: ip::protocol openstack::SecurityRule.ip_protocol

      The type of ip protocol to allow. Currently this support tcp/udp/icmp/sctp or all

   .. inmanta:attribute:: ip::port openstack::SecurityRule.port=0


   .. inmanta:relation:: openstack::SecurityGroup openstack::SecurityRule.group [1]

      other end: :inmanta:relation:`openstack::SecurityGroup.rules [0:\*]<openstack::SecurityGroup.rules>`


.. inmanta:entity:: openstack::Service

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   .. inmanta:attribute:: string openstack::Service.type


   .. inmanta:attribute:: string openstack::Service.name


   .. inmanta:attribute:: string openstack::Service.description


   .. inmanta:relation:: openstack::EndPoint openstack::Service.endpoint [0:1]

      other end: :inmanta:relation:`openstack::EndPoint.service [1]<openstack::EndPoint.service>`

   .. inmanta:relation:: openstack::Provider openstack::Service.provider [1]

      other end: :inmanta:relation:`openstack::Provider.services [0:\*]<openstack::Provider.services>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::Subnet

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A neutron network subnet
   

   .. inmanta:attribute:: ip::cidr openstack::Subnet.network_address


   .. inmanta:attribute:: string openstack::Subnet.allocation_end=''


   .. inmanta:attribute:: bool openstack::Subnet.dhcp


   .. inmanta:attribute:: string openstack::Subnet.allocation_start=''


   .. inmanta:attribute:: ip::ip openstack::Subnet.dns_servers=List()


   .. inmanta:attribute:: string openstack::Subnet.name


   .. inmanta:relation:: openstack::Router openstack::Subnet.router [0:1]

      other end: :inmanta:relation:`openstack::Router.subnets [0:\*]<openstack::Router.subnets>`

   .. inmanta:relation:: openstack::RouterPort openstack::Subnet.routers [0:\*]

      other end: :inmanta:relation:`openstack::RouterPort.subnet [0:1]<openstack::RouterPort.subnet>`

   .. inmanta:relation:: openstack::Provider openstack::Subnet.provider [1]

      other end: :inmanta:relation:`openstack::Provider.subnets [0:\*]<openstack::Provider.subnets>`

   .. inmanta:relation:: openstack::HostPort openstack::Subnet.host_ports [0:\*]

      other end: :inmanta:relation:`openstack::HostPort.subnet [1]<openstack::HostPort.subnet>`

   .. inmanta:relation:: openstack::Project openstack::Subnet.project [1]

      other end: :inmanta:relation:`openstack::Project.subnets [0:\*]<openstack::Project.subnets>`

   .. inmanta:relation:: openstack::Network openstack::Subnet.network [1]

      other end: :inmanta:relation:`openstack::Network.subnets [0:\*]<openstack::Network.subnets>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::User

   Parents: :inmanta:entity:`openstack::OpenStackResource`

   A user in openstack. A handler for this entity type is loaded by agents.
   
   

   .. inmanta:attribute:: string openstack::User.password=''

      The password for this user. The handler will always reset back to this password. The handler will ignore this attribute when an empty string is set.

   .. inmanta:attribute:: bool openstack::User.enabled=True

      Enable or disable this user

   .. inmanta:attribute:: string openstack::User.name

      The name of the user. The name of the user has to be unique on a specific IaaS. The handler will use this name to query for the exact user and its ID.

   .. inmanta:attribute:: string openstack::User.email

      The email address of the user to use.

   .. inmanta:relation:: openstack::Role openstack::User.roles [0:\*]

      other end: :inmanta:relation:`openstack::Role.user [1]<openstack::Role.user>`

   .. inmanta:relation:: openstack::Provider openstack::User.provider [1]

      other end: :inmanta:relation:`openstack::Provider.users [0:\*]<openstack::Provider.users>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: openstack::VMAttributes

   Parents: :inmanta:entity:`platform::UserdataVM`

   .. inmanta:attribute:: string openstack::VMAttributes.flavor


   .. inmanta:attribute:: string openstack::VMAttributes.user_data


   .. inmanta:attribute:: bool openstack::VMAttributes.install_agent=False


   .. inmanta:attribute:: bool openstack::VMAttributes.config_drive=False


   .. inmanta:attribute:: string openstack::VMAttributes.image



.. inmanta:entity:: openstack::VirtualMachine

   Parents: :inmanta:entity:`openstack::OpenStackResource`, :inmanta:entity:`openstack::VMAttributes`

   .. inmanta:attribute:: string openstack::VirtualMachine.name


   .. inmanta:relation:: openstack::SecurityGroup openstack::VirtualMachine.security_groups [0:\*]

      other end: :inmanta:relation:`openstack::SecurityGroup.virtual_machines [0:\*]<openstack::SecurityGroup.virtual_machines>`

   .. inmanta:relation:: openstack::HostPort openstack::VirtualMachine.eth0_port [1]

   .. inmanta:relation:: openstack::Provider openstack::VirtualMachine.provider [1]

      other end: :inmanta:relation:`openstack::Provider.virtual_machines [0:\*]<openstack::Provider.virtual_machines>`

   .. inmanta:relation:: openstack::Host openstack::VirtualMachine.host [0:1]

      other end: :inmanta:relation:`openstack::Host.vm [1]<openstack::Host.vm>`

   .. inmanta:relation:: openstack::HostPort openstack::VirtualMachine.ports [0:\*]

      other end: :inmanta:relation:`openstack::HostPort.vm [1]<openstack::HostPort.vm>`

   .. inmanta:relation:: ssh::Key openstack::VirtualMachine.key_pair [1]

   .. inmanta:relation:: openstack::Project openstack::VirtualMachine.project [1]

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`
      * :inmanta:implementation:`openstack::userData`
        constraint ``install_agent``


Implementations
---------------

.. inmanta:implementation:: openstack::agentConfig

.. inmanta:implementation:: openstack::endPoint

.. inmanta:implementation:: openstack::eth0Port

.. inmanta:implementation:: openstack::fipName

.. inmanta:implementation:: openstack::openstackVM

.. inmanta:implementation:: openstack::roleImpl

.. inmanta:implementation:: openstack::userData

Plugins
-------

.. py:function:: openstack.find_flavor(provider: openstack::Provider, vcpus: number, ram: number, pinned: bool=False) -> string

   Find the flavor that matches the closest to the resources requested.
   
   :param vcpus: The number of virtual cpus in the flavor
   :param ram: The amount of ram in megabyte
   :param pinned: Wether the CPUs need to be pinned (#vcpu == #pcpu)
   

.. py:function:: openstack.find_image(provider: openstack::Provider, os: std::OS, name: string=None) -> string

   Search for an image that matches the given operating system. This plugin uses
   the os_distro and os_version tags of an image and the name and version attributes of
   the OS parameter.
   
   If multiple images match, the most recent image is returned.
   
   :param provider: The provider to query for an image
   :param os: The operating system and version (using os_distro and os_version metadata)
   :param name: An optional string that the image name should contain
   

Resources
---------

.. py:class:: openstack.EndPoint

   An endpoint for a service
   

 * Resource for entity :inmanta:Entity:`openstack::EndPoint`
 * Id attribute ``service_id``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.EndpointHandler`

.. py:class:: openstack.FloatingIP

   A floating ip
   

 * Resource for entity :inmanta:Entity:`openstack::FloatingIP`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.FloatingIPHandler`

.. py:class:: openstack.HostPort

   A port in a router
   

 * Resource for entity :inmanta:Entity:`openstack::HostPort`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.HostPortHandler`

.. py:class:: openstack.Network

   This class represents a network in neutron
   

 * Resource for entity :inmanta:Entity:`openstack::Network`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.NetworkHandler`

.. py:class:: openstack.Project

   This class represents a project in keystone
   

 * Resource for entity :inmanta:Entity:`openstack::Project`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.ProjectHandler`

.. py:class:: openstack.Role

   A role that adds a user to a project
   

 * Resource for entity :inmanta:Entity:`openstack::Role`
 * Id attribute ``role_id``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.RoleHandler`

.. py:class:: openstack.Router

   This class represent a router in neutron
   

 * Resource for entity :inmanta:Entity:`openstack::Router`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.RouterHandler`

.. py:class:: openstack.RouterPort

   A port in a router
   

 * Resource for entity :inmanta:Entity:`openstack::RouterPort`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.RouterPortHandler`

.. py:class:: openstack.SecurityGroup

   A security group in an OpenStack tenant
   

 * Resource for entity :inmanta:Entity:`openstack::SecurityGroup`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.SecurityGroupHandler`

.. py:class:: openstack.Service

   A service for which endpoints can be registered
   

 * Resource for entity :inmanta:Entity:`openstack::Service`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.ServiceHandler`

.. py:class:: openstack.Subnet

   This class represent a subnet in neutron
   

 * Resource for entity :inmanta:Entity:`openstack::Subnet`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.SubnetHandler`

.. py:class:: openstack.User

   A user in keystone
   

 * Resource for entity :inmanta:Entity:`openstack::User`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.UserHandler`

.. py:class:: openstack.VirtualMachine

   A virtual machine managed by a hypervisor or IaaS
   

 * Resource for entity :inmanta:Entity:`openstack::VirtualMachine`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`openstack.VirtualMachineHandler`

Handlers
--------

.. py:class:: openstack.RouterPortHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::RouterPort`

.. py:class:: openstack.HostPortHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::HostPort`

.. py:class:: openstack.FloatingIPHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::FloatingIP`

.. py:class:: openstack.EndpointHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::EndPoint`

.. py:class:: openstack.RoleHandler

   creates roles and user, project, role assocations
   

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Role`

.. py:class:: openstack.SubnetHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Subnet`

.. py:class:: openstack.ProjectHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Project`

.. py:class:: openstack.VirtualMachineHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::VirtualMachine`

.. py:class:: openstack.ServiceHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Service`

.. py:class:: openstack.SecurityGroupHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::SecurityGroup`

.. py:class:: openstack.RouterHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Router`

.. py:class:: openstack.NetworkHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::Network`

.. py:class:: openstack.UserHandler

 * Handler name ``openstack``
 * Handler for entity :inmanta:Entity:`openstack::User`
