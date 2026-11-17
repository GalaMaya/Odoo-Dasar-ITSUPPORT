from odoo import models, fields, api


class ItDevice(models.Model):
    _inherit = 'it.device'

    ticket_ids = fields.One2many('it.support.ticket', 'device_id', string='Riwayat Tiket')
    ticket_count = fields.Integer(compute='_compute_ticket_count', string='Jumlah Tiket')

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for device in self:
            device.ticket_count = len(device.ticket_ids)

    def action_view_tickets(self):
        """Action to view tickets related to this device"""
        self.ensure_one()
        return {
            'name': f'Riwayat Tiket untuk {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'it.support.ticket',
            'view_mode': 'list,form',
            'domain': [('device_id', '=', self.id)],
            'context': {'default_device_id': self.id},
        }
