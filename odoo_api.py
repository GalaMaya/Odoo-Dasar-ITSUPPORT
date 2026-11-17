"""Contoh integrasi Odoo lewat XML-RPC.

Kredensial diambil dari environment variable agar password tidak
tersimpan di dalam repository:

    set ODOO_URL=http://localhost:8069
    set ODOO_DB=odoo-tutorial
    set ODOO_USER=admin
    set ODOO_PASSWORD=admin

Jalankan dengan: python odoo_api.py
"""

import os
import sys
import xmlrpc.client

url = os.environ.get("ODOO_URL", "http://localhost:8069")
db = os.environ.get("ODOO_DB", "odoo-tutorial")
username = os.environ.get("ODOO_USER", "admin")
password = os.environ.get("ODOO_PASSWORD", "admin")

print("connecting odoo server...")
print("================================")

# authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Authenticate failed, periksa ODOO_DB / ODOO_USER / ODOO_PASSWORD")
    sys.exit(1)

print(f"Authenticate success, uid: {uid}")

# connect model
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# create new ticket
print("Creating new ticket...")
ticket_id = models.execute_kw(db, uid, password, "it.support.ticket", "create", [{
    "name": "URGENT Server Down",
    "description": "The main server is down and needs immediate attention.",
    "status": "draft",
}])

print(f"New ticket created with ID: {ticket_id}")
print("================================")

# fetch details of ticket
print("fetching ticket details...")
tickets = models.execute_kw(
    db, uid, password, "it.support.ticket", "search_read",
    [[("id", "=", ticket_id)]],
    {"fields": ["id", "name", "description", "status", "duration_hours"]},
)

# print ticket details
for ticket in tickets:
    print(f"Ticket ID: {ticket['id']}")
    print(f"Name: {ticket['name']}")
    print(f"Description: {ticket['description']}")
    print(f"Status: {ticket['status']}")
    print(f"Duration Hours: {ticket['duration_hours']}")

print("================================")
