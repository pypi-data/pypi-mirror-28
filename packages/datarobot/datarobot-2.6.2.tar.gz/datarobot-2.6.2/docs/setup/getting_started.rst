###############
Getting Started
###############

Installation
============
You will need the following

- Python 2.7 or 3.4+
- DataRobot account
- pip

Installing for Cloud DataRobot
******************************

If you are using the cloud version of DataRobot, the easiest way to get the latest version of the package is:

.. code-block:: shell

  pip install datarobot

.. note::
   If you are not running in a Python virtualenv_, you probably want to use ``pip install --user datarobot``.


Installing for an On-Site Deploy
*************************************

If you are using an on-site deploy of DataRobot, the latest version of the package is not the most appropriate for you.  Contact your CFDS for guidance on the appropriate version range.

.. code-block:: shell

    pip install "datarobot>=$(MIN_VERSION),<$(EXCLUDE_VERSION)"

For some particular installation of DataRobot, the correct value of $(MIN_VERSION) could be 2.0 with an $(EXCLUDE_VERSION) of 2.3.  This ensures that all the features the client expects to be
present on the backend will always be correct.

.. note::
   If you are not running in a Python virtualenv_, you probably want to use ``pip install --user "datarobot>=$(MIN_VERSION),<$(MAX_VERSION)``.

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/


Installing pyOpenSSL
********************
On versions of Python earlier than 2.7.9 you might have InsecurePlatformWarning_ in your output.
To prevent this without updating your Python version you should install pyOpenSSL_ package:

.. _pyOpenSSL: https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
.. _InsecurePlatformWarning: https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning

.. code-block:: shell

    pip install pyopenssl ndg-httpsclient pyasn1

Configuration
=============
Each authentication method will specify credentials for DataRobot, as well as
the location of the DataRobot deployment. We currently support configuration
using a configuration file, by setting environment variables, or
within the code itself.

.. _credentials:

Credentials
***********
You will have to specify an API token and an endpoint in order to use the client.  You can manage
your API tokens in the DataRobot webapp, in your profile. This section describes how to use these
options. Their order of precedence is as follows, noting that the first available option will be used:

1. Setting endpoint and token in code using `datarobot.Client`
2. Configuring from a config file as specified directly using `datarobot.Client`
3. Configuring from a config file as specified by the environment variable `DATAROBOT_CONFIG_FILE`
4. Configuring from the environment variables `DATAROBOT_ENDPOINT` and `DATAROBOT_API_TOKEN`
5. Searching for a config file in the home directory of the current user, at `~/.config/datarobot/drconfig.yaml`

.. note::

    If you access the DataRobot webapp at
    `https://app.datarobot.com`, then the correct endpoint to specify would be
    `https://app.datarobot.com/api/v2`.  If you have a local installation, update the endpoint
    accordingly to point at the installation of DataRobot available on your local network.

Set Credentials Explicitly in Code
**********************************

Explicitly set credentials in code:

.. code-block:: python

   import datarobot as dr
   dr.Client(token='your_token', endpoint='https://app.datarobot.com/api/v2')

You can also point to a YAML config file to use:

.. code-block:: python

   import datarobot as dr
   dr.Client(config_path='/home/user/my_datarobot_config.yaml')


Use a Configuration File
************************
You can use a configuration file to specify the client setup.

The following is an example configuration file that should be saved as ``~/.config/datarobot/drconfig.yaml``:

.. code-block:: yaml

    token: yourtoken
    endpoint: https://app.datarobot.com/api/v2

You can specify a different location for the DataRobot configuration file by setting
the ``DATAROBOT_CONFIG_FILE`` environment variable.  Note that if you specify a filepath, you should
use an absolute path so that the API client will work when run from any location.

Set Credentials Using Environment Variables
*******************************************

Set up an endpoint by setting environment variables in the UNIX shell:

.. code-block:: shell

   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'
   export DATAROBOT_API_TOKEN=your_token
