import requests, re, time

def set_pppoe(admin_user, admin_pass, username, password):
    router_url = "http://cudy.net/cgi-bin/luci"
    config_url = f"{router_url}/admin/network/wan/config/pppoe?embedded="
    token_url = f"{router_url}/admin/network/wan/config/static?embedded="
    status_url = f"{router_url}/admin/network/ifstatus/wan?proto=pppoe"

    # Login using router admin credentials
    admin_creds = {
        "luci_language": "en",
        "luci_username": admin_user,
        "luci_password": admin_pass
    }
    s = requests.Session()
    s.post(router_url, data=admin_creds)

    # Retrieve CSRF token from token_url
    r = s.get(token_url)
    m = re.search(r'name="token" value="([^"]+)"', r.text)
    if not m:
        raise Exception("CSRF token not found")
    token = m.group(1)

    # Use current timestamp as timeclock
    payload = {
        "token": token,
        "timeclock": str(int(time.time())),
        "cbi.submit": "1",
        "cbid.network.wan.username": username,
        "cbid.network.wan.password": password,
        "cbi.apply": ""
    }
    s.post(config_url, data=payload)
    time.sleep(1)

    # Get and return PPPoE status (key and class)
    status = s.get(status_url).json()
    key = status.get("key")
    cls = status.get("class")
    print("Key:", key)
    print("Class:", cls)
    return key, cls
