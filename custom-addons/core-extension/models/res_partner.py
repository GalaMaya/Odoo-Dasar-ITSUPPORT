from odoo import models, fields

class ResPartner(models.Model):
    
    # modifikasi dari model res.partner bawaan Odoo
    _inherit = 'res.partner'
    
    # menambahkan field baru untuk catatan internal
    x_internal_notes = fields.Text(string="Internal Notes", help="Catatan internal untuk partner ini.")
    
    x_is_vip_customer = fields.Boolean(string="Is VIP Customer", default=False, tracking=True)
    