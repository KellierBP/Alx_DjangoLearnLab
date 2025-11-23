# Permissions and Groups Setup

This Django application implements a permission-based access control system using Django's built-in groups and permissions framework.

## Custom Permissions

Custom permissions have been added to the `Book` model in `relationship_app/models.py`:

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

The following views enforce permissions using the `@permission_required` decorator:

- `list_books`: Requires `can_view` permission
- `add_book`: Requires `can_create` permission
- `edit_book`: Requires `can_edit` permission
- `delete_book`: Requires `can_delete` permission

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