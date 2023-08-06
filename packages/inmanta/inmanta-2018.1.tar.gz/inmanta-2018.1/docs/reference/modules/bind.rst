Module bind
===========

 * License: Apache 2.0
 * Version: 0.4
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/bind.git

Entities
--------

.. inmanta:entity:: bind::Server

   Parents: :inmanta:entity:`dns::Server`

   .. inmanta:attribute:: string bind::Server._pkg_name


   .. inmanta:attribute:: string bind::Server._svc_name


   .. inmanta:attribute:: string bind::Server.additional_config=''


   .. inmanta:attribute:: string bind::Server.axfr_allowed=''


   .. inmanta:attribute:: string bind::Server._zone_dir


   .. inmanta:attribute:: string bind::Server.work_dir


   The following implementations are defined for this entity:

      * :inmanta:implementation:`bind::bindDnsServer`
      * :inmanta:implementation:`bind::bindUbuntu`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`bind::bindDnsServer`
        constraint ``std::familyof(host.os,'redhat')``
      * :inmanta:implementation:`bind::bindUbuntu`
        constraint ``std::familyof(host.os,'ubuntu')``


Implementations
---------------

.. inmanta:implementation:: bind::bindDnsServer

.. inmanta:implementation:: bind::bindUbuntu

.. inmanta:implementation:: bind::zoneFile

Plugins
-------

.. py:function:: bind.nameservers(master_zones: list, slave_zones: list=[]) -> list

   Returns a list of all the name servers in ns records in the list of zones
   

.. py:function:: bind.serial(zone: string, zonefile: string) -> string

   This plugin will check if the zonefile has been updated since the last compile. If the zone
   is update it will replace __SERIAL__ with the current UTC timestamp. If the zonefile has
   not been updated, it will use the previous serial.
   
   :param zone: The name of the zone to check
   :param zonefile: The actual zone file. This is a complete and valid zonefile with __SERIAL__
                    in it as placeholder. This placeholder is replaced with the current
                    serial.
   
