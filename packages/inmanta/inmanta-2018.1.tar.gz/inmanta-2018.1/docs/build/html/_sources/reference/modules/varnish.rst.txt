Module varnish
==============

 * License: Apache 2.0
 * Version: 0.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/varnish.git

Entities
--------

.. inmanta:entity:: varnish::Proxy

   Parents: :inmanta:entity:`web::HostedLoadBalancer`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`varnish::varnishProxy`


Implementations
---------------

.. inmanta:implementation:: varnish::varnishProxy

Plugins
-------

.. py:function:: varnish.escape(name: string) -> string

   Escape all dots. This can be used to use a domain name in a regular expression
   
   :param name: The hostname to escape
   

.. py:function:: varnish.var(name: string) -> string

   Plugin that replaces characters that are not allowed in varnish identifiers
   
   :param name: The identifier to clean up
   
