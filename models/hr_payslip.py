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
        """Ensure an ATTN input line exists on the payslip with count from attendance"""
        for payslip in self:
            # Calculate unique days of attendance
            attendance_domain = [
                ('employee_id', '=', payslip.employee_id.id),
                ('check_in', '>=', payslip.date_from),
                ('check_in', '<=', payslip.date_to),
            ]
            attendances = self.env['hr.attendance'].search(attendance_domain)
            # Use a set to count unique days (dates only)
            unique_days = {a.check_in.date() for a in attendances if a.check_in}
            worked_days = float(len(unique_days))
            
            # Check if ATTN input already exists
            attn_input = payslip.input_line_ids.filtered(lambda x: x.code == 'ATTN')
            if not attn_input:
                # Create the input line directly with attendance count
                self.env['hr.payslip.input'].create({
                    'payslip_id': payslip.id,
                    'contract_id': payslip.contract_id.id,
                    'code': 'ATTN',
                    'name': 'Attendance/Worked Days (ATTN)',
                    'amount': worked_days,
                })
            else:
                # Update existing one (synced with current attendance)
                attn_input.write({'amount': worked_days})

    def compute_sheet(self):
        self._ensure_attn_input()
        return super(HrPayslip, self).compute_sheet()
