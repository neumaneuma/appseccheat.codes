interface Config {
  API_BASE_URL: string
}

function loadConfig(): Config {
  // Check if we're running on Cloudflare Pages using their environment variable
  // https://developers.cloudflare.com/pages/configuration/build-configuration/#environment-variables
  const isCloudflarePages = Boolean(import.meta.env.CF_PAGES)

  if (isCloudflarePages) {
    return { API_BASE_URL: 'https://api.appseccheat.codes' }
  }

  // Default to localhost if not on Cloudflare Pages
  return { API_BASE_URL: 'http://127.0.0.1:12301' }
}

export const config = loadConfig()
export const API_BASE_URL = config.API_BASE_URL
const VULNERABLE_PATH = 'vulnerabilities'

export const SUBMISSION_URL = `${API_BASE_URL}/submission`
export const SQLI_LOGIN_BYPASS_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli1/login/`
export const SQLI_SECOND_ORDER_API_REGISTER_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/register/`
export const SQLI_SECOND_ORDER_API_CHANGE_PASSWORD_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/change_password/`
export const SSRF_WEBHOOK_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf1/submit_webhook/`
export const SSRF_LOCAL_FILE_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf2/submit_api_url/`
