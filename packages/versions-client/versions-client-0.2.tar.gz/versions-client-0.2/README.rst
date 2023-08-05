Versions Client
===============

Adds a Prometheus exporter to your web application to read out version information.


Installation
++++++++++++

.. code-block:: sh

    pip install versions-client

    # This stores the OS packages upfront because it's very resource intensive
    os-package-versions > /var/local/os-package-versions.yaml


Usage
+++++

.. code-block:: python

    >>> import versions_client
    >>> versions_client.generate_versions(version='1.0', revision='d0935f4')

    # HELP version_application version info.
    # TYPE version_application gauge
    version_application{version="1.0",revision="d0935f4"} 1
    # HELP version_platform version info.
    # TYPE version_platform gauge
    version_platform{achitecture="64bit",name="linux",system="4.13.3-coreos",distro_version="8.9",distro_id="debian",distro_name="debian",type="x86_64"} 1
    # HELP version_python version info.
    # TYPE version_python gauge
    version_python{date="2017-10-10 02:49:49",implementation="cpython",version="2.7.14",compiler="gcc 4.9.2"} 1
    # HELP version_package version info.
    # TYPE version_package gauge
    version_package{version="4.9.2",group="os",name="libgcc1"} 1
    version_package{version="4.9.2",group="os",name="libitm1"} 1
    version_package{version="2.0.21",group="os",name="libevent-2.0-5"} 1
    ...
    version_package{version="0.30.0",group="python",name="wheel"} 1
    version_package{version="15.1.0",group="python",name="virtualenv"} 1
    version_package{version="1.0.0",group="python",name="versions-client"} 1
    version_package{version="36.5.0",group="python",name="setuptools"} 1
    version_package{version="3.12",group="python",name="pyyaml"} 1
    version_package{version="0.0.21",group="python",name="prometheus-client"} 1
    version_package{version="9.0.1",group="python",name="pip"} 1
    version_package{version="0.2.0",group="python",name="envparse"} 1
    ...


Settings
--------

+------------------------------+----------------------------------------------------------------------+
| Environment variable         | Description                                                          |
+==============================+======================================================================+
| ``VERSIONS_OS_PACKAGE_PATH`` | The path to the stored os packages file.                             |
+------------------------------+----------------------------------------------------------------------+


Usage with Django
-----------------

#.

    Add application labels to your django settings:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'versions_client',
            # ...
        )

        ...

        VERSIONS_AUTH = [('admin', 'secret')]
        VERSIONS_LABELS = {
            'version': 'v1.0',
            'revision': 'd0935f4',
        }


#.

    \a. Add the included URL's:

    .. code-block:: python

        # urls.py

        from django.conf.urls import include, url


        urlpatterns = [
            url(r'^', include('versions_client.django.urls')),
        ]

    This creates an endpoint on `/versionz`.


    \b. Or create your own URL's and views:

    .. code-block:: python

        # urls.py

        from django.conf.urls import include, url

        from . import views


        urlpatterns = [
            url(r'^metrics$', views.metrics_view, name='prometheus-django-metrics'),
        ]


    To get more metrics, you could integrate `django-prometheus <https://pypi.python.org/pypi/django-prometheus>`_.

    In this example we combine our metrics with those from `prometheus-client <https://pypi.python.org/pypi/prometheus-client>`_.

    .. code-block:: python

        # views.py

        import prometheus_client
        from django.conf import settings
        from django.http.response import HttpResponse
        import versions_client


        @versions_client.django.auth.basic
        def metrics_view(request):
            application_labels = getattr(settings, 'VERSIONS_LABELS', {})
            metrics_page = prometheus_client.generate_latest()
            version_page = versions_client.generate_versions(**application_labels)
            return HttpResponse(
                metrics_page + version_page,
                content_type=prometheus_client.CONTENT_TYPE_LATEST)
