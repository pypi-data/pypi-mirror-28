Module logging
==============

 * License: Apache 2.0
 * Version: 0.4.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/logging.git

Entities
--------

.. inmanta:entity:: logging::LogDir

   Parents: :inmanta:entity:`std::Entity`

   Models a log file in the configuration model
   

   .. inmanta:attribute:: string logging::LogDir.type=''


   .. inmanta:attribute:: string logging::LogDir.path


   .. inmanta:attribute:: string logging::LogDir.tag=''


   .. inmanta:attribute:: string logging::LogDir.priority


   .. inmanta:attribute:: string logging::LogDir.matches='.*\\.log'


   .. inmanta:attribute:: string logging::LogDir.name


   .. inmanta:relation:: std::Host logging::LogDir.host [1]

      other end: :inmanta:relation:`std::Host.log_dirs [0:\*]<std::Host.log_dirs>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: logging::LogFile

   Parents: :inmanta:entity:`std::Entity`

   Models a log file in the configuration model
   

   .. inmanta:attribute:: string logging::LogFile.type=''


   .. inmanta:attribute:: string logging::LogFile.path


   .. inmanta:attribute:: string logging::LogFile.tag=''


   .. inmanta:relation:: std::Host logging::LogFile.host [1]

      other end: :inmanta:relation:`std::Host.log_files [0:\*]<std::Host.log_files>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`

