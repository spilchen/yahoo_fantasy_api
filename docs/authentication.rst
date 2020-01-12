Authentication
==============

Before you can do any sort of authentication, you will first need to request an `API key <https://developer.yahoo.com/apps/create/>`_ from Yahoo!  The process is quick, and you will be given a consumer key and a consumer secret, which you use as part of the authentication.

There is a lengthy overview of the authentication requirement to access the Yahoo! fantasy APIs in its developer `guide <https://developer.yahoo.com/fantasysports/guide/>`_.   However, to save you some time in understanding that, this package makes use of the work done in the `yahoo_oauth <https://pypi.org/project/yahoo_oauth/>`__ to implement the oauth protocol.  In fact, all of the classes in this package expect the `yahoo_oauth.OAuth2` object to be passed in.  

Here is some sample code that constructs the `yahoo_oauth.OAuth2` object.

::

    from yahoo_oauth import OAuth2
    import os
    import json

    if not os.path.exists('oauth2.json'):
        creds = {'consumer_key': 'my_key', 'consumer_secret': 'my_secret'}
        with open(args['<json>'], "w") as f:
            f.write(json.dumps(creds))

    oauth = OAuth2(None, None, from_file='oauth2.json')


You can then pass in `oauth2` when construct the various classes in this package.  See the `documentation <https://yahoo-oauth.readthedocs.io/en/latest/>`_ for `yahoo_oauth` for more information.
