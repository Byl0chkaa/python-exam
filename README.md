AutoRia Clone API
A modern, scalable platform for automotive sales, featuring support for dealerships, premium analytics for users, and real-time chat.

Tech Stack
Framework: Django 6.0, Django Rest Framework
Real-time: Django Channels (WebSockets)
Task Queue: Celery + Redis (currency updates, moderation)
Infrastructure: Docker, Docker Compose, Nginx


Getting Started
The project is fully containerized. Ensure you have Docker installed.

Environment Variables:
Create a .env file in the root directory based on .env.example.



Run the project:

Bash
docker-compose up -d --build
Access API:
The API will be available at http://localhost:8888/



API Documentation
After launching the project, you can explore the API endpoints and test them directly via:
Swagger: http://localhost:8888/swagger/


Core Business Logic
Automated Moderation: Ads containing prohibited content are automatically rejected by a Celery worker. After 3 failed attempts, a notification email with a direct link to the moderation panel is sent to the managers.
Currency Conversion: Prices are automatically recalculated daily at 06:00 AM using the PrivatBank API.
Premium Analytics: Exclusive features for Premium accounts, including view counts and average market price analysis (by region and nationwide).