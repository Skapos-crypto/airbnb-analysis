# Dashboard Deployment Guide

This guide covers multiple deployment options for your Airbnb Pricing Analysis Dashboard.

## ✅ Prerequisites Checklist
- [x] requirements.txt created
- [x] Procfile created (for Heroku/Render)
- [x] render.yaml created (for Render)
- [x] .gitignore created
- [x] dashboard.py modified to expose Flask server
- [x] dataset.csv included (required for the app)

---

## 🚀 Option 1: Deploy to Render (Recommended - Free Tier Available)

Render is a modern cloud platform with a generous free tier.

### Steps:

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Airbnb dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/airbnb-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: airbnb-dashboard
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn dashboard:server`
   - Click "Create Web Service"

3. **Access Your Dashboard**
   - Your app will be live at: `https://airbnb-dashboard.onrender.com` (or similar)
   - First deployment takes 3-5 minutes

---

## 🔷 Option 2: Deploy to Heroku

Heroku is a mature platform with easy deployment.

### Steps:

1. **Install Heroku CLI**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli

2. **Deploy**
   ```bash
   heroku login
   heroku create airbnb-dashboard-analysis
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

3. **Open Your App**
   ```bash
   heroku open
   ```

---

## ☁️ Option 3: Deploy to Railway

Railway offers $5 free credit per month.

### Steps:

1. **Deploy via GitHub**
   - Push code to GitHub (same as Render step 1)
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and uses Procfile

2. **Access Your Dashboard**
   - Click on your deployment
   - Go to "Settings" → "Generate Domain"
   - Your app will be accessible at the generated URL

---

## 🐳 Option 4: Deploy with Docker

If you prefer containerization, I can create a Dockerfile.

### Quick Docker Setup:

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8050
   CMD ["gunicorn", "-b", "0.0.0.0:8050", "dashboard:server"]
   ```

2. Build and Run:
   ```bash
   docker build -t airbnb-dashboard .
   docker run -p 8050:8050 airbnb-dashboard
   ```

---

## 🌐 Option 5: Deploy to PythonAnywhere

Free hosting for Python apps.

### Steps:

1. Sign up at https://www.pythonanywhere.com
2. Upload your files via dashboard
3. Create a new web app
4. Configure WSGI file to point to `dashboard:server`
5. Install requirements via console

---

## 📊 Important Notes

### File Size Considerations
- Your `dataset.csv` is required for the dashboard
- If the CSV is large (>100MB), consider:
  - Using Git LFS (Large File Storage)
  - Hosting data separately (AWS S3, Google Cloud Storage)
  - Using a database instead of CSV

### Environment Variables
For sensitive configuration, create a `.env` file (don't commit this):
```
DEBUG=False
PORT=8050
```

### Performance Optimization
For production, consider:
- Caching data with `@cache` decorator
- Using a CDN for static assets
- Implementing pagination for large datasets
- Using Dash Enterprise for enterprise features

---

## 🔧 Testing Deployment Locally

Before deploying, test with Gunicorn locally:

```bash
pip install gunicorn
gunicorn dashboard:server
```

Visit http://localhost:8000

---

## 📝 Post-Deployment Checklist

- [ ] Dashboard loads without errors
- [ ] All visualizations render correctly
- [ ] Data displays properly
- [ ] Navigation works smoothly
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS (usually automatic)
- [ ] Monitor performance and logs

---

## 🆘 Troubleshooting

### Common Issues:

1. **App crashes on deployment**
   - Check logs for missing dependencies
   - Verify Python version compatibility
   - Ensure dataset.csv is uploaded

2. **Slow loading**
   - Consider data caching
   - Optimize data loading
   - Use smaller sample for testing

3. **Port binding errors**
   - Ensure you're using `host='0.0.0.0'` in dashboard.py
   - Let hosting platform assign port dynamically

---

## 🎉 You're Ready to Deploy!

Choose your preferred platform above and follow the steps. Render is recommended for beginners due to its simplicity and free tier.

Need help? Check the platform-specific documentation:
- Render: https://render.com/docs
- Heroku: https://devcenter.heroku.com
- Railway: https://docs.railway.app
