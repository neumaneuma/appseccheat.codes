import json
import time
import uuid
from enum import Enum

import requests

from backend.passphrases import Passphrases

url_prefix = "http://127.0.0.1:12300"
verify = False


class SQLI:
    class LoginBypass:
        class Vulnerabilities:
            expected_data_for_login: tuple[str, int] = (
                f"{url_prefix}/vulnerabilities/sqli1/login/",
                200,
            )

        class Patches:
            expected_data_for_login: tuple[str, int] = (
                f"{url_prefix}/patches/sqli1/login/",
                403,
            )

    class SecondOrder:
        class Vulnerabilities:
            expected_data_for_register: tuple[str, int] = (
                f"{url_prefix}/vulnerabilities/sqli2/register/",
                200,
            )
            expected_data_for_change_password: tuple[str, int] = (
                f"{url_prefix}/vulnerabilities/sqli2/change_password/",
                200,
            )

        class Patches:
            expected_data_for_register: tuple[str, int] = (
                f"{url_prefix}/patches/sqli2/register/",
                200,
            )
            expected_data_for_change_password: tuple[str, int] = (
                f"{url_prefix}/patches/sqli2/change_password/",
                400,
            )


class SSRF:
    class Webhook:
        class Vulnerabilities:
            submit_webhook_url: str = (
                f"{url_prefix}/vulnerabilities/ssrf1/submit_webhook/"
            )

        class Patches:
            submit_webhook_url: str = f"{url_prefix}/patches/ssrf1/submit_webhook/"

    class LocalFileInclusion:
        class Vulnerabilities:
            submit_api_url_url: str = (
                f"{url_prefix}/vulnerabilities/ssrf2/submit_api_url/"
            )

        class Patches:
            submit_api_url_url: str = f"{url_prefix}/patches/ssrf2/submit_api_url/"


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


class State(Enum):
    VULNERABLE = "vulnerable"
    PATCHED = "patched"


def check_status_code(
    expected_status_code: int,
    actual_status_code: int,
    *,
    url: str = "",
    appended_custom_msg: str = "",
) -> bool:
    if expected_status_code != actual_status_code:
        msg = f"FAILED {appended_custom_msg}\n\tExpected status code: {expected_status_code}\n\tActual_status_code: {actual_status_code}"
        if url:
            msg += f"\n\tFAILED URL: {url}"
        print(msg)
        return False
    else:
        print(f"PASSED {appended_custom_msg}")
        return True


def test_submission(challenge: Passphrases) -> bool:
    url = f"{url_prefix}/submission"
    data = {"secret": challenge.value, "challenge": challenge.name}
    r = requests.post(url, json=data, verify=verify)
    return check_status_code(200, r.status_code)


def sqli_login_bypass(state: State) -> bool:
    username = "administrator"
    password = "' OR 'a' = 'a"
    data = {"username": username, "password": password}

    match state:
        case State.VULNERABLE:
            url, status_code = SQLI.LoginBypass.Vulnerabilities.expected_data_for_login
        case State.PATCHED:
            url, status_code = SQLI.LoginBypass.Patches.expected_data_for_login
        case _:
            raise ValueError(f"Invalid state: {state}")

    r = requests.post(url, json=data, verify=verify)
    return check_status_code(status_code, r.status_code)


def sqli_second_order(state: State) -> bool:
    password = str(uuid.uuid4())

    match state:
        case State.VULNERABLE:
            url, status_code = (
                SQLI.SecondOrder.Vulnerabilities.expected_data_for_register
            )
        case State.PATCHED:
            url, status_code = SQLI.SecondOrder.Patches.expected_data_for_register
        case _:
            raise ValueError(f"Invalid state: {state}")

    username = "batman-- "
    data = {"username": username, "password": password}
    r = requests.post(url, json=data, verify=verify)
    first_check = check_status_code(
        status_code, r.status_code, appended_custom_msg="(1/2)"
    )

    match state:
        case State.VULNERABLE:
            url, status_code = (
                SQLI.SecondOrder.Vulnerabilities.expected_data_for_change_password
            )
        case State.PATCHED:
            url, status_code = (
                SQLI.SecondOrder.Patches.expected_data_for_change_password
            )
        case _:
            raise ValueError(f"Invalid state: {state}")

    data = {"old": password, "new": password, "new_verify": password}
    r = requests.post(url, json=data, cookies=r.cookies, verify=verify)
    second_check = check_status_code(
        status_code, r.status_code, appended_custom_msg="(2/2)"
    )

    return first_check and second_check


def ssrf_webhook(state: State) -> bool:
    match state:
        case State.VULNERABLE:
            url = SSRF.Webhook.Vulnerabilities.submit_webhook_url
            file_name = "ssrf_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.Webhook.Patches.submit_webhook_url
            file_name = "ssrf_test_urls_patched.json"
        case _:
            raise ValueError(f"Invalid state: {state}")

    # ssrf1_test_urls[0]["http://internal_api/"] = 202
    # ssrf1_test_urls[1]["http://internal_api/"] = 400
    # ssrf1_test_urls[0]["http://internal_api:12301/"] = 200
    # ssrf1_test_urls[1]["http://internal_api:12301/"] = 400
    # ssrf1_test_urls[0]["http://internal_api:12301/reset_admin_password/"] = 200
    # ssrf1_test_urls[1]["http://internal_api:12301/reset_admin_password/"] = 400
    # ssrf1_test_urls[0]["http://127.0.0.1:12302/permanent/"] = 202
    # ssrf1_test_urls[1]["http://127.0.0.1:12302/permanent/"] = 400
    # ssrf1_test_urls[0]["http://127.0.0.1:12302/temporary/"] = 202
    # ssrf1_test_urls[1]["http://127.0.0.1:12302/temporary/"] = 400

    with open(file_name) as test_urls:
        custom_urls: dict[str, int] = json.load(test_urls)

    for custom_url, status_code in custom_urls.items():
        data = {"custom_url": custom_url}
        r = requests.post(url, json=data, verify=verify)
        return check_status_code(status_code, r.status_code, url=f"{url}({custom_url})")


def ssrf_local_file_inclusion(state: State) -> bool:
    match state:
        case State.VULNERABLE:
            url = SSRF.LocalFileInclusion.Vulnerabilities.submit_api_url_url
            file_name = "ssrf_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.LocalFileInclusion.Patches.submit_api_url_url
            file_name = "ssrf_test_urls_patched.json"
        case _:
            raise ValueError(f"Invalid state: {state}")

    # ssrf1_test_urls[0]["http://internal_api/"] = 400
    # ssrf1_test_urls[1]["http://internal_api/"] = 400
    # ssrf1_test_urls[0]["http://internal_api:12301/"] = 200
    # ssrf1_test_urls[1]["http://internal_api:12301/"] = 200
    # ssrf2_test_urls[0]["http://internal_api:12301/get_cat_coin_price_v1/"] = 200
    # ssrf2_test_urls[1]["http://internal_api:12301/get_cat_coin_price_v1/"] = 200
    # ssrf2_test_urls[0]["http://internal_api:12301/get_cat_coin_price_v2/"] = 200
    # ssrf2_test_urls[1]["http://internal_api:12301/get_cat_coin_price_v2/"] = 200

    with open(file_name) as test_urls:
        custom_urls: dict[str, int] = json.load(test_urls)

    for custom_url, status_code in custom_urls.items():
        data = {"custom_url": custom_url}
        r = requests.post(url, json=data, verify=verify)
        return check_status_code(status_code, r.status_code, url=f"{url}({custom_url})")


start_time = round(time.time() * 1000)
print("Starting functional test...\n\n")
results = []

for challenge in Passphrases:
    print(f"Testing submission for challenge {challenge.name}...")
    results.append(test_submission(challenge))


for state in State:
    print(f"Testing {state} state for SQLi login bypass...")
    results.append(sqli_login_bypass(state))

    print(f"Testing {state} state for SQLi second order...")
    results.append(sqli_second_order(state))

    # print(f"Testing {state} state for SSRF webhook...")
    # results.append(ssrf_webhook(state))

    # print(f"Testing {state} state for SSRF local file inclusion...")
    # results.append(ssrf_local_file_inclusion(state))

stop_time = round(time.time() * 1000)
run_time = (stop_time - start_time) / 1000
print(f"\n\nFinished running functional tests. Run time: {run_time} seconds")

assert all(results), "There were failed tests 😭"
