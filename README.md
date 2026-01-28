# Django Project Deployment on AWS EC2

## Production-Level (8-oy)

---

## 1. Exam Overview

Ushbu yakuniy exam **Django backend loyihani production muhitiga deploy qilish** bo‘yicha talabaning real kompetensiyasini baholashga mo‘ljallangan.

Exam davomida talaba:

* Django projectni production mindset bilan ishlab chiqishi
* Linux server bilan mustaqil ishlashi
* AWS EC2’da to‘liq deployment pipeline’ni amalga oshirishi
* Security va best practice’larni to‘g‘ri qo‘llashi

shart.

---

## 2. Tanlangan Project

### Project Nomi: **EventPulse**

### Project Tavsifi

**EventPulse** — bu **online va offline tadbirlarni boshqarish** uchun mo‘ljallangan backend servis bo‘lib, quyidagi funksionalliklarni taqdim etadi:

* Event yaratish (online / offline)
* Eventlarga foydalanuvchilarni ro‘yxatdan o‘tkazish
* Joylar limiti (capacity management)
* RSVP holati (registered / cancelled)
* Event statistikasi
* Admin uchun himoyalangan endpointlar

**Izoh:** Project ataylab oddiy CRUD’dan yuqori darajada tanlangan bo‘lib, unda real biznes logika mavjud.

---

## 3. Texnik Stack (Majburiy)

Talaba quyidagi texnologiyalardan **foydalanishi shart**:

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Application Server:** Gunicorn
* **Reverse Proxy:** Nginx
* **Cloud Platform:** AWS EC2 (Ubuntu 22.04 LTS)
* **Process Manager:** systemd
* **Static Files:** Nginx orqali serve qilinadi
* **Version Control:** Git, GitHub

---

## 4. Functional Requirements

### 4.1 Authentication & Authorization

* Custom User model ishlatilishi shart
* Token-based authentication:

  * DRF Token **yoki**
  * SimpleJWT
* Admin-only endpointlar mavjud bo‘lishi shart

---

### 4.2 Event Management

**Event modeli quyidagi field’larga ega bo‘lishi kerak:**

* title
* description
* event_type (ONLINE / OFFLINE)
* location (nullable, faqat OFFLINE eventlar uchun)
* start_time
* end_time
* capacity (integer)
* created_by (User FK)

#### Business Rules:

* `capacity = 0` bo‘lsa → eventga registration yopiladi
* `end_time < start_time` bo‘lsa → validation error qaytarilishi shart

---

### 4.3 Event Registration Logic (Core Part)

Bu qism examning **eng muhim qismi** hisoblanadi.

Majburiy talablar:

* Foydalanuvchi bitta eventga **faqat 1 marta** ro‘yxatdan o‘ta oladi
* Event capacity oshib ketmasligi kerak
* Registration’ni bekor qilish (cancel) imkoniyati bo‘lishi shart
* Alohida `Registration` modeli mavjud bo‘lishi shart

**Eslatma:** Capacity logikasi noto‘g‘ri ishlasa, project avtomatik past baholanadi.

---

### 4.4 Statistics Endpoints

Kamida quyidagi statistik endpointlar bo‘lishi kerak:

* Eventga ro‘yxatdan o‘tgan foydalanuvchilar soni
* Eventdagi bo‘sh joylar soni
* Eng ko‘p registration bo‘lgan eventlar (Top 5)

---

## 5. Deployment Requirements (EXAM CORE)

### 5.1 Server Provisioning

Talaba quyidagilarni **mustaqil** bajarishi shart:

* AWS EC2 instance yaratish
* SSH orqali serverga ulanish

---

### 5.2 Environment Configuration

* `.env` fayldan foydalanish majburiy
* Quyidagi o‘zgaruvchilar bo‘lishi shart:

  * `SECRET_KEY`
  * `DEBUG=False`
  * Database credentials
* `python-decouple` ishlatilishi kerak

---

### 5.3 Database Configuration (PostgreSQL)

* PostgreSQL server o‘rnatilgan bo‘lishi kerak
* Production database yaratilgan
* Django `migrate` bajarilgan
* Django superuser yaratilgan

---

### 5.4 Gunicorn & systemd

* Gunicorn service yozilgan bo‘lishi shart
* systemd orqali:

  * auto-start
  * process monitoring

---

### 5.5 Nginx Reverse Proxy

* HTTP (port 80) orqali ishlashi
* Static files Nginx orqali serve qilinishi
* Quyidagi endpointlar to‘g‘ri ishlashi shart:

  * `/admin/`
  * `/api/`

---

### 5.6 Security Requirements (Majburiy)

* `DEBUG=False`
* `ALLOWED_HOSTS` to‘g‘ri sozlangan
* SSH port ochiq
* Database port tashqi tarmoqdan yopiq
* `.env` fayl **repository’da bo‘lmasligi shart**

---

## 6. Testing & Validation

Talaba quyidagilarni amalda ko‘rsatib bera olishi kerak:

* Public IP yoki domain orqali API ishlayapti
* Django admin panel ochilyapti
* Registration logikasi to‘g‘ri ishlayapti
* Capacity limiti buzilmayapti

---

## 7. Topshirish Tartibi

Talaba quyidagilarni topshirishi shart:

1. **GitHub repository**
2. **Public IP yoki domain**

   * Admin login / password (tekshiruv uchun)
3. **README.md**, unda:

   * Project description
   * API endpoints ro‘yxati
   * Deployment steps (qisqacha)
4. Screenshotlar:

   * AWS EC2 instance
   * Nginx configuration
   * systemd service status


















# EventPulse - Tadbirlarni Boshqarish Tizimi

## 📌 Loyiha Haqida

EventPulse - bu online va offline tadbirlarni boshqarish uchun mo'ljallangan Django REST Framework asosidagi backend servis. Loyiha AWS EC2 serverida production muhitida deploy qilingan.

Asosiy funksiyalar:
- Foydalanuvchi autentifikatsiyasi (ro'yxatdan o'tish va kirish)
- Online va offline tadbirlarni yaratish va boshqarish
- Tadbirlarga ro'yxatdan o'tish va bekor qilish tizimi
- Tadbir sig'imi (capacity) boshqaruvi
- Tadbir statistikasi va hisobotlar

---

## 🌐 Jonli Server

Server URL: http://13.62.52.209

Admin Panel: http://13.62.52.209/admin/

---

## 🛠️ Texnologiyalar

### Backend
- Framework: Django 
- API: Django REST Framework
- Ma'lumotlar bazasi: PostgreSQL
- Autentifikatsiya: Token-based (DRF Token)

### Server Infratuzilmasi
- Cloud Platform: AWS EC2
- Operatsion Tizim: Ubuntu 22.04 LTS
- Application Server: Gunicorn
- Reverse Proxy: Nginx
- Process Manager: systemd

---

## 📡 API Endpointlar

### 1. Autentifikatsiya (Authentication)

#### Ro'yxatdan O'tish
POST /auth/register/

Request Body:
{
  "username": "foydalanuvchi",
  "email": "email@example.com",
  "password": "parol"
}

#### Tizimga Kirish
POST /auth/login/

Request Body:
{
  "username": "foydalanuvchi",
  "password": "parol"
}

Response:
{
  "token": "your-auth-token-here"
}

---

### 2. Tadbirlar (Events)

#### Tadbir Yaratish
POST /events/create/
Headers: Authorization: Token <your-token>

Request Body:
{
  "title": "Tech Conference 2026",
  "description": "Yillik texnologiya konferensiyasi",
  "event_type": "ONLINE",
  "location": null,
  "start_time": "2026-03-15T10:00:00Z",
  "end_time": "2026-03-15T18:00:00Z",
  "capacity": 100
}

Qoidalar:
- event_type: "ONLINE" yoki "OFFLINE"
- location: Faqat OFFLINE tadbirlar uchun majburiy
- capacity: Tadbir sig'imi (0 dan katta)
- end_time > start_time bo'lishi shart

#### Tadbirga Ro'yxatdan O'tish
POST /events/register/
Headers: Authorization: Token <your-token>

Request Body:
{
  "event_id": 1
}

Biznes logika:
- Har bir foydalanuvchi bitta tadbirga faqat 1 marta ro'yxatdan o'ta oladi
- Tadbir sig'imi to'lgan bo'lsa (capacity = 0), yangi ro'yxatdan o'tish rad etiladi
- Muvaffaqiyatli ro'yxatdan o'tgandan keyin capacity 1 ga kamayadi

#### Ro'yxatdan O'tishni Bekor Qilish
POST /events/register/cancel/<registration_id>
Headers: Authorization: Token <your-token>

Natija:
- Ro'yxatdan o'tish bekor qilinadi
- Tadbir capacity 1 ga ortadi

#### Tadbir Statistikasi
GET /events/stats/
Headers: Authorization: Token <your-token>

Response:
{
  "total_events": 10,
  "total_registrations": 45,
  "top_events": [
    {
      "id": 1,
      "title": "Tech Conference 2026",
      "registration_count": 85,
      "available_spots": 15
    }
  ]
}

---

## 🚀 Deployment Jarayoni (Qisqacha)

### 1. Server Tayyorlash
# AWS EC2 Ubuntu 22.04 instance yaratish
# SSH orqali serverga ulanish
ssh -i keypair.pem ubuntu@server-ip

### 2. Zarur Paketlarni O'rnatish
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-dev postgresql \
    postgresql-contrib libpq-dev nginx git build-essential

### 3. PostgreSQL Sozlash
sudo -u postgres psql
CREATE DATABASE event;
CREATE USER dbuser WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE event TO dbuser;

### 4. Loyihani Deploy Qilish
# Loyihani klonlash
git clone <repository-url> exam08
cd exam08

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
pip install gunicorn

# .env fayl yaratish (environment variables)
# Migration
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

### 5. Gunicorn Service
```bash
# /etc/systemd/system/gunicorn.service yaratish
sudo systemctl