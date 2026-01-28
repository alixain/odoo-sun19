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
        for payslip in self:
            if not payslip.input_line_ids.filtered(lambda x: x.code == 'ATTN'):
                # Search for the input type with code 'ATTN' first
                input_type = self.env['hr.payslip.input.type'].search([('code', '=', 'ATTN')], limit=1)
                if not input_type:
                    # Create input type if it doesn't exist
                    input_type = self.env['hr.payslip.input.type'].create({
                        'name': 'Attendance/Worked Days (ATTN)',
                        'code': 'ATTN',
                    })
                
                self.env['hr.payslip.input'].create({
                    'payslip_id': payslip.id,
                    'input_type_id': input_type.id,
                    'amount': 0.0,
                })

    def compute_sheet(self):
        self._ensure_attn_input()
        return super(HrPayslip, self).compute_sheet()
