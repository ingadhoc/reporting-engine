from odoo import models, api, _


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    @api.multi
    def payment_print(self):
        self.ensure_one()
        self.sent = True

        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)

        return self.env['ir.actions.report'].get_report(self).report_action(
            self)

    @api.multi
    def action_payment_sent(self):
        """ Open a window to compose an email, with the edi payment template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(
            'report_extended_payment_group.email_template_edi_payment_group',
            False)
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.payment.group',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_payment_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
