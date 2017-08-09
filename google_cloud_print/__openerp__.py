# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Google Cloud Printer",
    'category': 'Generic Modules/Base',
    'author': 'ADHOC SA',
    'license': 'AGPL-3',
    "depends": [
        'base_report_to_printer',
        'google_account',
        'server_mode',
        # to improove user experience
        # 'web_widget_one2many_tags',
        # 'web_ir_actions_act_window_none',
    ],
    "data": [
        'views/res_users_view.xml',
        'res_config_view.xml',
        'gcp_data.xml',
        'wizard/update_printers.xml',
        'security/ir.model.access.csv',
    ],
    "demo": [],
    "installable": True,
    "version": '9.0.1.0.0',
}
