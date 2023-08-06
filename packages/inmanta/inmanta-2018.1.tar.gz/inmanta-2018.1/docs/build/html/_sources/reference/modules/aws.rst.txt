Module aws
==========

 * License: Apache 2.0
 * Version: 2.1.0
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.2 or higher
 * Upstream project: https://github.com/inmanta/aws.git

Typedefs
--------

.. inmanta:typedef:: aws::direction

   * Base type ``string``
   * Type constraint ``((self == 'ingress') or (self == 'egress'))``

.. inmanta:typedef:: aws::instance_tenancy

   * Base type ``string``
   * Type constraint ``(self regex re.compile('^(default|dedicated|host)$'))``


Entities
--------

.. inmanta:entity:: aws::AWSResource

   Parents: :inmanta:entity:`std::PurgeableResource`, :inmanta:entity:`std::ManagedResource`

   .. inmanta:relation:: aws::Provider aws::AWSResource.provider [1]


.. inmanta:entity:: aws::ELB

   Parents: :inmanta:entity:`aws::AWSResource`

   An ELB load balancer
   
   

   .. inmanta:attribute:: number aws::ELB.listen_port=80


   .. inmanta:attribute:: string aws::ELB.protocol='http'


   .. inmanta:attribute:: number aws::ELB.dest_port=80


   .. inmanta:attribute:: string aws::ELB.security_group='default'


   .. inmanta:attribute:: string aws::ELB.name


   .. inmanta:relation:: aws::VirtualMachine aws::ELB.instances [0:\*]

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::GroupRule

   Parents: :inmanta:entity:`aws::SecurityRule`

   .. inmanta:relation:: aws::SecurityGroup aws::GroupRule.remote_group [1]

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::Host

   Parents: :inmanta:entity:`aws::VMAttributes`, :inmanta:entity:`ip::Host`

   A subclass of ip::Host that creates a virtual machine on AWS.
   

   .. inmanta:relation:: aws::VirtualMachine aws::Host.vm [1]

   .. inmanta:relation:: ip::IP aws::Host.public_ip [0:1]

   .. inmanta:relation:: aws::Provider aws::Host.provider [1]

   .. inmanta:relation:: aws::Subnet aws::Host.subnet [0:1]

   .. inmanta:relation:: aws::SecurityGroup aws::Host.security_groups [0:\*]

   .. inmanta:relation:: ip::IP aws::Host.private_ip [1]

   .. inmanta:relation:: ssh::Key aws::Host.public_key [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`aws::awsHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::hostDefaults`, :inmanta:implementation:`aws::awsHost`


.. inmanta:entity:: aws::IPrule

   Parents: :inmanta:entity:`aws::SecurityRule`

   .. inmanta:attribute:: ip::cidr aws::IPrule.remote_prefix


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::InternetGateway

   Parents: :inmanta:entity:`aws::AWSResource`

   An Internet gateway for use with a VPC.
   
   

   .. inmanta:attribute:: string aws::InternetGateway.name


   .. inmanta:relation:: aws::VPC aws::InternetGateway.vpc [0:1]

      other end: :inmanta:relation:`aws::VPC.internet_gateway [0:1]<aws::VPC.internet_gateway>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::Provider

   Parents: :inmanta:entity:`std::Entity`

   The configuration to access Amazon Web Services
   

   .. inmanta:attribute:: bool aws::Provider.auto_agent=True


   .. inmanta:attribute:: string aws::Provider.availability_zone


   .. inmanta:attribute:: string aws::Provider.name


   .. inmanta:attribute:: string aws::Provider.region


   .. inmanta:attribute:: string aws::Provider.access_key


   .. inmanta:attribute:: string aws::Provider.secret_key


   The following implementations are defined for this entity:

      * :inmanta:implementation:`aws::agentConfig`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`
      * :inmanta:implementation:`aws::agentConfig`
        constraint ``auto_agent``


.. inmanta:entity:: aws::SecurityGroup

   Parents: :inmanta:entity:`aws::AWSResource`

   

   .. inmanta:attribute:: string aws::SecurityGroup.description=''


   .. inmanta:attribute:: number aws::SecurityGroup.retries=10

      A security group can only be deleted when it is no longer in use. The API confirms the delete of a virtual machine for example, but it might still be in progress. This results in a failure to delete the security group. To speed up deployments, the handler can retry this number of times before skipping the resource.

   .. inmanta:attribute:: bool aws::SecurityGroup.manage_all=True


   .. inmanta:attribute:: number aws::SecurityGroup.wait=5

      The number of seconds to wait between retries.

   .. inmanta:attribute:: string aws::SecurityGroup.name


   .. inmanta:relation:: aws::VPC aws::SecurityGroup.vpc [1]

   .. inmanta:relation:: aws::SecurityRule aws::SecurityGroup.rules [0:\*]

      other end: :inmanta:relation:`aws::SecurityRule.group [1]<aws::SecurityRule.group>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::SecurityRule

   Parents: :inmanta:entity:`std::Entity`

   A filter rule in the a security group
   
   

   .. inmanta:attribute:: ip::port aws::SecurityRule.port=0


   .. inmanta:attribute:: ip::protocol aws::SecurityRule.ip_protocol

      The type of ip protocol to allow. Currently this support tcp/udp/icmp/sctp or all

   .. inmanta:attribute:: ip::port aws::SecurityRule.port_max=0


   .. inmanta:attribute:: aws::direction aws::SecurityRule.direction


   .. inmanta:attribute:: ip::port aws::SecurityRule.port_min=0


   .. inmanta:relation:: aws::SecurityGroup aws::SecurityRule.group [1]

      other end: :inmanta:relation:`aws::SecurityGroup.rules [0:\*]<aws::SecurityGroup.rules>`


.. inmanta:entity:: aws::Subnet

   Parents: :inmanta:entity:`aws::AWSResource`

   A subnet in a vpc
   
   

   .. inmanta:attribute:: ip::cidr aws::Subnet.cidr_block

      The IPv4 network range for the VPC, in CIDR notation. For example, 10.0.0.0/24.

   .. inmanta:attribute:: string aws::Subnet.availability_zone=<inmanta.execute.util.NoneValue object at 0x7fa196106630>

      The Availability Zone for the subnet.

   .. inmanta:attribute:: bool aws::Subnet.map_public_ip_on_launch=False

      Specify true to indicate that network interfaces created in the specified subnet should be assigned a public IPv4 address. This includes a network interface that's created when launching an instance into the subnet (the instance therefore receives a public IPv4 address).

   .. inmanta:attribute:: string aws::Subnet.name

      The name of the subnet. Inmanta uses this name to idenfiy the subnet. It is set as the name tag on the subnet resource.

   .. inmanta:relation:: aws::VPC aws::Subnet.vpc [1]

      The VPC the subnet is created in.
      

      other end: :inmanta:relation:`aws::VPC.subnets [0:\*]<aws::VPC.subnets>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::VMAttributes

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string aws::VMAttributes.flavor


   .. inmanta:attribute:: bool aws::VMAttributes.source_dest_check=True


   .. inmanta:attribute:: string aws::VMAttributes.image


   .. inmanta:attribute:: string aws::VMAttributes.subnet_id=<inmanta.execute.util.NoneValue object at 0x7fa1961627b8>


   .. inmanta:attribute:: string aws::VMAttributes.user_data



.. inmanta:entity:: aws::VPC

   Parents: :inmanta:entity:`aws::AWSResource`

   A VPC on Amazon
   
   

   .. inmanta:attribute:: bool aws::VPC.enableDnsHostnames=False


   .. inmanta:attribute:: bool aws::VPC.enableDnsSupport=False


   .. inmanta:attribute:: ip::cidr aws::VPC.cidr_block

      The IPv4 network range for the VPC, in CIDR notation. For example, 10.0.0.0/16.

   .. inmanta:attribute:: aws::instance_tenancy aws::VPC.instance_tenancy='default'

      The tenancy options for instances launched into the VPC. For default , instances are launched with shared tenancy by default. You can launch instances with any tenancy into a shared tenancy VPC. For dedicated , instances are launched as dedicated tenancy instances by default. You can only launch instances with a tenancy of dedicated or host into a dedicated tenancy VPC.

   .. inmanta:attribute:: string aws::VPC.name

      The name of the VPC. Inmanta uses this name to idenfiy the vpc. It is set as the name tag on the vpc resource.

   .. inmanta:relation:: aws::Subnet aws::VPC.subnets [0:\*]

      The VPC the subnet is created in.
      

      other end: :inmanta:relation:`aws::Subnet.vpc [1]<aws::Subnet.vpc>`

   .. inmanta:relation:: aws::InternetGateway aws::VPC.internet_gateway [0:1]

      other end: :inmanta:relation:`aws::InternetGateway.vpc [0:1]<aws::InternetGateway.vpc>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: aws::VirtualMachine

   Parents: :inmanta:entity:`aws::VMAttributes`, :inmanta:entity:`aws::AWSResource`

   This entity represents a virtual machine that is hosted on an IaaS
   
   

   .. inmanta:attribute:: dict aws::VirtualMachine.tags=Dict()


   .. inmanta:attribute:: string aws::VirtualMachine.name


   .. inmanta:relation:: aws::Subnet aws::VirtualMachine.subnet [0:1]

      Boot the vm in this subnet. Either use this relation or provide a subnet id directly.
      

   .. inmanta:relation:: aws::SecurityGroup aws::VirtualMachine.security_groups [0:\*]

      The security groups that apply to this vm. If no group is supplied the default security group will 
      be applied by EC2
      

   .. inmanta:relation:: ssh::Key aws::VirtualMachine.public_key [1]

   .. inmanta:relation:: aws::Volume aws::VirtualMachine.volumes [0:\*]

      other end: :inmanta:relation:`aws::Volume.vm [0:1]<aws::Volume.vm>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`aws::req`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`aws::req`


.. inmanta:entity:: aws::Volume

   Parents: :inmanta:entity:`aws::AWSResource`

   .. inmanta:attribute:: bool aws::Volume.encrypted=False


   .. inmanta:attribute:: string aws::Volume.volume_type='gp2'


   .. inmanta:attribute:: string aws::Volume.availability_zone


   .. inmanta:attribute:: dict aws::Volume.tags=Dict()


   .. inmanta:attribute:: string aws::Volume.attachmentpoint='/dev/sdb'


   .. inmanta:attribute:: number aws::Volume.size=10


   .. inmanta:attribute:: string aws::Volume.name


   .. inmanta:relation:: aws::VirtualMachine aws::Volume.vm [0:1]

      other end: :inmanta:relation:`aws::VirtualMachine.volumes [0:\*]<aws::VirtualMachine.volumes>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


Implementations
---------------

.. inmanta:implementation:: aws::agentConfig

.. inmanta:implementation:: aws::awsHost

.. inmanta:implementation:: aws::req

Plugins
-------

.. py:function:: aws.decrypt(key_data: string, cipher_text: string) -> string

.. py:function:: aws.elbid(name: string) -> string

.. py:function:: aws.get_api_id(provider: aws::Provider, api_name: string) -> string

Resources
---------

.. py:class:: aws.ELB

   Amazon Elastic loadbalancer
   

 * Resource for entity :inmanta:Entity:`aws::ELB`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.ELBHandler`

.. py:class:: aws.InternetGateway

 * Resource for entity :inmanta:Entity:`aws::InternetGateway`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.InternetGatewayHandler`

.. py:class:: aws.SecurityGroup

   A security group in an OpenStack tenant
   

 * Resource for entity :inmanta:Entity:`aws::SecurityGroup`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.SecurityGroupHandler`

.. py:class:: aws.Subnet

 * Resource for entity :inmanta:Entity:`aws::Subnet`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.SubnetHandler`

.. py:class:: aws.VPC

 * Resource for entity :inmanta:Entity:`aws::VPC`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.VPCHandler`

.. py:class:: aws.VirtualMachine

 * Resource for entity :inmanta:Entity:`aws::VirtualMachine`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.VirtualMachineHandler`

.. py:class:: aws.Volume

 * Resource for entity :inmanta:Entity:`aws::Volume`
 * Id attribute ``name``
 * Agent name ``provider.name``
 * Handlers :py:class:`aws.VolumeHandler`

Handlers
--------

.. py:class:: aws.SubnetHandler

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::Subnet`

.. py:class:: aws.InternetGatewayHandler

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::InternetGateway`

.. py:class:: aws.VirtualMachineHandler

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::VirtualMachine`

.. py:class:: aws.VolumeHandler

 * Handler name ``volume``
 * Handler for entity :inmanta:Entity:`aws::Volume`

.. py:class:: aws.SecurityGroupHandler

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::SecurityGroup`

.. py:class:: aws.VPCHandler

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::VPC`

.. py:class:: aws.ELBHandler

   This class manages ELB instances on amazon ec2
   

 * Handler name ``ec2``
 * Handler for entity :inmanta:Entity:`aws::ELB`
