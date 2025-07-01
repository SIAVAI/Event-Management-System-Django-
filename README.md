# Event Management System (Django)

A robust and user-friendly web application built with Django, designed for efficient management of events, participants, and categories. This system provides a comprehensive platform for event organizers to plan, track, and analyze their events, while offering a clear interface for participants.

## ✨ Live Demo

Experience the application live:
[https://event-management-system-django-huow.onrender.com/](https://event-management-system-django-huow.onrender.com/)

## 🚀 Features

* **Event CRUD:** Create, Read, Update, and Delete events with detailed information including name, description, date, time, location, and category.
* **Participant Management:** Register and manage participants for each event.
* **Category Management:** Organize events by custom categories (e.g., "Conference," "Workshop," "Webinar").
* **Comprehensive Search & Filtering:**
    * Search events by `name` or `location` using a flexible `icontains` query.
    * Filter events by `category`.
    * Filter events by `date range` (start date, end date, or both).
* **Event Status Indicators:** Visually distinguish between "Upcoming," "Upcoming Today," and "Past Event" directly in the event listings.
* **Organizer Dashboard:**
    * A dedicated dashboard providing key statistics: Total Events, Upcoming Events, Past Events, and Total Registered Participants.
    * Interactive list of events on the dashboard, filterable by "All," "Upcoming," "Past," or "Today."
* **Responsive Design:** Built with **Tailwind CSS** for a modern, mobile-first, and responsive user interface.
* **Database Efficiency:** Utilizes `select_related` and `prefetch_related` for optimized database queries (reducing N+1 problems) and `annotate` for efficient participant counts.
* **Debug Toolbar:** Integrated `django-debug-toolbar` for development-time performance monitoring and debugging.

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Database:** PostgreSQL (or SQLite for development)
* **Frontend:** HTML, Tailwind CSS, Django Templates
* **Deployment:** Render.com (as indicated by the live link)
* **Package Management:** pip, virtual environments

### Prerequisites

* Python 3.8+
* pip (Python package installer)
* Node.js & npm (for Tailwind CSS compilation)


## ⚙️ Configuration

* **`settings.py`**: Main Django settings.
* **`urls.py`**: Project-level URL routing.
* **`events/` app**: Contains models, views, forms, and templates for event management.
* **`tailwind.config.js`**: Tailwind CSS configuration, including paths for scanning templates.

## 🤝 Contributing

Feel free to fork the repository, create pull requests, or open issues if you find any bugs or have feature suggestions.
