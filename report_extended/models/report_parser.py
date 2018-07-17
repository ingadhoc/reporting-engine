from odoo import models


class ReportAerooAbstract(models.AbstractModel):
    _inherit = 'report.report_aeroo.abstract'

    def myset(self, pair):
        if isinstance(pair, dict):
            self.localcontext['storage'].update(pair)
        return False

    def myget(self, key):
        if key in self.localcontext['storage'] and self.localcontext[
                'storage'][key]:
            return self.localcontext['storage'][key]
        return False

    def _set_lang(self, lang, obj=None):
        self.localcontext.update({
            'myset': self.myset,
            'myget': self.myget,
            'storage': {}
        })
        return super(ReportAerooAbstract, self)._set_lang(lang, obj=obj)
