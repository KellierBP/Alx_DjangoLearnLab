# Social Media API

A Django REST Framework-based Social Media API with custom user authentication, profile management, and social features.

## Features

- **Custom User Model**: Extended Django's AbstractUser with additional fields:
  - `bio`: User biography (TextField)
  - `profile_picture`: User profile image (ImageField)
  - `followers`: Many-to-many relationship for following functionality

- **Token Authentication**: Secure token-based authentication using Django REST Framework
- **User Registration**: Create new accounts with email validation
- **User Login**: Authenticate and receive auth tokens
- **Profile Management**: View and update user profiles

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (if applicable):
   ```bash
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### Register a New User
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "bio": "Hello, I'm John!",
    "profile_picture": null
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2025-12-21T19:22:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "User registered successfully"
  }
  ```

#### Login
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2025-12-21T19:22:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "Login successful"
  }
  ```

#### View/Update Profile
- **URL**: `/api/accounts/profile/`
- **Methods**: `GET`, `PUT`, `PATCH`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2025-12-21T19:22:00Z"
  }
  ```

### Posts Endpoints

#### List All Posts
- **URL**: `/api/posts/`
- **Method**: `GET`
- **Query Parameters**: `page`, `page_size`, `search`, `ordering`
- **Example**: `/api/posts/?search=django&page=1`

#### Create a Post
- **URL**: `/api/posts/`
- **Method**: `POST`
- **Authentication**: Required
- **Body**: `{"title": "Post Title", "content": "Post content"}`

#### Update/Delete a Post
- **URL**: `/api/posts/{id}/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required (author only for PUT/PATCH/DELETE)

### Comments Endpoints

#### List/Create Comments
- **URL**: `/api/comments/`
- **Methods**: `GET`, `POST`
- **Query Parameters**: `post` (filter by post ID)
- **Example**: `/api/comments/?post=1`

#### Update/Delete a Comment
- **URL**: `/api/comments/{id}/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required (author only for PUT/PATCH/DELETE)

### Follow/Unfollow Endpoints

#### Follow a User
- **URL**: `/api/accounts/follow/<user_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: Success message and user data

#### Unfollow a User
- **URL**: `/api/accounts/unfollow/<user_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: Success message and user data

### Feed Endpoint

#### Get Personalized Feed
- **URL**: `/api/feed/`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Shows posts from users you follow, ordered by newest first
- **Query Parameters**: `page`, `page_size`

## Testing with Postman

### 1. Register a New User
- Set method to `POST`
- URL: `http://127.0.0.1:8000/api/accounts/register/`
- Body (raw JSON):
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "bio": "Test user bio"
  }
  ```
- Copy the `token` from the response

### 2. Login
- Set method to `POST`
- URL: `http://127.0.0.1:8000/api/accounts/login/`
- Body (raw JSON):
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```

### 3. View Profile
- Set method to `GET`
- URL: `http://127.0.0.1:8000/api/accounts/profile/`
- Headers:
  - Key: `Authorization`
  - Value: `Token YOUR_TOKEN_HERE`

### 4. Update Profile
- Set method to `PATCH`
- URL: `http://127.0.0.1:8000/api/accounts/profile/`
- Headers:
  - Key: `Authorization`
  - Value: `Token YOUR_TOKEN_HERE`
- Body (raw JSON):
  ```json
  {
    "bio": "Updated bio text"
  }
  ```

## Testing with cURL

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "bio": "Test user bio"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### View Profile
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Project Structure

```
social_media_api/
├── manage.py
├── requirements.txt
├── README.md
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

## User Model Fields

### Default Django Fields
- `username`: Unique username
- `email`: Email address
- `password`: Hashed password
- `first_name`: First name (optional)
- `last_name`: Last name (optional)
- `is_active`: Account active status
- `is_staff`: Staff status
- `date_joined`: Registration date

### Custom Fields
- `bio`: Text field for user biography (max 500 characters)
- `profile_picture`: Image field for profile picture (uploaded to `media/profile_pictures/`)
- `followers`: Many-to-many field for follower relationships (symmetrical=False)

## Features Implemented

### User Authentication
- Custom user model with bio, profile picture, and followers
- Token-based authentication
- User registration and login
- Profile management

### Posts & Comments
- Create, read, update, and delete posts
- Create, read, update, and delete comments
- Author-only permissions for editing/deleting
- Pagination (10 items per page)
- Search posts by title and content
- Filter comments by post

## Next Steps

- Create follow/unfollow endpoints
- Add user feed based on followed users
- Implement likes functionality
- Add notifications system
- Implement real-time updates with WebSockets

## License

This project is part of the ALX Django Learning Lab.
