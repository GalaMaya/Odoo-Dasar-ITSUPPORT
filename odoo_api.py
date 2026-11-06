import xmlrpc.client

url = "http://localhost:8069"
db = "odoo-tutorial"

# credencial login odoo
username = "galuhprahadi04@gmail.com"
password = "Galamayastudio!"

print("connecting odoo server...")
print("================================")


# authenticate
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Authenticate failed")
else:
    print("Authenticate success, uid: {}".format(uid))

    # connect model
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # create new ticket
    print("Creating new ticket...")
    ticket_id = models.execute_kw(db, uid, password, 'it.support.ticket', 'create', [{
        'name': "URGENT Server Down",
        'description': "The main server is down and needs immediate attention.",
        'status': "draft",
    }])
    
    print("New ticket created with ID: {}".format(ticket_id))
    print("================================")
    
    # fetch details of ticket
    print("fetching ticket details...")
    tickets = models.execute_kw(db, uid, password, 'it.support.ticket', 'search_read', 
    [[('id', '=', ticket_id)]], {'fields': ['name', 'description', 'status', 'duration_hours']})
    
    
    # print ticket details
    for ticket in tickets:
        print("Ticket ID: {}".format(ticket['id']))
        print("Name: {}".format(ticket['name']))
        print("Description: {}".format(ticket['description']))
        print("Status: {}".format(ticket['status']))
        print("Duration Hours: {}".format(ticket['duration_hours']))
    
    print("================================")