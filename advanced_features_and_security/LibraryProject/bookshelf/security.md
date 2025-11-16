# Security documentations and HTTPS Configuration

# 🔐 Django Application Security Configuration

This document outlines the steps taken to secure the Django application by enforcing HTTPS, securing cookies, implementing secure headers, configuring the deployment environment, and documenting the changes.

---

## ✅ Step 1: Enforce HTTPS in Django

To ensure all traffic is securely transmitted over HTTPS, the following settings were added to `settings.py`:
----

```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True 
```
----



## Step 2: Enforce Secure Cookies
To prevent cookies from being transmitted over insecure connections, the following settings were applied:
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


Purpose:
- Ensures session and CSRF cookies are only sent over HTTPS.


## Step 3: Implement Secure Headers
The following headers were configured in settings.py to mitigate common web vulnerabilities:
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True


Purpose:
- Prevents clickjacking by disallowing framing.
- Blocks MIME-type sniffing to reduce exposure to drive-by downloads.
- Enables browser-based XSS protection.

## Step 4: Update Deployment Configuration
SSL/TLS Certificate Setup
- Certificate Provider: Let's Encrypt (via Certbot)
- Web Server: Nginx or Apache
- Certificate Path: /etc/letsencrypt/live/yourdomain.com/
Nginx Configuration Example
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}


Apache Configuration Example
<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>

<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>


## Step 5: Documentation and Review
Review Checklist
- [x] HTTPS redirection enabled
- [x] HSTS configured with preload and subdomain support
- [x] Secure cookies enforced
- [x] Security headers implemented
- [x] SSL/TLS certificates installed and auto-renewed
- [x] Web server redirects HTTP to HTTPS
- [x] Tested with SSL Labs and SecurityHeaders.com
Notes
- Ensure DEBUG = False in production.
- Use environment variables or a .env file to manage sensitive settings.
- Regularly audit security settings and update dependencies.


