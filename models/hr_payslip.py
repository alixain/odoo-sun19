from odoo import models, fields, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # Custom columns removed as requested, using 'Other Inputs' instead.

    @api.model
    def create(self, vals):
        res = super(HrPayslip, self).create(vals)
        res._ensure_attn_input()
        return res

    def _ensure_attn_input(self):
        """Ensure an ATTN input line exists on the payslip"""
        for payslip in self:
            # Check if ATTN input already exists
            if not payslip.input_line_ids.filtered(lambda x: x.code == 'ATTN'):
                # Create the input line directly
                self.env['hr.payslip.input'].create({
                    'payslip_id': payslip.id,
                    'code': 'ATTN',
                    'name': 'Attendance/Worked Days (ATTN)',
                    'amount': 0.0,
                })

    def compute_sheet(self):
        self._ensure_attn_input()
        return super(HrPayslip, self).compute_sheet()
