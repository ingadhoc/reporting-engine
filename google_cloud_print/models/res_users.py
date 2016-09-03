# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    google_cloudprint_rtoken = fields.Char(
        'Refresh Token',
        copy=False,
        readonly=True,
    )
    google_cloudprint_authorization_code = fields.Char(
        string='Authorization Code',
    )
    google_cloudprint_uri = fields.Char(
        compute='_compute_cloudprint_uri',
        string='URI',
        help="The URL to generate the authorization code from Google"
    )
    gcprinter_ids = fields.One2many(
        'printing.printer',
        'gc_user_id',
        'My Google Cloud Printers',
    )

    def get_google_cloudprint_scope(self):
        return (
            'https://www.googleapis.com/auth/cloudprint '
            'https://www.googleapis.com/auth/drive.readonly')

    @api.one
    @api.depends('google_cloudprint_authorization_code')
    def _compute_cloudprint_uri(self):
        google_cloudprint_uri = self.env[
            'google.service']._get_google_token_uri(
                'cloudprint',
                scope=self.get_google_cloudprint_scope())
        self.google_cloudprint_uri = google_cloudprint_uri

    @api.one
    @api.constrains('google_cloudprint_authorization_code')
    def set_google_cloudprint_authorization_code(self):
        self.ensure_one()
        # ICP = self.env['ir.config_parameter']
        authorization_code = self.google_cloudprint_authorization_code
        if authorization_code:
            refresh_token = self.env['google.service'].generate_refresh_token(
                'cloudprint', authorization_code)
            self.google_cloudprint_rtoken = refresh_token
        else:
            self.google_cloudprint_rtoken = False

    @api.multi
    def update_user_gc_printers(self):
        for user in self:
            if user.google_cloudprint_rtoken:
                self.env['printing.printer'].update_gc_printers(
                    user=user)
        return {'type': 'ir.actions.act_window.none'}

    @api.multi
    def update_user_gc_printers_status(self):
        for user in self:
            if user.google_cloudprint_rtoken:
                self.env['printing.printer'].update_gc_printers_status(
                    user=user)
        return {'type': 'ir.actions.act_window.none'}
