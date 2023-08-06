Module param
============

 * License: Apache 2.0
 * Version: 0.5.1
 * Author: Inmanta <code@inmanta.com>
 * Upstream project: https://github.com/inmanta/param.git

Typedefs
--------

.. inmanta:typedef:: param::email

   * Base type ``string``
   * Type constraint ``(self regex re.compile('[^@]+@[^@]+\\.[^@]+'))``


Entities
--------

.. inmanta:entity:: param::Form

   Parents: :inmanta:entity:`std::Entity`

   A form definition should inherit this type to define a form
   
   Attributes defined in subclasses of this entity become fields in the form. This form can be
   filled in through the REST API, cli or dashboard.
   
   Each field has one of the basic types or a special typedef that adds constraints on the
   type. This can be used for validation but also for the dashboard to provide specific
   input widgets.
   
   Attributes that start with _ are reserved for type options. The following attributes are
   currently supported:
   
    * _min_records: The minimal number of records required. If this number is higher than the
      actual number of records, unknowns are emitted.
    * _max_records: The maximal number of records that can be defined.
    * _record_count: The exact number of records that should exist. The main use case is a single
      singleton instance. A form with this value set to 1 can be queried with the :py:func:`param.one`
      plugin.
    * _title: The title of the form.
    * _help: A help text for the form
   
   Attributes that start with an existing attributename and than __ are used to specify attribute
   specific options:
   
    * __widget: Specify a special widget for this field. textarea, options and slider are supported.
    * __options: A list of options that should be chosen from. The list is provided as a comma
      separated string.
    * __label: A label for the form field
    * __help: A help text for the form field
    * __min: Option for the slider widget
    * __max: Option for the slider widget
   


Plugins
-------

.. py:function:: param.get(name: string, instance: string=) -> any

   Get a field in a record from the server.
   
   :param name: The name of the field in the record (instance) to query.
   :param instance: The record to get a parameter from.
   :return:  The value of the record. Returns an unknown to sequence the orchestration process
             when the parameter is not available. 
   

.. py:function:: param.instances(instance_type: string, expecting: number=0) -> list

   Return a list of records (instances) of the given type (form). This plugin uploads the record
   definition to the server. This makes the REST API available on the server and the form definition
   in the dashboard.
   
   :param instance_type: The entity (type) of the record (form)
   :param expecting: The minimal number of parameters to expect
   

.. py:function:: param.one(name: string, entity: string) -> any

   Get a parameter from a form that can have only one instance. This combines the 
   :py:func:`param.instances` and :py:func:`param.get` plugin in a single call. This plugin 
   only works on forms that limit the number of records to 1 (see :inmanta:entity:`param::Form`)
   
   Calling this plugin will upload the definition of the form to the server and make the REST API
   and Form in available.
   
   :param name: The name of the field in the record.
   :param entity: The name of the entity type to get the record for.
   

.. py:function:: param.report(name: string, value: string)

   This plugin reports a parameter to the server from the compile process. This can be used for
   `output` like parameter like in HEAT or TOSCA templates.
   
   The dashboard will explicitly show these values as well.
   
   :param name: The name/label of the value
   :param value: The value to report.
   
