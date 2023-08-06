======
Models
======

When a blueprint has been trained on a specific dataset at a specified sample
size, the result is a model. Models can be inspected to analyze their accuracy.

Quick Reference
***************

.. code-block:: python

    # Get all models of an existing project

    import datarobot as dr
    my_projects = dr.Project.list()
    project = my_projects[0]
    models = project.get_models()

List Finished Models
********************
You can use the ``get_models`` method to return a list of the project models
that have finished training:

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get('5506fcd38bd88f5953219da0')
    models = project.get_models()
    print(models[:5])
    >>> [Model(Decision Tree Classifier (Gini)),
         Model(Auto-tuned K-Nearest Neighbors Classifier (Minkowski Distance)),
         Model(Gradient Boosted Trees Classifier (R)),
         Model(Gradient Boosted Trees Classifier),
         Model(Logistic Regression)]
    model = models[0]

    project.id
    >>> u'5506fcd38bd88f5953219da0'
    model.id
    >>> u'5506fcd98bd88f1641a720a3'

You can pass following parameters to change result:

* ``search_params`` -- dict, used to filter returned projects. Currently you can query models by

    * ``name``
    * ``sample_pct``

* ``order_by`` -- str or list, if passed returned models are ordered by this attribute or attributes.
* ``with_metric`` -- str, If not `None`, the returned models will only have scores for this metric. Otherwise all the metrics are returned.

**List Models Example:**

.. code-block:: python

    Project('pid').get_models(order_by=['-created_time', 'sample_pct', 'metric'])

    # Getting models that contain "Ridge" in name
    # and with sample_pct more than 64
    Project('pid').get_models(
        search_params={
            'sample_pct__gt': 64,
            'name': "Ridge"
        })


Retrieve a Known Model
**********************
If you know the ``model_id`` and ``project_id`` values of a model, you can
retrieve it directly:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)

You can also use an instance of ``Project`` as the parameter for ``get``

.. code-block:: python

    model = dr.Model.get(project=project,
                         model_id=model_id)


Train a Model on a Different Sample Size
****************************************
One of the key insights into a model and the data behind it is how its
performance varies with more training data.
In Autopilot mode, DataRobot will run at several sample sizes by default,
but you can also create a job that will run at a specific sample size.
You can also specify featurelist that should be used for training of new model
and scoring type.
``train`` method of ``Model`` instance will put a new modeling job into the queue and return id of created
:doc:`ModelJob </entities/model_job>`.
You can pass ModelJob id to :ref:`wait_for_async_model_creation<wait_for_async_model_creation-label>` function,
that polls async model creation status and returns newly created model when it's finished.


.. code-block:: python

    model_job_id = model.train(sample_pct=33)

    # retraining model on custom featurelist using cross validation
    import datarobot as dr
    model_job_id = model.train(
        sample_pct=55,
        featurelist_id=custom_featurelist.id,
        scoring_type=dr.SCORING_TYPE.cross_validation,
    )

Find the Features Used
**********************
Because each project can have many associated featurelists, it is
important to know which features a model requires in order to run. This helps ensure that the the necessary features are provided when generating predictions.

.. code-block:: python

    feature_names = model.get_features_used()
    print(feature_names)
    >>> ['MonthlyIncome',
         'VisitsLast8Weeks',
         'Age']

.. _feature_impact-label:

Feature Impact
**************
Feature Impact measures how much worse a model's error score would be if DataRobot made predictions
after randomly shuffling a particular column (a technique sometimes called
`Permutation Importance`).

The following example code snippet shows how a featurelist with just the features with the highest
feature impact could be created.

.. code-block:: python

    import datarobot as dr

    max_num_features = 10
    time_to_wait_for_impact = 4 * 60  # seconds

    try:
        feature_impacts = model.get_feature_impact()  # if they've already been computed
    except dr.errors.ClientError as e:
        assert e.status_code == 404  # the feature impact score haven't been computed yet
        impact_job = model.request_feature_impact()
        feature_impacts = impact_job.get_result_when_complete(time_to_wait_for_impact)

    feature_impacts.sort(key=lambda x: x['impactNormalized'], reverse=True)
    final_names = [f['featureName'] for f in feature_impacts[:max_num_features]]

    project.create_featurelist('highest_impact', final_names)

Predict new data
****************
After creating models you can use them to generate predictions on new data.
See :doc:`PredictJob </entities/predict_job>` for further information on how to request predictions
from a model.

Model IDs Vs. Blueprint IDs
***************************
Each model has both an ``model_id`` and a ``blueprint_id``. What is the difference between these two IDs?

A model is the result of training a blueprint on a dataset at a specified
sample percentage. The ``blueprint_id`` is used to keep track of which
blueprint was used to train the model, while the ``model_id`` is used to
locate the trained model in the system.

Model parameters
****************
Some models can have parameters that provide data needed to reproduce its predictions.

For additional usage information see DataRobot documentation, section "Coefficients tab and
pre-processing details"

.. code-block:: python

    import datarobot as dr

    model = dr.Model.get(project=project, model_id=model_id)
    mp = model.get_parameters()
    print mp.derived_features()
    >>> [{
             'coefficient': -0.015,
             'originalFeature': u'A1Cresult',
             'derivedFeature': u'A1Cresult->7',
             'type': u'CAT',
             'transformations': [{'name': u'One-hot', 'value': u"'>7'"}]
        }]

Create a Blender
****************
You can blend multiple models; in many cases, the resulting blender model is more accurate
than the parent models. To do so you need to select parent models and a blender method from
``datarobot.enums.BLENDER_METHOD``.

Be aware that the tradeoff for better prediction accuracy is bigger resource consumption
and slower predictions.

.. code-block:: python

    import datarobot as dr

    pr = dr.Project.get(pid)
    models = pr.get_models()
    parent_models = [model.id for model in models[:2]]
    pr.blend(parent_models, dr.enums.BLENDER_METHOD.AVERAGE)