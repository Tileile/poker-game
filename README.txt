# Poker Game

A web-based Poker game built with Python (Flask) and JavaScript.

## Features
- Play Poker against bots
- Dynamic card rendering
- Flask backend
- HTML, CSS, JavaScript frontend

---

## Project Structure
```
project-root/
├── main.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── index.html
├── venv/ (optional)
└── README.md
```

---

## Setup

### 1. Clone repository
```
git clone <repo-url>
cd <project-folder>
```

### 2. Create virtual environment
```
python -m venv venv
```

### 3. Activate virtual environment (Windows PowerShell)
```
.\venv\Scripts\Activate
```

### 4. Install dependencies
```
pip install Flask flask-cors
```

Or:
```
pip install -r requirements.txt
```

### 5. Run the app
```
python main.py
```

### 6. Open in browser
```
http://127.0.0.1:5000/
```

---

## Notes
- Static files must be in `static/`
- Templates must be in `templates/`
- Use `url_for('static', filename='...')` for static paths

---

## License
Educational project