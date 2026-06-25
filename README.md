AutoRia Clone API

A modern, scalable REST API platform for automotive sales, built with Django and Django REST Framework. Supports
role-based access control, dealership management, premium analytics, automated ad moderation, currency conversion via
PrivatBank API, and real-time chat via WebSockets.



Tech Stack

| Layer                  | Technology                            |
|------------------------|---------------------------------------|
| Backend                | Django 6.0, Django REST Framework     |
| Database               | MySQL 8 (AWS RDS)                     |
| Cache / Message Broker | Redis (Alpine)                        |
| Task Queue             | Celery + Celery Beat                  |
| Real-time              | Django Channels + Daphne (WebSockets) |
| Web Server             | Nginx                                 |
| Containerization       | Docker, Docker Compose                |



Environment Setup

Create a `.env` file in the **root** of the project (next to `docker-compose.yml`) simillar to .env.example

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular
> password.


---

## Running the Project

### 1. Clone the repository

### 2. Create the `.env` file

Copy the template and fill in your values.

### 3. Build and start all containers

```bash
docker compose up --build
```

This single command will:

- Build the Docker image
- Start Redis, Nginx, App, Celery Worker, and Celery Beat
- Wait for the database to be ready
- Run all migrations automatically
- Load catalog fixtures (brands, models, cities, etc.)
- Seed forbidden words for ad moderation
- Fetch current exchange rates from PrivatBank API
- Start the ASGI server (Daphne)

### 4. Access the application

| Service         | URL                       |
|-----------------|---------------------------|
| API             | http://localhost/api/     |
| Swagger Docs    | http://localhost/api/doc/ |


---

## Docker Services

| Service       | Description                     | Port                  |
|---------------|---------------------------------|-----------------------|
| `app`         | Django/Daphne ASGI server       | 9999 (internal: 8000) |
| `redis`       | Message broker + Channels layer | 6379                  |
| `celery`      | Background task worker          | —                     |
| `celery-beat` | Scheduled task scheduler        | —                     |
| `web`         | Nginx reverse proxy             | 80                    |

---



## Creating the First Admin User

```bash
docker compose exec app python manage.py shell -c "
from apps.users.models import UserModel, ProfileModel
user = UserModel.objects.create_superuser(
    email='admin@example.com',
    password='Admin1234!',
    username='admin'
)
ProfileModel.objects.create(user=user, name='Admin', surname='Admin', age=30)
print('Admin created successfully!')
"
```

**Admin credentials for testing:**
| Field | Value |
|---|---|
| Email | `admin@example.com` |
| Password | `Admin1234!` |

---

## API Endpoints

###  Authentication — `/api/auth/`

| Method | Endpoint                      | Auth   | Description                |
|--------|-------------------------------|--------|----------------------------|
| POST   | `/api/auth/register/`         | No     | Register a new user        |
| POST   | `/api/auth/login/`            | No     | Login and get JWT tokens   |
| POST   | `/api/auth/refresh/`          | No     | Refresh access token       |
| PATCH  | `/api/auth/activate/<token>/` | No     | Activate account via email |
| POST   | `/api/auth/recovery/`         | No     | Request password recovery  |
| POST   | `/api/auth/recovery/<token>/` | No     | Set new password           |
| GET    | `/api/auth/socket/`           | Bearer | Get WebSocket token        |

**Register body:**

```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "username": "johndoe",
  "profile": {
    "name": "John",
    "surname": "Doe",
    "age": 25
  }
}
```

---

###  Users — `/api/users/`

| Method | Endpoint                       | Auth           | Description                 |
|--------|--------------------------------|----------------|-----------------------------|
| GET    | `/api/users/profile/`          | Bearer         | Get current user profile    |
| PATCH  | `/api/users/profile/`          | Bearer         | Update current user profile |
| POST   | `/api/users/managers/`         | Bearer (Admin) | Create a manager account    |
| PATCH  | `/api/users/<pk>/upgrade/`     | Bearer (Admin) | Change account type         |
| PATCH  | `/api/users/<pk>/change-role/` | Bearer (Admin) | Change user role            |

**Upgrade account body:**

```json
{
  "account_type": "Premium"
}
```

**Change role body:**

```json
{
  "role": "Seller"
}
```

> Available roles: `Buyer`, `Seller`, `Manager`, `Admin`

---

###  Ads — `/api/ads/`

| Method | Endpoint                    | Auth                   | Description                        |
|--------|-----------------------------|------------------------|------------------------------------|
| GET    | `/api/ads/`                 | No                     | List all active ads (with filters) |
| POST   | `/api/ads/`                 | Bearer                 | Create a new ad                    |
| GET    | `/api/ads/<pk>/`            | No                     | Get ad details (counts as a view)  |
| PATCH  | `/api/ads/<pk>/`            | Bearer                 | Update ad                          |
| DELETE | `/api/ads/<pk>/`            | Bearer                 | Delete ad                          |
| POST   | `/api/ads/<pk>/images/`     | Bearer                 | Upload image for ad                |
| GET    | `/api/ads/<pk>/statistics/` | Bearer (Premium)       | Get ad statistics                  |
| PATCH  | `/api/ads/<pk>/moderate/`   | Bearer (Manager/Admin) | Approve or reject ad               |

**Create ad body:**

```json
{
  "brand": "BMW",
  "car_model": "X5",
  "body_type": "SUV",
  "fuel_type": "Petrol",
  "transmission": "Automatic",
  "city": "Львів",
  "year": 2022,
  "mileage": 35000,
  "description": "Excellent condition, full service history.",
  "original_price": "45000.00",
  "original_currency": "USD"
}
```

> Available currencies: `USD`, `EUR`, `UAH`

**Filter ads (query params):**

```
GET /api/ads/?brand_filter=BMW
GET /api/ads/?city_filter=Київ
GET /api/ads/?price_filter_min=10000&price_filter_max=50000
GET /api/ads/?year_filter_min=2018&year_filter_max=2023
```

**Moderate ad body:**

```json
{
  "status": "Active"
}
```

> Available statuses for moderation: `Active`, `Rejected`

---

###  Dealerships — `/api/dealerships/`

| Method | Endpoint                           | Auth           | Description                                 |
|--------|------------------------------------|----------------|---------------------------------------------|
| GET    | `/api/dealerships/`                | Bearer         | List all dealerships                        |
| POST   | `/api/dealerships/`                | Bearer         | Create a dealership (creator becomes Owner) |
| GET    | `/api/dealerships/<pk>/`           | Bearer         | Get dealership details                      |
| PATCH  | `/api/dealerships/<pk>/`           | Bearer (Owner) | Update dealership                           |
| DELETE | `/api/dealerships/<pk>/`           | Bearer (Owner) | Delete dealership                           |
| GET    | `/api/dealerships/<pk>/employees/` | Bearer         | List employees                              |
| POST   | `/api/dealerships/<pk>/employees/` | Bearer (Owner) | Add employee                                |

**Add employee body:**

```json
{
  "user": 5,
  "role": "Sales"
}
```

> Available employee roles: `Owner`, `Sales`, `Mechanic`

---

###  Catalog — `/api/catalog/`

All catalog endpoints are public (no authentication required).

| Method | Endpoint                              | Description                             |
|--------|---------------------------------------|-----------------------------------------|
| GET    | `/api/catalog/brands/`                | List all car brands                     |
| GET    | `/api/catalog/car-models/`            | List all car models                     |
| GET    | `/api/catalog/body-types/`            | List body types                         |
| GET    | `/api/catalog/fuel-types/`            | List fuel types                         |
| GET    | `/api/catalog/transmissions/`         | List transmission types                 |
| GET    | `/api/catalog/regions/`               | List Ukrainian regions                  |
| GET    | `/api/catalog/cities/`                | List Ukrainian cities                   |
| POST   | `/api/catalog/missing-brand-request/` | Request a missing brand (auth required) |

---

###  WebSocket Chat — `ws://localhost/api/chat/<room>/`

**Step 1:** Get a socket token

```
GET /api/auth/socket/
Authorization: Bearer <access_token>
```

**Step 2:** Connect via WebSocket

```
ws://localhost/api/chat/general/?token=<socket_token>
```

**Step 3:** Send a public message

```json
{
  "action": "send_message",
  "request_id": "1",
  "data": {
    "text": "Hello everyone!"
  }
}
```

**Send a private message (buyer → seller):**

```json
{
  "action": "send_private_message",
  "request_id": "2",
  "data": {
    "userId": 5,
    "adId": 3,
    "text": "Is this car still available?"
  }
}
```

---

## Business Logic

### Roles

| Role      | Description                                     |
|-----------|-------------------------------------------------|
| `Buyer`   | Browse platform, contact sellers                |
| `Seller`  | Create and manage car listings                  |
| `Manager` | Moderate ads, ban users (created by Admin only) |
| `Admin`   | Full access to everything                       |

### Account Types

| Type      | Ad Limit  | Statistics |
|-----------|-----------|------------|
| `Basic`   | 1 ad      | No         |
| `Premium` | Unlimited | Yes        |

### Ad Moderation Flow

1. Ad created → status: `Pending`
2. Celery worker checks for forbidden words automatically
3. No bad words → status: `Active` 
4. Bad words found → edit attempts counter incremented
5. After 3 failed attempts → status: `Manager_review`, email sent to all managers
6. Manager reviews and sets: `Active` or `Rejected`

### Currency Conversion

- Prices are stored in USD, EUR, and UAH simultaneously
- Rates are fetched from **PrivatBank API** daily at **06:00 UTC**
- All existing ad prices are recalculated automatically on each update

---


## Notes

- The MySQL database is hosted on **AWS RDS** — no local DB container needed
- On first startup, catalog data (brands, models, cities) is loaded automatically
- Forbidden words for moderation are seeded automatically on startup
- Exchange rates are fetched from PrivatBank on every startup and daily at 06:00 UTC
- Socket tokens expire after **1 hour** — get a new one if disconnected