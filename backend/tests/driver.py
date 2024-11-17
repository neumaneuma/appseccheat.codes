import json
import re
import time
import uuid
from enum import Enum
from typing import assert_never

import requests

from backend.passphrases import Passphrases

url_prefix = "http://127.0.0.1:12300"
verify = False


class SQLI:
    class LoginBypass:
        class Vulnerabilities:
            expected_data_for_login: tuple[str, int, str] = (
                f"{url_prefix}/vulnerabilities/sqli1/login/",
                200,
                Passphrases.sqli1.value,
            )

        class Patches:
            expected_data_for_login: tuple[str, int, dict[str, str]] = (
                f"{url_prefix}/patches/sqli1/login/",
                403,
                {"detail": "Login failed"},
            )

    class SecondOrder:
        class Vulnerabilities:
            expected_data_for_register: tuple[str, int, str] = (
                f"{url_prefix}/vulnerabilities/sqli2/register/",
                200,
                "Successfully registered",
            )
            expected_data_for_change_password: tuple[str, int, str] = (
                f"{url_prefix}/vulnerabilities/sqli2/change_password/",
                200,
                Passphrases.sqli2.value,
            )

        class Patches:
            expected_data_for_register: tuple[str, int, str] = (
                f"{url_prefix}/patches/sqli2/register/",
                200,
                "Successfully registered",
            )
            expected_data_for_change_password: tuple[str, int, str] = (
                f"{url_prefix}/patches/sqli2/change_password/",
                200,
                "Successfully changed password",
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


class State(Enum):
    VULNERABLE = "vulnerable"
    PATCHED = "patched"


def check_response(
    *,
    expected_status_code: int,
    actual_status_code: int,
    expected_response: str | dict[str, bool] | dict[str, str],
    actual_response: str | dict[str, bool] | dict[str, str],
    url: str = "",
    appended_custom_msg: str = "",
) -> bool:
    assert (
        type(expected_response) is type(actual_response)
    ), f"Expected and actual response types do not match. Expected: {type(expected_response)}, Actual: {type(actual_response)}.\n\t- Expected response: {expected_response}\n\t- Actual response: {actual_response}"
    success = (
        expected_status_code == actual_status_code
        and expected_response == actual_response
    )
    if success:
        msg = f"\tPASSED {appended_custom_msg}"
    else:
        msg = f"\tFAILED {appended_custom_msg}"
        if expected_status_code != actual_status_code:
            msg += f"\n\t- Expected status code: {expected_status_code}\n\t- Actual_status_code: {actual_status_code}"
        if expected_response != actual_response:
            msg += f"\n\t- Expected response: {expected_response}\n\t- Actual response: {actual_response}"

    if url:
        msg += f"\n\t- URL: {url}"

    print(msg)
    return success


def test_submission(challenge: Passphrases) -> bool:
    url = f"{url_prefix}/submission"
    data = {"secret": challenge.value, "challenge": challenge.name}
    r = requests.post(url, json=data, verify=verify)
    return check_response(
        expected_status_code=200,
        actual_status_code=r.status_code,
        expected_response={"result": True},
        actual_response=r.json(),
    )


def sqli_login_bypass(state: State) -> bool:
    expected_response: str | dict[str, str]
    username = "administrator"
    password = "' OR 'a' = 'a"
    data = {"username": username, "password": password}

    match state:
        case State.VULNERABLE:
            url, status_code, expected_response = (
                SQLI.LoginBypass.Vulnerabilities.expected_data_for_login
            )
        case State.PATCHED:
            url, status_code, expected_response = (
                SQLI.LoginBypass.Patches.expected_data_for_login
            )
        case _:
            assert_never(state)

    r = requests.post(url, json=data, verify=verify)
    response = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=r.json(),
    )
    return response


def sqli_second_order(state: State) -> bool:
    password = str(uuid.uuid4())

    match state:
        case State.VULNERABLE:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Vulnerabilities.expected_data_for_register
            )
        case State.PATCHED:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Patches.expected_data_for_register
            )
        case _:
            assert_never(state)

    username = "batman';-- "
    data = {"username": username, "password": password}
    r = requests.post(url, json=data, verify=verify)
    first_check = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=r.json(),
        appended_custom_msg="(1/2)",
    )

    match state:
        case State.VULNERABLE:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Vulnerabilities.expected_data_for_change_password
            )
        case State.PATCHED:
            url, status_code, expected_response = (
                SQLI.SecondOrder.Patches.expected_data_for_change_password
            )
        case _:
            assert_never(state)

    data = {"old": password, "new": password, "new_verify": password}
    r = requests.post(url, json=data, cookies=r.cookies, verify=verify)
    second_check = check_response(
        expected_status_code=status_code,
        actual_status_code=r.status_code,
        expected_response=expected_response,
        actual_response=r.json(),
        appended_custom_msg="(2/2)",
    )

    return first_check and second_check


def ssrf_webhook(state: State) -> list[bool]:
    match state:
        case State.VULNERABLE:
            url = SSRF.Webhook.Vulnerabilities.submit_webhook_url
            file_name = "backend/tests/ssrf_webhook_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.Webhook.Patches.submit_webhook_url
            file_name = "backend/tests/ssrf_webhook_test_urls_patched.json"
        case _:
            assert_never(state)

    with open(file_name) as test_urls:
        expected_responses: list[dict[str, str] | dict[str, dict[str, str]]] = (
            json.load(test_urls)
        )

    all_response_checks = []
    for i, expected_response in enumerate(expected_responses):
        payload_url = expected_response["url"]
        raw_status_code = expected_response["status_code"]
        assert isinstance(raw_status_code, str), "Status code is not an string"
        status_code = int(raw_status_code)
        response = expected_response["response"]

        # Hacky way of dealing with not being able to access python from the json file
        if response == "Passphrases.ssrf1.value":
            response = Passphrases.ssrf1.value

        data = {"url": payload_url}
        r = requests.post(url, json=data, verify=verify)
        is_correct_response = check_response(
            expected_status_code=status_code,
            actual_status_code=r.status_code,
            expected_response=response,
            actual_response=r.json(),
            url=payload_url,
            appended_custom_msg=f"({i + 1}/{len(expected_responses)})",
        )
        all_response_checks.append(is_correct_response)
        if not is_correct_response:
            break

    return all_response_checks


def ssrf_local_file_inclusion(state: State) -> bool:
    cat_coin_price_pattern = re.compile(
        r"Price at \d{2}:\d{2}:\d{2}\.\d{6} - \$\d+\.\d+"
    )

    match state:
        case State.VULNERABLE:
            url = SSRF.LocalFileInclusion.Vulnerabilities.submit_api_url_url
            file_name = "backend/tests/ssrf_lfi_test_urls_vulnerable.json"
        case State.PATCHED:
            url = SSRF.LocalFileInclusion.Patches.submit_api_url_url
            file_name = "backend/tests/ssrf_lfi_test_urls_patched.json"
        case _:
            assert_never(state)

    with open(file_name) as test_urls:
        expected_responses: list[dict[str, str] | dict[str, dict[str, str]]] = (
            json.load(test_urls)
        )

    all_response_checks = []
    for i, expected_response in enumerate(expected_responses):
        payload_url = expected_response["url"]
        raw_status_code = expected_response["status_code"]
        assert isinstance(raw_status_code, str), "Status code is not an string"
        status_code = int(raw_status_code)
        response = expected_response["response"]

        # Hacky way of dealing with not being able to access python from the json file
        if response == "Passphrases.ssrf2.value":
            response = Passphrases.ssrf2.value

        data = {"url": payload_url}
        r = requests.post(url, json=data, verify=verify)

        actual_response = r.json()
        if isinstance(actual_response, str) and cat_coin_price_pattern.match(
            actual_response
        ):
            actual_response = "Cat coin price"

        is_correct_response = check_response(
            expected_status_code=status_code,
            actual_status_code=r.status_code,
            expected_response=response,
            actual_response=actual_response,
            url=payload_url,
            appended_custom_msg=f"({i + 1}/{len(expected_responses)})",
        )
        all_response_checks.append(is_correct_response)
        if not is_correct_response:
            break

    return all_response_checks


start_time = round(time.time() * 1000)
print("Starting functional test...\n\n")
results = []

for challenge in Passphrases:
    print(f"Testing submission for challenge {challenge.name}...")
    results.append(test_submission(challenge))

for state in State:
    print(f"Testing {state.name} state for SQLi login bypass...")
    results.append(sqli_login_bypass(state))

    print(f"Testing {state.name} state for SQLi second order...")
    results.append(sqli_second_order(state))

    print(f"Testing {state.name} state for SSRF webhook...")
    results.extend(ssrf_webhook(state))

    print(f"Testing {state.name} state for SSRF local file inclusion...")
    results.extend(ssrf_local_file_inclusion(state))

stop_time = round(time.time() * 1000)
run_time = (stop_time - start_time) / 1000
print(
    f"\n\nFinished running {len(results)} functional tests. Run time: {run_time} seconds"
)

assert all(results), "There were failed tests 😭"
