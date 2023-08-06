Module yum
==========

 * License: Apache 2.0
 * Version: 0.5.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/yum.git

Entities
--------

.. inmanta:entity:: yum::Repository

   Parents: :inmanta:entity:`std::Entity`

   A yum repositoy
   

   .. inmanta:attribute:: string yum::Repository.gpgkey=''


   .. inmanta:attribute:: string yum::Repository.baseurl


   .. inmanta:attribute:: bool yum::Repository.gpgcheck=False


   .. inmanta:attribute:: string yum::Repository.name


   .. inmanta:attribute:: bool yum::Repository.enabled=True


   .. inmanta:attribute:: number yum::Repository.metadata_expire=7200


   .. inmanta:relation:: std::Host yum::Repository.host [1]

      other end: :inmanta:relation:`std::Host.repos [0:\*]<std::Host.repos>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`yum::redhatRepo`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`yum::redhatRepo`
        constraint ``std::familyof(host.os,'redhat')``


Implementations
---------------

.. inmanta:implementation:: yum::redhatRepo
