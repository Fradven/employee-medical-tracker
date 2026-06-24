from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.fields import Date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    last_medical_check_date = fields.Date(string='Last Medical Check')
    medical_check_frequency_months = fields.Integer(
        string='Check Frequency (months)', default=12)
    next_medical_check_date = fields.Date(
        string='Next Medical Check Due', compute='_compute_next_check_date',
        store=True)
    medical_check_status = fields.Selection([
        ('ok', 'Up to date'),
        ('due_soon', 'Due Soon'),
        ('overdue', 'Overdue'),
        ('unknown', 'No Record'),
    ], compute='_compute_medical_check_status', store=True, string='Medical Check Status')

    @api.depends('last_medical_check_date', 'medical_check_frequency_months')
    def _compute_next_check_date(self):
        for emp in self:
            if emp.last_medical_check_date:
                emp.next_medical_check_date = emp.last_medical_check_date + relativedelta(
                    months=emp.medical_check_frequency_months)
            else:
                emp.next_medical_check_date = False

    @api.depends('next_medical_check_date')
    def _compute_medical_check_status(self):
        today = Date.context_today(self)
        for emp in self:
            if not emp.next_medical_check_date:
                emp.medical_check_status = 'unknown'
            elif emp.next_medical_check_date < today:
                emp.medical_check_status = 'overdue'
            elif emp.next_medical_check_date <= today + relativedelta(days=30):
                emp.medical_check_status = 'due_soon'
            else:
                emp.medical_check_status = 'ok'

    def _cron_create_medical_check_activities(self):
        """Scheduled action: create reminder activities for due/overdue checks."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')
        employees = self.search([
            ('medical_check_status', 'in', ['due_soon', 'overdue']),
        ])
        for emp in employees:
            existing = self.env['mail.activity'].search([
                ('res_model', '=', 'hr.employee'),
                ('res_id', '=', emp.id),
                ('activity_type_id', '=', activity_type.id),
            ], limit=1)
            if not existing:
                emp.activity_schedule(
                    activity_type_id=activity_type.id,
                    summary='Medical check due',
                    note=f'Employee {emp.name} medical check is {emp.medical_check_status}.',
                    user_id=emp.parent_id.user_id.id or self.env.uid,
                    date_deadline=emp.next_medical_check_date,
                )