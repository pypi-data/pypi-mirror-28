Module mongodb
==============

 * License: Apache 2.0
 * Version: 0.3.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/mongodb.git

Entities
--------

.. inmanta:entity:: mongodb::Database

   Parents: :inmanta:entity:`std::State`

   Mongodb database
   

   .. inmanta:attribute:: bool mongodb::Database.purged=False


   .. inmanta:attribute:: string mongodb::Database.name


   .. inmanta:relation:: mongodb::MongoDB mongodb::Database.server [1]

      other end: :inmanta:relation:`mongodb::MongoDB.databases [0:\*]<mongodb::MongoDB.databases>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: mongodb::MongoDB

   Parents: :inmanta:entity:`ip::services::Server`

   Set up a single mongodb server
   

   .. inmanta:attribute:: bool mongodb::MongoDB.smallfiles=False


   .. inmanta:attribute:: ip::ip mongodb::MongoDB.bindip='127.0.0.1'


   .. inmanta:relation:: mongodb::ReplicaSet mongodb::MongoDB.rs_slave [0:1]

      other end: :inmanta:relation:`mongodb::ReplicaSet.slave_servers [2:\*]<mongodb::ReplicaSet.slave_servers>`

   .. inmanta:relation:: mongodb::Database mongodb::MongoDB.databases [0:\*]

      other end: :inmanta:relation:`mongodb::Database.server [1]<mongodb::Database.server>`

   .. inmanta:relation:: mongodb::ReplicaSet mongodb::MongoDB.rs_master [0:1]

      other end: :inmanta:relation:`mongodb::ReplicaSet.master_server [1]<mongodb::ReplicaSet.master_server>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`mongodb::mongoServerFedora`
      * :inmanta:implementation:`mongodb::mongoServerEpel`
      * :inmanta:implementation:`mongodb::mongoServerUbuntu`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`mongodb::mongoServerFedora`
        constraint ``std::familyof(host.os,'fedora')``
      * :inmanta:implementation:`mongodb::mongoServerEpel`
        constraint ``std::familyof(host.os,'rhel')``
      * :inmanta:implementation:`mongodb::mongoServerUbuntu`
        constraint ``std::familyof(host.os,'ubuntu')``


.. inmanta:entity:: mongodb::ReplicaSet

   Parents: :inmanta:entity:`std::Entity`

   A mongo replica set
   

   .. inmanta:attribute:: string mongodb::ReplicaSet.name='rs01'


   .. inmanta:relation:: mongodb::MongoDB mongodb::ReplicaSet.master_server [1]

      other end: :inmanta:relation:`mongodb::MongoDB.rs_master [0:1]<mongodb::MongoDB.rs_master>`

   .. inmanta:relation:: mongodb::MongoDB mongodb::ReplicaSet.slave_servers [2:\*]

      other end: :inmanta:relation:`mongodb::MongoDB.rs_slave [0:1]<mongodb::MongoDB.rs_slave>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`mongodb::mongoServerMaster`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`mongodb::mongoServerMaster`


Implementations
---------------

.. inmanta:implementation:: mongodb::mongoServerEpel

.. inmanta:implementation:: mongodb::mongoServerFedora

.. inmanta:implementation:: mongodb::mongoServerMaster

.. inmanta:implementation:: mongodb::mongoServerUbuntu

Resources
---------

.. py:class:: mongodb.Database

   A mongodb database
   

 * Resource for entity :inmanta:Entity:`mongodb::Database`
 * Id attribute ``name``
 * Agent name ``server.host.name``
 * Handlers :py:class:`mongodb.DatabaseHandler`

Handlers
--------

.. py:class:: mongodb.DatabaseHandler

   A handler to manage database on a mongodb server and snapshot/restore
   
   (this handler currently does nothing because mongo creates its database lazily)
   

 * Handler name ``mongodb``
 * Handler for entity :inmanta:Entity:`mongodb::Database`
