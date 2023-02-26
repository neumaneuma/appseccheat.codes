import json
import time
import requests

url_prefix = "http://127.0.0.1:12300"
verify = False
requests.packages.urllib3.disable_warnings()


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
ssrf2_urls = [
    f"{url_prefix}/vulnerabilities/ssrf2/submit_api_url/",
    f"{url_prefix}/patches/ssrf2/submit_api_url/",
]


urls_for_verifying_ssrf_safety = {}
with open("ssrf_test_urls.json") as test_urls:
    urls_for_verifying_ssrf_safety = json.load(test_urls)

# index 0 for vulnerabilities, index 1 for patches
ssrf1_test_urls = [
    dict(urls_for_verifying_ssrf_safety),
    dict(urls_for_verifying_ssrf_safety),
]
ssrf2_test_urls = [
    dict(urls_for_verifying_ssrf_safety),
    dict(urls_for_verifying_ssrf_safety),
]

# def convert_to_hex_representation(s):
#     hex_repr = ""
#     for c in s:
#         hex_repr += hex(ord(c)).replace("0x", "%")
#
#     return hex_repr
#
#
# def double_url_enc(s):
#     hex_repr = ""
#     for c in s:
#         hex_repr += "%25"
#         hex_repr += hex(ord(c)).replace("0x", "")
#
#     return hex_repr
#
# print(convert_to_hex_representation("127.0.0.1"))
# print(convert_to_hex_representation("localhost"))
# print(convert_to_hex_representation("169.254.169.254"))
# print(convert_to_hex_representation("ssh"))
# print(double_url_enc("127.0.0.1"))
# print(double_url_enc("localhost"))
# print(double_url_enc("169.254.169.254"))
# print(double_url_enc("ssh"))


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
    # do not need to add this for the patches urls because it's already included
    ssrf1_test_urls[0]["http://127.0.0.1"] = 202
    ssrf1_test_urls[0]["http://127.0.0.1:3389/"] = 202
    ssrf1_test_urls[0]["http://localhost"] = 202
    ssrf1_test_urls[0]["http://localhost:22/"] = 202

    ssrf1_test_urls[0]["http://internal_api/"] = 202
    ssrf1_test_urls[1]["http://internal_api/"] = 400
    ssrf1_test_urls[0]["http://internal_api:12301/"] = 200
    ssrf1_test_urls[1]["http://internal_api:12301/"] = 400
    ssrf1_test_urls[0]["http://internal_api:12301/reset_admin_password/"] = 200
    ssrf1_test_urls[1]["http://internal_api:12301/reset_admin_password/"] = 400
    ssrf1_test_urls[0]["http://127.0.0.1:12302/permanent/"] = 202
    ssrf1_test_urls[1]["http://127.0.0.1:12302/permanent/"] = 400
    ssrf1_test_urls[0]["http://127.0.0.1:12302/temporary/"] = 202
    ssrf1_test_urls[1]["http://127.0.0.1:12302/temporary/"] = 400

    for index in range(len(ssrf1_urls)):
        url = ssrf1_urls[index]
        for custom_url, status_code in ssrf1_test_urls[index].items():
            data = {"custom_url": custom_url}
            r = requests.post(url, data=data, verify=verify)
            check_status_code(status_code, r.status_code,
                              f"{url}({custom_url})")


def ssrf2():
    # do not need to add this for the patches urls because it's already included
    ssrf2_test_urls[0]["file:///etc/passwd"] = 200
    ssrf2_test_urls[0]["file:///etc/shadow"] = 200
    ssrf2_test_urls[0]["file://etc/passwd"] = 202
    ssrf2_test_urls[0]["file://etc/shadow"] = 202
    ssrf2_test_urls[0]["file://\\/\\/etc/passwd"] = 202
    ssrf2_test_urls[0]["file://\\/\\/etc/shadow"] = 202

    ssrf1_test_urls[0]["http://internal_api/"] = 400
    ssrf1_test_urls[1]["http://internal_api/"] = 400
    ssrf1_test_urls[0]["http://internal_api:12301/"] = 200
    ssrf1_test_urls[1]["http://internal_api:12301/"] = 200
    ssrf2_test_urls[0]["http://internal_api:12301/get_cat_coin_price_v1/"] = 200
    ssrf2_test_urls[1]["http://internal_api:12301/get_cat_coin_price_v1/"] = 200
    ssrf2_test_urls[0]["http://internal_api:12301/get_cat_coin_price_v2/"] = 200
    ssrf2_test_urls[1]["http://internal_api:12301/get_cat_coin_price_v2/"] = 200
    ssrf2_test_urls[0]["http://127.0.0.1:12302/permanent/"] = 400
    ssrf2_test_urls[1]["http://127.0.0.1:12302/permanent/"] = 400
    ssrf2_test_urls[0]["http://127.0.0.1:12302/temporary/"] = 400
    ssrf2_test_urls[1]["http://127.0.0.1:12302/temporary/"] = 400

    for index in range(len(ssrf2_urls)):
        url = ssrf2_urls[index]
        for custom_url, status_code in ssrf2_test_urls[index].items():
            data = {"custom_url": custom_url}
            r = requests.post(url, data=data, verify=verify)
            check_status_code(status_code, r.status_code,
                              f"{url}({custom_url})")


start_time = round(time.time() * 1000)
print("Starting functional test...")
sqli1()
sqli2()
ssrf1()
ssrf2()
stop_time = round(time.time() * 1000)
run_time = (stop_time - start_time) / 1000
print(f"Finished running functional tests. Run time: {run_time} seconds")
