wsgiauth0
=========

.. image:: https://gitlab.com/dialogue/wsgiauth0/badges/master/build.svg
.. image:: https://gitlab.com/dialogue/wsgiauth0/badges/master/coverage.svg?job=Run%20py.test

This is an Auth0 middleware for multiple client configurations.

It adds 4 keys to `environ` mapping:

* `wsgiauth0.jwt_claims`: The decoded claims dict or `None` if any error
  occurred. Example::

        {
            'iss': 'issuer',
            'sub': 'auth0|user_id',
            'aud': 'https://example.com,
            'exp': 1234567890,
            'iat': 1134567890,
        }

* `wsgiauth0.jwt_error`: A mapping with keys `code` and `description` or `None`
  if no error occurred, Example::

        {
            'code': 'invalid_header',
            'description': 'Authorization header must be "Bearer token".',
        }

* `wsgiauth0.jwt_client`: A mapping with the client info used if any info were
  successfully deduced from json web token received::

        {
            'id': 'NieY4eekoo3aed2fe9ei',
            'audience': 'https://example.com',
            'secret': 'shei6eehuF2ui9OphahW',
        }

* `REMOTE_USER`: The decoded subject from `wsgiauth0.jwt_claims` or `None` if
  any error occurred.

Usage
-----

Configure your wsgi pipeline in paste deploy ini file::

    [filter:wsgiauth0]
    use = egg:wsgiauth0#middleware
    clients_config_file = %(here)s/auth0_clients_config.yml

    [pipeline:main]
    pipeline =
        wsgiauth0
        myapp

    [app:myapp]
    use = egg:wsgiapp#main

    [server:main]
    use = egg:waitress#main
    host = 0.0.0.0
    port = 6543


Configuration with DynamoDB
---------------------------

It expects a `clients_config_file` key pointing to auth0 client configuration
yaml file.

Here is an example of a yaml configuration file.

.. code:: yaml

    Client 1:
        id: oZ0ahm4Thoh1Oghiqu4oe9qu
        audience: oZ0ahm4Thoh1Oghiqu4oe9qu
        secret:
            value: noh4feibaighikeeD0inah9Rei3nei6yeenoa7uar2Dah2yaeKioph8Jux8ahte
            type: base64_url_encoded

    Client 2:
        id: Aen1XobahDoh7queing3eaS0@clients
        audience: https://example.com/
        secret:
            value: |
                -----BEGIN CERTIFICATE REQUEST-----
                MIIBZjCB0AIBADANMQswCQYDVQQGEwJDQTCBnzANBgkqhkiG9w0BAQEFAAOBjQAw
                gYkCgYEAx2LwsUexPKQ/0GIHqugXZtIGZxSOovO754KWn3ZWBbDvm/wuh+QfmMj8
                ZTxnxRymHjSNJ04nCMcqtzl3VDwapMkM433CnyZjoJjA/fRwLRjUepLAMbmoqkOG
                k1BKNAyidyko7DBnkMayzJRfmnCwFy1hsuikh6oFSinU7MP3LBsCAwEAAaAaMBgG
                CSqGSIb3DQEJBzELEwljaGFsbGVuZ2UwDQYJKoZIhvcNAQELBQADgYEAP819zy3q
                1gh5z5FLeFanc3TpdlcGHCQxcTMC/x9iyMpbSd2XkKLrZ02Is1Y8Ox/XeT8zNjOg
                /nulPg6YrIsywpKFR4orMvuUUMZ8uT8UVNj1pnatmXy9ikjdGtBXeU+EKkMZ4q6a
                OrG8qyB4o/WETphyxfneazWt3jrLHkKBvXA=
                -----END CERTIFICATE REQUEST-----
            type: certiticate


Configuration with DynamoDB
---------------------------

DynamoDB can be used as a configuration source.  The configuration
table should have an item for each key that should be used for
authentication.

Specify the table name with the `clients_config_table` key, and the
service name with `clients_config_service`.

The table should have a hash key on the `service` field, and a sort
key on the `label` field (a human friendly description for the key).
The other fields are `id`, `audience`, `and secret` with sub-keys
`type` and `value`.

You should require the `dynamodb` extra dependency
(i.e. wsgiauth0[dynamodb]).
