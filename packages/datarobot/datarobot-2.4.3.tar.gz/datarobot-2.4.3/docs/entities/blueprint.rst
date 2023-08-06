##########
Blueprints
##########

The set of computation paths that a dataset passes through before producing
predictions from data is called a blueprint. A blueprint can be trained on
a dataset to generate a model.

Quick Reference
***************
The following code block summarizes the interactions available for blueprints. 

.. code-block:: python

    # Get the set of blueprints recommended by datarobot
    import datarobot as dr
    my_projects = dr.Project.list()
    project = my_projects[0]
    menu = project.get_blueprints()

    first_blueprint = menu[0]
    project.train(first_blueprint)

List Blueprints
***************
When a file is uploaded to a project and the target is set, DataRobot
recommends a set of blueprints that are appropriate for the task at hand.
You can use the ``get_blueprints`` method to get the list of blueprints recommended for a project:

.. code-block:: python

    project = dr.Project.get('5506fcd38bd88f5953219da0')
    menu = project.get_blueprints()
    blueprint = menu[0]

Blueprint Attributes
********************
The ``Blueprint`` class holds the data required to use the blueprint
for modeling. This includes the ``blueprint_id`` and ``project_id``.
There are also two attributes that help distinguish blueprints: ``model_type``
and ``processes``.

.. code-block:: python

    print(blueprint.id)
    >>> u'8956e1aeecffa0fa6db2b84640fb3848'
    print(blueprint.project_id)
    >>> u5506fcd38bd88f5953219da0'
    print(blueprint.model_type)
    >>> Logistic Regression
    print(blueprint.processes)
    >>> [u'One-Hot Encoding',
         u'Missing Values Imputed',
         u'Standardize',
         u'Logistic Regression']

Create a Model from a Blueprint
*******************************
You can use a blueprint instance to train a model. The default dataset for the project is used.

.. code-block:: python

    model_job_id = project.train(blueprint, sample_pct=25)

This method will put a new modeling job into the queue and returns id of created
:doc:`ModelJob </entities/model_job>`.
You can pass ModelJob id to :ref:`wait_for_async_model_creation <wait_for_async_model_creation-label>` function,
that polls async model creation status and returns newly created model when it's finished.
