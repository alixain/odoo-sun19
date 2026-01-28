from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    gst_number = fields.Char(string='GST#')

class AccountMove(models.Model):
    _inherit = 'account.move'

    advertiser_id = fields.Many2one('res.partner', string='Advertiser')
    ro_number = fields.Char(string='RO#')
    tc_number = fields.Char(string='TC No.')
    spl_pid_number = fields.Char(string='SPL/PID#')
    advertiser_ntn = fields.Char(string='Advertiser NTN/FTN#', related='advertiser_id.vat', readonly=False, store=True)
    advertiser_gst = fields.Char(string='Advertiser GST#', related='advertiser_id.gst_number', readonly=False, store=True)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    commission_amount = fields.Monetary(string='Commission')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'advertiser_id': self.advertiser_id.id,
            'ro_number': self.ro_number,
            'tc_number': self.tc_number,
            'spl_pid_number': self.spl_pid_number,
            'advertiser_ntn': self.advertiser_ntn,
            'advertiser_gst': self.advertiser_gst,
        })
        return res
