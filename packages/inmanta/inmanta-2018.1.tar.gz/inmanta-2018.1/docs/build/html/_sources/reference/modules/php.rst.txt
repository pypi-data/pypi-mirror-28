Module php
==========

 * License: Apache 2.0
 * Version: 0.3
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/php.git

Entities
--------

.. inmanta:entity:: php::Application

   Parents: :inmanta:entity:`web::Application`

   A web application that requires PHP
   

   .. inmanta:attribute:: bool php::Application.php55w=False


   The following implementations are defined for this entity:

      * :inmanta:implementation:`php::phpApacheRPM`
      * :inmanta:implementation:`php::php55el`
      * :inmanta:implementation:`php::phpApacheDEB`

   The following implements statements select implementations for this entity:

      * :inmanta:implementation:`php::phpApacheRPM`
        constraint ``(std::familyof(host.os,'redhat') and (php55w == False))``
      * :inmanta:implementation:`php::phpApacheDEB`
        constraint ``std::familyof(host.os,'ubuntu')``
      * :inmanta:implementation:`php::php55el`
        constraint ``(std::familyof(host.os,'redhat') and (php55w == True))``


Implementations
---------------

.. inmanta:implementation:: php::php55el

      This modules installs a common set of php modules and support for webservers
      either through a plugin or a cgi like interface.
      

.. inmanta:implementation:: php::phpApacheDEB

      This modules installs a common set of php modules and support for webservers
      either through a plugin or a cgi like interface.
      

.. inmanta:implementation:: php::phpApacheRPM

      This modules installs a common set of php modules and support for webservers
      either through a plugin or a cgi like interface.
      
