##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    @api.model
    def _default_google_cloudprint_authorization_code(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'google_cloudprint_authorization_code')

    google_cloudprint_authorization_code = fields.Char(
        string='Authorization Code',
        default=_default_google_cloudprint_authorization_code,
    )
    google_cloudprint_uri = fields.Char(
        compute='_compute_cloudprint_uri',
        string='URI',
        help="The URL to generate the authorization code from Google",
    )

    def get_google_cloudprint_scope(self):
        return (
            'https://www.googleapis.com/auth/cloudprint '
            'https://www.googleapis.com/auth/drive.readonly')

    @api.depends('google_cloudprint_authorization_code')
    def _compute_cloudprint_uri(self):
        google_cloudprint_uri = self.env[
            'google.service']._get_google_token_uri(
                'cloudprint',
                scope=self.get_google_cloudprint_scope())
        for config in self:
            config.google_cloudprint_uri = google_cloudprint_uri

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        authorization_code = self.google_cloudprint_authorization_code
        if authorization_code and authorization_code != ICP.get_param(
                'google_cloudprint_authorization_code'):
            refresh_token = self.env['google.service'].generate_refresh_token(
                'cloudprint', authorization_code)
            ICP.set_param(
                'google_cloudprint_refresh_token',
                refresh_token)
        ICP.set_param(
            'google_cloudprint_authorization_code',
            authorization_code)
