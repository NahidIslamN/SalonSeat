# SalonSeat

Django-based multi-vendor salon platform where salon owners create listings and professionals find jobs fast. Built with Django REST Framework + JWT, Celery + Redis for async processing, and Channels/WebSockets for real-time features.

## Tech
- Django, Django REST Framework
- JWT (SimpleJWT)
- Celery + Redis
- Channels + Redis (WebSocket)
- django-celery-beat

## API Design
- Listings CRUD (Salon Owner): [docs/listings_api_design.md](docs/listings_api_design.md)
