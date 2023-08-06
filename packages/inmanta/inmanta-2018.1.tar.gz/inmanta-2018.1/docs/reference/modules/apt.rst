Module apt
==========

 * License: Apache 2.0
 * Version: 0.4.1
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.1 or higher
 * Upstream project: https://github.com/inmanta/apt.git

Entities
--------

.. inmanta:entity:: apt::Repository

   Parents: :inmanta:entity:`std::Entity`

   An apt repository
   

   .. inmanta:attribute:: string apt::Repository.base_url


   .. inmanta:attribute:: string apt::Repository.release


   .. inmanta:attribute:: bool apt::Repository.trusted=False


   .. inmanta:attribute:: string apt::Repository.name


   .. inmanta:attribute:: string apt::Repository.repo


   .. inmanta:relation:: std::Host apt::Repository.host [1]

      other end: :inmanta:relation:`std::Host.repository [0:\*]<std::Host.repository>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`apt::simpleRepo`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`apt::simpleRepo`


Implementations
---------------

.. inmanta:implementation:: apt::simpleRepo

Handlers
--------

.. py:class:: apt.AptPackage

   A Package handler that uses apt
   
   TODO: add latest support
   

 * Handler name ``apt``
 * Handler for entity :inmanta:Entity:`std::Package`
