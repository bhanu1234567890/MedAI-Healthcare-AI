# MedAI – AI-Powered Healthcare Platform

## 📌 Overview

MedAI is an AI-powered healthcare web application designed to improve medication adherence and patient understanding of prescriptions. The system leverages AI to simplify complex medical information, provide interactive chatbot support, and deliver timely medication reminders.

This project demonstrates the practical application of Artificial Intelligence in healthcare, focusing on usability, accessibility, and real-world impact.
While the project was developed collaboratively, the design and implementation of the backend architecture and AI integration were carried out independently.

---

## 🚀 Key Features

* **AI-Based Medication Explanation**
  Simplifies complex prescription details into easy-to-understand language.

* **Interactive Chatbot (Adherence Coach)**
  Provides real-time responses to patient queries using AI.

* **Medication Management System**
  Add, view, and remove medications dynamically.

* **Reminder System**
  Schedule and manage medication reminders.

* **Fallback Mechanism**
  Provides offline responses when AI API is unavailable.

---

## 🏗️ System Architecture

* **Frontend:** HTML (minimal UI for demonstration)
* **Backend:** Python (Flask)
* **AI Integration:** Groq API using LLaMA-based Large Language Model for generating medication explanations and chatbot responses
* **Data Handling:** In-memory storage (for prototype demonstration)

---

## ⚙️ Tech Stack

* Python
* Flask
* REST APIs
* HTML/CSS
* JavaScript
* AI API Integration

---

## 📂 Project Structure

```
MedAI-Healthcare-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── MedAI_Report.pdf
│
├── templates/
│   ├── login.html
│   └── index.html
```

---

## 🖼️ Screenshots

```
MedAI-Healthcare-AI/
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│   └── chatbot.png
```


## ▶️ How to Run

1. Clone the repository:

```
git clone https://github.com/bhanu1234567890/MedAI-Healthcare-AI.git
cd MedAI-Healthcare-AI
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

4. Run the application:

```
python app.py
```

5. Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

* `POST /api/medicine-explanation`
  Returns simplified explanation of a medicine

* `POST /api/adherence-coach`
  AI chatbot for medication-related queries

* `POST /api/add-reminder`
  Add medication reminder

* `GET /api/reminders`
  Fetch all reminders

* `DELETE /api/remove-reminder/<id>`
  Remove reminder

---

## 🧠 Use Case

MedAI is designed for:

* Patients who need help understanding prescriptions
* Individuals struggling with medication adherence
* Healthcare-focused AI experimentation and prototyping

---

## 👨‍💻 Authorship

This project was developed as part of a team final year Bachelor's of technology AI Project.
My primary contributions include:

* Backend development using Flask
* AI API integration for chatbot and prescription explanation
* Implementation of reminder system
* workflow architecture

---

## 📈 Future Enhancements

* Cloud deployment (AWS / GCP)
* Database integration (persistent storage)
* Mobile application version
* Advanced personalization using user data
* Integration with healthcare/pharmacy systems

---

## ⚠️ Disclaimer

This project is a prototype developed for educational purposes. It is not intended to replace professional medical advice.

---

## 📄 License

This project is for academic and demonstration purposes.
