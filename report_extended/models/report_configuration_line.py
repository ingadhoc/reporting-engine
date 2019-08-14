##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ReportConfigurationLine(models.Model):
    _name = 'report.configuration.line'
    _description = 'Line of the configuration information'

    name = fields.Char(
        'Key',
        required=True
    )
    value_type = fields.Selection(
        [('text', 'Text'), ('boolean', 'Boolean')],
        'Value Type',
        required=True,
    )
    value_text = fields.Text(
        'Value (Text)',
        required=False,
    )
    value_boolean = fields.Boolean(
        'Value (Yes/No)',
        required=False,
    )
    report_id = fields.Many2one(
        'ir.actions.report',
        'Report',
        required=True,
        ondelete='cascade',
    )
