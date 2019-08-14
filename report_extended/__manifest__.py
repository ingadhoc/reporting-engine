##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
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
    'name': 'Report Extended',
    'version': '12.0.1.0.0',
    'category': 'Reporting Subsystem',
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base',
        # there isn't a method that we can use for any reporting engine
        # so we need to update data dict for aeroo specificaclly
        'report_aeroo',
    ],
    'data': [
        'views/company_view.xml',
        'views/ir_actions_report_views.xml',
        'views/report_configuration_default_views.xml',
        'views/report_configuration_line_views.xml',
        'security/report_extended_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
