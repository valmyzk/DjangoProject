## 🚀 How to Run XChange

### 🐳 Run with Docker

1. **Make sure you have [Docker](https://docs.docker.com/get-docker/) installed** 

2. **Clone the repository**
```bash
git clone https://github.com/valmyzk/DjangoProject.git
cd DjangoProject
```

3. **(Optional) Create a `.env` file** to override any environment variables (e.g., `SECRET_KEY`, `DEBUG`, etc.)

4. **Build and start the application**
```bash
docker-compose up
```

5. **Access the application**
   - Open your browser and go to: [http://localhost:8000](http://localhost:8000)

---

### 🛠 Development Notes

- The app runs on Django's development server by default.
- You can run admin tasks like migrations from inside the container:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---
