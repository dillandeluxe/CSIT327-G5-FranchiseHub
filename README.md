# 🌐 FranchiseHub: Connecting Franchisors with Potential Franchisees 🔗



## 💡 Project Overview

**FranchiseHub** is a comprehensive, web-based platform designed to **streamline the franchise application and management process**.

The system offers a dual interface:
* **For Users (Potential Franchisees):** A marketplace to easily browse, filter, and compare franchise opportunities, view detailed investment requirements, product catalogs, and seamlessly submit inquiries or applications.
* **For Franchisors (Admins):** A dedicated admin dashboard for managing, updating, and publishing franchise listings and tracking applicant submissions.

---

## 🛠 Tech Stack & Dependencies

The project is built on the robust **Django** framework, using a modern, scalable stack:

| Component | Technology | Version / Tool |
| :--- | :--- | :--- |
| **Backend Framework** | Django | `5.2.7` |
| **Database** | Supabase | **PostgreSQL** (hosted) |
| **Frontend** | Standard Web | HTML, CSS, Django Templates |
| **Language** | Python | `3.13` |
| **Version Control** | Git + GitHub | |
| **Environment** | Virtual Environment | `venv` |

---

## ⚙️ Local Development Setup & Run Instructions

Follow these steps to get the **FranchiseHub** development server running locally.

### 1️⃣ Clone the Repository & Navigate

```bash
git clone [https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git](https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git)
cd CSIT327-G5-FranchiseHub

That's a solid, well-structured README.md! It already covers all the essential information.To make it better, you should focus on:Clarity and Brevity: Make the value proposition immediately clear.Professionalism and Security: Use placeholder credentials and formalize the tech stack.Engagement: Add visual elements and a clearer call-to-action.Here is a revised version with specific improvements and the rationale for each:🚀 Suggested Enhanced README.mdMarkdown# 🌐 FranchiseHub: Connecting Franchisors with Potential Franchisees 🔗



## 💡 Project Overview

**FranchiseHub** is a comprehensive, web-based platform designed to **streamline the franchise application and management process**.

The system offers a dual interface:
* **For Users (Potential Franchisees):** A marketplace to easily browse, filter, and compare franchise opportunities, view detailed investment requirements, product catalogs, and seamlessly submit inquiries or applications.
* **For Franchisors (Admins):** A dedicated admin dashboard for managing, updating, and publishing franchise listings and tracking applicant submissions.

---

## 🛠 Tech Stack & Dependencies

The project is built on the robust **Django** framework, using a modern, scalable stack:

| Component | Technology | Version / Tool |
| :--- | :--- | :--- |
| **Backend Framework** | Django | `5.2.7` |
| **Database** | Supabase | **PostgreSQL** (hosted) |
| **Frontend** | Standard Web | HTML, CSS, Django Templates |
| **Language** | Python | `3.13` |
| **Version Control** | Git + GitHub | |
| **Environment** | Virtual Environment | `venv` |

---

## ⚙️ Local Development Setup & Run Instructions

Follow these steps to get the **FranchiseHub** development server running locally.

### 1️⃣ Clone the Repository & Navigate

```bash
git clone [https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git](https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git)
cd CSIT327-G5-FranchiseHub
2️⃣ Virtual Environment SetupIt is crucial to use a virtual environment to isolate project dependencies.ActionCommand (Windows PowerShell)Command (Mac / Linux)Createpython -m venv venvpython3 -m venv venvActivatevenv\Scripts\activatesource venv/bin/activate

That's a solid, well-structured README.md! It already covers all the essential information.To make it better, you should focus on:Clarity and Brevity: Make the value proposition immediately clear.Professionalism and Security: Use placeholder credentials and formalize the tech stack.Engagement: Add visual elements and a clearer call-to-action.Here is a revised version with specific improvements and the rationale for each:🚀 Suggested Enhanced README.mdMarkdown# 🌐 FranchiseHub: Connecting Franchisors with Potential Franchisees 🔗



## 💡 Project Overview

**FranchiseHub** is a comprehensive, web-based platform designed to **streamline the franchise application and management process**.

The system offers a dual interface:
* **For Users (Potential Franchisees):** A marketplace to easily browse, filter, and compare franchise opportunities, view detailed investment requirements, product catalogs, and seamlessly submit inquiries or applications.
* **For Franchisors (Admins):** A dedicated admin dashboard for managing, updating, and publishing franchise listings and tracking applicant submissions.

---

## 🛠 Tech Stack & Dependencies

The project is built on the robust **Django** framework, using a modern, scalable stack:

| Component | Technology | Version / Tool |
| :--- | :--- | :--- |
| **Backend Framework** | Django | `5.2.7` |
| **Database** | Supabase | **PostgreSQL** (hosted) |
| **Frontend** | Standard Web | HTML, CSS, Django Templates |
| **Language** | Python | `3.13` |
| **Version Control** | Git + GitHub | |
| **Environment** | Virtual Environment | `venv` |

---

## ⚙️ Local Development Setup & Run Instructions

Follow these steps to get the **FranchiseHub** development server running locally.

### 1️⃣ Clone the Repository & Navigate

```bash
git clone [https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git](https://github.com/dillandeluxe/CSIT327-G5-FranchiseHub.git)
cd CSIT327-G5-FranchiseHub
2️⃣ Virtual Environment SetupIt is crucial to use a virtual environment to isolate project dependencies.ActionCommand (Windows PowerShell)Command (Mac / Linux)Createpython -m venv venvpython3 -m venv venvActivatevenv\Scripts\activatesource venv/bin/activate3️⃣ Install DependenciesWith your virtual environment active, install all necessary packages:Bashpip install -r requirements.txt

4️⃣ Configure Environment Variables ⚠️
Create a file named .env in the root directory (where manage.py is located) and populate it with your Supabase credentials. The credentials below are placeholders and will not work.

Code snippet

# Database Configuration (Supabase PostgreSQL)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=zJC1nH7t0DevHR8m
DB_HOST=db.imtakkkdsincyjeszvi.supabase.co
DB_PORT=5432 

5️⃣ Apply Migrations
Set up the database schema by applying the Django migrations:

Bash

python manage.py makemigrations
python manage.py migrate