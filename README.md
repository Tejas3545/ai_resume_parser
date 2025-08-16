# 📄 Automated Resume Parser

## 📌 Description
A **Flask-based web application** that automatically extracts structured information (Name, Email, Phone, Skills, Education, Experience) from resumes in **PDF/DOCX** formats.  
The extracted data is then stored in a **PostgreSQL database**, making candidate information easy to search, filter, and manage.

---

## 🚀 Tech Stack
- **Backend:** Python, Flask  
- **NLP:** spaCy  
- **Parsing:** pdfplumber, docx2txt  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Frontend:** HTML, CSS (basic table UI)  

---

## ⚡ Features
✅ Upload resumes in **PDF/DOCX** format  
✅ Extract key details:  
- Name  
- Email  
- Phone  
- Skills  
- Education  
- Experience  

✅ Store extracted data into PostgreSQL  
✅ View parsed resumes in a clean table UI  
✅ Delete unwanted records from the database  
✅ Easy API integration for automation  

---

## 🛠️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/resume_parser.git
cd resume_parser
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL
- Make sure PostgreSQL is installed and running.
- Create a new database (e.g., `resume_db`).
- Update your database credentials in `config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/resume_db"
```

### 5. Run database migrations
```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Run the app
```bash
flask run
```
App will be live at: **http://127.0.0.1:5000/**

---

## 📂 Project Structure
```
resume_parser/
│── app.py                # Flask entry point
│── models.py             # Database models
│── database.py           # Database connection + helpers
│── resume_parser.py      # Resume parsing logic
│── templates/
│   └── index.html        # UI template
│── static/
│   └── style.css         # CSS for UI
│── requirements.txt      # Python dependencies
│── config.py             # Database configuration
│── migrations/           # Alembic migrations
```

---

## 📊 Example Output
After uploading a resume, data will be extracted and shown like this:

| ID | Name             | Email                     | Phone        | Skills                  | Education | Experience |
|----|------------------|---------------------------|-------------|-------------------------|-----------|------------|
| 1  | Tejas J Solanki  | tjs4@gmail.com | +91 8554... | Python, Java, React, SQL | B.Tech    | Intern, Projects |

---

## 📡 API Endpoints

### ➤ Upload Resume
**POST** `/upload`  
Uploads a resume file and saves extracted data.

Example (cURL):
```bash
curl -X POST -F "file=@resume.pdf" http://127.0.0.1:5000/upload
```

---

### ➤ Get All Resumes
**GET** `/resumes`  
Fetch all parsed resumes.

Example:
```bash
curl http://127.0.0.1:5000/resumes
```

---

### ➤ Delete a Resume
**DELETE** `/resumes/<id>`  
Delete a resume by ID.

Example:
```bash
curl -X DELETE http://127.0.0.1:5000/resumes/1
```

---

## 🤝 Contributing
Contributions are welcome!  
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-xyz`)  
3. Commit changes (`git commit -m "Add feature xyz"`)  
4. Push to branch (`git push origin feature-xyz`)  
5. Open a Pull Request  

---

## 📜 License
This project is licensed under the **MIT License**.  

---

## 🌟 Acknowledgements
- [spaCy](https://spacy.io/) for NLP  
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction  
- [docx2txt](https://github.com/ankushshah89/python-docx2txt) for DOCX parsing  
- [Flask](https://flask.palletsprojects.com/) for web framework  
