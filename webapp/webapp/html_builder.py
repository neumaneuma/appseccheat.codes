SQLI1_LINKS = {
    "vulnerability_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/vulnerabilities/sqli_login_bypass.py",
    "vulnerability_gist": "https://gist.github.com/neumaneuma/39a853dfe14e7084ecc8ac8b304c60a3.js",
    "exploit_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/sqli_login_bypass.py",
    "exploit_gist": "https://gist.github.com/neumaneuma/2cd5ffda86a9f3beee7858fd3ee21b10.js",
    "patch_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/patches/sqli_login_bypass.py",
    "patch_gist": "https://gist.github.com/neumaneuma/0076b3c6735f6002c680415483566e6e.js",
}

SQLI2_LINKS = {
    "vulnerability_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/vulnerabilities/sqli_second_order.py",
    "vulnerability_gist": "https://gist.github.com/neumaneuma/a96c8d6c304e94cdd343a17a7ad0a7ee.js",
    "exploit_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/sqli_second_order.py",
    "exploit_gist": "https://gist.github.com/neumaneuma/a258d30a2551184f00e455969d9fc413.js",
    "patch_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/patches/sqli_second_order.py",
    "patch_gist": "https://gist.github.com/neumaneuma/bef037bcd02ae91e6c6ecf1aac46546d.js",
}
SSRF1_LINKS = {
    "vulnerability_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/vulnerabilities/ssrf_webhook.py",
    "vulnerability_gist": "https://gist.github.com/neumaneuma/b107ad89537341dcbc9c6d2867d0ba96.js",
    "exploit_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/ssrf_webhook.py",
    "exploit_gist": "https://gist.github.com/neumaneuma/4e9b0e8700422697206de9be019f0af0.js",
    "patch_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/patches/ssrf_webhook.py",
    "patch_gist": "https://gist.github.com/neumaneuma/c392c3eb4bd101f87810c058419cdc29.js",
}

SSRF2_LINKS = {
    "vulnerability_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/vulnerabilities/ssrf_lfi.py",
    "vulnerability_gist": "https://gist.github.com/neumaneuma/118a03193a5c35bdbe737cbbb501554a.js",
    "exploit_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/ssrf_lfi.py",
    "exploit_gist": "https://gist.github.com/neumaneuma/7f7128165a65b55ae7c229b5e30394ce.js",
    "patch_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/patches/ssrf_lfi.py",
    "patch_gist": "https://gist.github.com/neumaneuma/2eb5ec307ed39e0630bdd4c87560941b.js",
}


def build_headers(title, introduction, congratulations_message):
    return {
        "title": title,
        "introduction": introduction,
        "congratulations_message": congratulations_message,
        "news": "Heard about it in the news?",
        "challenge": "Challenge",
        "explanation": "Explanation",
    }
