# 🚀 Quick Deploy to Render (5 Minutes)

The fastest way to get your dashboard online for free!

## Step-by-Step Guide

### 1. Create a GitHub Account (if you don't have one)
- Go to https://github.com
- Sign up for free

### 2. Create a New Repository
1. Click the "+" icon → "New repository"
2. Name it: `airbnb-dashboard`
3. Keep it Public (for free deployment)
4. Click "Create repository"

### 3. Push Your Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Deploy Airbnb pricing dashboard"

# Connect to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/airbnb-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Deploy on Render

1. **Sign up at Render**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Click "Connect GitHub account" (if not already)
   - Find and select your `airbnb-dashboard` repository

3. **Configure Service**
   - **Name**: airbnb-dashboard (or any name you want)
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Root Directory**: leave blank
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn dashboard:server`

4. **Select Free Plan**
   - Click "Free" plan
   - Click "Create Web Service"

5. **Wait for Deployment**
   - First deployment takes 3-5 minutes
   - Watch the logs in real-time
   - When you see "Your service is live 🎉", it's ready!

### 5. Access Your Dashboard

Your dashboard will be live at:
```
https://airbnb-dashboard-XXXX.onrender.com
```

The exact URL will be shown in your Render dashboard.

---

## 🎉 That's It!

Your dashboard is now live and accessible from anywhere in the world!

### What You Get (Free Tier):
- ✅ 750 hours/month (enough for continuous hosting)
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push
- ✅ Free subdomain
- ✅ Web dashboard with logs

### ⚠️ Free Tier Notes:
- Spins down after 15 minutes of inactivity
- First load after spin-down takes ~30 seconds
- Perfect for demos and portfolios!

---

## 🔄 Updating Your Dashboard

To update your live dashboard:

```powershell
# Make your changes to files
# Then:
git add .
git commit -m "Update dashboard"
git push
```

Render automatically redeploys when you push to GitHub! 🚀

---

## 🆘 Troubleshooting

### Build Failed?
- Check Render logs for errors
- Verify requirements.txt has correct package versions
- Ensure dataset.csv is committed to git

### Dashboard Not Loading?
- Check Render logs for Python errors
- Verify the start command is: `gunicorn dashboard:server`
- Make sure dataset.csv exists in repository

### Need Help?
- Check Render documentation: https://render.com/docs
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for more options

---

## 💡 Pro Tips

1. **Add a Custom Domain** (Render supports this on free tier!)
2. **Monitor Usage** in Render dashboard
3. **Check Logs** if something goes wrong
4. **Upgrade to Paid** ($7/month) for:
   - No spin-down
   - Faster performance
   - More resources

---

## 📊 Share Your Dashboard!

Once deployed, share your dashboard URL with:
- Your team
- Portfolio
- LinkedIn
- GitHub README

**Your dashboard is now live! 🎉**
