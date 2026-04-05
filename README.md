# 🚆 Train Ticket Application

A full-stack web application for managing train ticket bookings, built with **Django (Python)** using **Agile Scrum** methodology across 2 sprints.

---

## 📋 Project Overview

The Train Ticket Application is a web-based platform that allows users to search for trains, book tickets, manage reservations, and handle payments — similar to IRCTC. It includes a full admin panel for managing users and KYC approvals.

---

## ✅ Features

### Sprint 1 — Foundation
- 🔐 User Registration, Login & Logout with session timeout
- 👤 Profile Management with KYC document upload (ID & Address Proof)
- 💰 Wallet Management — add money from Savings Account or Credit Card
- 🎫 Booking History — view past reservations and details
- 🛡️ Admin Dashboard — manage users and approve KYC
- 🔒 Role-Based Access Control (Admin vs Regular User)
- 🚫 Custom 404 & 500 Error Pages

### Sprint 2 — Reservation & Payment
- 🔍 Train Search — filter by route, date, class, and passengers
- 🎟️ Book a Train — full booking flow with seat management
- 💳 Multiple Payment Methods — Wallet, Savings Account, Credit Card
- 💸 Partial Payment — split fare between wallet and another source
- ❌ Cancel Booking — automatic full refund to wallet
- 📅 Change Journey Date — reschedule with train availability check
- ⭐ Post-Booking Feedback — star rating with comments

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.x (Python) |
| Frontend | Django Templates (HTML5, CSS3) |
| Database | SQLite (Development) |
| Authentication | Django Auth + Custom Session Management |
| File Uploads | Django FileField + Pillow |
| Version Control | Git + GitHub |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/gsahoo211004/Train-Ticket-App.git
cd Train-Ticket-App
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install django pillow
```

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Seed train data**
```bash
python manage.py seed_trains
```

**6. Create a superuser**
```bash
python manage.py createsuperuser
```

**7. Run the development server**
```bash
python manage.py runserver
```

**8. Open in browser**
```
http://127.0.0.1:8000/
```

---

## 🔑 Make Yourself an Admin

After registering, run this in the Django shell to give yourself admin access:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from accounts.models import Profile

u = User.objects.get(username='your_username')
u.profile.role = 'admin'
u.profile.save()
exit()
```

Then visit: `http://127.0.0.1:8000/accounts/admin-dashboard/`

---

## 📁 Project Structure

```
train_ticket_app/
├── train_ticket/          # Project settings and URLs
├── accounts/              # Auth, Profile, KYC, Admin
├── wallet/                # Wallet and Payment Sources
├── bookings/              # Trains, Bookings, Search, Feedback
│   └── management/
│       └── commands/
│           └── seed_trains.py
├── templates/             # Base template, Error pages
└── manage.py
```

---

## 📱 App Pages

| URL | Page |
|-----|------|
| `/` | Redirects to Login |
| `/accounts/login/` | Login Page |
| `/accounts/register/` | Register Page |
| `/accounts/dashboard/` | User Dashboard |
| `/accounts/profile/` | Profile Management |
| `/accounts/admin-dashboard/` | Admin Panel |
| `/wallet/` | Wallet & Payment Sources |
| `/bookings/` | Booking History |
| `/bookings/search/` | Search Trains |
| `/bookings/book/<id>/` | Book a Train |
| `/bookings/<id>/` | Booking Detail |
| `/bookings/<id>/cancel/` | Cancel Booking |
| `/bookings/<id>/change-date/` | Change Journey Date |
| `/bookings/<id>/feedback/` | Submit Feedback |
| `/admin/` | Django Admin Panel |

---

## 🗓️ Sprint Summary

| Sprint | Period | Focus | Status |
|--------|--------|-------|--------|
| Sprint 1 | Jan 22 – Mar 10, 2026 | Auth, Profile, Wallet, Booking History | ✅ Complete |
| Sprint 2 | Mar 11 – Apr 5, 2026 | Search, Booking, Payment, Cancel, Feedback | ✅ Complete |

---

## 📄 License

This project was developed as part of an academic Agile Scrum exercise.