# 🛡 Secure Docs

**Secure Docs** is a modern, responsive digital document locker built using **Django**.  
It allows users to securely upload, organize, preview, download, and manage important documents with a clean UI optimized for both **desktop and mobile**.

---

## 🚀 Features

- 🔐 Secure user authentication (login / logout)
- 📁 Upload & manage documents
- 👁 Preview documents
- ⬇ Download documents
- 🗑 Single & **multiple delete** support
- 🏷 Category-based filtering
- 🔍 Search documents
- 📱 Fully responsive (mobile & desktop)
- 🎨 Modern glassmorphism UI
- 🛡 Custom 404 & 500 error pages
- 🌙 Dark-themed professional design

---

## 🖼 UI Highlights

- Custom **CSS shield brand icon**
- Mobile slide sidebar navigation
- Dropdown menus with proper stacking
- Toast notifications
- Bulk action bar for multi-delete

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Bootstrap 5 + Custom CSS
- **Database:** SQLite (default, can be changed)
- **Icons:** Custom CSS / SVG (no heavy icon libraries)

---

## 📂 Project Structure

```text
secure-docs/
├── manage.py
├── README.md
├── requirements.txt
├── locker/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── templates/
├── templates/
│   ├── 404.html
│   └── 500.html
├── static/
│   └── locker/
│       ├── css/
│       │   └── style.css
│       └── favicon.svg
└── db.sqlite3
