keystoneauth plugin for Rackspace authentication
================================================

.. image:: https://travis-ci.org/rackerlabs/python-rackspace-auth.svg
    :target: https://travis-ci.org/rackerlabs/python-rackspace-auth

This package provides plugins to
`keystoneauth1 <https://pypi.python.org/pypi/keystoneauth1/>`_,
the OpenStack Keystone authentication library, for Rackspace's supported
authentication methods: API key, password, and token.

Usage
-----

The following example authenticates Mayor McCheese with his API key,
as found in his `control panel <https://mycloud.rackspace.com/>`_. ::

    from rackspaceauth import v2
    from keystoneauth1 import session

    auth = v2.APIKey(username="Mayor McCheese",
                     api_key="OMGCHEESEISGREAT")

    sess = session.Session(auth=auth)
    sess.get_token()

To use in a
`clouds.yaml <https://docs.openstack.org/developer/os-client-config/#config-files>`_
file, for use with shade, ansible, os-client-config, and other tools, one might
add a section like this::

    clouds:
      rackspace-iad
        profile: rackspace
        auth:
          username: mayor-mccheese
          api_key: OMGCHEESEISGREAT
        auth_type: rackspace_apikey
        region_name: IAD
