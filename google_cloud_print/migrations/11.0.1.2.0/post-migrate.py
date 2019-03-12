##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, 'google_cloud_print',
        'migrations/11.0.1.2.0/noupdate_changes.xml',
    )
    global_rule = env.ref(
        'google_cloud_print.cupsprint_rule', raise_if_not_found=False)
    if global_rule:
        global_rule.unlink()
