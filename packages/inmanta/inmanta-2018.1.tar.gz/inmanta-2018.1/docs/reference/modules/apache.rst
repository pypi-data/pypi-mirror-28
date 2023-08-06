Module apache
=============

 * License: Apache 2.0
 * Version: 0.3.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/apache.git

Entities
--------

.. inmanta:entity:: apache::Server

   Parents: :inmanta:entity:`web::ApplicationContainer`

   An apache server
   

   The following implementations are defined for this entity:

      * :inmanta:implementation:`apache::apacheServerRPM`
      * :inmanta:implementation:`apache::apacheServerDEB`
      * :inmanta:implementation:`apache::serverLogs`
      * :inmanta:implementation:`apache::patchhttp2`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`apache::apacheServerRPM`, :inmanta:implementation:`apache::serverLogs`, :inmanta:implementation:`apache::patchhttp2`
        constraint ``(std::familyof(host.os,'fedora') and (host.os.version == 23))``
      * :inmanta:implementation:`apache::apacheServerRPM`, :inmanta:implementation:`apache::serverLogs`
        constraint ``(std::familyof(host.os,'rhel') or (std::familyof(host.os,'fedora') and (not (host.os.version == 23))))``
      * :inmanta:implementation:`apache::apacheServerDEB`, :inmanta:implementation:`apache::serverLogs`
        constraint ``std::familyof(host.os,'ubuntu')``


Implementations
---------------

.. inmanta:implementation:: apache::apacheServerDEB

.. inmanta:implementation:: apache::apacheServerRPM

.. inmanta:implementation:: apache::appImplDEB

.. inmanta:implementation:: apache::appImplRPM

.. inmanta:implementation:: apache::patchhttp2

.. inmanta:implementation:: apache::serverLogs
