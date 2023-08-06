Module mysql
============

 * License: Apache 2.0
 * Version: 0.5.2
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.2 or higher
 * Upstream project: https://github.com/inmanta/mysql.git

Entities
--------

.. inmanta:entity:: mysql::DBMS

   Parents: :inmanta:entity:`std::Entity`

   A DB management system (a service on a machina, DBaaS, ...)
   
   

   .. inmanta:attribute:: string mysql::DBMS.hostref

      reference to host, e.g. ip or hostname

   .. inmanta:attribute:: ip::port mysql::DBMS.port=3306


   .. inmanta:relation:: mysql::Database mysql::DBMS.databases [0:\*]

      other end: :inmanta:relation:`mysql::Database.server [1]<mysql::Database.server>`


.. inmanta:entity:: mysql::Database

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string mysql::Database.collation='utf8-ci'


   .. inmanta:attribute:: string mysql::Database.password


   .. inmanta:attribute:: string mysql::Database.name


   .. inmanta:attribute:: string mysql::Database.user


   .. inmanta:attribute:: string mysql::Database.encoding='utf8'


   .. inmanta:relation:: mysql::DBMS mysql::Database.server [1]

      other end: :inmanta:relation:`mysql::DBMS.databases [0:\*]<mysql::DBMS.databases>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`mysql::dBDependsOnServer`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`mysql::dBDependsOnServer`


.. inmanta:entity:: mysql::ManagedMysql

   Parents: :inmanta:entity:`mysql::DBMS`

   .. inmanta:attribute:: string mysql::ManagedMysql.password


   .. inmanta:attribute:: string mysql::ManagedMysql.user


   .. inmanta:relation:: ip::Host mysql::ManagedMysql.agenthost [1]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`mysql::manageManaged`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`mysql::manageManaged`


.. inmanta:entity:: mysql::Server

   Parents: :inmanta:entity:`ip::services::Server`, :inmanta:entity:`mysql::DBMS`

   Mysql server configuration
   

   The following implementations are defined for this entity:

      * :inmanta:implementation:`mysql::ports`
      * :inmanta:implementation:`mysql::mysqlRedhat`
      * :inmanta:implementation:`mysql::mysqlMariaDB`
      * :inmanta:implementation:`mysql::ubuntuMysql`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`mysql::ports`
      * :inmanta:implementation:`mysql::mysqlRedhat`
        constraint ``(std::familyof(host.os,'rhel') and (host.os.version <= 6))``
      * :inmanta:implementation:`mysql::mysqlMariaDB`
        constraint ``((std::familyof(host.os,'rhel') and (host.os.version >= 7)) or std::familyof(host.os,'fedora'))``
      * :inmanta:implementation:`mysql::ubuntuMysql`
        constraint ``std::familyof(host.os,'ubuntu')``


Implementations
---------------

.. inmanta:implementation:: mysql::dBDependsOnServer

.. inmanta:implementation:: mysql::manageManaged

.. inmanta:implementation:: mysql::mysqlMariaDB

.. inmanta:implementation:: mysql::mysqlRedhat

.. inmanta:implementation:: mysql::ports

.. inmanta:implementation:: mysql::ubuntuMysql
