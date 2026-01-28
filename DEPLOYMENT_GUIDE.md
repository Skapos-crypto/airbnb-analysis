# 🚀 Deployment Guide for Streamlit Dashboard

## Option 1: Streamlit Community Cloud (Recommended - FREE & EASIEST)

### Prerequisites
- GitHub account
- Your code in a GitHub repository

### Steps:

1. **Push your code to GitHub**
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial commit: Airbnb pricing dashboard"
   
   # Create a new repository on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `streamlit_dashboard.py`
   - Click "Deploy"

3. **Done!** 🎉
   - Your app will be live at: `https://YOUR_USERNAME-YOUR_REPO_NAME.streamlit.app`
   - Auto-deploys when you push to GitHub

### Important Notes:
- Make sure `dataset.csv` is in your repository
- Free tier includes: 1GB storage, unlimited public apps
- Apps sleep after inactivity but wake up automatically

---

## Option 2: Render (FREE tier available)

### Steps:

1. **Create account at https://render.com**

2. **Create `render.yaml` in your project**
   ```yaml
   services:
     - type: web
       name: airbnb-dashboard
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run streamlit_dashboard.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Push to GitHub** (same as Option 1)

4. **Connect to Render**
   - Dashboard → New → Web Service
   - Connect your GitHub repository
   - Render will auto-detect settings
   - Click "Create Web Service"

5. **Your app will be live at**: `https://YOUR_APP_NAME.onrender.com`

---

## Option 3: Heroku

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create `Procfile`**
   ```
   web: streamlit run streamlit_dashboard.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

---

## Option 4: Railway

### Steps:

1. **Create account at https://railway.app**

2. **Click "New Project" → "Deploy from GitHub"**

3. **Select your repository**

4. **Railway auto-detects Python and runs:**
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_dashboard.py
   ```

5. **Done!** App is live

---

## Quick Deployment Checklist

✅ Files needed:
- `streamlit_dashboard.py` - Main app file
- `dataset.csv` - Your data file
- `requirements.txt` - Dependencies
- `.streamlit/config.toml` - Configuration (optional)
- `README.md` - Documentation

✅ Git commands:
```bash
git init
git add .
git commit -m "Add Streamlit dashboard"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

✅ Test locally first:
```bash
streamlit run streamlit_dashboard.py
```

---

## Troubleshooting

### Issue: App crashes on startup
- Check that `dataset.csv` is in the repository
- Verify all packages in `requirements.txt`
- Check file paths are relative, not absolute

### Issue: Dataset too large
- GitHub has 100MB file limit
- Consider using Git LFS for large files
- Or upload data to cloud storage (S3, Google Drive) and load via URL

### Issue: Slow loading
- Add `@st.cache_data` decorator (already included)
- Consider compressing dataset
- Use `st.spinner()` for loading indicators (already included)

---

## Best Practices

1. **Environment Variables**
   - Store sensitive data in secrets
   - Streamlit Cloud: Add in Settings → Secrets
   - Format: TOML (`.streamlit/secrets.toml`)

2. **Performance**
   - Use `@st.cache_data` for data loading
   - Optimize data processing
   - Compress large datasets

3. **Monitoring**
   - Check deployment logs
   - Monitor resource usage
   - Set up error tracking

---

## Next Steps After Deployment

1. **Custom Domain** (Streamlit Cloud Pro or other platforms)
2. **Password Protection** (use `streamlit-authenticator`)
3. **Analytics** (add Google Analytics)
4. **CI/CD** (automatic testing before deployment)

---

## Cost Comparison

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| **Streamlit Cloud** | ✅ Unlimited public apps | $250/mo for private apps |
| **Render** | ✅ 750 hrs/mo | $7/mo for always-on |
| **Railway** | $5 credit/mo | $5-20/mo |
| **Heroku** | ❌ No free tier | $7/mo minimum |

**Recommendation**: Start with **Streamlit Community Cloud** - it's free, easy, and perfect for dashboards!
