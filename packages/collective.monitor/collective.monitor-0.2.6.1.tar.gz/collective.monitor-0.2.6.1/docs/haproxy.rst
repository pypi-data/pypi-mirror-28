HAProxy Recipe
==============

This outlines the relevant parts of the HAProxy configuration to use the probes
`health_db_connected` or `health_ok` for health checks.

::

    defaults

        default-server inter 2s slowstart 1m

    backend zope

        option tcp-check
        tcp-check send health_db_connected\r\n
        tcp-check expect string OK

        server instance1 127.0.0.1:8080 check port 8888
        server instance2 127.0.0.1:8081 check port 8889


For more Information on configuring HAProxy please consult the
`HAProxy Documentation <https://cbonte.github.io/haproxy-dconv/>`_
