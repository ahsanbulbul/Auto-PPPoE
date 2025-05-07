import sys
import os
from Credentials import get_admin, get_users
from iUsers import get_usage_time
from PPPoE_checker import pppoe_checker
from PPPoE_setter import set_pppoe

# Constants
USAGE_SOFT_LIMIT = 9000
USAGE_HARD_LIMIT = 11500
USAGE_SYSTEM_LIMIT = 12000
FALLBACK_USERNAME = "WildEdgeCase"
FALLBACK_PASSWORD = ":)"

def get_user_usage(user):
    """Get usage for a user and add to user dict."""
    username = user['username']
    password = user['password']
    user['usage'] = get_usage_time(username, password)
    user['under_soft_limit'] = user['usage'] < USAGE_SOFT_LIMIT
    user['under_hard_limit'] = user['usage'] < USAGE_HARD_LIMIT
    return user

def display_status(users, admin):
    """Display status for all users and current PPPoE ID."""
    for user in users:
        get_user_usage(user)
        if user['under_soft_limit']:
            status = "OK"
        elif user['usage'] >= USAGE_SYSTEM_LIMIT:
            status = "OVER"
        elif user['under_hard_limit']:
            status = "WARN"
        else:
            status = "OVER"
        print(f"{user['username']}\t{user['usage']}\t{status}")
    
    print("Current PPPoE ID =>", pppoe_checker(admin['username'], admin['password']))

def find_and_set_eligible_user(users, admin, current_user):
    """Find eligible user and set PPPoE if necessary using the three-tier strategy."""
    # Check if current user is still under soft limit
    for user in users:
        if user['username'] == current_user and user['under_soft_limit']:
            print("Current ID can be used further (under soft limit)")
            return True
    
    # Try to find a user under soft limit
    for user in users:
        if user['under_soft_limit']:
            print("Applying ID (under soft limit):", user['username'])
            reply = set_pppoe(admin['username'], admin['password'], user['username'], user['password'])
            print(reply)
            return True
    
    # Check if current user is under hard limit
    for user in users:
        if user['username'] == current_user and user['under_hard_limit']:
            print("Current ID can be used further (under hard limit)")
            return True
    
    # Try to find a user under hard limit
    for user in users:
        if user['under_hard_limit']:
            print("Applying ID (under hard limit):", user['username'])
            reply = set_pppoe(admin['username'], admin['password'], user['username'], user['password'])
            print(reply)
            return True
    
    # All users are over hard limit, set to fallback settings
    print("All accounts over usage limits! Fallback Setting.")
    reply = set_pppoe(admin['username'], admin['password'], FALLBACK_USERNAME, FALLBACK_PASSWORD)
    print(reply)
    return True

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