##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    move_internal_notes = fields.Boolean(
        'Mover notas internas a transferencias de stock y facturas',
    )
    move_note = fields.Boolean(
        'Mover términos y condiciones a transferencias de stock y facturas',
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(move_internal_notes=get_param(
            'sale.propagate_internal_notes') == 'True')
        res.update(move_note=get_param('sale.propagate_note') == 'True')
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('sale.propagate_internal_notes',
                  repr(self.move_internal_notes))
        set_param('sale.propagate_note', repr(self.move_note))
