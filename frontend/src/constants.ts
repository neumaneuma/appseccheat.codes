interface Config {
  API_BASE_URL: string
}

async function loadConfig(): Promise<Config> {
  try {
    const response = await fetch('/config.json')
    const config: Config = await response.json()
    return config
  } catch (error) {
    // If config.json isn't present for some reason, try to guess the right API_BASE_URL
    console.log('Error loading config')
    const isRunningLocally =
      window.location.hostname === '0.0.0.0' ||
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1'

    if (isRunningLocally) {
      return { API_BASE_URL: 'http://127.0.0.1:12301' }
    }
    return { API_BASE_URL: 'https://api.appseccheat.codes' }
  }
}

export const config = await loadConfig()
export const API_BASE_URL = config.API_BASE_URL
const VULNERABLE_PATH = 'vulnerabilities'

export const SUBMISSION_URL = `${API_BASE_URL}/submission`
export const SQLI_LOGIN_BYPASS_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli1/login/`
export const SQLI_SECOND_ORDER_API_REGISTER_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/register/`
export const SQLI_SECOND_ORDER_API_CHANGE_PASSWORD_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/change_password/`
export const SSRF_WEBHOOK_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf1/submit_webhook/`
export const SSRF_LOCAL_FILE_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf2/submit_api_url/`
