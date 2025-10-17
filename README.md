📚 Student Event Manager API
🌟 Project Overview
The Student Event Manager is a web application designed to help university students easily discover and register for academic and interest-based events relevant to their major. The platform ensures students don't miss out on valuable opportunities that align with their career goals and passions.


This repository contains the backend API built using Django and Django REST Framework (DRF).

🛠️ Technology Stack
Backend Framework: Python (3.11+) and Django (5.x)

API Framework: Django REST Framework (DRF)

Database: SQLite (development) or PostgreSQL (production)

Authentication: Token-based Authentication (DRF's authtoken)

✨ Key Features
The API supports a role-based system differentiating between Students and Organizers.

1. User Management & Authentication 


Role-Based Registration: Supports sign-up for both Students (requires major) and Organizers (requires organization_name).




Login/Logout: Authenticates users and issues secure tokens.


Profile Management: Users can view and update their profile details.


2. Event Management (CRUD) 


Event Listing: Anyone can view the list of events.



Filtering: Events can be filtered by category (major) and date.


Organizer Panel: Organizers can create, update, and delete their own events.





Social Integration (Future): Events support Likes and Comments for community engagement.

3. Event Registration (Student Only) 


Registration: Students can register for an event using the event ID.



Dashboard View: Students can view a list of all their registered events.


Cancellation: Students can cancel their registration.

⚙️ Setup and Installation
Follow these steps to get the project running locally.

Prerequisites
Python 3.11+

pip (Python package installer)

Installation Steps
Clone the repository:

Bash

git clone [Your GitHub Repo URL]
cd student_event_manager
Create and activate a virtual environment:

Bash

python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/macOS
Install dependencies:

Bash

pip install -r requirements.txt
# OR: pip install django djangorestframework django-filter [etc.]
Run Migrations:

Bash

python manage.py migrate
Create a Superuser (Optional, for Admin Access):

Bash

python manage.py createsuperuser
Run the development server:

Bash

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

🔗 API Endpoints
All endpoints are prefixed with /api/.

Feature	HTTP Method	Endpoint	Access	Description
Register	POST	/api/users/register/	Public	
Register as Student or Organizer.

Login	POST	/api/users/login/	Public	
Authenticate and return token.

Profile	GET, PUT	/api/users/profile/	Auth Required	
View/Update authenticated user's profile.


Events	GET, POST	/api/events/	Public (GET)	
List all events. Create new event (Organizer only).


Event Detail	GET, PUT, DELETE	/api/events/{id}/	Public (GET)	
View details. Update/Delete event (Owner Organizer only).



Register	POST	/api/registrations/	Student Only	
Register for an event.

My Registrations	GET	/api/registrations/	Student Only	
View registered events list.

Cancel Reg.	DELETE	/api/registrations/{id}/cancel/	Student Only	
Cancel registration.


Export to Sheets
🧪 Testing the API
We recommend using Postman or Insomnia to test the API endpoints.

Obtain Token: Use POST /api/users/login/ to get an authentication token.

Use Token: For protected endpoints (Auth Required), set the request header:
Authorization: Token <Your Auth Token>
