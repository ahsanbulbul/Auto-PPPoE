import sys
import os
from Credentials import get_admin, get_users
from iUsers import get_usage_time
from PPPoE_checker import pppoe_checker
from PPPoE_setter import set_pppoe

# Constants
USAGE_SOFT_LIMIT = 9000

def get_user_usage(user):
    """Get usage for a user and add to user dict."""
    username = user['username']
    password = user['password']
    user['usage'] = get_usage_time(username, password)
    user['eligibility'] = user['usage'] < USAGE_SOFT_LIMIT
    return user

def display_status(users, admin):
    """Display status for all users and current PPPoE ID."""
    for user in users:
        get_user_usage(user)
        print(f"{user['username']}: {user['usage']}")
    
    print("Current PPPoE ID =>", pppoe_checker(admin['username'], admin['password']))

def find_and_set_eligible_user(users, admin, current_user):
    """Find eligible user and set PPPoE if necessary."""
    # Check if current user is still eligible
    for user in users:
        if user['username'] == current_user and user['eligibility']:
            print("Current ID can be used further")
            return True
    
    # Find and set first eligible user
    for user in users:
        if user['eligibility']:
            print("Applying ID:", user['username'])
            reply = set_pppoe(admin['username'], admin['password'], user['username'], user['password'])
            print(reply)
            return True
    
    print("No eligible users found")
    return False

def main():

    # Get script directory and DB file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, "credentials.db")
    
    # Fetch data
    users = get_users(db_file)
    admin = get_admin(db_file)
    
    # Handle status mode
    status_mode = "s" in sys.argv
    if status_mode:
        display_status(users, admin)
        return
    
    # Get current user
    current_user = pppoe_checker(admin['username'], admin['password'])
    print("Current PPPoE ID =>", current_user)
    
    # Process all users
    for user in users:
        get_user_usage(user)
    
    # Find and set eligible user if needed
    find_and_set_eligible_user(users, admin, current_user)

if __name__ == "__main__":
    main()