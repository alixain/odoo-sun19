from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    advertiser_id = fields.Many2one('res.partner', string='Advertiser')
    ro_number = fields.Char(string='RO#')
    tc_number = fields.Char(string='TC No.')
    spl_pid_number = fields.Char(string='SPL/PID#')
    advertiser_ntn = fields.Char(string='Advertiser NTN/FTN#', related='advertiser_id.vat', readonly=False, store=True)
    advertiser_gst = fields.Char(string='Advertiser GST#', related='advertiser_id.gst_number', readonly=False, store=True)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    commission_amount = fields.Monetary(string='Commission')

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({
            'commission_amount': self.commission_amount,
        })
        return res

    @api.onchange('advertiser_id')
    def _onchange_advertiser_id(self):
        if self.advertiser_id:
            self.advertiser_ntn = self.advertiser_id.vat # Assuming NTN is stored in vat field or similar
            # If there's a specific field for GST, we should use it. For now, just setting NTN.
