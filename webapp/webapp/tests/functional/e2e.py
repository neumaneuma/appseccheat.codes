import requests

url_prefix = "http://127.0.0.1:5000"
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


sqli1()
sqli2()
