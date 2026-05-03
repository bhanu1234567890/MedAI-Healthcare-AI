from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for  # ✅ added session, redirect, url_for
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)
app.secret_key = 'your-secret-key'  # ✅ required for session

GROQ_API_KEY = os.getenv("GROQ_API_KEY") # For security reasons actual key is not provided
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# Simple in-memory storage for medications
medications = []

# Simple in-memory storage for reminders (let's give them unique IDs for easier removal)
reminders = []
next_reminder_id = 1

# Fallback responses for common medicines
MEDICINE_INFO = {
    "paracetamol": """Paracetamol is a common pain reliever and fever reducer.
Uses: Headaches, muscle aches, arthritis, backache, toothaches, colds, and fevers.
Side effects: Generally safe but may include liver problems with high doses.
Precautions: Don't exceed recommended dose, avoid alcohol, consult doctor if pregnant.""",
    "ibuprofen": """Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID).
Uses: Pain relief, fever reduction, and inflammation reduction.
Side effects: Stomach upset, heartburn, dizziness, mild headache.
Precautions: Take with food, avoid if you have stomach ulcers or heart conditions.""",
    "aspirin": """Aspirin is a common pain reliever and blood thinner.
Uses: Pain relief, fever reduction, prevention of heart attacks and strokes.
Side effects: Stomach upset, bleeding risk, ringing in ears.
Precautions: Avoid in children, consult doctor if on blood thinners."""
}

# Fallback responses for adherence coach
COACH_RESPONSES = {
    "forgot": "It's important to take your medication as prescribed. Try setting reminders on your phone or using a pill organizer. If you miss a dose, don't double up - just take your next dose as scheduled.",
    "side effects": "If you're experiencing side effects, don't stop taking your medication without consulting your doctor. They can adjust your dosage or switch you to a different medication.",
    "schedule": "Creating a medication schedule is important. Try taking your medicine at the same time each day and linking it to daily activities like breakfast or bedtime.",
    "default": "Remember that medication adherence is crucial for your health. If you have concerns, please consult with your healthcare provider."
}

# ✅ LOGIN ROUTES ONLY (added)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'admin@example.com' and password == 'password':
            session['user'] = email
            return redirect(url_for('index'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ✅ Modified: protect index route
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/add_medication', methods=['POST'])
def add_medication():
    if request.method == 'POST':
        data = request.get_json()
        medication_name = data.get('name')
        if medication_name:
            medications.append(medication_name)
            print(f"Medication '{medication_name}' added. Current medications: {medications}")
            return jsonify({'status': 'success', 'message': f'Medication "{medication_name}" added successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Medication name cannot be empty'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'})

@app.route('/api/medicines', methods=['GET'])
def get_medications():
    return jsonify({'status': 'success', 'medicines': medications})

@app.route('/api/remove_medication/<medication_name>', methods=['DELETE'])
def remove_medication(medication_name):
    try:
        medications.remove(medication_name)
        print(f"Medication '{medication_name}' removed. Current medications: {medications}")
        return jsonify({'status': 'success', 'message': f'Medication "{medication_name}" removed'})
    except ValueError:
        return jsonify({'status': 'error', 'message': f'Medication "{medication_name}" not found'})

@app.route('/api/add-reminder', methods=['POST'])
def add_reminder():
    global next_reminder_id
    if request.method == 'POST':
        data = request.get_json()
        medication_name = data.get('medication')
        reminder_time = data.get('time')
        if medication_name and reminder_time:
            new_reminder = {'id': next_reminder_id, 'medication': medication_name, 'time': reminder_time}
            reminders.append(new_reminder)
            print(f"Reminder added: {new_reminder}. Current reminders: {reminders}")
            next_reminder_id += 1
            return jsonify({'status': 'success', 'message': f'Reminder added for "{medication_name}" at "{reminder_time}"', 'reminder': new_reminder})
        else:
            return jsonify({'status': 'error', 'message': 'Medication name and reminder time are required'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'})

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    return jsonify({'status': 'success', 'reminders': reminders})

@app.route('/api/remove-reminder/<int:reminder_id>', methods=['DELETE'])
def remove_reminder(reminder_id):
    global reminders
    initial_len = len(reminders)
    reminders = [reminder for reminder in reminders if reminder.get('id') != reminder_id]
    if len(reminders) < initial_len:
        print(f"Reminder with ID {reminder_id} removed. Current reminders: {reminders}")
        return jsonify({'status': 'success', 'message': f'Reminder with ID {reminder_id} removed'})
    else:
        return jsonify({'status': 'error', 'message': f'Reminder with ID {reminder_id} not found'})

@app.route('/api/medicine-explanation', methods=['POST'])
def medicine_explanation():
    data = request.json
    medicine = data.get('name', '').lower()
    try:
        prompt = f"Explain the use, side effects, and precautions of {medicine} in simple terms."
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROQ_API_KEY}'
        }
        groq_data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=groq_data)
        if response.status_code == 200:
            explanation = response.json()['choices'][0]['message']['content']
            return jsonify({'explanation': explanation})
        else:
            raise Exception(f"Groq API error: {response.status_code} {response.text}")
    except Exception as e:
        if medicine in MEDICINE_INFO:
            return jsonify({'explanation': MEDICINE_INFO[medicine]})
        else:
            return jsonify({'explanation': 'Information not available in offline mode. Please try another medicine or check with your healthcare provider.'})

@app.route('/api/adherence-coach', methods=['POST'])
def adherence_coach():
    data = request.json
    message = data.get('message', '').lower()
    try:
        prompt = f"You are a medication adherence coach. {message}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROQ_API_KEY}'
        }
        groq_data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=groq_data)
        if response.status_code == 200:
            coach_reply = response.json()['choices'][0]['message']['content']
            return jsonify({'reply': coach_reply})
        else:
            raise Exception(f"Groq API error: {response.status_code} {response.text}")
    except Exception as e:
        for key, response_text in COACH_RESPONSES.items():
            if key in message:
                return jsonify({'reply': response_text})
        return jsonify({'reply': COACH_RESPONSES['default']})

@app.route('/api/pharmacy-integration', methods=['POST'])
def pharmacy_integration():
    data = request.json
    return jsonify({'status': 'success', 'message': 'Pharmacy data received.'})

@app.route('/frontend.html')
def frontend():
    return send_from_directory(app.static_folder, 'frontend.html')

if __name__ == '__main__':
    app.run(debug=True)
