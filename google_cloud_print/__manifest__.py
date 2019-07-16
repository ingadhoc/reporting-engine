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
    "version": '11.0.1.2.1',
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
        'views/printing_printer_view.xml',
        'wizards/res_config_settings_view.xml',
        'data/ir_config_parameter_data.xml',
        'data/printing_server_data.xml',
        'wizards/printing_printer_update_wizard.xml',
        'security/ir.model.access.csv',
        'security/google_cloud_print_security.xml',
    ],
    'installable': False,
}
