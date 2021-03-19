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
    "vulnerability_gist": "https://gist.github.com/neumaneuma/39a853dfe14e7084ecc8ac8b304c60a3.js",
    "exploit_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/exploits/sqli_second_order.py",
    "exploit_gist": "https://gist.github.com/neumaneuma/2cd5ffda86a9f3beee7858fd3ee21b10.js",
    "patch_source_code": "https://github.com/neumaneuma/appseccheat.codes/blob/main/webapp/webapp/patches/sqli_second_order.py",
    "patch_gist": "https://gist.github.com/neumaneuma/0076b3c6735f6002c680415483566e6e.js",
}

def build_headers(introduction):
    return {
        "introduction": introduction,
        "news": "Heard about it in the news?",
        "challenge": "Challenge",
        "code": "Code",
        "vulnerability": "Vulnerability",
        "exploit": "Exploit",
        "patch": "Patch",
        "explanation": "Explanation",
    }
