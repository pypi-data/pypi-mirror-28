trytond_account_payment_beanstream
==================================

The account_payment_beanstream module of the Tryton application platform.

This module adds a payment processing method to account_payment for processing
payment transactions through BeanStream's gateway using client-side interface.
This module does NOT collect any payment card information; that is done by the
user's web browser and sent driectly to BeanStream's system, which responds
with a single-use token.  That token is used by this module to process the
pending transaction to determine if it is approved, declined or failed.

Installing
----------

See INSTALL

Support
-------

If you encounter any problems with Tryton, please don't hesitate to ask
questions on the Tryton bug tracker, mailing list, wiki or IRC channel:

  http://bugs.tryton.org/
  http://groups.tryton.org/
  http://wiki.tryton.org/
  irc://irc.freenode.net/tryton

If you need support specific to this module contact
Coalesco Digital Systems:

  https://src.coalesco.ca/tryton/modules/cds_trytond_account_payment_beanstream

License
-------

See LICENSE

Copyright
---------

See COPYRIGHT


For more information about Tryton please visit the Tryton web site:

  http://www.tryton.org/


