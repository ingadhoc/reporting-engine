##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ConfigurationDefault(models.Model):
    _name = 'report.configuration.default'
    _description = 'Default Keys For Reports'

    name = fields.Char(
        'Key',
        required=True,
    )
    apply_to_all = fields.Boolean(
        string='Apply To All Models',
        default=True,
    )
    apply_to_model_id = fields.Many2one(
        'ir.model',
        string='Apply To Model',
        required=False,
    )
    override_values = fields.Boolean(
        'Override Values',
        help='If true, override values in already created Aeroo Report '
        'Configuration when saved.'
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
    )
