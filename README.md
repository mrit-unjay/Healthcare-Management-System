🏥 Healthcare Management System
A lightweight, web-based Healthcare Management System built with Python (Flask) and modern frontend technologies. This system allows healthcare professionals to manage patients, appointments, resources, and healthcare provider collaborations through a clean and interactive dashboard.

🚀 Features
👤 Add & View Patient Information
📅 Schedule Appointments
🏥 Check-In System for Patients
📦 Resource Inventory Management
👨‍⚕️ Healthcare Provider Management
🧭 View Hierarchies and Collaborations
⚡ Responsive and interactive UI
🛠️ Tech Stack
Backend: Python 3, Flask
Frontend: HTML5, CSS3, JavaScript (Vanilla)
Styling: Custom CSS with Roboto font
Communication: RESTful API (AJAX with Fetch API)
📁 File Structure
├── app.py # Flask backend server handling API routes ├── index.html # Frontend dashboard interface ├── script.js # Frontend logic for menu navigation and form handling ├── styles.css # Styling for layout and UI components ├── .gitattributes # Git attributes for consistent handling

🧪 How It Works
Each action on the sidebar menu (like "Add Patient" or "Schedule Appointment") sends a command to the Flask backend. The backend parses and executes these commands, simulating a basic healthcare workflow.

Sample Commands Executed by Frontend:
1 John 35 Fever → Adds a patient
2 John 10:00AM → Schedules an appointment
5 John 2024-05-16T09:00 → Checks in a patient
The backend responds with the result, displayed in the output panel on the right.

🔧 Setup Instructions
1. Clone the Repository
git clone https://github.com/yourusername/healthcare-management-system.git
cd healthcare-management-system

2. Install Dependencies
Ensure you have Python 3 and pip installed.
pip install flask


3. Run the Flask App
python app.py

This will start a local server at http://127.0.0.1:5000/.

4. Open in Browser
Open index.html in any modern browser. The frontend interacts with the Flask backend at localhost.

📸 UI Preview
Add screenshots here if you want to showcase the interface!

✨ Future Enhancements
Persistent database integration (SQLite/PostgreSQL)

Authentication for admin access

Appointment reminders & email notifications

Real-time collaboration via WebSocket

🤝 Contributing
Pull requests are welcome! Feel free to fork this project and contribute by fixing bugs or adding new features.

📄 License
This project is open-source and available under the MIT License.
