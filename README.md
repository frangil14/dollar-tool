# 💰 Dollar Tool

Argentina has experienced significant economic instability in recent years, with high inflation rates and multiple exchange rate systems. This volatility has made it crucial for individuals and businesses to monitor different dollar exchange rates across various platforms to find the best deals.

**Dollar Tool** is a real-time price tracking application that monitors different dollar types (Blue Dollar, Crypto) and their variations compared to the Argentine peso. Born from the need to quickly compare exchange rates across multiple platforms and track historical trends, this personal project was created as an initiative to explore modern web development practices while building something useful for Argentina's complex economic landscape.

## 🔎 At a Glance

- **Full Stack Application**: React + Flask
- **Real-time scraping & visualization** with interactive charts
- **Dockerized** with multi-stage builds and security best practices
- **Demonstrates proficiency** in Frontend, Backend, and DevOps

## 🚀 Features

- **Real-time price updates** every 30 seconds
- **Multiple data sources**: DolarHoy, Cronista, Binance P2P, Lemon Cash
- **Historical data visualization** with interactive charts
- **Auto-refresh** with manual control
- **Responsive design** with modern UI
- **Docker containerized** for easy deployment

## 🏗️ Architecture

### Backend (Python/Flask)
- **Web scraping** with BeautifulSoup
- **SQLite database** for historical data
- **REST API** with proper error handling
- **Scheduled data collection** with APScheduler
- **Modular architecture** with separated concerns

### Frontend (React)
- **Component-based architecture**
- **Custom hooks** for API management
- **Real-time updates** with auto-refresh
- **Professional UI** with DevExtreme components
- **Error handling** and loading states

## 🐳 Docker Deployment

This application uses **optimized multi-stage Docker builds** for both backend and frontend, resulting in smaller, more secure production images.

### Key Docker Optimizations
- **Multi-stage builds** - Separate build and production stages
- **Alpine Linux** - Lightweight base images
- **Non-root users** - Enhanced security
- **Layer caching** - Optimized build times
- **Minimal dependencies** - Only production packages in final images

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dollar-tool
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:5000

That's all you need!

## 🛠️ Development Setup

### Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Frontend Setup
```bash
cd ui

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 API Endpoints

- `GET /API/dollar_blue` - Get current blue dollar prices
- `GET /API/dollar_cripto` - Get crypto dollar prices
- `GET /API/get_historic_data` - Get historical price data
- `POST /API/write_historic_data` - Write new historical data

## 🎯 Technologies Used

### Backend
- **Python 3.9** - Programming language
- **Flask** - Web framework
- **BeautifulSoup** - Web scraping
- **SQLite** - Database
- **APScheduler** - Task scheduling
- **Requests** - HTTP client

### Frontend
- **React 18** - UI framework
- **DevExtreme** - UI components
- **Axios** - HTTP client
- **Custom hooks** - State management

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **Nginx** - Web server (production)
- **Alpine Linux** - Lightweight base images
- **Non-root users** - Security best practices


## 🔧 Configuration

### Environment Variables
- `FLASK_DEBUG` - Flask debug mode (True/False)
- `PYTHONPATH` - Python path configuration
- `TZ` - Timezone configuration

### Auto-refresh Settings
The application automatically refreshes data every 30 seconds. This can be configured in the `useApiData` hook.


## 👨‍💻 Author

Developed by **Francisco Gil** as a full-stack + DevOps portfolio project, demonstrating skills in React, Python/Flask, Docker, and modern web development while solving a real-world problem in Argentina.

**💼 LinkedIn**: [linkedin.com/in/francisco-gil/](https://linkedin.com/in/francisco-gil/)


