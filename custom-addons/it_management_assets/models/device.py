from odoo import models, fields

class ItDevice(models.Model):
    _name = 'it.device'
    _description = 'Perangkat IT'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Device', required=True, tracking=True)
    device_type = fields.Selection([
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('printer', 'Printer'),
        ('server', 'Server'),
        ('network', 'Network Device'),
        ('other', 'Other')
    ], string='Tipe Device', required=True, tracking=True)
    
    serial_number = fields.Char(string='Serial Number / Asset Tag', tracking=True)
    user_id = fields.Many2one('res.users', string='Pengguna', tracking=True)
    location = fields.Char(string='Lokasi')
    
    status = fields.Selection([
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired')
    ], string='Status', default='active', tracking=True)
    
    specs = fields.Text(string='Spesifikasi')
    purchase_date = fields.Date(string='Tanggal Pembelian')
    warranty_date = fields.Date(string='Garansi Sampai')