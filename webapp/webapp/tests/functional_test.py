import time
import requests

url_prefix = "http://127.0.0.1:5000"
verify = False
requests.packages.urllib3.disable_warnings()

# https://www.neuralegion.com/blog/ssrf-server-side-request-forgery/
urls_for_verifying_ssrf_safety_minus_private_ip = {
    "https://dzone.com/services/internal/action/dzoneUsers-isUserEmailValidated": 400,
    "169.254.169.254": 400,
    "http://74": 400,
    "https://01111111.00000000.00000000.00000001": 400,
    "https://google.com": 400,
    "file://etc/passwd": 400,
    "file:///etc/passwd": 400,
    "file://\/\/etc/passwd": 400,
    "ftp://apple.com:11211/": 400,
    "sftp://apple.com:11111/": 400,
    "tftp://apple.com:123456/TESTUDP": 400,
    "ldap://127.0.0.1/%0astats%0aquit": 400,
    "ldap://localhost:11211/%0astats%0aquit": 400,
    "gopher://127.0.0.1:25/xHELO%20localhost%250d%250aMAIL%20FROM%3A%attacker@attack.net%3E%250d%250aRCPT%20TO%3A%3Cvictim@target.com%3E%250d%250aDATA%250d%250aFrom%3A%20%5BAttacker%5D%20%3Cattacker@attack.net%3E%250d%250aTo%3A%20%3Cvictime@target.com%3E%250d%250aDate%3A%20Fri%2C%2013%20Mar%202020%2003%3A33%3A00%20-0600%250d%250aSubject%3A%20Hacked%250d%250a%250d%250aYou%27ve%20been%20exploited%20%3A%28%20%21%250d%250a%250d%250a%250d%250a.%250d%250aQUIT%250d%250a": 400,
    "http://192.168.0.0/16": 400,
    "http://172.16.0.0/12": 400,
    "http://10.0.0.0/8": 400,
    "http://169.254.169.254/latest/user-data": 400,
    "http://192.0.0.192/latest/meta-data/": 400,
    "https://localhost/": 400,
    "http://[::]/": 400,
    "http://[::]:80/": 400,
    "http://0000::1/": 400,
    "http://0000::1:80/": 400,
    "http://localtest.me": 400,
    "http://test.app.127.0.0.1.nip.io": 400,
    "http://test-app-127-0-0-1.nip.io": 400,
    "httP://test.app.127.0.0.1.xip.io": 400,
    "http://127.127.127.127/": 400,
    "http://127.0.1.3/": 400,
    "http://[0:0:0:0:0:ffff:127.0.0.1]/": 400,
    "http://0177.0.0.1/": 400,
    "http://2130706433/": 400,
    "http://3232235521/": 400,
    "http://3232235777/": 400,
    "localhost:+11211aaa": 400,
    "localhost:00011211aaaa": 400,
    "localhost:11211": 400,
    "http://0/": 400,
    "http://127.1/": 400,
    "http://127.0.1/": 400,
    "http://①②⑦.⓪.⓪.①/": 400,
    "http://⓵⓶⓻.⓪.⓪.⓵/": 400,
    "http://127.1.1.1:80\@127.2.2.2:80/": 400,
    "http://127.1.1.1:80\@@127.2.2.2:80/": 400,
    "http://169.254.169.254.xip.io/": 400,
    "http://1ynrnhl.xip.io": 400,
    "http://425.510.425.510": 400,
    "http://2852039166": 400,
    "http://7147006462": 400,
    "http://0xA9.0xFE.0xA9.0xFE": 400,
    "http://0xA9FEA9FE": 400,
    "http://0x41414141A9FEA9FE": 400,
    "http://0251.0376.0251.0376": 400,
    "http://0251.00376.000251.0000376": 400,
    "https://127.0.0.1/": 400,
}
urls_for_verifying_ssrf_safety_with_private_ip_addresses = {
    "http://localhost:22/": 400,
    "http://127.0.0.1:3389/": 400,
    "http://localhost": 400,
    "http://127.0.0.1": 400,
}
urls_for_verifying_ssrf_safety_with_private_ip_addresses.update(
    urls_for_verifying_ssrf_safety_minus_private_ip
)


sqli1_urls = {
    f"{url_prefix}/vulnerabilities/sqli1/login/": 200,
    f"{url_prefix}/patches/sqli1/login/": 401,
}
sqli2_urls = [
    [
        [f"{url_prefix}/vulnerabilities/sqli2/get_username/", 200],
        [f"{url_prefix}/vulnerabilities/sqli2/register/", 200],
        [f"{url_prefix}/vulnerabilities/sqli2/change_password/", 200],
    ],
    [
        [f"{url_prefix}/patches/sqli2/get_username/", 200],
        [f"{url_prefix}/patches/sqli2/register/", 200],
        [f"{url_prefix}/patches/sqli2/change_password/", 400],
    ],
]
ssrf1_urls = [
    f"{url_prefix}/vulnerabilities/ssrf1/submit_webhook/",
    f"{url_prefix}/patches/ssrf1/submit_webhook/",
]
# index 0 for vulnerabilities, index 1 for patches
ssrf1_test_urls = [
    dict(urls_for_verifying_ssrf_safety_minus_private_ip),
    dict(urls_for_verifying_ssrf_safety_with_private_ip_addresses),
]
# do not need to add this for the patches urls because it's already included in the other dictionary
ssrf1_test_urls[0]["http://127.0.0.1"] = 202
ssrf1_test_urls[0]["http://localhost"] = 202

ssrf1_test_urls[0]["http://admin_panel/"] = 202
ssrf1_test_urls[1]["http://admin_panel/"] = 400
ssrf1_test_urls[0]["http://admin_panel:8484/"] = 200
ssrf1_test_urls[1]["http://admin_panel:8484/"] = 400
ssrf1_test_urls[0]["http://admin_panel:8484/reset_admin_password/"] = 200
ssrf1_test_urls[1]["http://admin_panel:8484/reset_admin_password/"] = 400


def check_status_code(expected_status_code, actual_status_code, url):
    assert (
        expected_status_code == actual_status_code
    ), f"{url}\nExpected status code: {expected_status_code}\nActual_status_code: {actual_status_code}"


def sqli1():
    username = "administrator"
    password = "' OR 'a' = 'a"
    data = {"username": username, "password": password}

    for url, status_code in sqli1_urls.items():
        r = requests.post(url, data=data, verify=verify)
        check_status_code(status_code, r.status_code, url)


def sqli2():
    original_password = "test"
    new_password = "123456"
    for i in range(2):
        url, status_code = sqli2_urls[i][0][0], sqli2_urls[i][0][1]
        r = requests.get(url, verify=verify)
        check_status_code(status_code, r.status_code, url)
        username = f"{r.text}'-- "
        data = {"username": username, "password": original_password}

        url, status_code = sqli2_urls[i][1][0], sqli2_urls[i][1][1]
        r = requests.post(url, data=data, cookies=r.cookies, verify=verify)
        check_status_code(status_code, r.status_code, url)

        url, status_code = sqli2_urls[i][2][0], sqli2_urls[i][2][1]
        data = {
            "old_password": original_password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        r = requests.post(url, data=data, cookies=r.cookies, verify=verify)
        check_status_code(status_code, r.status_code, url)


def ssrf1():
    for index in range(len(ssrf1_urls)):
        url = ssrf1_urls[index]
        for custom_url, status_code in ssrf1_test_urls[index].items():
            data = {"custom_url": custom_url}
            r = requests.post(url, data=data, verify=verify)
            check_status_code(status_code, r.status_code, custom_url)


start_time = round(time.time() * 1000)
print("Starting functional test...")
sqli1()
sqli2()
ssrf1()
stop_time = round(time.time() * 1000)
run_time = (stop_time - start_time) / 1000
print(f"Finished running functional tests. Run time: {run_time} seconds")
