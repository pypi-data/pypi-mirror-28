Module monitoring
=================

 * License: Apache 2.0
 * Version: 0.2
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/monitoring.git

Entities
--------

.. inmanta:entity:: monitoring::Aggregator

   Parents: :inmanta:entity:`std::Entity`

   A generic aggregator
   

   .. inmanta:relation:: std::Host monitoring::Aggregator.host [1]

      other end: :inmanta:relation:`std::Host.aggregators [0:\*]<std::Host.aggregators>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::EventAggregator

   Parents: :inmanta:entity:`monitoring::Aggregator`

   Aggregate events
   

   .. inmanta:relation:: monitoring::HostTransport monitoring::EventAggregator.event_transport [0:\*]

      other end: :inmanta:relation:`monitoring::HostTransport.event_aggregators [0:1]<monitoring::HostTransport.event_aggregators>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::EventSource

   Parents: :inmanta:entity:`monitoring::Source`

   A source of events
   


.. inmanta:entity:: monitoring::HostTransport

   Parents: :inmanta:entity:`std::Entity`

   A component on a host that transports metrics, logs and events to
   somewhere. That can be over the network or to a file.
   

   .. inmanta:relation:: monitoring::EventAggregator monitoring::HostTransport.event_aggregators [0:1]

      other end: :inmanta:relation:`monitoring::EventAggregator.event_transport [0:\*]<monitoring::EventAggregator.event_transport>`

   .. inmanta:relation:: monitoring::MetricAggregator monitoring::HostTransport.metric_aggregators [0:1]

      other end: :inmanta:relation:`monitoring::MetricAggregator.metric_transport [0:\*]<monitoring::MetricAggregator.metric_transport>`

   .. inmanta:relation:: std::Host monitoring::HostTransport.host [1]

      other end: :inmanta:relation:`std::Host.monitoring_transport [0:\*]<std::Host.monitoring_transport>`

   .. inmanta:relation:: monitoring::LogAggregator monitoring::HostTransport.log_aggregators [0:1]

      other end: :inmanta:relation:`monitoring::LogAggregator.log_transport [0:\*]<monitoring::LogAggregator.log_transport>`

   .. inmanta:relation:: monitoring::QueryAggregator monitoring::HostTransport.query_aggregators [1]

      other end: :inmanta:relation:`monitoring::QueryAggregator.query_transport [0:\*]<monitoring::QueryAggregator.query_transport>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::JmxSource

   Parents: :inmanta:entity:`monitoring::LogSource`, :inmanta:entity:`monitoring::MetricSource`, :inmanta:entity:`monitoring::EventSource`

   Collect monitoring data from JMX
   

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::JournaldTail

   Parents: :inmanta:entity:`monitoring::LogSource`

   Tail the output of journald and collect messages
   

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::LogAggregator

   Parents: :inmanta:entity:`monitoring::Aggregator`

   Aggregate logs
   

   .. inmanta:relation:: monitoring::HostTransport monitoring::LogAggregator.log_transport [0:\*]

      other end: :inmanta:relation:`monitoring::HostTransport.log_aggregators [0:1]<monitoring::HostTransport.log_aggregators>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::LogSource

   Parents: :inmanta:entity:`monitoring::Source`

   A source of log data
   


.. inmanta:entity:: monitoring::LogTail

   Parents: :inmanta:entity:`monitoring::LogSource`

   Put a tail on a log file and collect the log message
   

   .. inmanta:attribute:: string monitoring::LogTail.path


   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::MetricAggregator

   Parents: :inmanta:entity:`monitoring::Aggregator`

   Aggregate metrics
   

   .. inmanta:relation:: monitoring::HostTransport monitoring::MetricAggregator.metric_transport [0:\*]

      other end: :inmanta:relation:`monitoring::HostTransport.metric_aggregators [0:1]<monitoring::HostTransport.metric_aggregators>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::MetricCollector

   Parents: :inmanta:entity:`monitoring::MetricSource`

   Enable a sensor collect on a host
   

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::MetricSource

   Parents: :inmanta:entity:`monitoring::Source`

   A source of metric data
   


.. inmanta:entity:: monitoring::QueryAggregator

   Parents: :inmanta:entity:`monitoring::Aggregator`

   The query interface
   

   .. inmanta:relation:: monitoring::HostTransport monitoring::QueryAggregator.query_transport [0:\*]

      other end: :inmanta:relation:`monitoring::HostTransport.query_aggregators [1]<monitoring::HostTransport.query_aggregators>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`


.. inmanta:entity:: monitoring::Source

   Parents: :inmanta:entity:`std::Entity`

   A source of monitoring data
   

   .. inmanta:relation:: std::Host monitoring::Source.host [1]

      other end: :inmanta:relation:`std::Host.monitoring_source [0:\*]<std::Host.monitoring_source>`

   .. inmanta:relation:: monitoring::Tag monitoring::Source.tags [0:\*]

      other end: :inmanta:relation:`monitoring::Tag.base [1]<monitoring::Tag.base>`


.. inmanta:entity:: monitoring::Tag

   Parents: :inmanta:entity:`std::Entity`

   A tag on a data source for monitoring tools
   
   

   .. inmanta:attribute:: string monitoring::Tag.name

      The name of the tag

   .. inmanta:relation:: monitoring::Source monitoring::Tag.base [1]

      other end: :inmanta:relation:`monitoring::Source.tags [0:\*]<monitoring::Source.tags>`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`std::none`

