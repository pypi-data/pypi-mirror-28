Instabrowser
============

|Build Status| |PyPI| |Code Climate|

| 💻 Library for instagram.com automation.
| ♥️ Like instagram feed, username profile, location, tag.
| 📊 Get statistic of any public account.

Requirements
------------

-  Pyhton 2.7/3
-  `ChromeDriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__
   for headless web-surfing

Examples
--------

-  Example of using package for getting account statistic:

   .. code:: python

       from insta_browser import InstaMeter   
       im = InstaMeter(username='al_kricha')   
       im.analyze_profile()   
       im.print_account_statistic()
       im.print_top_liked()   

-  Example of using package for liking specific user:

   .. code:: python

       import os
       from insta_browser import browser

       br = browser.Browser(
           debug=True,cookie_path=os.path.join('var', 'cookies'),
           log_path=os.path.join('var', 'logs'),
           db_path=os.path.join('var', 'db'),
           exclude=os.path.join('var', 'exclude.txt')
       )

       try:
           br.auth('YOUR_INSTA_LOGIN', 'YOUR_INSTA_PASSWORD')
           br.process_user('al_kricha')
           print(br.get_summary())
       finally:
           br.close_all()

Other examples can be seen in my repository:
`insta_bot <https://github.com/aLkRicha/insta_bot>`__

.. |Build Status| image:: https://travis-ci.org/aLkRicha/insta_browser.svg?branch=master
   :target: https://travis-ci.org/aLkRicha/insta_browser
.. |PyPI| image:: https://img.shields.io/pypi/v/insta_browser.svg
   :target: https://pypi.org/pypi/insta_browser
.. |Code Climate| image:: https://img.shields.io/codeclimate/github/aLkRicha/insta_browser.svg
   :target: https://codeclimate.com/github/aLkRicha/insta_browser
