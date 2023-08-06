Module graphite
===============

 * License: Apache 2.0
 * Version: 0.5.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/graphite.git

Entities
--------

.. inmanta:entity:: graphite::Carbon

   Parents: :inmanta:entity:`ip::services::Server`

   Collect metrics and store them
   

   .. inmanta:relation:: graphite::Frontend graphite::Carbon.graphite_frontend [0:1]

      other end: :inmanta:relation:`graphite::Frontend.carbon_server [1]<graphite::Frontend.carbon_server>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`graphite::carbonServerRedhat`
      * :inmanta:implementation:`graphite::carbonServerUbuntu`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`graphite::carbonServerRedhat`
        constraint ``std::familyof(host.os,'redhat')``
      * :inmanta:implementation:`graphite::carbonServerUbuntu`
        constraint ``std::familyof(host.os,'ubuntu')``


.. inmanta:entity:: graphite::Frontend

   Parents: :inmanta:entity:`web::Application`

   .. inmanta:relation:: graphite::Carbon graphite::Frontend.carbon_server [1]

      other end: :inmanta:relation:`graphite::Carbon.graphite_frontend [0:1]<graphite::Carbon.graphite_frontend>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`graphite::graphiteWeb`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`graphite::graphiteWeb`


Implementations
---------------

.. inmanta:implementation:: graphite::carbonServerRedhat

.. inmanta:implementation:: graphite::carbonServerUbuntu

.. inmanta:implementation:: graphite::graphiteWeb
