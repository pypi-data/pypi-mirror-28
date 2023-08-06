social-auth-backend-csh
=======================

A `Python Social Auth`_ backend for Computer Science House.

Usage
-----

In your Social Auth configuration, add this module to the list of
backends in your app settings/configuration:

::

    AUTHENTICATION_BACKENDS = (
        ...
        'csh_auth.CSHAuth',
    )

Then add the following to your app settings/configuration, replacing the
values with the client ID and client secret for your application:

::

    SOCIAL_AUTH_CSH_KEY = '<client_id>'
    SOCIAL_AUTH_CSH_SECRET = '<client_secret>'

Need a client ID/secret? Reach out to any RTP via email or in #opcomm on
Slack.

.. _Python Social Auth: http://python-social-auth.readthedocs.io
