# Blog App — README

This `blog` app includes recent feature additions for user authentication, profile management, and full CRUD for blog posts. This document summarizes what was added and how to run and test the features locally.

## What was added

- Post model (`blog/models.py`)
  - `title` (CharField)
  - `content` (TextField)
  - `published_date` (DateTimeField, auto_now_add=True)
  - `author` (ForeignKey to Django `User`)

- Profile model
  - `Profile` (OneToOne with `User`) with `bio` and `avatar` (ImageField)
  - Signal to create/update profile automatically when a `User` is saved

- Authentication
  - `CustomUserCreationForm` extends `UserCreationForm` to include `email`
  - Views: login (built-in `LoginView`), logout (built-in `LogoutView`), `register`, and `profile` (edit account + avatar)
  - Templates: `blog/templates/blog/login.html`, `register.html`, `logout.html`, `profile.html`

- Blog CRUD (class-based views)
  - `PostListView` — lists posts (paginated)
  - `PostDetailView` — shows single post
  - `PostCreateView` — authenticated users can create posts (author auto-assigned)
  - `PostUpdateView` — only post authors may edit (ownership check)
  - `PostDeleteView` — only post authors may delete (ownership check)
  - Form: `PostForm` (ModelForm for `Post` with `title` and `content`)
  - Templates: `post_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`

- URLs
  - `blog/urls.py` includes routes for login, logout, register, profile, and all post CRUD operations
  - Project `urls.py` includes `blog.urls` and serves `MEDIA_URL` in DEBUG

- Static & Templates config
  - `settings.py` updated: `TEMPLATES['DIRS']` includes project-level `templates/`
  - Static files organized under `blog/static/blog/` and referenced with `{% static 'blog/css/style.css' %}`
  - `STATIC_ROOT`, `STATICFILES_DIRS`, and `MEDIA_ROOT` use `BASE_DIR / '...'` style

- Admin
  - `Post` and `Profile` registered in admin with useful `list_display`, `search_fields`, and filters

## Files added/modified (high level)
- `blog/models.py` — Post, Profile (+ signals)
- `blog/forms.py` — `CustomUserCreationForm`, `UserUpdateForm`, `ProfileForm`, `PostForm`
- `blog/views.py` — auth views, profile view, CRUD class-based views
- `blog/urls.py` — auth + CRUD routes
- `blog/templates/blog/` — all templates (base, auth, profile, and CRUD templates)
- `blog/static/blog/` — `css/style.css`, `js/script.js`
- `blog/admin.py` — model registrations
- `django_blog/settings.py` — static & media settings, templates config
- `django_blog/urls.py` — includes `blog.urls` and serves media in DEBUG

## Local setup / quick start
1. Activate your virtualenv (example PowerShell):

```powershell
& C:/Users/Amos/Alx_DjangoLearnLab/django_blog/.venv/Scripts/Activate.ps1
```

2. Install dependencies (if not already):

```powershell
pip install -r requirements.txt
# Ensure Pillow for ImageField and psycopg2-binary for PostgreSQL if needed
pip install Pillow psycopg2-binary
```

3. (Optional) Configure PostgreSQL — if you will use Postgres, set DB env vars in project `.env`:

```
DB_NAME=django_blog_db
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Make and run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser and run server:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

6. Visit the site:
- Home / posts: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Login: `http://127.0.0.1:8000/login/`

## Permission notes
- Creating posts: any authenticated user (LoginRequiredMixin)
- Editing & deleting posts: enforced ownership check via `UserPassesTestMixin.test_func()` (only `post.author` may edit/delete)
- You can extend `test_func()` to allow staff/superuser edits by checking `user.is_staff` or `user.is_superuser`.

## Testing & Debugging tips
- If static files not showing, run `python manage.py collectstatic` (for production) or confirm `STATICFILES_DIRS` and `STATIC_URL` in `settings.py` during development.
- For avatar/image upload issues, ensure `MEDIA_ROOT` and `MEDIA_URL` are set and `MEDIA_URL` served during DEBUG (already included in project `urls.py`).
- If using PostgreSQL, ensure `psycopg2-binary` is installed and DB creds in `.env` are correct.

## Next improvements (ideas)
- Add unit tests for ownership permissions and view responses.
- Add comments and tagging for posts, or allow drafts vs published states.
- Add richer profile fields (social links) and image resizing on upload.

If you want, I can also:
- Create a short test suite to assert ownership rules for update/delete operations.
- Add staff/superuser editing support to `test_func()`.
- Run migrations and start the dev server for you.

---
Generated on 2025-12-06 — if you want the README updated with more detail or project-specific instructions, tell me what to include.
