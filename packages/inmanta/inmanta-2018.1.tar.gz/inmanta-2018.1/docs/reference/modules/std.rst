Module std
==========

 * License: Apache 2.0
 * Version: 0.17.0
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.3 or higher
 * Upstream project: https://github.com/inmanta/std.git

Typedefs
--------

.. inmanta:typedef:: std::hoststring

   * Base type ``string``
   * Type constraint ``(self regex re.compile('^[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*$'))``

.. inmanta:typedef:: std::package_state

   * Base type ``string``
   * Type constraint ``(((self == 'installed') or (self == 'removed')) or (self == 'latest'))``

.. inmanta:typedef:: std::service_state

   * Base type ``string``
   * Type constraint ``((self == 'running') or (self == 'stopped'))``

.. inmanta:typedef:: std::uuid

   * Base type ``string``
   * Type constraint ``(self regex re.compile('[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'))``


Entities
--------

.. inmanta:entity:: std::AgentConfig

   Parents: :inmanta:entity:`std::PurgeableResource`

   Control agent settings. Currently these settings are only applied to autostarted agents
   
   

   .. inmanta:attribute:: string std::AgentConfig.agentname

      The name of the agent to which this config applies.

   .. inmanta:attribute:: bool std::AgentConfig.autostart

      When this flag is set to true, the resource will be exported and set the agent map on the orchestrator. When false (or not set), this instance is ignore but can be used to generate agent configuration files.

   .. inmanta:attribute:: string std::AgentConfig.agent='internal'

      If a resource is exported, agent manages the resource.

   .. inmanta:attribute:: string std::AgentConfig.uri='local:'

      The uri that indicates how the agent should execute. Currently the following uri are supported: * "" An empty string. This is the same as running it locally * local: Manage resource locally * ssh://[user@]hostname[:port] Login using ssh. When user is left out, root is assumed. For port, the system default is used. * host The actual hostname or ip to use. Altough this is not a valid host in uri form it is supported.

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: std::ConfigFile

   Parents: :inmanta:entity:`std::File`

   A file with often used defaults for configuration files.
   

   .. inmanta:attribute:: string std::ConfigFile.owner='root'


   .. inmanta:attribute:: string std::ConfigFile.group='root'


   .. inmanta:attribute:: number std::ConfigFile.mode=644


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::fileHost`


.. inmanta:entity:: std::DefaultDirectory

   Parents: :inmanta:entity:`std::Directory`

   A directory that is world readable. It is also writable for its owner root.
   

   .. inmanta:attribute:: string std::DefaultDirectory.owner='root'


   .. inmanta:attribute:: string std::DefaultDirectory.group='root'


   .. inmanta:attribute:: number std::DefaultDirectory.mode=755


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::dirHost`


.. inmanta:entity:: std::Directory

   Parents: :inmanta:entity:`std::Reload`, :inmanta:entity:`std::PurgeableResource`

   A directory on the filesystem
   

   .. inmanta:attribute:: string std::Directory.path


   .. inmanta:attribute:: string std::Directory.owner


   .. inmanta:attribute:: number std::Directory.mode


   .. inmanta:attribute:: string std::Directory.group


   .. inmanta:attribute:: bool std::Directory.purge_on_delete=False


   .. inmanta:relation:: std::Host std::Directory.host [1]

      other end: :inmanta:relation:`std::Host.directories [0:\*]<std::Host.directories>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::dirHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::dirHost`


.. inmanta:entity:: std::Entity


   The entity all other entities inherit from.
   

   .. inmanta:relation:: std::Entity std::Entity.provides [0:\*]

      other end: :inmanta:relation:`std::Entity.requires [0:\*]<std::Entity.requires>`

   .. inmanta:relation:: std::Entity std::Entity.requires [0:\*]

      other end: :inmanta:relation:`std::Entity.provides [0:\*]<std::Entity.provides>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: std::File

   Parents: :inmanta:entity:`std::Reload`, :inmanta:entity:`std::PurgeableResource`

   This represents a file on the filesystem
   
   

   .. inmanta:attribute:: string std::File.path

      The path of the file

   .. inmanta:attribute:: string std::File.owner

      The owner of the file

   .. inmanta:attribute:: bool std::File.send_event


   .. inmanta:attribute:: string std::File.content

      The file contents

   .. inmanta:attribute:: bool std::File.purge_on_delete=False


   .. inmanta:attribute:: string std::File.group

      The group of the file

   .. inmanta:attribute:: number std::File.mode

      The permissions of the file

   .. inmanta:relation:: std::Host std::File.host [1]

      other end: :inmanta:relation:`std::Host.files [0:\*]<std::Host.files>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::fileHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::fileHost`


.. inmanta:entity:: std::Host

   Parents: :inmanta:entity:`std::ManagedDevice`

   A host models a server of computer in the managed infrastructure
   

   .. inmanta:relation:: std::Symlink std::Host.symlinks [0:\*]

      other end: :inmanta:relation:`std::Symlink.host [1]<std::Symlink.host>`

   .. inmanta:relation:: apt::Repository std::Host.repository [0:\*]

      other end: :inmanta:relation:`apt::Repository.host [1]<apt::Repository.host>`

   .. inmanta:relation:: std::Package std::Host.packages [0:\*]

      other end: :inmanta:relation:`std::Package.host [1]<std::Package.host>`

   .. inmanta:relation:: net::Interface std::Host.ifaces [0:\*]

      other end: :inmanta:relation:`net::Interface.host [1]<net::Interface.host>`

   .. inmanta:relation:: std::File std::Host.files [0:\*]

      other end: :inmanta:relation:`std::File.host [1]<std::File.host>`

   .. inmanta:relation:: std::HostConfig std::Host.host_config [1]

      other end: :inmanta:relation:`std::HostConfig.host [1]<std::HostConfig.host>`

   .. inmanta:relation:: std::Directory std::Host.directories [0:\*]

      other end: :inmanta:relation:`std::Directory.host [1]<std::Directory.host>`

   .. inmanta:relation:: std::Service std::Host.services [0:\*]

      other end: :inmanta:relation:`std::Service.host [1]<std::Service.host>`

   .. inmanta:relation:: std::OS std::Host.os [1]

      Each host has an OS defined. This values is mostly used to select implementation in the
      where clause of an `implement` statement. The :py:func:`familyof` plugin can be used
      for this.
      

   .. inmanta:relation:: std::HostGroup std::Host.host_groups [0:\*]

      other end: :inmanta:relation:`std::HostGroup.hosts [0:\*]<std::HostGroup.hosts>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::hostDefaults`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::hostDefaults`


.. inmanta:entity:: std::HostConfig

   Parents: :inmanta:entity:`std::Entity`

   This represents generic configuration for a host. This entity is used
   by other modules to include their host specific configuration. This
   should be instantiated in the implementation of std::Host or subclasses.
   This host specific configuration cannot be included by just implementing
   std::Host because possibly subclasses of std::Host are instantiated and
   implementations are not inherited.
   

   .. inmanta:relation:: std::Host std::HostConfig.host [1]

      other end: :inmanta:relation:`std::Host.host_config [1]<std::Host.host_config>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`redhat::scl::epel7`
      * :inmanta:implementation:`redhat::network::config`
      * :inmanta:implementation:`ip::agentConfig`
      * :inmanta:implementation:`redhat::epel::epel7`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`redhat::scl::epel7`
        constraint ``(std::familyof(host.os,'rhel') and (host.os.version >= 7))``
      * :inmanta:implementation:`redhat::network::config`
        constraint ``std::familyof(host.os,'redhat')``
      * :inmanta:implementation:`std::none`
      * :inmanta:implementation:`ip::agentConfig`
        constraint ``(host.ip is defined is defined and host.remote_agent)``
      * :inmanta:implementation:`redhat::epel::epel7`
        constraint ``(std::familyof(host.os,'rhel') and (host.os.version >= 7))``


.. inmanta:entity:: std::HostGroup

   Parents: :inmanta:entity:`std::Entity`

   This entity represents a group of hosts. For example a cluster of machines.
   

   .. inmanta:attribute:: string std::HostGroup.name


   .. inmanta:relation:: std::Host std::HostGroup.hosts [0:\*]

      other end: :inmanta:relation:`std::Host.host_groups [0:\*]<std::Host.host_groups>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: std::ManagedDevice

   Parents: :inmanta:entity:`std::Entity`

   This interface represents all devices that can be managed
   

   .. inmanta:attribute:: std::hoststring std::ManagedDevice.name



.. inmanta:entity:: std::ManagedResource

   Parents: :inmanta:entity:`std::Resource`

   A base class for a resource that can be ignored/unmanaged by Inmanta.
   
   

   .. inmanta:attribute:: bool std::ManagedResource.managed=True

      This determines whether this resource is managed by Inmanta or not.


.. inmanta:entity:: std::OS

   Parents: :inmanta:entity:`std::Entity`

   Defines an operating system
   

   .. inmanta:attribute:: number std::OS.version=0


   .. inmanta:attribute:: string std::OS.name


   .. inmanta:relation:: std::OS std::OS.member [0:\*]

      other end: :inmanta:relation:`std::OS.family [0:1]<std::OS.family>`

   .. inmanta:relation:: std::OS std::OS.family [0:1]

      other end: :inmanta:relation:`std::OS.member [0:\*]<std::OS.member>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: std::Package

   Parents: :inmanta:entity:`std::Reload`

   A software package installed on a managed device.
   
   

   .. inmanta:attribute:: std::package_state std::Package.state

      The state of the package. Valid values are 'installed', 'removed' or 'latest'. latest will upgrade the package when an update is available.

   .. inmanta:attribute:: string std::Package.name

      The name of the package to manage

   .. inmanta:relation:: std::Host std::Package.host [1]

      other end: :inmanta:relation:`std::Host.packages [0:\*]<std::Host.packages>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::pkgHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::pkgHost`


.. inmanta:entity:: std::PurgeableResource

   Parents: :inmanta:entity:`std::Resource`

   A base class for a resource that can be purged and can be purged by Inmanta whenever the resource is no
   longer managed.
   
   

   .. inmanta:attribute:: bool std::PurgeableResource.purged=False

      Set whether this resource should exist or not.

   .. inmanta:attribute:: bool std::PurgeableResource.purge_on_delete=True

      Purge the resource when it is deleted from the configuration model. When this attribute is true, the server will include a resource with purged=true when this resource is no longer included in the configuration model.


.. inmanta:entity:: std::Reload

   Parents: :inmanta:entity:`std::Resource`

   An entity to make the (old) reload mechanism compatible with the event mechanism
   
   

   .. inmanta:attribute:: bool std::Reload.reload=False

      If a service requires this file, reload or restart the service when this file changes.

   .. inmanta:attribute:: bool std::Reload.send_event


   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::reload`


.. inmanta:entity:: std::Resource

   Parents: :inmanta:entity:`std::Entity`

   A base entity for resources that can be exported. This type add specific attributes
   that are common for most handlers.
   It is not required to inherit from this entity at the moment but highly recommended for documentation purposes.
   
   

   .. inmanta:attribute:: bool std::Resource.send_event=False

      This controls wether a resource should send its deploy state to the resources in its provides.


.. inmanta:entity:: std::Service

   Parents: :inmanta:entity:`std::Reload`

   Manage a service on a host.
   
   

   .. inmanta:attribute:: std::service_state std::Service.state

      The desired state of the service. Valid values are 'running' or 'stopped'

   .. inmanta:attribute:: bool std::Service.onboot

      Should the service start on boot.

   .. inmanta:attribute:: string std::Service.name

      The name of the service to manage

   .. inmanta:relation:: std::Host std::Service.host [1]

      other end: :inmanta:relation:`std::Host.services [0:\*]<std::Host.services>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::serviceHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::serviceHost`


.. inmanta:entity:: std::State

   Parents: :inmanta:entity:`std::Entity`

   Baseclass for entities that contain state
   
   

   .. inmanta:attribute:: string std::State.state_id=''

      The id to identify the state. If left empty, the resource id is used. (This can be used for cross environment/model restores)

   .. inmanta:attribute:: bool std::State.allow_snapshot=True

      Allow a snapshot of the state contained in this entity

   .. inmanta:attribute:: bool std::State.allow_restore=True

      Allow a restore of the state containted in this entity


.. inmanta:entity:: std::Symlink

   Parents: :inmanta:entity:`std::Reload`, :inmanta:entity:`std::PurgeableResource`

   A symbolic link on the filesystem
   

   .. inmanta:attribute:: string std::Symlink.target


   .. inmanta:attribute:: bool std::Symlink.send_event


   .. inmanta:attribute:: string std::Symlink.source


   .. inmanta:attribute:: bool std::Symlink.purge_on_delete=False


   .. inmanta:relation:: std::Host std::Symlink.host [1]

      other end: :inmanta:relation:`std::Host.symlinks [0:\*]<std::Host.symlinks>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`std::symHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::reload`, :inmanta:implementation:`std::symHost`


Implementations
---------------

.. inmanta:implementation:: std::dirHost

.. inmanta:implementation:: std::fileHost

.. inmanta:implementation:: std::hostDefaults

.. inmanta:implementation:: std::none

      An empty implementation that can be used as a safe default.
      

.. inmanta:implementation:: std::pkgHost

.. inmanta:implementation:: std::reload

.. inmanta:implementation:: std::serviceHost

.. inmanta:implementation:: std::symHost

Plugins
-------

.. py:function:: std.all(item_list: list, expression: expression) -> bool

   This method returns false when at least one item does not evaluate
   expression to true, otherwise it returns true
   
   :param expression: An expression that accepts one argument and
       returns true or false
   

.. py:function:: std.any(item_list: list, expression: expression) -> bool

   This method returns true when at least on item evaluates expression
   to true, otherwise it returns false
   
   :param expression: An expression that accepts one arguments and
       returns true or false
   

.. py:function:: std.assert(expression: bool, message: string=)

   Raise assertion error is expression is false
   

.. py:function:: std.at(objects: list, index: number) -> any

   Get the item at index
   

.. py:function:: std.attr(obj: any, attr: string) -> any

.. py:function:: std.capitalize(string: string) -> string

   Capitalize the given string
   

.. py:function:: std.count(item_list: list) -> number

   Returns the number of elements in this list
   

.. py:function:: std.delay(x: any) -> any

   Delay evaluation
   

.. py:function:: std.each(item_list: list, expression: expression) -> list

   Iterate over this list executing the expression for each item.
   
   :param expression: An expression that accepts one arguments and
       is evaluated for each item. The returns value of the expression
       is placed in a new list
   

.. py:function:: std.environment() -> string

   Return the environment id
   

.. py:function:: std.environment_name() -> string

   Return the name of the environment (as defined on the server)
   

.. py:function:: std.environment_server() -> string

   Return the address of the management server
   

.. py:function:: std.equals(arg1: any, arg2: any, desc: string=None)

   Compare arg1 and arg2
   

.. py:function:: std.familyof(member: std::OS, family: string) -> bool

   Determine if member is a member of the given operating system family
   

.. py:function:: std.file(path: string) -> string

   Return the textual contents of the given file
   

.. py:function:: std.first_of(value: list, type_name: string) -> any

   Return the first in the list that has the given type
   

.. py:function:: std.flatten(item_list: list) -> list

   Flatten this list
   

.. py:function:: std.generate_password(pw_id: string, length: number=20) -> string

   Generate a new random password and store it in the data directory of the
   project. On next invocations the stored password will be used.
   
   :param pw_id: The id of the password to identify it.
   :param length: The length of the password, default length is 20
   

.. py:function:: std.get(path: string) -> any

   This function return the variable with given string path
   

.. py:function:: std.get_env(name: string, default_value: string=None) -> string

.. py:function:: std.get_env_int(name: string, default_value: number=None) -> number

.. py:function:: std.getfact(resource: any, fact_name: string, default_value: any=None) -> any

   Retrieve a fact of the given resource
   

.. py:function:: std.inlineif(conditional: bool, a: any, b: any) -> any

   An inline if
   

.. py:function:: std.is_instance(obj: any, cls: string) -> bool

.. py:function:: std.is_set(obj: any, attribute: string) -> bool

.. py:function:: std.isset(value: any) -> bool

   Returns true if a value has been set
   

.. py:function:: std.item(objects: list, index: number) -> list

   Return a list that selects the item at index from each of the sublists
   

.. py:function:: std.key_sort(items: list, key: any) -> list

   Sort an array of object on key
   

.. py:function:: std.objid(value: any) -> string

.. py:function:: std.order_by(item_list: list, expression: expression=None, comparator: expression=None) -> list

   This operation orders a list using the object returned by
   expression and optionally using the comparator function to determine
   the order.
   
   :param expression: The expression that selects the attributes of the
       items in the source list that are used to determine the order
       of the returned list.
   
   :param comparator: An optional expression that compares two items.
   

.. py:function:: std.password(pw_id: string) -> string

   Retrieve the given password from a password file. It raises an exception when a password is not found
   
   :param pw_id: The id of the password to identify it.
   

.. py:function:: std.print(message: any)

   Print the given message to stdout
   

.. py:function:: std.replace(string: string, old: string, new: string) -> string

.. py:function:: std.select(objects: list, attr: string) -> list

   Return a list with the select attributes
   

.. py:function:: std.select_attr(item_list: list, attr: string) -> list

   This query method projects the list onto a new list by transforming
   the list as defined in the expression.
   

.. py:function:: std.select_many(item_list: list, expression: expression, selector_expression: expression=None) -> list

   This query method is similar to the select query but it merges
   the results into one list.
   
   :param expresion: An expression that returns the item that is to be
       included in the resulting list. If that item is a list itself
       it is merged into the result list. The first argument of the
       expression is the item in the source sequence.
   
   :param selector_expression: This optional arguments allows to
       provide an expression that projects the result of the first
       expression. This selector expression is equivalent to what the
       select method expects. If the returned item of expression is
       not a list this expression is not applied.
   

.. py:function:: std.sequence(i: number, start: number=0, offset: number=0) -> list

   Return a sequence of i numbers, starting from zero or start if supplied.
   

.. py:function:: std.server_ca() -> string

.. py:function:: std.server_port() -> number

.. py:function:: std.server_token() -> string

.. py:function:: std.source(path: string) -> string

   Return the textual contents of the given file
   

.. py:function:: std.split(string_list: string, delim: string) -> list

   Split the given string into a list
   
   :param string_list: The list to split into parts
   :param delim: The delimeter to split the text by
   

.. py:function:: std.template(path: string)

   Execute the template in path in the current context. This function will
   generate a new statement that has dependencies on the used variables.
   

.. py:function:: std.timestamp(dummy: any=None) -> number

   Return an integer with the current unix timestamp
   
   :param any: A dummy argument to be able to use this function as a filter
   

.. py:function:: std.type(obj: any) -> any

.. py:function:: std.unique(item_list: list) -> bool

   Returns true if all items in this sequence are unique
   

.. py:function:: std.unique_file(prefix: string, seed: string, suffix: string, length: number=20) -> string

.. py:function:: std.where(item_list: list, expression: expression) -> list

   This query method selects the items in the list that evaluate the
   expression to true.
   
   :param expression: An expression that returns true or false
       to determine if an item from the list is included. The first
       argument of the expression is the item that is to be evaluated.
       The second optional argument is the index of the item in the
       list.
   

.. py:function:: std.where_compare(item_list: list, expr_list: list) -> list

   This query selects items in a list but uses the tupples in expr_list
   to select the items.
   
   :param expr_list: A list of tupples where the first item is the attr
       name and the second item in the tupple is the value
   

Resources
---------

.. py:class:: std.resources.AgentConfig

   A resource that can modify the agentmap for autostarted agents
   

 * Resource for entity :inmanta:Entity:`std::AgentConfig`
 * Id attribute ``agentname``
 * Agent name ``agent``
 * Handlers :py:class:`std.resources.AgentConfigHandler`

.. py:class:: std.resources.Directory

   A directory on a filesystem
   

 * Resource for entity :inmanta:Entity:`std::Directory`
 * Id attribute ``path``
 * Agent name ``host.name``
 * Handlers :py:class:`std.resources.DirectoryHandler`

.. py:class:: std.resources.File

   A file on a filesystem
   

 * Resource for entity :inmanta:Entity:`std::File`
 * Id attribute ``path``
 * Agent name ``host.name``
 * Handlers :py:class:`std.resources.PosixFileProvider`

.. py:class:: std.resources.Package

   A software package installed on an operating system.
   

 * Resource for entity :inmanta:Entity:`std::Package`
 * Id attribute ``name``
 * Agent name ``host.name``
 * Handlers :py:class:`std.resources.YumPackage`, :py:class:`apt.AptPackage`

.. py:class:: std.resources.Service

   This class represents a service on a system.
   

 * Resource for entity :inmanta:Entity:`std::Service`
 * Id attribute ``name``
 * Agent name ``host.name``
 * Handlers :py:class:`std.resources.SystemdService`, :py:class:`std.resources.ServiceService`, :py:class:`ubuntu.UbuntuService`

.. py:class:: std.resources.Symlink

   A symbolic link on the filesystem
   

 * Resource for entity :inmanta:Entity:`std::Symlink`
 * Id attribute ``target``
 * Agent name ``host.name``
 * Handlers :py:class:`std.resources.SymlinkProvider`

Handlers
--------

.. py:class:: std.resources.SystemdService

   A handler for services on systems that use systemd
   

 * Handler name ``systemd``
 * Handler for entity :inmanta:Entity:`std::Service`

.. py:class:: std.resources.ServiceService

   A handler for services on systems that use service
   

 * Handler name ``redhat_service``
 * Handler for entity :inmanta:Entity:`std::Service`

.. py:class:: std.resources.SymlinkProvider

   This handler can deploy symlinks on unix systems
   

 * Handler name ``posix_symlink``
 * Handler for entity :inmanta:Entity:`std::Symlink`

.. py:class:: std.resources.AgentConfigHandler

 * Handler name ``agentrest``
 * Handler for entity :inmanta:Entity:`std::AgentConfig`

.. py:class:: std.resources.DirectoryHandler

   A handler for creating directories
   
   TODO: add recursive operations
   

 * Handler name ``posix_directory``
 * Handler for entity :inmanta:Entity:`std::Directory`

.. py:class:: std.resources.YumPackage

   A Package handler that uses yum
   

 * Handler name ``yum``
 * Handler for entity :inmanta:Entity:`std::Package`

.. py:class:: std.resources.PosixFileProvider

   This handler can deploy files on a unix system
   

 * Handler name ``posix_file``
 * Handler for entity :inmanta:Entity:`std::File`
