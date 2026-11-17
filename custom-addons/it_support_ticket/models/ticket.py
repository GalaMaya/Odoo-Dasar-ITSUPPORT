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

    # Tambahkan field ini di antara field lainnya
    device_id = fields.Many2one('it.device', string='Perangkat Terkait', tracking=True)

    @api.depends('status', 'create_date', 'date_closed')
    def _compute_duration_hours(self):
        for ticket in self:
            if ticket.status == 'done' and ticket.create_date and ticket.date_closed:
                delta = ticket.date_closed - ticket.create_date
                # clamp ke 0: jam server web & database bisa berbeda beberapa
                # milidetik sehingga hasilnya bisa negatif untuk tiket instan
                ticket.duration_hours = max(delta.total_seconds() / 3600.0, 0.0)
            else:
                ticket.duration_hours = 0.0

    def write(self, vals):
        if 'status' in vals:
            if vals['status'] == 'done':
                # isi tanggal selesai hanya jika belum dikirim eksplisit
                if 'date_closed' not in vals:
                    vals['date_closed'] = fields.Datetime.now()
            elif 'date_closed' not in vals:
                # status berubah keluar dari 'done' -> bersihkan tanggal selesai
                vals['date_closed'] = False
        return super().write(vals)
    
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
    
    # ==========================================================
    # --- FITUR BARU: OTOMATISASI SAAT PEMBUATAN TIKET ---
    # ==========================================================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Cek apakah field 'name' ada dan mengandung kata "URGENT"
            if vals.get('name') and 'URGENT' in vals['name'].upper():
                vals['status'] = 'in_progress'

            # Pastikan tiket yang langsung dibuat dengan status 'done'
            # tetap punya tanggal selesai (dipakai oleh duration_hours)
            if vals.get('status') == 'done' and not vals.get('date_closed'):
                vals['date_closed'] = fields.Datetime.now()

        # Simpan ke database
        tickets = super(ItSupportTicket, self).create(vals_list)
        
        # Kirim pesan ke Chatter setelah berhasil dibuat
        for ticket in tickets:
            if ticket.status == 'in_progress' and 'URGENT' in ticket.name.upper():
                ticket.message_post(
                    body="TIKET URGENT TERDETEKSI! Status otomatis diubah menjadi Sedang Dikerjakan oleh sistem.",
                    subject="Peringatan Tiket Urgent",
                    message_type='notification'
                )
                
        return tickets