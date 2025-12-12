
# 📘 Social Media API — Posts & Comments Documentation

This section documents all available endpoints for interacting with **Posts** and **Comments** in the Social Media API.  
All endpoints require **Token Authentication** unless otherwise stated.

---

# 🔐 Authentication

Include your token in the header:

```
Authorization: Token <your_token>
```

---

# 📝 Posts API

## ✅ List All Posts
**GET** `/api/posts/`

### Example Response
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "amos",
      "title": "My First Post",
      "content": "Hello world!",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z",
      "comments": []
    }
  ]
}
```

---

## ✅ Create a Post
**POST** `/api/posts/`

### Request Body
```json
{
  "title": "New Post",
  "content": "This is my content"
}
```

### Example Response
```json
{
  "id": 3,
  "author": "amos",
  "title": "New Post",
  "content": "This is my content",
  "created_at": "2025-01-12T10:00:00Z",
  "updated_at": "2025-01-12T10:00:00Z",
  "comments": []
}
```

---

## ✅ Retrieve a Single Post
**GET** `/api/posts/<id>/`

---

## ✅ Update a Post (Author Only)
**PUT** `/api/posts/<id>/`

### Request Body
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

---

## ✅ Partial Update a Post
**PATCH** `/api/posts/<id>/`

---

## ✅ Delete a Post (Author Only)
**DELETE** `/api/posts/<id>/`

---

# 💬 Comments API

## ✅ List All Comments
**GET** `/api/comments/`

---

## ✅ Create a Comment
**POST** `/api/comments/`

### Request Body
```json
{
  "post": 1,
  "content": "Nice post!"
}
```

### Example Response
```json
{
  "id": 5,
  "post": 1,
  "author": "amos",
  "content": "Nice post!",
  "created_at": "2025-01-12T10:30:00Z",
  "updated_at": "2025-01-12T10:30:00Z"
}
```

---

## ✅ Retrieve a Single Comment
**GET** `/api/comments/<id>/`

---

## ✅ Update a Comment (Author Only)
**PUT** `/api/comments/<id>/`

---

## ✅ Delete a Comment (Author Only)
**DELETE** `/api/comments/<id>/`

---

# 🔍 Searching Posts

You can search posts by **title** or **content**:

```
GET /api/posts/?search=django
```

---

# 📄 Pagination

All list endpoints return paginated results:

```
GET /api/posts/?page=2
```

---

# ✅ Summary of Features

| Feature | Supported |
|--------|-----------|
| Create posts | ✅ |
| Edit/delete own posts | ✅ |
| Comment on posts | ✅ |
| Edit/delete own comments | ✅ |
| Pagination | ✅ |
| Search posts | ✅ |
| Token authentication | ✅ |
| ViewSets + Routers | ✅ |

---

