junit2influx
============

This library provide some utilities to manipulate test data from junit files
and sendthem to a influxdb server.


Installation
------------

.. code-block:: bash

    pip install junit2influx


Usage
-----

A CLI is available, as shown below:

.. code-block:: bash

    $ junit2influx --help

    Usage: junit2influx [OPTIONS] JUNIT_FILE

    Extract test data from a junit file and send it to influxdb:

        junit2influx test.xml --influxdb-url url

    Each test is send as a single datapoint with its result and
    duration under the "tests" measurement, and overall data
    (number of tests, total duration, etc.) is sent under
    the "builds" measurement.

    You can provide additional tags and fields to be sent with
    each datapoint to influxdb by using the --field and --tag
    flags:

        junit2influx test.xml --influxdb-url url --tag host=myhost --field commit=dh876d0

    All additional tags and fields are sent as string by default, but
    you can cast them to specific json types (bool, float and int) if needed:

        --tag int:stage=1      # add an integer "stage" tag with a value of 1
        --tag bool:fake=true   # add a boolean "fake" tag with a value of True
        --field float:dur=3.5  # add a float "dur" field with a value of 3.5

    Multiple --field and --tag flags can be provided.


