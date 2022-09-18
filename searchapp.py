# We could have done all this work in django as well.
# 1. Load all the files trough management command into model
# 2. model structure will be like 1:1 (user:organizatio) and 1:M (user:tickets)
# 3. We could simply use the djano ORM to search the related field e.g; users.objects.filter(_id=val) and through this method we could get the organization info as well e.g; user.organization.name (using related field)


import json


def get_json_file_data(file_path):
    try:
        with open(file_path, 'r') as f_in:
            return json.load(f_in)
    except:
        raise Exception('file currupted')


def print_user_info(user, org, tickets):
    for key in user.keys():
        print(key.ljust(50 ,' '), user[key])

    print('organization_name'.ljust(50, ' '), org) if org else None

    for i, ticket in enumerate(tickets):
        print('ticket_{}'.format(i).ljust(50, ' '), ticket)


def search_users(users, orgs, tickets, term, val):
    user = [u for u in users if str(u.get(term) or '') == val]
    user = user[0] if user else None
    if not user:
        print('\n\t\tNo User Found!\n')
        return

    user_org = [org['name'] for org in orgs if org['_id'] == user['organization_id']]
    user_org = user_org[0] if user_org else ''
    user_tickets = [t['subject'] for t in tickets if t['submitter_id'] == user['_id']]

    print_user_info(user, user_org, user_tickets)


def print_organization(org):
    for key in org.keys():
        print(key.ljust(50 ,' '), org[key])


def search_organizations(orgs, term, val):
    org = [org for org in orgs if str(org.get(term) or '') == val]
    org = org[0] if org else None
    if not org:
        print('\nNo Organization Found!\n')
        return

    print_organization(org)


def print_ticket(ticket):
    for key in ticket.keys():
        print(key.ljust(50 ,' '), ticket[key])


def search_tickets(tickets, term, val):
    ticket = [ticket for ticket in tickets if str(ticket.get(term) or '') == val]
    ticket = ticket[0] if ticket else None
    if not ticket:
        print('\nNo Tickets Found!\n')
        return

    print_organization(ticket)


def start_search(users, orgs, tickets):
    user_input = input('Select 1) Users or 2) Organizations 3) Tickets\nPress any key to return\n')
    if user_input not in ['1', '2', '3']:
        return

    user_term = input('Enter search term: ')
    user_value = input('Enter search value: ')
    if user_input == '1':
        search_users(users, orgs, tickets, user_term, user_value)
    elif user_input == '2':
        search_organizations(orgs, user_term, user_value)
    elif user_input == '3':
        search_tickets(tickets, user_term, user_value)


if __name__ == '__main__':
    users = get_json_file_data('./users.json')
    organizations = get_json_file_data('./organizations.json')
    tickets = get_json_file_data('./tickets.json')

    print("\t\tWelcome to Custom Search!")
    running = True
    while running:
        print('\n\t\tSelect search option:\n')
        print('\t\t* Press 1 to search')
        print('\t\t* Press 2 to view a list of searchable fields')
        print('\t\t* Press q to quit')
        user_input = input()

        if user_input == '1':
            start_search(users, organizations, tickets)
        elif user_input == '2':
            print('----------------------------------------------------')
            print('Search Users with:')
            print('\n'.join(users[0].keys()) if users else 'No Users Found!', '\n')
            print('----------------------------------------------------')
            print('Search Organizations with:')
            print('\n'.join(organizations[0].keys()) if organizations else 'No Organizations Found!', '\n')
            print('----------------------------------------------------')
            print('Search Tickets with:')
            print('\n'.join(tickets[0].keys()) if tickets else 'No Tickets Found!', '\n')
        elif user_input == 'q':
            running = False