# Social Media API - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Social Media API to production using Heroku (recommended) or alternative hosting services.

## Prerequisites

- Git installed and repository initialized
- Heroku CLI installed (for Heroku deployment)
- PostgreSQL knowledge (for database management)
- Basic understanding of environment variables

---

## Quick Start: Heroku Deployment

### 1. Install Heroku CLI

Download and install from: https://devcenter.heroku.com/articles/heroku-cli

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create Heroku Application

```bash
cd social_media_api
heroku create your-app-name
```

### 4. Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

### 5. Configure Environment Variables

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

### 6. Deploy to Heroku

```bash
git add .
git commit -m "Configure for production deployment"
git push heroku main
```

### 7. Run Migrations

```bash
heroku run python manage.py migrate
```

### 8. Create Superuser

```bash
heroku run python manage.py createsuperuser
```

### 9. Collect Static Files

```bash
heroku run python manage.py collectstatic --noinput
```

### 10. Open Your Application

```bash
heroku open
```

Your API should now be live at: `https://your-app-name.herokuapp.com`

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `your-app.herokuapp.com` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Heroku |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` (if DEBUG=False) |
| `SESSION_COOKIE_SECURE` | Secure session cookies | `True` (if DEBUG=False) |
| `CSRF_COOKIE_SECURE` | Secure CSRF cookies | `True` (if DEBUG=False) |

### Setting Environment Variables

**Heroku**:
```bash
heroku config:set VARIABLE_NAME="value"
```

**Local Development** (.env file):
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Production Configuration Files

### Procfile
Defines how Heroku runs your application:
```
web: gunicorn social_media_api.wsgi --log-file -
release: python manage.py migrate
```

### runtime.txt
Specifies Python version:
```
python-3.11.0
```

### requirements.txt
Production dependencies:
```
Django>=4.2,<5.0
djangorestframework>=3.14.0
django-filter>=23.0
Pillow>=10.0.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.9
whitenoise>=6.6.0
python-decouple>=3.8
dj-database-url>=2.1.0
```

---

## Security Checklist

- [x] `DEBUG = False` in production
- [x] Strong `SECRET_KEY` (never commit to Git)
- [x] `ALLOWED_HOSTS` properly configured
- [x] HTTPS enabled (automatic on Heroku)
- [x] `SECURE_SSL_REDIRECT = True`
- [x] `SESSION_COOKIE_SECURE = True`
- [x] `CSRF_COOKIE_SECURE = True`
- [x] `SECURE_BROWSER_XSS_FILTER = True`
- [x] `X_FRAME_OPTIONS = 'DENY'`
- [x] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [x] HSTS enabled for production

---

## Testing Your Deployment

### 1. Test API Endpoints

```bash
# Health check
curl https://your-app-name.herokuapp.com/api/

# Register a user
curl -X POST https://your-app-name.herokuapp.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'

# Login
curl -X POST https://your-app-name.herokuapp.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 2. Test Admin Interface

Visit: `https://your-app-name.herokuapp.com/admin/`

### 3. Check Logs

```bash
heroku logs --tail
```

---

## Monitoring & Maintenance

### View Logs

```bash
# Real-time logs
heroku logs --tail

# Last 100 lines
heroku logs -n 100

# Filter by source
heroku logs --source app
```

### Database Management

```bash
# Access database
heroku pg:psql

# Database info
heroku pg:info

# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download
```

### Scaling

```bash
# Scale web dynos
heroku ps:scale web=2

# Check dyno status
heroku ps
```

---

## Alternative Deployment: DigitalOcean

### Requirements

- Ubuntu 22.04 server
- Nginx
- Gunicorn
- PostgreSQL
- Supervisor (process management)
- SSL certificate (Let's Encrypt)

### Basic Setup Steps

1. **Create Droplet** on DigitalOcean
2. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

3. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

4. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure PostgreSQL**:
   ```bash
   sudo -u postgres createdb socialmedia
   sudo -u postgres createuser socialmediauser
   ```

6. **Set Environment Variables** in `.env` file

7. **Configure Nginx** as reverse proxy

8. **Set up Gunicorn** with Supervisor

9. **Configure SSL** with Let's Encrypt

---

## Troubleshooting

### Common Issues

**Issue**: Application crashes on startup  
**Solution**: Check logs with `heroku logs --tail` and verify environment variables

**Issue**: Static files not loading  
**Solution**: Run `heroku run python manage.py collectstatic`

**Issue**: Database connection errors  
**Solution**: Verify `DATABASE_URL` is set correctly

**Issue**: CORS errors  
**Solution**: Install and configure `django-cors-headers` if needed

### Debug Mode

**Never enable DEBUG=True in production!**

For debugging production issues:
1. Check Heroku logs
2. Use error monitoring service (Sentry)
3. Enable verbose logging temporarily

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check application uptime

### Weekly
- Review security logs
- Check database size
- Monitor API response times

### Monthly
- Update dependencies
- Review and rotate secrets
- Database backup verification

### Quarterly
- Security audit
- Performance optimization
- Dependency vulnerability scan

---

## Scaling Considerations

### When to Scale

- Response times > 500ms
- CPU usage > 80%
- Memory usage > 80%
- Database connections maxed out

### Scaling Options

1. **Vertical Scaling**: Upgrade dyno size
   ```bash
   heroku ps:resize web=standard-2x
   ```

2. **Horizontal Scaling**: Add more dynos
   ```bash
   heroku ps:scale web=3
   ```

3. **Database Scaling**: Upgrade PostgreSQL plan
   ```bash
   heroku addons:upgrade heroku-postgresql:standard-0
   ```

4. **Caching**: Add Redis for caching
   ```bash
   heroku addons:create heroku-redis:mini
   ```

---

## Additional Resources

- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## Support & Contact

For issues or questions:
- Check Heroku logs: `heroku logs --tail`
- Review Django documentation
- Check project README.md
