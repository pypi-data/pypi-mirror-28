Module ansible
==============

 * License: Apache 2.0
 * Version: 0.2.1
 * Upstream project: https://github.com/inmanta/ansible.git

Entities
--------

.. inmanta:entity:: ansible::Arg

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string ansible::Arg.value=''


   .. inmanta:attribute:: string ansible::Arg.name


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ansible::JsonArg

   Parents: :inmanta:entity:`ansible::Arg`

   .. inmanta:attribute:: string ansible::JsonArg.json


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: ansible::Task

   Parents: :inmanta:entity:`std::Entity`

   An ansible task
   
   

   .. inmanta:attribute:: string ansible::Task.host='localhost'

      The host (target) to execute the task on

   .. inmanta:attribute:: string ansible::Task.module

      The ansible module that has to be invoked

   .. inmanta:attribute:: string ansible::Task.agent='ansible'

      The agent that should run the task

   .. inmanta:attribute:: dict ansible::Task.args

      The args to pass to the task. This dict is directly serialized to json and included varbetim in the playbook

   .. inmanta:attribute:: string ansible::Task.name

      The name of the task. This has to be unique in combination with the host

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


Resources
---------

.. py:class:: ansible.Task

 * Resource for entity :inmanta:Entity:`ansible::Task`
 * Id attribute ``name``
 * Agent name ``agent``
 * Handlers :py:class:`ansible.TaskHandler`

Handlers
--------

.. py:class:: ansible.TaskHandler

 * Handler name ``task``
 * Handler for entity :inmanta:Entity:`ansible::Task`
