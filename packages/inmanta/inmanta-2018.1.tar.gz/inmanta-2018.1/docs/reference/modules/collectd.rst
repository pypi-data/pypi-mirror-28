Module collectd
===============

 * License: Apache 2.0
 * Version: 0.2.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/collectd.git

Entities
--------

.. inmanta:entity:: collectd::Agent

   Parents: :inmanta:entity:`collectd::NetworkInput`, :inmanta:entity:`collectd::NetworkOutput`

   A collectd agent that collects metrics
   
   

   .. inmanta:attribute:: bool collectd::Agent.forward=False

      Instruct the network plugin to forward inputs to outputs

   .. inmanta:attribute:: string collectd::Agent._plugin_config_path


   .. inmanta:attribute:: string collectd::Agent._service_name


   .. inmanta:relation:: collectd::Plugin collectd::Agent.plugins [0:\*]

      other end: :inmanta:relation:`collectd::Plugin.agent [1]<collectd::Plugin.agent>`

   .. inmanta:relation:: collectd::Type collectd::Agent.types [0:\*]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::collectdAgent`
      * :inmanta:implementation:`collectd::collectdAgentUbuntu`
      * :inmanta:implementation:`collectd::customTypes`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::collectdAgent`
        constraint ``(std::familyof(host.os,'rhel') or std::familyof(host.os,'fedora'))``
      * :inmanta:implementation:`collectd::collectdAgentUbuntu`
        constraint ``std::familyof(host.os,'ubuntu')``


.. inmanta:entity:: collectd::NetworkInput

   Parents: :inmanta:entity:`ip::services::Server`

   A collectd network input: accepts metrics using the collectd network protocol.
   

   .. inmanta:relation:: collectd::NetworkOutput collectd::NetworkInput.outputs [0:\*]

      other end: :inmanta:relation:`collectd::NetworkOutput.inputs [0:\*]<collectd::NetworkOutput.inputs>`


.. inmanta:entity:: collectd::NetworkOutput

   Parents: :inmanta:entity:`ip::services::BaseClient`

   A collectd network output: sends metrics over the network using the collect protocol.
   

   .. inmanta:relation:: collectd::NetworkInput collectd::NetworkOutput.inputs [0:\*]

      other end: :inmanta:relation:`collectd::NetworkInput.outputs [0:\*]<collectd::NetworkInput.outputs>`


.. inmanta:entity:: collectd::Plugin

   Parents: :inmanta:entity:`std::Entity`

   A collectd plugin that collects metrics
   

   .. inmanta:attribute:: string collectd::Plugin.config


   .. inmanta:attribute:: string collectd::Plugin.name


   .. inmanta:attribute:: number collectd::Plugin.interval=0


   .. inmanta:attribute:: number collectd::Plugin.load_order=10


   .. inmanta:relation:: collectd::Agent collectd::Plugin.agent [1]

      other end: :inmanta:relation:`collectd::Agent.plugins [0:\*]<collectd::Agent.plugins>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::loadPlugin`


.. inmanta:entity:: collectd::Type

   Parents: :inmanta:entity:`std::Entity`

   Add a new type to a custom types db
   

   .. inmanta:attribute:: string collectd::Type.min='U'


   .. inmanta:attribute:: string collectd::Type.name


   .. inmanta:attribute:: string collectd::Type.type


   .. inmanta:attribute:: string collectd::Type.max='U'


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: collectd::Varnish

   Parents: :inmanta:entity:`collectd::Plugin`

   Enable the Varnish collectd plugin
   

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::varnish`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::varnish`


.. inmanta:entity:: collectd::graphite::GraphiteWriter

   Parents: :inmanta:entity:`collectd::Plugin`

   A plugin to write metrics to graphite
   

   .. inmanta:attribute:: string collectd::graphite::GraphiteWriter.escape_character='_'


   .. inmanta:attribute:: string collectd::graphite::GraphiteWriter.prefix=''


   .. inmanta:attribute:: string collectd::graphite::GraphiteWriter.postfix=''


   .. inmanta:relation:: graphite::Carbon collectd::graphite::GraphiteWriter.carbon [1]

      other end: :inmanta:relation:`graphite::Carbon.collectd_writer [0:\*]<graphite::Carbon.collectd_writer>`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::graphite::graphiteWriter`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::graphite::graphiteWriter`


.. inmanta:entity:: collectd::plugins::CPU

   Parents: :inmanta:entity:`collectd::Plugin`

   Collectd CPU plugin.
   
   

   .. inmanta:attribute:: bool collectd::plugins::CPU.valuespercentage=False

      This option is only considered when both, ReportByCpu and ReportByState are set to true. In this case, by default, metrics will be reported as Jiffies. By setting this option to true, you can request percentage values in the un-aggregated (per-CPU, per-state) mode as well.

   .. inmanta:attribute:: bool collectd::plugins::CPU.reportbycpu=True

      When set to true, the default, reports per-CPU (per-core) metrics. When set to false, instead of reporting metrics for individual CPUs, only a global sum of CPU states is emitted.

   .. inmanta:attribute:: bool collectd::plugins::CPU.reportbystate=True

      When set to true, the default, reports per-state metrics, e.g. "system", "user" and "idle". When set to false, aggregates (sums) all non-idle states into one "active" metric.

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::cpu`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::cpu`, :inmanta:implementation:`collectd::loadPlugin`


.. inmanta:entity:: collectd::plugins::Df

   Parents: :inmanta:entity:`collectd::Plugin`

   Disk free plugin
   
   

   .. inmanta:attribute:: bool collectd::plugins::Df.reportreserved=True


   .. inmanta:attribute:: bool collectd::plugins::Df.valuesabsolute=True

      Enables or disables reporting of free and used disk space in 1K-blocks. Defaults to true.

   .. inmanta:attribute:: bool collectd::plugins::Df.ignoreselected=False

      Invert the selection: If set to true, all partitions except the ones that match any one of the criteria are collected. By default only selected partitions are collected if a selection is made. If no selection is configured at all, all partitions are selected.

   .. inmanta:attribute:: bool collectd::plugins::Df.reportbydevice=False

      Report using the device name rather than the mountpoint. i.e. with this false, (the default), it will report a disk as "root", but with it true, it will be "sda1" (or whichever).

   .. inmanta:attribute:: string collectd::plugins::Df.device

      Select partitions based on the devicename.

   .. inmanta:attribute:: bool collectd::plugins::Df.valuespercentage=False

      Enables or disables reporting of free and used disk space in percentage. Defaults to false. This is useful for deploying collectd on the cloud, where machines with different disk size may exist. Then it is more practical to configure thresholds based on relative disk size.

   .. inmanta:attribute:: bool collectd::plugins::Df.reportinodes=True

      Enables or disables reporting of free, reserved and used inodes. Defaults to inode collection being disabled. Enable this option if inodes are a scarce resource for you, usually because many small files are stored on the disk. This is a usual scenario for mail transfer agents and web caches.

   .. inmanta:attribute:: list collectd::plugins::Df.mountpoints


   .. inmanta:attribute:: list collectd::plugins::Df.fstypes


   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::df`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::df`


.. inmanta:entity:: collectd::plugins::Disk

   Parents: :inmanta:entity:`collectd::Plugin`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::disk`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::disk`


.. inmanta:entity:: collectd::plugins::Interface

   Parents: :inmanta:entity:`collectd::Plugin`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::interface`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::interface`


.. inmanta:entity:: collectd::plugins::SNMP

   Parents: :inmanta:entity:`collectd::Plugin`

   .. inmanta:relation:: collectd::plugins::SNMPData collectd::plugins::SNMP.data [0:\*]

   .. inmanta:relation:: collectd::plugins::SNMPHost collectd::plugins::SNMP.hosts [0:\*]

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::snmp`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::snmp`, :inmanta:implementation:`collectd::loadPlugin`


.. inmanta:entity:: collectd::plugins::SNMPData

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string collectd::plugins::SNMPData.values


   .. inmanta:attribute:: number collectd::plugins::SNMPData.scale=1.0


   .. inmanta:attribute:: bool collectd::plugins::SNMPData.table=False


   .. inmanta:attribute:: string collectd::plugins::SNMPData.type


   .. inmanta:attribute:: string collectd::plugins::SNMPData.name


   .. inmanta:attribute:: string collectd::plugins::SNMPData.instance


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: collectd::plugins::SNMPHost

   Parents: :inmanta:entity:`std::Entity`

   .. inmanta:attribute:: string collectd::plugins::SNMPHost.hostname


   .. inmanta:attribute:: number collectd::plugins::SNMPHost.version


   .. inmanta:attribute:: ip::ip collectd::plugins::SNMPHost.ip


   .. inmanta:attribute:: string collectd::plugins::SNMPHost.community


   .. inmanta:attribute:: number collectd::plugins::SNMPHost.interval=10


   .. inmanta:relation:: collectd::plugins::SNMPData collectd::plugins::SNMPHost.collect [1:\*]

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: collectd::plugins::StatsD

   Parents: :inmanta:entity:`collectd::Plugin`

   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::statsd`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::statsd`, :inmanta:implementation:`collectd::loadPlugin`


.. inmanta:entity:: collectd::plugins::WriteHttp

   Parents: :inmanta:entity:`collectd::Plugin`

   Write http plugin. The default format is JSON.
   

   .. inmanta:attribute:: string collectd::plugins::WriteHttp.url


   .. inmanta:attribute:: string collectd::plugins::WriteHttp.format='JSON'


   The following implementations are defined for this entity:

      * :inmanta:implementation:`collectd::plugins::writehttp`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`collectd::plugins::writehttp`, :inmanta:implementation:`collectd::loadPlugin`


Implementations
---------------

.. inmanta:implementation:: collectd::collectdAgent

.. inmanta:implementation:: collectd::collectdAgentUbuntu

.. inmanta:implementation:: collectd::customTypes

.. inmanta:implementation:: collectd::loadPlugin

.. inmanta:implementation:: collectd::varnish

.. inmanta:implementation:: collectd::graphite::graphiteWriter

.. inmanta:implementation:: collectd::plugins::cpu

.. inmanta:implementation:: collectd::plugins::df

.. inmanta:implementation:: collectd::plugins::disk

.. inmanta:implementation:: collectd::plugins::interface

.. inmanta:implementation:: collectd::plugins::snmp

.. inmanta:implementation:: collectd::plugins::statsd

.. inmanta:implementation:: collectd::plugins::writehttp
