.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Google Cloud Printer
====================

This module extends the functionality of direct printing. It allows to add your google cloud printers to odoo

IMPORTANT: this module is not adapted yet to oca/report-print-send, for now you need to use the one located on ingadhoc/patches

Installation
============

To install this module, you need to:

#. Just Install the module

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


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.adhoc.com.ar/

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* ADHOC SA: `Icon <http://fotos.subefotos.com/83fed853c1e15a8023b86b2b22d6145bo.png>`_.

Contributors
------------


Maintainer
----------

.. image:: http://fotos.subefotos.com/83fed853c1e15a8023b86b2b22d6145bo.png
   :alt: Odoo Community Association
   :target: https://www.adhoc.com.ar

This module is maintained by the ADHOC SA.

To contribute to this module, please visit https://www.adhoc.com.ar.
