Perfect ✅

Let’s merge **everything** — your working codebase (Users, Events, Registrations apps) and the planning documents (Part 1 + Part 2 PDFs) — into a **complete, professional README.md**.

---

# 📚 Student Event Manager API

A **Django + Django REST Framework (DRF)** project that helps **university students** discover, register for, and manage events related to their academic majors and interests — while enabling **organizers** to host and manage events.

---

## 🌟 Project Overview

**Student Event Manager** bridges the gap between students and relevant academic or extracurricular opportunities.
It allows:

* 🧑‍🎓 **Students** → to find and register for events aligned with their major.
* 🧑‍💼 **Organizers** → to create and manage their own events.

---

## 🛠️ Technology Stack

| Layer            | Technology                                              |
| ---------------- | ------------------------------------------------------- |
| Language         | Python 3.11 +                                           |
| Framework        | Django 5.x                                              |
| API              | Django REST Framework (DRF)                             |
| Database         | SQLite (for development) / PostgreSQL (for production)  |
| Auth             | Token-based Authentication (`rest_framework.authtoken`) |
| Filtering/Search | `django-filter`, DRF Search Filter, Ordering Filter     |
| Frontend         | HTML Templates (for login, registration, dashboard)     |

---

## ✨ Core Features

### 🔐 User Management & Authentication

* **Role-based signup** for:

  * **Students** → requires `major`
  * **Organizers** → requires `organization_name`
* **Login / Logout**
* **Profile Management** (view & update)
* Token authentication via DRF AuthToken.

### 🎫 Event Management

* **CRUD** (Create, Read, Update, Delete) for Events
* **Filtering & Search** by `category`, `date`, `location`
* **Organizer permissions** → only event owners can edit/delete
* **Social integration (future)** → Likes and Comments

### 🧾 Event Registration (Student-Only)

* Students can:

  * **Register** for events (using event ID)
  * **List** their registered events in a personal dashboard
  * **Cancel** registrations
* Prevents duplicate registrations.

---

## 🧩 Project Structure

| App              | Purpose                                                         |
| ---------------- | --------------------------------------------------------------- |
| **users**        | Authentication, roles (Student / Organizer), profile management |
| **events**       | Event CRUD, filtering, likes/comments                           |
| **registration** | Track student registrations, cancel registrations               |

---

## 🗃️ Database Schema (Simplified)

### `CustomUser`

* `id`, `name`, `email`, `password`
* `role` = [`student`, `organizer`]
* `major` (for students)
* `organization_name` (for organizers)

### `Event`

* `id`, `title`, `description`, `location`
* `date`, `end_date`, `category`
* `organizer` (FK → User)
* `likes`, `comments` (related fields)

### `Registration`

* `id`, `user` (FK → User)
* `event` (FK → Event)
* `timestamp`

---

## 🔗 API Endpoints

All API routes are prefixed with `/api/`.

### 👥 Authentication & User Management

| Method    | Endpoint               | Access        | Description                     |
| --------- | ---------------------- | ------------- | ------------------------------- |
| POST      | `/api/users/register/` | Public        | Register (Student or Organizer) |
| POST      | `/api/users/login/`    | Public        | Login & return token            |
| GET       | `/api/users/profile/`  | Auth Required | Retrieve user profile           |
| PUT/PATCH | `/api/users/profile/`  | Auth Required | Update profile                  |

**Example Bodies:**

```json
// Student
{
  "role": "student",
  "name": "Sara",
  "email": "sara@email.com",
  "password": "123456",
  "major": "CS"
}

// Organizer
{
  "role": "organizer",
  "name": "Tech Club",
  "email": "club@email.com",
  "password": "123456",
  "organization_name": "Tech Hub"
}
```

---

### 🎟️ Events (Organizer & Public)

| Method    | Endpoint            | Access         | Description                             |
| --------- | ------------------- | -------------- | --------------------------------------- |
| GET       | `/api/events/`      | Public         | List events (+ filter by category/date) |
| GET       | `/api/events/{id}/` | Public         | View event details                      |
| POST      | `/api/events/`      | Organizer Only | Create a new event                      |
| PUT/PATCH | `/api/events/{id}/` | Organizer Only | Update owned event                      |
| DELETE    | `/api/events/{id}/` | Organizer Only | Delete owned event                      |

**POST Example**

```json
{
  "title": "Hackathon 2025",
  "description": "24-hour coding challenge",
  "location": "Tech Hall",
  "category": "Technology",
  "date": "2025-11-01T09:00:00Z",
  "end_date": "2025-11-02T09:00:00Z"
}
```

---

### 🧍‍♀️ Registrations (Student Only)

| Method | Endpoint                          | Access       | Description                       |
| ------ | --------------------------------- | ------------ | --------------------------------- |
| POST   | `/api/registrations/`             | Student Only | Register for event via `event_id` |
| GET    | `/api/registrations/`             | Student Only | View registered events            |
| DELETE | `/api/registrations/{id}/cancel/` | Student Only | Cancel registration               |

**POST Example**

```json
{
  "event_id": 3
}
```

---



The API is now available at [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)

---

## 🧪 Testing the API (Postman)

1. **Register a User**

   * POST → `/api/users/register/`
   * Body → Student or Organizer payload

2. **Login to Get Token**

   * POST → `/api/users/login/`
   * Copy the returned `token`

3. **Authenticate Requests**

   * In Postman, add header:
     `Authorization: Token <your_token_here>`

4. **Create Events** (as Organizer)

5. **Register for Events** (as Student)

6. **Cancel a Registration**

---

## 🧭 Project Timeline

| Part   | Focus                                               |
| ------ | --------------------------------------------------- |
| Part 1 | Idea & Planning                                     |
| Part 2 | Design (ERD + API Endpoints)                        |
| Part 3 | Setup Django Project & Models                       |
| Part 4 | Implement CRUD & Role Permissions                   |
| Part 5 | Final Testing & Documentation (Demo Video + README) |

---

## 🚀 Future Enhancements

* 📍 Google Maps API integration (for event locations)
* 📅 Google Calendar API (sync event dates)
* ❤️ Likes & 💬 Comments system
* 📧 Email notifications for upcoming events
* 📊 Admin analytics dashboard

---

## 👨‍💻 Author

**Sedrah Mourad**
ALX Back End Track
*Student Event Manager Capstone Project*