Module ssh
==========

 * License: Apache 2.0
 * Version: 0.5.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/ssh.git

Entities
--------

.. inmanta:entity:: ssh::Key

   Parents: :inmanta:entity:`std::Entity`

   A public ssh-key used to access virtual machine
   
   

   .. inmanta:attribute:: string ssh::Key.options=''

      SSH options associated with this public key

   .. inmanta:attribute:: string ssh::Key.public_key

      The actual public key that needs to be deployed

   .. inmanta:attribute:: string ssh::Key.command=''

      The command that can be executed with this public key

   .. inmanta:attribute:: string ssh::Key.name

      An identifier for the public key

   .. inmanta:relation:: ssh::SSHUser ssh::Key.ssh_users [0:\*]

      other end: :inmanta:relation:`ssh::SSHUser.ssh_keys [0:\*]<ssh::SSHUser.ssh_keys>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ssh::SSHUser

   Parents: :inmanta:entity:`std::Entity`

   An ssh users allows authorized keys to be installed
   

   .. inmanta:attribute:: string ssh::SSHUser.group


   .. inmanta:attribute:: string ssh::SSHUser.home_dir


   .. inmanta:attribute:: string ssh::SSHUser.user


   .. inmanta:relation:: ssh::Key ssh::SSHUser.ssh_keys [0:\*]

      other end: :inmanta:relation:`ssh::Key.ssh_users [0:\*]<ssh::Key.ssh_users>`

   .. inmanta:relation:: std::Host ssh::SSHUser.host [1]

      other end: :inmanta:relation:`std::Host.ssh_users [0:\*]<std::Host.ssh_users>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`ssh::sshUser`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`ssh::sshUser`


.. inmanta:entity:: ssh::Server

   Parents: :inmanta:entity:`ip::services::Server`

   A ssh server
   

   The following implementations are defined for this entity:

      * :inmanta:implementation:`ssh::sshServer`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`ssh::sshServer`


Implementations
---------------

.. inmanta:implementation:: ssh::sshServer

.. inmanta:implementation:: ssh::sshUser

Plugins
-------

.. py:function:: ssh.get_private_key(name: string) -> string

   Create or return if it already exists a key with the given name. The
   private key is returned.
   

.. py:function:: ssh.get_public_key(name: string) -> string

   See get_private_key
   

.. py:function:: ssh.get_putty_key(name: string) -> string
