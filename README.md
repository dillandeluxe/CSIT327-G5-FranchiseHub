# CSIT327-G5-FranchiseHub

## 📘 Project Overview
**FranchiseHub** is a web-based platform designed to connect potential franchisees with franchisors by showcasing franchise opportunities, product details, and application processes.  
Users can browse listings, view investment requirements, and submit inquiries or applications.  
The system also includes an admin dashboard for franchisors to manage listings.

---

## 🛠 Tech Stack
- **Backend:** Django 5.2.7  
- **Database:** Supabase (PostgreSQL)  
- **Frontend:** HTML / CSS / Django Templates  
- **Version Control:** Git + GitHub  
- **Environment:** Python 3.13 + Virtual Environment (venv)

---

## ⚙️ Setup & Run Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git
cd CSIT327-G5-FranchiseHub
2️⃣ Create and activate a virtual environment
Create:

bash

python -m venv venv
Activate (Windows PowerShell):

bash

venv\Scripts\activate
Activate (Mac / Linux):

bash

source venv/bin/activate
3️⃣ Install all dependencies
bash

pip install -r requirements.txt
4️⃣ Set up your environment variables
Create a file named .env in the same folder as manage.py and add:

env

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=dillanq123
DB_HOST=db.imtakkkdsincyjeszvi.supabase.co
DB_PORT=5432


5️⃣ Apply database migrations
bash

python manage.py makemigrations
python manage.py migrate
6️⃣ Create a superuser (for admin access)
bash

python manage.py createsuperuser
Follow the prompts to create your admin credentials.

7️⃣ Run the development server
bash

python manage.py runserver
Then open these URLs in your browser:

Registration page: http://127.0.0.1:8000/accounts/register/

Login page: http://127.0.0.1:8000/accounts/login/

Admin page: http://127.0.0.1:8000/admin/

Note: The main homepage (/) is not yet implemented — use the routes above to access current features.

##👥 Team Members
Lanz Roy Sumalpong      Product Owner       lanzroy.sumalpong@cit.edu
Jethro Salindato        Business Analyst    jethro.salindato@cit.edu
David Ryan Sia          Scrum Master        davidryan.sia@cit.edu
Dillan Marquin Ycoy     Lead Developer      dillanmarquin.ycoy@cit.edu
German Oliver Velasco   FullStack Developer germanoliver.velasco@cit.edu
John James Palis        FullStack Developer johnjames.palis@cit.edu


