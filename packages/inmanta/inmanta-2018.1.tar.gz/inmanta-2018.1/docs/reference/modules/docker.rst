Module docker
=============

Module to manage docker based containers

 * License: Apache 2.0
 * Version: 0.4.0
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/docker.git

Typedefs
--------

.. inmanta:typedef:: docker::container_state

   * Base type ``string``
   * Type constraint ``((((self == 'running') or (self == 'stopped')) or (self == 'latest')) or (self == 'purged'))``


Entities
--------

.. inmanta:entity:: docker::Container

   Parents: :inmanta:entity:`std::Entity`

   A docker container deployed on a container service
   
   

   .. inmanta:attribute:: string docker::Container.image

      The image to base this container on

   .. inmanta:attribute:: docker::container_state docker::Container.state='running'

      The state of the container

   .. inmanta:attribute:: string docker::Container.entrypoint=''

      The entrypoint of the container

   .. inmanta:attribute:: string docker::Container.memory_limit='0'

      RAM allocated to the container in human readable format ("128MB")

   .. inmanta:attribute:: string docker::Container.name

      The name of the docker container

   .. inmanta:attribute:: string docker::Container.command=''

      The command to execute

   .. inmanta:attribute:: bool docker::Container.detach=True

      Detach this container when started?

   .. inmanta:relation:: docker::Volume docker::Container.volumes [0:\*]

      other end: :inmanta:relation:`docker::Volume.container [1]<docker::Volume.container>`

   .. inmanta:relation:: docker::Service docker::Container.service [1]

      other end: :inmanta:relation:`docker::Service.containers [0:\*]<docker::Service.containers>`

   .. inmanta:relation:: docker::Port docker::Container.ports [0:\*]

      other end: :inmanta:relation:`docker::Port.container [1]<docker::Port.container>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: docker::Port

   Parents: :inmanta:entity:`std::Entity`

   A portmapping between the container and the host
   

   .. inmanta:attribute:: ip::ip docker::Port.host_ip='0.0.0.0'


   .. inmanta:attribute:: ip::port docker::Port.host_port


   .. inmanta:attribute:: ip::port docker::Port.container_port


   .. inmanta:relation:: docker::Container docker::Port.container [1]

      other end: :inmanta:relation:`docker::Container.ports [0:\*]<docker::Container.ports>`


.. inmanta:entity:: docker::Registry

   Parents: :inmanta:entity:`ip::services::Server`

   Deploy a docker registry
   

   The following implementations are defined for this entity:

      * :inmanta:implementation:`docker::dockerRegistry`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`docker::dockerRegistry`


.. inmanta:entity:: docker::Service

   Parents: :inmanta:entity:`ip::services::Server`

   A docker service
   

   .. inmanta:attribute:: ip::cidr docker::Service.bridge_ip='172.17.0.1/16'


   .. inmanta:relation:: docker::Container docker::Service.containers [0:\*]

      other end: :inmanta:relation:`docker::Container.service [1]<docker::Container.service>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`docker::docker`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`docker::docker`


.. inmanta:entity:: docker::Volume

   Parents: :inmanta:entity:`std::Entity`

   A volume mounted from the host into the container
   

   .. inmanta:attribute:: string docker::Volume.options='rw'


   .. inmanta:attribute:: string docker::Volume.container_path


   .. inmanta:attribute:: string docker::Volume.host_path


   .. inmanta:relation:: docker::Container docker::Volume.container [1]

      other end: :inmanta:relation:`docker::Container.volumes [0:\*]<docker::Container.volumes>`


Implementations
---------------

.. inmanta:implementation:: docker::docker

.. inmanta:implementation:: docker::dockerRegistry

Resources
---------

.. py:class:: docker.Container

   This class represents a docker container
   

 * Resource for entity :inmanta:Entity:`docker::Container`
 * Id attribute ``name``
 * Agent name ``service.host.name``
 * Handlers :py:class:`docker.ContainerHandler`

Handlers
--------

.. py:class:: docker.ContainerHandler

 * Handler name ``docker``
 * Handler for entity :inmanta:Entity:`docker::Container`
