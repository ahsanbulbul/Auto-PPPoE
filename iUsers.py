import requests
import re

def get_usage_time(username, password):
    MAX=9999999
    login_url = "http://10.220.20.12/index.php/home/loginProcess"
    dashboard_url = "http://10.220.20.12/index.php/home/dashboard"

    # Start a session to handle cookies
    session = requests.Session()

    # Log in, maintain session
    payload = {"username": username, "password": password}
    session.post(login_url, data=payload)

    # Fetch dashboard
    response = session.get(dashboard_url)
    html_content = response.text

    # Extract Free Limit and Total Use
    # free_limit_match = re.search(r"Free Limit:\s*</td>\s*<td.*?>(\d+)</td>", html_content, re.DOTALL)
    total_use_match = re.search(r"Total Use:\s*</td>\s*<td.*?>(\d+)\s*Minute", html_content, re.DOTALL)

    # free_limit = free_limit_match.group(1) if free_limit_match else MAX
    total_use = int(total_use_match.group(1)) if total_use_match else MAX

    return total_use
