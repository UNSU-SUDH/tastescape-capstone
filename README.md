# 🍽️ TasteScape - Capstone Project

**TasteScape** is a full-stack restaurant review platform built as a capstone project by Sudhanshu (IIT Patna). It allows users to explore restaurants, add reviews, and discover popular dishes.

---

## 👨‍🎓 Project Overview
- **Project Type**: BSc Capstone Project (IIT Patna)
- **Developer**: Sudhanshu
- **Stack**: React (Frontend), Flask (Backend), MySQL (Database)
- **Purpose**: Demonstrate full-stack development skills through a real-world web application

---

## 🛠️ Technologies Used
- **Frontend**: React, Axios, HTML, CSS
- **Backend**: Flask, Flask-CORS
- **Database**: MySQL (Local)

---

## 🔧 Features
- View list of restaurants with average ratings
- Add new restaurants
- View reviews for each restaurant
- Add new reviews with star ratings and comments
- View popular dishes with prices and ratings

---

## 📁 Folder Structure
```
TasteScape/
├── backend/              # Flask backend (API layer)
│   ├── app.py
│   └── requirements.txt
├── tastescape-frontend/  # React frontend
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── App.css
│   └── package.json
├── tastescape_schema.sql # MySQL schema (setup file)
└── README.md             # Project documentation
```

---

## 🚀 Local Setup Guide

### 🔹 1. Set Up MySQL
1. Open MySQL Workbench or terminal
2. Import the schema:
```bash
mysql -u root -p < tastescape_schema.sql
```

### 🔹 2. Run the Backend (Flask)
```bash
cd backend
python -m venv venv
venv\Scripts\activate   
pip install -r requirements.txt
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
> Backend will run on: http://localhost:5000

### 🔹 3. Run the Frontend (React)
```bash
cd tastescape-frontend
npm install
npm start
```
> Frontend will run on: http://localhost:3000

### ⚠️ Proxy Setup
Ensure `package.json` inside `tastescape-frontend` has:
```json
"proxy": "http://localhost:5000"
```

---

## 🗃️ Database Tables

```sql
CREATE DATABASE tastescape;
USE tastescape;

CREATE TABLE restaurants (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  rating FLOAT DEFAULT 0
);

CREATE TABLE reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  restaurant_id INT,
  user VARCHAR(255),
  rating FLOAT,
  comment TEXT,
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE dishes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  price DECIMAL(10,2),
  rating FLOAT
);
```

## 📦 Future Improvements
- User authentication (login/signup)
- Image upload for dishes and restaurants
- Filter reviews by rating/date
- Responsive design (mobile friendly)
- Deployment to Netlify (frontend) & Render (backend)

---

## 🧑‍💻 Author
**Sudhanshu**  
Student, BSc Program  
IIT Patna  
Email: sudhanshu_24a12res1120@iitp.ac.in

---

## 📜 License
This project is for academic and learning purposes only.
