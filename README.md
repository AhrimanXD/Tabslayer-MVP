Here's a `README.md` template that provides API documentation for frontend developers who want to integrate your Flask-based category and resource management backend:

---

# 📚 KnowledgeBase API

A RESTful API built with Flask for managing categorized learning resources. Frontend developers can use this API to create and retrieve categories and associated resources. JWT authentication is required for all protected endpoints.

---

## 🚀 Getting Started

### Base URL

```
http://<your-domain>/api
```

Make sure to include the `Authorization: Bearer <JWT>` header for all secured endpoints.

---

## 🔐 Authentication

**Login and registration routes are handled separately.** Ensure your frontend obtains a JWT token for the user, which is required to access the endpoints listed below.

---

## 📁 Categories

### Create Category

**POST** `/category`

```json
Headers: { Authorization: Bearer <JWT> }

Body:
{
  "title": "Frontend Tools",
  "description": "Collection of frontend libraries and frameworks"
}
```

**Response:**

```json
{
  "message": "Category 'Frontend Tools' created",
  "data": { ... }
}
```

---

### Get All Categories

**GET** `/category`

```json
Headers: { Authorization: Bearer <JWT> }
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Frontend Tools",
    "description": "Collection of frontend libraries and frameworks"
  }
]
```

---

### Get Specific Category

**GET** `/category/<cat_id>`

```json
Headers: { Authorization: Bearer <JWT> }
```

---

### Update Category

**PUT** `/category/<cat_id>`

```json
Headers: { Authorization: Bearer <JWT> }

Body:
{
  "title": "Updated Title",
  "description": "Updated Description"
}
```

---

### Delete Category

**DELETE** `/category/<cat_id>`

```json
Headers: { Authorization: Bearer <JWT> }
```

---

## 🔗 Resources

### Create Resource

**POST** `/resource`

```json
Headers: { Authorization: Bearer <JWT> }

Body:
{
  "title": "React Docs",
  "link": "https://react.dev",
  "description": "Official documentation",
  "category_id": 1
}
```

---

### Get Specific Resource

**GET** `/resource/<resource_id>`

```json
Headers: { Authorization: Bearer <JWT> }
```

---

### Update Resource

**PUT** `/resource/<resource_id>`

```json
Headers: { Authorization: Bearer <JWT> }

Body:
{
  "title": "React Documentation",
  "link": "https://react.dev",
  "description": "Updated",
  "category_id": 2
}
```

---

### Delete Resource

**DELETE** `/resource/<resource_id>`

```json
Headers: { Authorization: Bearer <JWT> }
```

---

## 🛠️ Tech Stack

* Flask
* Flask-JWT-Extended
* SQLAlchemy

---

## 🧠 Notes

* All categories and resources are user-scoped.
* Ensure the JWT token is sent in the Authorization header.
* Category and resource updates are only permitted by their owners.

---

