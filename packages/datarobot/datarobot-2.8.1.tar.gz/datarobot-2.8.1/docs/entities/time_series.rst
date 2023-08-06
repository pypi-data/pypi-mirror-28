.. _time_series:

####################
Time Series Projects
####################

Time series projects, like OTV projects, use :ref:`datetime partitioning<set_up_datetime>`, and all
the workflow changes that apply to other datetime partitioned projects also apply to them.
Unlike other projects, time series projects produce different types of models which forecast
multiple future predictions instead of an individual prediction for each row.

DataRobot uses a general time series framework to configure how time series features are created
and what future values the models will output. This framework consists of a Forecast Point
(defining a time a prediction is being made), a Feature Derivation Window (a rolling window used
to create features), and a Forecast Window (a rolling window of future values to predict). These
components are described in more detail below.

Time series projects will automatically transform the dataset provided in order to apply this
framework. During the transformation, DataRobot uses the Feature Derivation Window to derive
time series features (such as lags and rolling statistics), and uses the Forecast Window to provide
examples of forecasting different distances in the future (such as time shifts).
After project creation, a new dataset and a new feature list are generated and used to train
the models. This process is reapplied automatically at prediction time as well in order to
generate future predictions based on the original data features.

The ``time_unit`` and ``time_step`` used to define the Feature Derivation and Forecast Windows are
taken from the datetime partition column, and can be retrieved for a given column in the input data
by looking at the corresponding attributes on the :py:class:`datarobot.Feature` object.

Setting Up A Time Series Project
================================

To set up a time series project, follow the standard :ref:`datetime partitioning<set_up_datetime>`
workflow and use the six new time series specific parameters on the
:py:class:`datarobot.DatetimePartitioning` object:

use_time_series
    bool, set this to True to enable time series for the project.
default_to_a_priori
    bool, set this to True to default to treating all features as a priori features.  Otherwise
    they will not be handled as a priori features.  See
    :ref:`the prediction documentation<time_series_predict>` for more information.
feature_derivation_window_start
    int, the offset into the past to the start of the feature derivation window.
feature_derivation_window_end
    int, the offset into the past to the end of the feature derivation window.
forecast_window_start
    int, the offset into the future to the start of the forecast window.
forecast_window_end
    int, the offset into the future to the end of the forecast window.

Feature Derivation Window
*************************

The Feature Derivation window represents the rolling window that is used to derive
time series features and lags, relative to the Forecast Point. It is defined in terms of
``feature_derivation_window_start`` and ``feature_derivation_window_end`` which are integer values
representing datetime offsets in terms of the ``time_unit`` (e.g. hours or days).

The Feature Derivation Window start and end must be less than or equal to zero, indicating they are
positioned before the forecast point. Additionally, the window must be specified as an integer
multiple of the ``time_step`` which defines the expected difference in time units between rows in
the data.

The window is closed, meaning the edges are considered to be inside the window.

Forecast Window
***************

The Forecast Window represents the rolling window of future values to predict, relative to the
Forecast Point. It is defined in terms of the ``forecast_window_start`` and ``forecast_window_end``,
which are positive integer values indicating datetime offsets in terms of the ``time_unit`` (e.g.
hours or days).

The Forecast Window start and end must be positive integers, indicating they are
positioned after the forecast point. Additionally, the window must be specified as an integer
multiple of the ``time_step`` which defines the expected difference in time units between rows in
the data.

The window is closed, meaning the edges are considered to be inside the window.

.. _input_vs_modeling:

Modeling Data and Time Series Features
======================================

In time series projects, a new set of modeling features is created after setting the
partitioning options.  If a featurelist is specified with the partitioning options, it will be used
to select which features should be used to derived modeling features; if a featurelist is not
specified, the default featurelist will be used.

These features are automatically derived from those in the project's
dataset and are the features used for modeling - note that the Project methods
``get_featurelists`` and ``get_modeling_featurelists`` will return different data in time series
projects.  Modeling featurelists are the ones that can be used for modeling and will be accepted by
the backend, while regular featurelists will continue to exist but cannot be used.  Modeling
features are only accessible once the target and partitioning options have been
set.  In projects that don't use time series modeling, once the target has been set,
modeling and regular features and featurelists will behave the same.

.. _time_series_predict:

Making Predictions
==================

Prediction datasets are uploaded :ref:`as normal <predictions>`. However, when uploading a
prediction dataset, a new parameter ``forecast_point`` can be specified. The forecast point of a
prediction dataset identifies the point in time relative which predictions should be generated, and
if one is not specified when uploading a dataset, the server will choose the most recent possible
forecast point. The forecast window specified when setting the partitioning options for the project
determines how far into the future from the forecast point predictions should be calculated.

When setting up a time series project, input features could be identified as a priori features.
These features are not used to generate lags, and are expected to be known for the rows in the
forecast window at predict time (e.g. "how much money will have been spent on marketing", "is this
a holiday").

When uploading datasets to a time series project, the dataset might look something like the
following, if "Time" is the datetime partition column, "Target" is the target column, and "Temp." is
an input feature.  If the dataset was uploaded with a forecast point of "2017-01-08" and during
partitioning the feature derivation window start and end were set to -5 and -3 and the forecast
window start and end were set to 1 and 3, then rows 1 through 3 are historical data, row 6 is the
forecast point, and rows 7 though 9 are forecast rows that will have predictions when predictions
are computed.

.. code-block:: text

   Row, Time, Target, Temp.
   1, 2017-01-03, 16443, 72
   2, 2017-01-04, 3013, 72
   3, 2017-01-05, 1643, 68
   4, 2017-01-06, ,
   5, 2017-01-07, ,
   6, 2017-01-08, ,
   7, 2017-01-09, ,
   8, 2017-01-10, ,
   9, 2017-01-11, ,

On the other hand, if the project instead used "Holiday" as an a priori input feature, the uploaded
dataset might look like the following.

.. code-block:: text

   Row, Time, Target, Holiday
   1, 2017-01-03, 16443, TRUE
   2, 2017-01-04, 3013, FALSE
   3, 2017-01-05, 1643, FALSE
   4, 2017-01-06, , FALSE
   5, 2017-01-07, , FALSE
   6, 2017-01-08, , FALSE
   7, 2017-01-09, , TRUE
   8, 2017-01-10, , FALSE
   9, 2017-01-11, , FALSE
