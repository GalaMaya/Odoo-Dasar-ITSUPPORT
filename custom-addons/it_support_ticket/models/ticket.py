from odoo import models, fields, api

class ItSupportTicket(models.Model):
    _name = 'it.support.ticket'
    _description = 'Tiket Dukungan IT'
    
    # INI BAGIAN PENTING YANG HARUS ADA:
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Judul Tiket', required=True, tracking=True)
    description = fields.Text(string='Deskripsi Masalah')
    status = fields.Selection([
        ('draft', 'Baru'),
        ('in_progress', 'Sedang Dikerjakan'),
        ('done', 'Selesai')
    ], string='Status', default='draft', required=True, tracking=True)
    
    assigned_to = fields.Many2one('res.users', string='Ditugaskan Kepada', default=lambda self: self.env.user, tracking=True)
    
    date_closed = fields.Datetime(string='Tanggal Selesai', readonly=True)
    duration_hours = fields.Float(string='Durasi (Jam)', compute='_compute_duration_hours', store=True)

    @api.depends('status', 'create_date', 'date_closed')
    def _compute_duration_hours(self):
        for ticket in self:
            if ticket.status == 'done' and ticket.create_date and ticket.date_closed:
                delta = ticket.date_closed - ticket.create_date
                ticket.duration_hours = delta.total_seconds() / 3600.0
            else:
                ticket.duration_hours = 0.0

    def write(self, vals):
        if vals.get('status') == 'done':
            vals['date_closed'] = fields.Datetime.now()
        return super(ItSupportTicket, self).write(vals)
    
    # reopen method to allow reopening a ticket
    def action_reopen(self):
        for ticket in self:
            # ubah data pada databases
            ticket.write({
                'status': 'draft',
                'date_closed': False
            })
            
            # kirim ke log (chatter)
            ticket.message_post(body=f"Tiket dibuka kembali oleh {self.env.user.name}")
        return True