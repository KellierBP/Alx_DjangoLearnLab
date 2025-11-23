# Permissions and Groups Setup

This Django application implements a permission-based access control system using Django's built-in groups and permissions framework.

## Custom Permissions

Custom permissions have been added to the `Book` model in `bookshelf/models.py`:

- `can_view`: Allows users to view books
- `can_create`: Allows users to create new books
- `can_edit`: Allows users to edit existing books
- `can_delete`: Allows users to delete books

## User Groups

Three user groups have been created with assigned permissions:

- **Viewers**: Can view books (`can_view`)
- **Editors**: Can create and edit books (`can_create`, `can_edit`)
- **Admins**: Have all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)

## Views with Permission Checks

The following views in `bookshelf/views.py` enforce permissions using the `@permission_required` decorator:

- `book_list`: Requires `can_view` permission
- `book_detail`: Requires `can_view` permission
- `book_create`: Requires `can_create` permission
- `book_update`: Requires `can_edit` permission
- `book_delete`: Requires `can_delete` permission

## Setup Instructions

1. Run migrations to update permissions:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create groups and assign permissions:
   ```
   python manage.py create_groups
   ```

3. Assign users to groups via Django admin or programmatically.

## Testing

To test the permissions:

1. Create test users in Django admin.
2. Assign users to different groups (Viewers, Editors, Admins).
3. Log in as each user and attempt to access:
   - Book list (requires can_view)
   - Add book (requires can_create)
   - Edit book (requires can_edit)
   - Delete book (requires can_delete)

Users should only be able to perform actions allowed by their group's permissions.

## Security Measures Implemented

### 1. Secure Settings Configuration
- `DEBUG = False` in production
- `SECURE_SSL_REDIRECT = True` - Redirects all HTTP requests to HTTPS
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` - Tells Django the connection is secure when behind a proxy
- `SECURE_HSTS_SECONDS = 31536000` - Enforces HTTPS for one year
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` - Includes subdomains in HSTS policy
- `SECURE_HSTS_PRELOAD = True` - Allows preloading in browser HSTS lists
- `SECURE_BROWSER_XSS_FILTER = True` - Enables XSS filtering
- `X_FRAME_OPTIONS = 'DENY'` - Prevents clickjacking
- `SECURE_CONTENT_TYPE_NOSNIFF = True` - Prevents MIME sniffing
- `CSRF_COOKIE_SECURE = True` - HTTPS-only CSRF cookies
- `SESSION_COOKIE_SECURE = True` - HTTPS-only session cookies

### 2. CSRF Protection
- All forms include `{% csrf_token %}` to prevent CSRF attacks

### 3. Input Validation and SQL Injection Prevention
- Uses Django ModelForms (`BookForm`) for all book operations
- Automatic input sanitization and validation
- ORM queries prevent SQL injection

### 4. Content Security Policy (CSP)
- Custom middleware sets CSP headers
- Restricts content sources to reduce XSS risk

### 5. Testing Security
- Manual testing: Create users, assign to groups, test access restrictions
- Verify forms reject invalid input
- Check browser developer tools for security headers

## HTTPS Deployment Configuration

To deploy this Django application with HTTPS support, follow these steps:

### 1. Obtain SSL/TLS Certificate
- Use Let's Encrypt (free) or purchase from a CA
- For development/testing, use self-signed certificates

### 2. Web Server Configuration

#### Nginx Configuration Example
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/static/files/;
    }

    location /media/ {
        alias /path/to/your/media/files/;
    }
}
```

#### Apache Configuration Example
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key

    <Location />
        ProxyPass http://127.0.0.1:8000/
        ProxyPassReverse http://127.0.0.1:8000/
        RequestHeader set X-Forwarded-Proto https
    </Location>

    Alias /static/ /path/to/your/static/files/
    <Directory "/path/to/your/static/files/">
        Require all granted
    </Directory>

    Alias /media/ /path/to/your/media/files/
    <Directory "/path/to/your/media/files/">
        Require all granted
    </Directory>
</VirtualHost>
```

### 3. Django Production Settings
Ensure these settings are configured for production:
- `DEBUG = False`
- `ALLOWED_HOSTS = ['yourdomain.com']`
- All security settings as configured in `settings.py`

### 4. Using Gunicorn with SSL (Alternative)
If using Gunicorn directly:
```bash
gunicorn --certfile=/path/to/cert.pem --keyfile=/path/to/key.pem LibraryProject.wsgi:application
```

### 5. Testing HTTPS Setup
- Access your site via https://yourdomain.com
- Verify HTTP requests redirect to HTTPS
- Check browser developer tools for security headers
- Use SSL Labs' SSL Test to verify certificate and configuration

## Security Review

### Implemented Security Measures

1. **HTTPS Enforcement**:
   - `SECURE_SSL_REDIRECT = True`: Automatically redirects all HTTP traffic to HTTPS, ensuring encrypted communication.
   - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`: Allows Django to detect HTTPS when behind a reverse proxy that terminates SSL.
   - `SECURE_HSTS_SECONDS = 31536000`: HTTP Strict Transport Security (HSTS) forces browsers to use HTTPS for the next year, preventing protocol downgrade attacks.
   - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Extends HSTS protection to all subdomains.
   - `SECURE_HSTS_PRELOAD = True`: Allows the domain to be included in browser preload lists for immediate HTTPS enforcement.

2. **Secure Cookies**:
   - `SESSION_COOKIE_SECURE = True`: Session cookies are only sent over HTTPS connections.
   - `CSRF_COOKIE_SECURE = True`: CSRF tokens are only transmitted securely.

3. **Security Headers**:
   - `X_FRAME_OPTIONS = 'DENY'`: Prevents clickjacking by blocking iframe embedding.
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents MIME type sniffing attacks.
   - `SECURE_BROWSER_XSS_FILTER = True`: Enables browser XSS filtering.

4. **Additional Protections**:
   - CSRF protection on all forms.
   - Input validation through Django ModelForms.
   - Content Security Policy (CSP) headers via custom middleware.
   - Permission-based access control with custom permissions and groups.

### How These Measures Secure the Application

- **Data Protection**: HTTPS ensures all data transmitted between client and server is encrypted, protecting sensitive information from eavesdropping.
- **Man-in-the-Middle Prevention**: HSTS and secure cookies prevent MITM attacks by enforcing secure connections.
- **Injection Attack Mitigation**: XSS filtering, CSP, and input validation prevent common web vulnerabilities.
- **Access Control**: Permission system ensures users can only perform authorized actions.

### Potential Areas for Improvement

1. **Certificate Management**: Implement automated certificate renewal (e.g., with certbot for Let's Encrypt).
2. **Advanced CSP**: Use django-csp package for more granular content source control.
3. **Security Monitoring**: Add logging and monitoring for security events.
4. **Rate Limiting**: Implement rate limiting to prevent brute force and DDoS attacks.
5. **Regular Security Audits**: Schedule periodic security reviews and dependency updates.
6. **Two-Factor Authentication**: Consider adding 2FA for enhanced user authentication.

### Recommendations for Production

- Use a reputable web server (Nginx/Apache) with proper SSL configuration.
- Regularly update Django and all dependencies.
- Implement backup and disaster recovery procedures.
- Use environment variables for sensitive settings instead of hardcoding.
- Enable Django's security middleware and keep DEBUG=False in production.