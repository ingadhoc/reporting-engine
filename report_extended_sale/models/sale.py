# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    internal_notes = fields.Text('Internal Notes')

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)

        report_name = self.env['ir.actions.report.xml'].get_report_name(
            self._name, self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.multi
    def _prepare_invoice(self):
        vals = super(sale_order, self)._prepare_invoice()
        if self.company_id.internal_notes:
            vals.update({
                'internal_notes': self.internal_notes})
        if 'comment' in vals and not self.company_id.external_notes:
            vals.pop('comment')
        return vals
