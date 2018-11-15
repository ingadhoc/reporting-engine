.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================
Google Cloud Printer
====================

This module extends the functionality of direct printing. It allows to add your google cloud printers to odoo

Installation
============

To install this module, you need to:

#. Only need to install the module

Configuration
=============

To configure this module, you need to:

#. Link your Google Cloud Print (GCP) account. You can do this generically or by user:

    #. generically:

        #. Go to Settings > Configuration > General Settings
        #. Under Google Cloud Print follow "Generate Google Authorization Code"
        #. Authorize odoo to connect with your GCP account

    #. by user:

        #. Go to Settings > Users > Users, choose a user
        #. Under Google Cloud Print tab follow "Generate Google Authorization Code"

#. Add printes to your GCP account (https://www.google.com/cloudprint)
#. Sync printers to odoo on Settings > Printing > Update Printers
#. Configure your Direct Print options (for more information check  base_report_to_printer module)

Usage
=====

NOTE: Jobs and Trays are not implemented yet to be syncronized with Google Cloud Printer, in order this we hide this information for this type of printers.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: http://runbot.adhoc.com.ar/

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/reporting-engine/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* |company| |icon|

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by the |company|.

To contribute to this module, please visit https://www.adhoc.com.ar.
