# 💳 CreditPay — Credit Card Processing Web App (Streamlit + SQLite)

CreditPay is a modern, mobile-friendly **credit card processing web application** built using **Python + Streamlit + SQLite**.  
It includes customer management, card validation using **Luhn Algorithm**, payment simulation, transaction history, and report downloads (CSV + PDF).

✅ **Premium UI (GPay-style)**  
✅ **Mobile responsive + desktop ready**  
✅ **Smooth navigation (Back/Next + Bottom Nav)**  
✅ **SQLite database for persistence**

---

## 🚀 Live Demo
🔗 **Streamlit Cloud App:**  
https://creditcard-webapp-cgqqy7ltoytsm2dykbzyis.streamlit.app/

---

## ✨ Features

### ✅ Dashboard
- Total Customers
- Total Transactions
- Total Amount Processed
- Success Rate Analytics

### ✅ Customer Management
- Add new customers
- View all customers
- Delete customer records

### ✅ Card Management
- Add card details (only saves last 4 digits)
- Card validation using **Luhn check**
- Delete saved cards

### ✅ Payments
- Simulate payment processing
- Auto success/failure logic (limit-based)
- Stores payment status in SQLite

### ✅ Transaction History
- View transaction list per customer
- Track amount, status, message, timestamp

### ✅ Reports
- Download Customers CSV
- Download Transactions CSV per customer
- Generate PDF transaction report

### ✅ UI / Experience
- Splash screen like payment apps
- Premium modern UI with gradients + cards
- Mobile view supported with bottom navigation

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**
- **Matplotlib**
- **FPDF (PDF generation)**

---

## 📂 Project Structure
creditpay/
│── app.py
│── db.py
│── utils.py
│── requirements.txt
│── README.md
│── .gitignore

