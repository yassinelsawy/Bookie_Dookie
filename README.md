# 📚 Bookie Dookie — Library Management REST API

A full-featured **Library Management System** back-end built with **Django 5.2** and **Django REST Framework 3.16**. The API powers user authentication, book catalog management, a borrowing system with availability tracking, wishlists, and an admin dashboard — all exposed as clean, RESTful endpoints.

---

## Table of Contents

1. [Getting Started](#getting-started)  
2. [Tech Stack](#tech-stack)  
3. [Project Architecture](#project-architecture)  
4. [Django & DRF Features Used](#django--drf-features-used)  
5. [Database Design & Schema](#database-design--schema)  
6. [API Endpoints](#api-endpoints)  
7. [Feature Examples](#feature-examples)  

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Bookie_Dookie.git
cd Bookie_Dookie/Bookie_Dookie_Dj

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.2.1 |
| REST API | Django REST Framework 3.16 |
| Authentication | Django's built-in session auth + `djangorestframework-simplejwt` |
| CORS | django-cors-headers 4.7 |
| Database | SQLite 3 (development) |
| Language | Python 3.x |

---

## Project Architecture

The project follows Django's **app-based modular architecture**, splitting the domain into three self-contained apps:

| App | Responsibility |
|---|---|
| **Users** | Authentication, book borrowing, and wishlist management |
| **Books** | Book catalog CRUD operations |
| **Dashboard** | Admin-facing endpoints (user listing) |

Each app encapsulates its own **models → serializers → views → urls** pipeline, keeping concerns cleanly separated.

---

## Django & DRF Features Used

### 1. Custom User Model (`AbstractUser`)

Instead of relying on Django's default `auth.User`, the project defines a **custom User model** by extending `AbstractUser`. This is wired into settings via:

```python
AUTH_USER_MODEL = "Users.User"
```

This allows adding domain-specific fields and relationships (e.g., `borrowed_books`, `wishlist`) directly on the User model while retaining full compatibility with Django's authentication system (`authenticate()`, `login()`, `logout()`, password hashing, etc.).

### 2. Django REST Framework Class-Based Views (`APIView`)

All endpoints are built using DRF's `APIView` class, providing a clean, object-oriented structure where each HTTP method (`get`, `post`, `put`, `delete`) is handled by its own method on the view class:

```python
class AddBook(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book added successfully"}, status=201)
        return Response(serializer.errors, status=400)
```

### 3. ModelSerializer for Validation & Serialization

DRF's `ModelSerializer` is used throughout to:
- **Validate** incoming request data against model field constraints.
- **Serialize** model instances into JSON for API responses.
- **Separate read and write concerns** by having distinct serializers (`AddBookSerializer` for input, `GetBookSerializer` for output with extra fields like `id` and `book_state`).

```python
class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'cover_url', 'description']

class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'cover_url', 'description', 'book_state']
```

### 4. Permission Classes

DRF's permission system is used to control access at the view level:
- **Global default** in `settings.py`: `IsAuthenticated` — all endpoints require login by default.
- **Per-view override**: Public endpoints (e.g., `GetBook`, `Login`, `SignUp`) use `AllowAny` to bypass authentication.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# In a public view:
class GetBook(APIView):
    permission_classes = [AllowAny]
```

### 5. Django Session-Based Authentication

The project uses Django's built-in session authentication with `authenticate()`, `login()`, and `logout()` functions. This provides secure, server-side session management — session cookies are issued on login and invalidated on logout.

### 6. ManyToManyField with a Through Model

The borrowing relationship between users and books is modeled with a **ManyToManyField** using an explicit **through model** (`UserBorrowedBook`). This allows storing extra data on the relationship — specifically the `borrow_date` timestamp:

```python
class User(AbstractUser):
    borrowed_books = models.ManyToManyField(
        'Books.Book',
        through='UserBorrowedBook',
        related_name='borrowers'
    )

class UserBorrowedBook(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Books.Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
```

### 7. ManyToManyField for Wishlist

The wishlist is a **direct ManyToMany relationship** (no through model needed since no extra data is stored):

```python
wishlist = models.ManyToManyField(Book, related_name='wishlisted_by', blank=True)
```

### 8. CORS Configuration

The project uses `django-cors-headers` to allow cross-origin requests from the front-end, with explicit origin whitelisting, credential support, and allowed HTTP methods:

```python
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:5501']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'PATCH', 'POST', 'PUT']
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:5501"]
```

### 9. Password Validation

Django's full suite of built-in password validators is enabled:
- `UserAttributeSimilarityValidator` — prevents passwords similar to user attributes.
- `MinimumLengthValidator` — enforces minimum password length.
- `CommonPasswordValidator` — blocks commonly used passwords.
- `NumericPasswordValidator` — prevents fully numeric passwords.

### 10. Secure User Creation with `create_user()`

The sign-up serializer uses Django's `create_user()` manager method, which properly **hashes the password** before storing it:

```python
def create(self, validated_data):
    is_staff = validated_data.pop('is_staff')
    user = User.objects.create_user(**validated_data)
    user.is_staff = is_staff
    user.save()
    return user
```

---

## Database Design & Schema

### Entity-Relationship Diagram

```
┌─────────────────────┐          ┌─────────────────────────────┐
│       User          │          │           Book              │
│─────────────────────│          │─────────────────────────────│
│ id (PK, BigAuto)    │          │ id (PK, BigAuto)            │
│ username (unique)   │          │ title (CharField, 100)      │
│ email (EmailField)  │          │ author (CharField, 100)     │
│ password (hashed)   │          │ category (CharField, 100)   │
│ first_name          │          │ cover_url (CharField, 200)  │
│ last_name           │          │ description (TextField)     │
│ date_joined (auto)  │          │ book_state (Boolean, def=1) │
│ is_staff (Boolean)  │          └──────────┬──────────────────┘
└──────┬──────┬───────┘                     │
       │      │                             │
       │      │  ┌──────────────────────┐   │
       │      └──┤  User_Wishlist (M2M) ├───┘
       │         │──────────────────────│
       │         │ user_id (FK → User)  │
       │         │ book_id (FK → Book)  │
       │         └──────────────────────┘
       │
       │         ┌──────────────────────────────┐
       └─────────┤  UserBorrowedBook (Through)  ├───── Book
                 │──────────────────────────────│
                 │ id (PK)                      │
                 │ user_id (FK → User)          │
                 │ book_id (FK → Book)          │
                 │ borrow_date (DateTime, auto) │
                 └──────────────────────────────┘
```

### Tables Overview

| Table | Purpose |
|---|---|
| **User** | Custom user model extending `AbstractUser`. Stores credentials, profile info, and links to books via borrowing and wishlist. |
| **Book** | The book catalog. Each book has metadata and a `book_state` boolean flag (`True` = available, `False` = currently borrowed). |
| **UserBorrowedBook** | Explicit through/junction table for the borrow relationship. Tracks *which* user borrowed *which* book and *when* (`borrow_date`). |
| **User_Wishlist** | Auto-generated M2M junction table linking users to their wishlisted books. |

### Key Design Decisions

- **`book_state` as an availability flag**: When a book is borrowed, `book_state` is set to `False`; when returned, it's reset to `True`. This provides an instant availability check without needing to query the borrowing table.
- **Through model for borrowing**: Using an explicit through model (`UserBorrowedBook`) instead of a plain M2M allows recording the borrow date, enabling future features like due-date tracking or borrowing history.
- **Direct M2M for wishlist**: Since the wishlist only links users to books with no extra metadata, a simple ManyToManyField is the right choice — clean and efficient.

---

## API Endpoints

### Authentication & User Management — `/users/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/users/signup/` | No | Register a new user |
| `POST` | `/users/login/` | No | Authenticate and create a session |
| `POST` | `/users/logout/` | Yes | Destroy the current session |
| `GET` | `/users/get_user_role/` | Yes | Returns the `is_staff` status of the logged-in user |

### Book Borrowing — `/users/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/users/get_borrow/` | Yes | List all books borrowed by the current user (with borrow dates) |
| `POST` | `/users/borrow/?book_id=<id>` | Yes | Borrow a book (marks it as unavailable) |
| `DELETE` | `/users/return/?book_id=<id>` | Yes | Return a borrowed book (marks it as available) |

### Wishlist — `/users/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/users/get_wishlist/` | No | Get the current user's wishlist (returns `[]` for anonymous users) |
| `POST` | `/users/wishlist/?book_id=<id>` | Yes | Add a book to the wishlist |
| `DELETE` | `/users/remove_wishlist/?book_id=<id>` | Yes | Remove a book from the wishlist |

### Book Catalog — `/books/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/books/get_book/` | No | List all books in the catalog |
| `GET` | `/books/get_book/?book_id=<id>` | No | Get a single book by ID |
| `POST` | `/books/add_book/` | Yes | Add a new book to the catalog |
| `PUT` | `/books/edit_book/?book_id=<id>` | Yes | Update an existing book's details |
| `DELETE` | `/books/delete_book/?book_id=<id>` | Yes | Remove a book from the catalog |

### Admin Dashboard — `/dashboard/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/dashboard/get_users/` | Yes | List all registered users (id, username, email, name) |

---

## Feature Examples

### 1. User Registration

**Request:**
```http
POST /users/signup/
Content-Type: application/json

{
    "first_name": "Ahmed",
    "last_name": "Hassan",
    "email": "ahmed@example.com",
    "username": "ahmed_h",
    "password": "securePass123!",
    "is_staff": false
}
```

**Response** `201 Created`:
```json
"User Registered Successfully"
```

The password is automatically hashed via `create_user()`, and all fields are validated by `signUpSerializer` against the model's constraints.

---

### 2. User Login (Session-Based)

**Request:**
```http
POST /users/login/
Content-Type: application/json

{
    "username": "ahmed_h",
    "password": "securePass123!"
}
```

**Response** `201 Created`:
```json
{
    "message": "Login successful",
    "is_staff": false
}
```

A session cookie (`sessionid`) is set in the response headers. All subsequent authenticated requests include this cookie.

---

### 3. Browse the Book Catalog

**Request:**
```http
GET /books/get_book/
```

**Response** `200 OK`:
```json
[
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Software Engineering",
        "cover_url": "https://example.com/clean-code.jpg",
        "description": "A handbook of agile software craftsmanship.",
        "book_state": true
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "category": "Software Engineering",
        "cover_url": "https://example.com/pragmatic.jpg",
        "description": "Your journey to mastery.",
        "book_state": false
    }
]
```

`book_state: true` means available; `book_state: false` means currently borrowed.

---

### 4. Borrow a Book

**Request:**
```http
POST /users/borrow/?book_id=1
Cookie: sessionid=abc123...
```

**Response** `201 Created`:
```json
{
    "message": "Book borrowed successfully"
}
```

Behind the scenes:
1. The book's `book_state` is set to `False` (unavailable).
2. A new `UserBorrowedBook` record is created with the current timestamp.

If the book is already borrowed, the API returns `400`:
```json
{
    "error": "Book is not available"
}
```

---

### 5. Return a Borrowed Book

**Request:**
```http
DELETE /users/return/?book_id=1
Cookie: sessionid=abc123...
```

**Response** `200 OK`:
```json
{
    "message": "Book returned successfully"
}
```

The book's `book_state` is restored to `True`, and the `UserBorrowedBook` record is deleted.

---

### 6. Manage the Wishlist

**Add to wishlist:**
```http
POST /users/wishlist/?book_id=2
Cookie: sessionid=abc123...
```
```json
{ "message": "Book added to wishlist" }
```

**View wishlist:**
```http
GET /users/get_wishlist/
Cookie: sessionid=abc123...
```
```json
[
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "category": "Software Engineering",
        "cover_url": "https://example.com/pragmatic.jpg",
        "description": "Your journey to mastery.",
        "book_state": false
    }
]
```

**Remove from wishlist:**
```http
DELETE /users/remove_wishlist/?book_id=2
Cookie: sessionid=abc123...
```
```json
{ "message": "Book removed from wishlist" }
```

---

### 7. Admin: Add a New Book

**Request:**
```http
POST /books/add_book/
Cookie: sessionid=admin123...
Content-Type: application/json

{
    "title": "Design Patterns",
    "author": "Gang of Four",
    "category": "Software Engineering",
    "cover_url": "https://example.com/design-patterns.jpg",
    "description": "Elements of Reusable Object-Oriented Software."
}
```

**Response** `201 Created`:
```json
{
    "message": "Book added successfully"
}
```

The book is validated through `AddBookSerializer` and saved with `book_state` defaulting to `True`.

---

### 8. Admin: View All Users

**Request:**
```http
GET /dashboard/get_users/
Cookie: sessionid=admin123...
```

**Response** `200 OK`:
```json
[
    {
        "id": 1,
        "username": "ahmed_h",
        "email": "ahmed@example.com",
        "first_name": "Ahmed",
        "last_name": "Hassan"
    },
    {
        "id": 2,
        "username": "sara_k",
        "email": "sara@example.com",
        "first_name": "Sara",
        "last_name": "Khaled"
    }
]
```

---

*Built with Django & Django REST Framework*
