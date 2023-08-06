Module user
===========

 * License: ASL 2
 * Version: 0.1.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/user.git

Entities
--------

.. inmanta:entity:: user::Group

   Parents: :inmanta:entity:`std::ManagedResource`, :inmanta:entity:`std::PurgeableResource`

   .. inmanta:attribute:: bool user::Group.system=False


   .. inmanta:attribute:: string user::Group.name


   .. inmanta:relation:: std::Host user::Group.host [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`user::execGroup`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`user::execGroup`


.. inmanta:entity:: user::User

   Parents: :inmanta:entity:`std::ManagedResource`, :inmanta:entity:`std::PurgeableResource`

   .. inmanta:attribute:: bool user::User.system=False


   .. inmanta:attribute:: string user::User.groups=List()


   .. inmanta:attribute:: string user::User.name


   .. inmanta:attribute:: string user::User.homedir


   .. inmanta:attribute:: string user::User.group


   .. inmanta:attribute:: string user::User.shell='/bin/bash'


   .. inmanta:relation:: std::Host user::User.host [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`user::execUser`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`user::execUser`


Implementations
---------------

.. inmanta:implementation:: user::execGroup

      Exec based implementation until a handler is available
      

.. inmanta:implementation:: user::execUser

      Exec based implementation until a handler is available
      
