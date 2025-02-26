import sys
import os
from Credentials import get_admin, get_users
from iUsers import get_usage_time # get_usage_time(username, password)
from PPPoE_checker import pppoe_checker # pppoe_checker(admin_user, admin_pass)
from PPPoE_setter import set_pppoe # set_pppoe(ADMIN_USER, ADMIN_PASS, username, pass)

# Check if status flag is passed
status_mode = "s" in sys.argv

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# DB_FILE = os.path.join(script_dir, "test.db")
# usage_limit=9000
DB_FILE = os.path.join(script_dir, "credentials.db")
usage_limit=500

# Fetch data
users = get_users(DB_FILE)
admin = get_admin(DB_FILE)


if status_mode:
    for user in users:
        username = user['username']
        user['usage'] = get_usage_time(username, user['password'])
        print(f"{username}: {user['usage']}")

    print("Current PPPoE ID =>", pppoe_checker(admin['username'], admin['password']))

    exit(0)  # Exit after printing the status

# Current ID in use
current_user = pppoe_checker(admin['username'], admin['password'])
print("Current PPPoE ID =>", current_user)

# Fetch usage and eligibility
for user in users:
    username = user['username']
    password = user['password']
    user['usage'] = get_usage_time(username, password)
    user['eligibility'] = user['usage'] < usage_limit

    if(username==current_user and user['eligibility']==True):
        print("Current ID can be used further")
        exit(0)

# # Print results
# print("Users:")
# for user in users:
#     print(f"Username: {user['username']}, Password: {user['password']}, Usage: {user['usage']}, Applicable: {user['eligibility']}")
#
# print("\nAdmin:")
# print(f"Username: {admin["username"]}, Password: {admin["password"]}")

# Assign new ID
for user in users:
    if(user['eligibility'] == True):
        print("Applying ID:", user['username'])
        reply=set_pppoe(admin['username'], admin['password'], user['username'], user['password'])
        print(reply)

