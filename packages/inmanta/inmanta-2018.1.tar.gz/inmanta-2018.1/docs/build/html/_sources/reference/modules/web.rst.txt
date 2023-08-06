Module web
==========

 * License: Apache 2.0
 * Version: 0.2.2
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/web.git

Entities
--------

.. inmanta:entity:: web::Alias

   Parents: :inmanta:entity:`std::Entity`

   An alias (hostname) for a web application
   

   .. inmanta:attribute:: std::hoststring web::Alias.hostname


   .. inmanta:relation:: web::Cluster web::Alias.cluster [0:1]

      other end: :inmanta:relation:`web::Cluster.name [1]<web::Cluster.name>`

   .. inmanta:relation:: web::LoadBalancedApplication web::Alias.loadbalancer [0:1]

      other end: :inmanta:relation:`web::LoadBalancedApplication.name [1]<web::LoadBalancedApplication.name>`

   .. inmanta:relation:: web::Application web::Alias.application_alias [0:\*]

      other end: :inmanta:relation:`web::Application.aliases [0:\*]<web::Application.aliases>`

   .. inmanta:relation:: web::Application web::Alias.application [0:\*]

      other end: :inmanta:relation:`web::Application.name [1]<web::Application.name>`

   .. inmanta:relation:: web::Cluster web::Alias.cluster_alias [0:1]

      other end: :inmanta:relation:`web::Cluster.aliases [0:\*]<web::Cluster.aliases>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: web::Application

   Parents: :inmanta:entity:`std::Entity`

   This entity models a webapplication
   

   .. inmanta:attribute:: string web::Application.document_root


   .. inmanta:relation:: web::Alias web::Application.name [1]

      other end: :inmanta:relation:`web::Alias.application [0:\*]<web::Alias.application>`

   .. inmanta:relation:: web::Alias web::Application.aliases [0:\*]

      other end: :inmanta:relation:`web::Alias.application_alias [0:\*]<web::Alias.application_alias>`

   .. inmanta:relation:: web::ApplicationContainer web::Application.container [1]

      other end: :inmanta:relation:`web::ApplicationContainer.application [0:\*]<web::ApplicationContainer.application>`

   .. inmanta:relation:: web::LoadBalancedApplication web::Application.lb_app [0:1]

      other end: :inmanta:relation:`web::LoadBalancedApplication.app_instances [1:\*]<web::LoadBalancedApplication.app_instances>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: web::ApplicationContainer

   Parents: :inmanta:entity:`ip::services::Server`

   A container that hosts webapplications
   
   

   .. inmanta:attribute:: string web::ApplicationContainer.group


   .. inmanta:attribute:: number web::ApplicationContainer.port=80


   .. inmanta:attribute:: string web::ApplicationContainer.user

      The group name of the group as which the process of this container runs

   .. inmanta:relation:: web::Application web::ApplicationContainer.application [0:\*]

      other end: :inmanta:relation:`web::Application.container [1]<web::Application.container>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: web::Cluster

   Parents: :inmanta:entity:`std::Entity`

   A webapplication that is hosted as a cluster
   

   .. inmanta:attribute:: number web::Cluster.cluster_size


   .. inmanta:relation:: web::LoadBalancedApplication web::Cluster.loadbalancer [1:\*]

      other end: :inmanta:relation:`web::LoadBalancedApplication.web_cluster [0:\*]<web::LoadBalancedApplication.web_cluster>`

   .. inmanta:relation:: web::Alias web::Cluster.aliases [0:\*]

      other end: :inmanta:relation:`web::Alias.cluster_alias [0:1]<web::Alias.cluster_alias>`

   .. inmanta:relation:: web::Alias web::Cluster.name [1]

      other end: :inmanta:relation:`web::Alias.cluster [0:1]<web::Alias.cluster>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: web::HostedLoadBalancer

   Parents: :inmanta:entity:`web::LoadBalancer`, :inmanta:entity:`ip::services::Server`


.. inmanta:entity:: web::LoadBalancedApplication

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: bool web::LoadBalancedApplication.nameonly=True


   .. inmanta:relation:: web::Alias web::LoadBalancedApplication.name [1]

      other end: :inmanta:relation:`web::Alias.loadbalancer [0:1]<web::Alias.loadbalancer>`

   .. inmanta:relation:: web::Cluster web::LoadBalancedApplication.web_cluster [0:\*]

      other end: :inmanta:relation:`web::Cluster.loadbalancer [1:\*]<web::Cluster.loadbalancer>`

   .. inmanta:relation:: web::LoadBalancer web::LoadBalancedApplication.loadbalancer [1:\*]

      other end: :inmanta:relation:`web::LoadBalancer.applications [0:\*]<web::LoadBalancer.applications>`

   .. inmanta:relation:: web::Application web::LoadBalancedApplication.app_instances [1:\*]

      other end: :inmanta:relation:`web::Application.lb_app [0:1]<web::Application.lb_app>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: web::LoadBalancer

   Parents: :inmanta:entity:`ip::services::BaseServer`

   A loadbalancer for web applications
   

   .. inmanta:relation:: web::LoadBalancedApplication web::LoadBalancer.applications [0:\*]

      other end: :inmanta:relation:`web::LoadBalancedApplication.loadbalancer [1:\*]<web::LoadBalancedApplication.loadbalancer>`

