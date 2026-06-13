# 🤖 AI Chatbot — OpenAI + Docker + AWS EC2 + GitHub Actions

A production-ready AI chatbot built with **Flask** and the **OpenAI API**, containerized using **Docker**, and deployed to **AWS EC2** via an automated **GitHub Actions CI/CD pipeline**.

---

## 🏗️ Architecture

```
User → EC2 (port 5000) → Docker Container → Flask App → OpenAI API
         ↑
  GitHub Actions
  (CI/CD Pipeline)
         ↑
    GitHub Push
```

---

## 🚀 Features

- 💬 Real-time AI responses via OpenAI GPT-3.5-turbo REST API
- 🔄 Multi-turn conversation with session management
- 🐳 Dockerized with multi-stage build for small image size
- ☁️ Deployed on AWS EC2
- ⚙️ Automated CI/CD: test → build → push → deploy on every `git push`
- 🧪 Pytest test suite with mocked OpenAI calls
- ❤️ Health check endpoint for monitoring

---

## 📁 Project Structure

```
ai-chatbot/
├── src/
│   └── app.py                  # Flask REST API + OpenAI integration
├── templates/
│   └── index.html              # Chat UI frontend
├── tests/
│   └── test_app.py             # Pytest test suite
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Local development setup
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md
```

---

## 🔧 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/ai-chatbot.git
cd ai-chatbot
```

### 2. Set up environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run with Docker (Recommended)
```bash
docker-compose up --build
```

### 4. OR run directly with Python
```bash
pip install -r requirements.txt
python src/app.py
```

Visit: `http://localhost:5000`

---

## 🧪 Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## ☁️ AWS EC2 Deployment

### Prerequisites
- AWS EC2 instance (Ubuntu 22.04, t2.micro or higher)
- Docker installed on EC2
- Docker Hub account
- Security group: port 22 (SSH) and 5000 open

### GitHub Secrets Required

Go to your repo → **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `EC2_HOST` | Public IP of your EC2 instance |
| `EC2_USER` | SSH user (e.g., `ubuntu`) |
| `EC2_SSH_KEY` | Contents of your EC2 `.pem` private key |

### Install Docker on EC2
```bash
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
# Log out and back in
```

---

## ⚙️ CI/CD Pipeline

On every push to `main`, GitHub Actions automatically:

1. **Test** — Runs `pytest` on all test cases
2. **Build & Push** — Builds Docker image, pushes to Docker Hub
3. **Deploy** — SSHs into EC2, pulls new image, restarts container

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat UI |
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Send a message |
| `POST` | `/reset` | Reset conversation |

### Example `/chat` request
```json
POST /chat
{
  "message": "What is DevOps?",
  "session_id": "user_abc"
}
```

### Example response
```json
{
  "response": "DevOps is a set of practices...",
  "session_id": "user_abc",
  "tokens_used": 142
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI | OpenAI GPT-3.5-turbo |
| Containerization | Docker (multi-stage build) |
| Cloud | AWS EC2 |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Testing | Pytest |

---

## 👤 Author

**Piyush** — BCA + MBA (Finance) | DevOps & Cloud Engineer  
[GitHub](https://github.com/piyush30082003) · [Portfolio](https://piyush30082003.github.io/piyush-portfolio/)