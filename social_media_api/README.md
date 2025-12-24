Social Media API
=================

**Description:**
- A small Django + DRF project implementing a social media API with Users, Posts, Comments, Likes, Follows and Notifications.

**Quick Start:**
- Create and activate a Python virtualenv, then install dependencies (example):

```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

- Run migrations and start the dev server:

```
python manage.py migrate
python manage.py runserver
```

**Authentication:**
- The project uses token-based authentication. Simple JWT authentication is available in some views; include an `Authorization: Bearer <token>` header for endpoints that require JWT.

**Endpoints (top-level):**
- **Admin:** `GET/POST` : `/admin/`

**Accounts (`/api/accounts/`):**
- **Register:** `POST` : `/api/accounts/register/` — create a user.
- **Login:** `POST` : `/api/accounts/login/` — obtain token and user info.
- **Follow:** `POST` : `/api/accounts/follow/<int:user_id>/` — follow user with id `user_id`.
- **Unfollow:** `POST` : `/api/accounts/unfollow/<int:user_id>/` — unfollow user with id `user_id`.

**Posts & Comments (`/api/`):**
- **Post list/create:** `GET/POST` : `/api/posts/`
- **Post detail/update/delete:** `GET/PATCH/DELETE` : `/api/posts/<int:pk>/`
- **Feed:** `GET` : `/api/feed/` — posts from users you follow (most recent first), paginated.
- **Like post:** `POST` : `/api/posts/<int:pk>/like/`
- **Unlike post:** `POST` : `/api/posts/<int:pk>/unlike/`

- **Comment list/create:** `GET/POST` : `/api/comments/`
- **Comment detail/update/delete:** `GET/PATCH/DELETE` : `/api/comments/<int:pk>/`

**Notifications (`/notifications/`):**
- **List notifications:** `GET` : `/notifications/` — unread shown first, includes `actor_avatar` and `time_since` fields.
- **Unread notifications:** `GET` : `/notifications/unread/` — newest unread first.
- **Unread count:** `GET` : `/notifications/unread_count/` — returns `{"unread_count": <int>}`.
- **Mark read:** `POST` : `/notifications/<int:pk>/mark_read/` — mark a notification as read.

**Behavior notes:**
- Like endpoints prevent duplicate likes and create a `Notification` for the post author when a new like occurs.
- Comment creation notifies the post author.
- Following a user creates a `Notification` for the followed user.
- `Feed` returns posts by users in your `following` relationship, ordered by `created_at` descending.

**Tests:**
- Run app tests with:

```
python manage.py test
```

**Recommended next steps / improvements:**
- Add a DB-level unique constraint on `Like` to enforce uniqueness at the database level.
- Add pagination settings or tune `PAGE_SIZE` in `settings.py`.
- Add frontend-friendly serializers (already included: `actor_avatar`, `time_since`).

**Files of interest:**
- `accounts/views.py`, `accounts/urls.py`
- `posts/views.py`, `posts/urls.py`
- `notifications/views.py`, `notifications/serializers.py`, `notifications/urls.py`
