import requests, re

def pppoe_checker(admin_user, admin_pass):
    router_url = "http://cudy.net/cgi-bin/luci"
    config_url = f"{router_url}/admin/network/wan/config/pppoe?embedded="

    s = requests.Session()
    s.post(router_url, data={
        "luci_language": "en",
        "luci_username": admin_user,
        "luci_password": admin_pass
    })

    html = s.get(config_url).text

    pppoe_username = re.search(r'name="cbid\.network\.wan\.username"[^>]*value="([^"]+)"', html)
    # pppoe_password = re.search(r'name="cbid\.network\.wan\.password"[^>]*value="([^"]+)"', html)

    pppoe_username = pppoe_username.group(1) if pppoe_username else None
    # pppoe_password = pppoe_password.group(1) if pppoe_password else None

    # return pppoe_username, pppoe_password
    return pppoe_username
