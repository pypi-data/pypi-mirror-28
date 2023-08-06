Module exec
===========

 * License: Apache 2.0
 * Version: 0.6.0
 * Author: Inmanta <code@inmanta.com>
 * This module requires compiler version 2017.1 or higher
 * Upstream project: https://github.com/inmanta/exec.git

Entities
--------

.. inmanta:entity:: exec::Run

   Parents: :inmanta:entity:`std::Entity`

   Run a command with almost exact semantics as the exec type of puppet
   
   

   .. inmanta:attribute:: number exec::Run.timeout=300

      The maximum time the command should take. If the command takes longer, the deploy agent will try to end it.

   .. inmanta:attribute:: string exec::Run.creates=''

      A file that the command creates, when the file already exists the command will not be executed. This helps to make simple commands idempotent

   .. inmanta:attribute:: string exec::Run.command

      The actual command to execute. The command should be almost always be idempotent.

   .. inmanta:attribute:: bool exec::Run.reload_only=False

      Only use this command to reload

   .. inmanta:attribute:: string exec::Run.path=''

      The path to search the command in

   .. inmanta:attribute:: string exec::Run.cwd=''

      The directory from which to run the command. WARNING: Command is spawned in a subshell. This implies that the real path of cwd is used and not a possible symlinked path.

   .. inmanta:attribute:: string exec::Run.unless=''

      If this attribute is set, the command will only execute if the command in this attribute is not successful (returns not 0). If the command passed to this attribute does not exist, this is interpreted as a non-successful execution.

   .. inmanta:attribute:: string exec::Run.reload=''

      The command to execute when this run needs to reload. If empty the command itself will be executed again.

   .. inmanta:attribute:: dict exec::Run.environment=Dict()

      Environment variables to set before the command is executed. An array of variables can be passed as strings in the form var=value

   .. inmanta:attribute:: number exec::Run.returns=List()

      A list of valid return codes, by default this is only 0

   .. inmanta:attribute:: string exec::Run.onlyif=''

      Only execute the command if this command is true (returns 0)

   .. inmanta:relation:: std::Host exec::Run.host [1]

      other end: :inmanta:relation:`std::Host.exec_run_commands [0:\*]<std::Host.exec_run_commands>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`exec::execHost`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`exec::execHost`


Implementations
---------------

.. inmanta:implementation:: exec::execHost

Resources
---------

.. py:class:: exec.Run

   This class represents a service on a system.
   

 * Resource for entity :inmanta:Entity:`exec::Run`
 * Id attribute ``command``
 * Agent name ``host.name``
 * Handlers :py:class:`exec.PosixRun`

Handlers
--------

.. py:class:: exec.PosixRun

   A handler to execute commands on posix compatible systems. This is
   a very atypical resource as this executes a command. The check_resource
   method will determine based on the "reload_only", "creates", "unless"
   and "onlyif" attributes if the command will be executed.
   

 * Handler name ``posix``
 * Handler for entity :inmanta:Entity:`exec::Run`
