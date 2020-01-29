Authentication
==============

Before you can do any sort of authentication, you will first need to request an `API key <https://developer.yahoo.com/apps/create/>`_ from Yahoo!  The process is quick, and you will be given a consumer key and a consumer secret, which you use as part of the authentication.

There is a lengthy overview of the authentication requirement to access the Yahoo! fantasy APIs in its developer `guide <https://developer.yahoo.com/fantasysports/guide/>`_.   However, to save you some time in understanding that, this package makes use of the work done in the `yahoo_oauth <https://pypi.org/project/yahoo_oauth/>`__ to implement the oauth protocol.  In fact, all of the classes in this package expect the `yahoo_oauth.OAuth2` object to be passed in.  

To simplify the usage of `yahoo_oauth.OAuth2` it is best to construct a file that has your access tokens in it.  You can then use this file whenever you construct `yahoo_oauth.OAuth2`.  There is a one time setup involved to create this file.  You can use the `init_oauth_env` script in this package to create it.  It will redirect you to a Yahoo site to authenticate.

You can then use the file in your own code like in the following code snippet:

::

    from yahoo_oauth import OAuth2
    import os
    import json

    # If you did not create the file with init_oauth_env, you need to
    # construct a the minimal file first and then setup through Yahoo.
    if not os.path.exists('oauth2.json'):
        creds = {'consumer_key': 'my_key', 'consumer_secret': 'my_secret'}
        with open(args['<json>'], "w") as f:
            f.write(json.dumps(creds))

    oauth = OAuth2(None, None, from_file='oauth2.json')


You can then pass in `oauth2` when construct the various classes in this package.  See the `documentation <https://yahoo-oauth.readthedocs.io/en/latest/>`_ for `yahoo_oauth` for more information.
