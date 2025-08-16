# 1) create venv (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 2) install deps
pip install -r requirements.txt
# (optional but recommended if you want better name extraction)
python -m spacy download en_core_web_sm

# 3) create MySQL DB 'resume_db' first, or change DB_URL in database.py
# then run the app:
python app.py

# open http://127.0.0.1:5000/
