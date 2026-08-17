# Annadarpan GitHub Actions login

This reproduces the RSA password-encryption step visible in the supplied frontend code and sends the JSON login request.

## Required repository secrets
- ANNADARPAN_USERNAME
- ANNADARPAN_PASSWORD
- ANNADARPAN_PUBLIC_KEY_B64
- ANNADARPAN_CAPTCHA_TOKEN (only if the application provides an approved CI-compatible way to obtain it)

The CAPTCHA is deliberately not bypassed. For reliable scheduled automation, obtain an official machine-to-machine/service-account/API authentication method from the application owner if CAPTCHA is mandatory.

Do not commit passwords, bearer tokens, cookies, or private keys.

Run: GitHub → Actions → Annadarpan login → Run workflow.

If it returns 400, share only the HTTP status and a redacted response body; never share credentials, cookies, Authorization headers, or CAPTCHA tokens.
