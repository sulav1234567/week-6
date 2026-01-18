# Quiz Authoring Platform

A professional full-stack web application for creating, managing, and taking quizzes. Built with modern technologies and designed for both local development and cloud deployment.

![System Status](https://img.shields.io/badge/status-prototype-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)

## 🎯 Features

- ✨ **Create Quizzes**: Build custom quizzes with multiple-choice questions
- 📝 **Manage Quizzes**: View, edit, and delete your quizzes
- 🎮 **Take Quizzes**: Interactive quiz-taking experience with instant feedback
- 🎨 **Premium UI**: Modern, beautiful interface with smooth animations
- 📱 **Responsive**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Built with React + Vite and FastAPI

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────┐
│   Web Browser   │
│   (React UI)    │
└────────┬────────┘
         │ HTTP/REST API
         │
┌────────▼────────┐
│  FastAPI Backend│
│  (Python)       │
└────────┬────────┘
         │ SQL
         │
┌────────▼────────┐
│ SQLite Database │
└─────────────────┘
```

### Technology Stack

**Frontend:**
- React 18 - UI framework
- Vite - Build tool & dev server
- Modern CSS with gradients & animations
- Google Fonts (Inter)

**Backend:**
- FastAPI - Python web framework
- SQLAlchemy - ORM for database
- Pydantic - Data validation
- Uvicorn - ASGI server

**Database:**
- SQLite - Lightweight relational database

**Infrastructure (Deployment):**
- AWS EC2 - Application hosting
- Docker - Containerization
- Nginx - Reverse proxy
- Gunicorn/Uvicorn - WSGI/ASGI server

## 📋 API Specification

All API endpoints are prefixed with `/api/quizzes`

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/quizzes` | GET | Retrieve all quizzes | - | Array of quiz objects |
| `/api/quizzes` | POST | Create a new quiz | Quiz object with questions | Created quiz object |
| `/api/quizzes/{quiz_id}` | GET | Get quiz details | - | Single quiz object |
| `/api/quizzes/{quiz_id}` | DELETE | Delete a quiz | - | Success message |

### Example Quiz Object

```json
{
  "id": 1,
  "title": "General Knowledge Quiz",
  "description": "Test your general knowledge",
  "questions": [
    {
      "question": "What is the capital of France?",
      "options": ["London", "Paris", "Berlin", "Madrid"],
      "correct_answer": 1
    }
  ],
  "created_at": "2026-01-18T23:00:00Z"
}
```

## 🚀 Local Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 🎮 Usage

1. **Create a Quiz:**
   - Click the "Create New Quiz" button
   - Enter quiz title and description
   - Add questions with multiple choice options
   - Mark the correct answer for each question
   - Click "Create Quiz"

2. **View Quizzes:**
   - Browse all quizzes on the main page
   - Click "View Quiz" to see details

3. **Take a Quiz:**
   - In quiz detail view, select answers for all questions
   - Click "Submit Answers" to see your score
   - Try again to improve your score

4. **Delete a Quiz:**
   - Click the "Delete" button on any quiz card
   - Confirm deletion

## 📦 Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### Backend Production Server

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🌐 Deployment

For detailed deployment instructions to AWS EC2 with Docker, Nginx, and domain setup, see [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 Project Structure

```
quiz-platform/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   └── quizzes.py       # Quiz API endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main App component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md                # This file
```

## 🧪 Testing

### API Testing with curl

```bash
# Get all quizzes
curl http://localhost:8000/api/quizzes

# Create a quiz
curl -X POST http://localhost:8000/api/quizzes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Quiz",
    "description": "A test quiz",
    "questions": [{
      "question": "Sample question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0
    }]
  }'

# Get quiz by ID
curl http://localhost:8000/api/quizzes/1

# Delete quiz
curl -X DELETE http://localhost:8000/api/quizzes/1
```

## 🛠️ Development

- Backend runs on port 8000 by default
- Frontend runs on port 5173 by default
- Database file: `backend/quiz_platform.db`
- CORS is enabled for `localhost:5173` and `localhost:3000`

## 📝 Assignment Requirements

This project fulfills all assignment requirements:

- ✅ **System Architecture**: Documented above with clear component separation
- ✅ **API Specification**: Complete RESTful API with all required endpoints
- ✅ **Publicly Accessible Prototype**: Ready for deployment (see DEPLOYMENT.md)

## 🤝 Contributing

This is a prototype assignment project. Feel free to extend it with additional features!

## 📄 License

MIT License - Feel free to use this project for learning and development.

---

**Built with ❤️ for Week 6 Assignment**
