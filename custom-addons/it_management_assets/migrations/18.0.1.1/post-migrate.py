"""Migrasi skema it.device dari versi lama ke versi 1.1.

Versi lama model it.device memakai field:
    assigned_to, category, brand
Versi baru memakai field:
    user_id, device_type, specs

Script ini memindahkan data lama ke field baru, lalu menghapus kolom lama
beserta constraint NOT NULL yang sudah tidak dipakai (mis. serial_number
yang sekarang opsional).
"""

import logging

from odoo.tools.sql import column_exists, table_exists

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version or not table_exists(cr, 'it_device'):
        return

    # assigned_to (res.users) -> user_id
    if column_exists(cr, 'it_device', 'assigned_to') and column_exists(cr, 'it_device', 'user_id'):
        cr.execute("""
            UPDATE it_device
               SET user_id = assigned_to
             WHERE user_id IS NULL
               AND assigned_to IS NOT NULL
        """)

    # category -> device_type
    if column_exists(cr, 'it_device', 'category') and column_exists(cr, 'it_device', 'device_type'):
        cr.execute("""
            UPDATE it_device
               SET device_type = CASE category
                       WHEN 'laptop' THEN 'laptop'
                       WHEN 'desktop' THEN 'desktop'
                       WHEN 'printer' THEN 'printer'
                       WHEN 'server' THEN 'server'
                       WHEN 'network_device' THEN 'network'
                       ELSE 'other'
                   END
             WHERE device_type IS NULL
        """)

    # brand -> specs (dipertahankan sebagai keterangan tambahan)
    if column_exists(cr, 'it_device', 'brand') and column_exists(cr, 'it_device', 'specs'):
        cr.execute("""
            UPDATE it_device
               SET specs = CONCAT_WS(E'\n', NULLIF(specs, ''), 'Merek: ' || brand)
             WHERE brand IS NOT NULL
               AND brand <> ''
        """)

    # Status lama -> status baru
    if column_exists(cr, 'it_device', 'status'):
        cr.execute("""
            UPDATE it_device
               SET status = 'active'
             WHERE status IN ('available', 'in_use')
        """)

    # Hapus kolom yang sudah tidak dipakai model
    for column in ('assigned_to', 'brand', 'category'):
        if column_exists(cr, 'it_device', column):
            cr.execute('ALTER TABLE it_device DROP COLUMN "%s" CASCADE' % column)

    # serial_number sekarang opsional
    if column_exists(cr, 'it_device', 'serial_number'):
        cr.execute("ALTER TABLE it_device ALTER COLUMN serial_number DROP NOT NULL")

    # device_type wajib diisi; pasang NOT NULL jika semua baris sudah terisi
    if column_exists(cr, 'it_device', 'device_type'):
        cr.execute("SELECT 1 FROM it_device WHERE device_type IS NULL LIMIT 1")
        if not cr.fetchone():
            cr.execute("ALTER TABLE it_device ALTER COLUMN device_type SET NOT NULL")

    _logger.info("Migrasi it.device ke skema 1.1 selesai.")
