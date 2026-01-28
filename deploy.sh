#!/bin/bash
# Quick deployment setup script

echo "🚀 Airbnb Dashboard - Deployment Setup"
echo "======================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Airbnb pricing dashboard"
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

echo ""
echo "📋 Deployment Options:"
echo ""
echo "1. Render (Recommended - Free tier)"
echo "   - Push to GitHub"
echo "   - Connect at https://render.com"
echo "   - Auto-deploys from render.yaml"
echo ""
echo "2. Heroku"
echo "   Run: heroku create airbnb-dashboard"
echo "   Run: git push heroku main"
echo ""
echo "3. Railway"
echo "   - Push to GitHub"
echo "   - Connect at https://railway.app"
echo ""
echo "4. Local with Gunicorn"
echo "   Run: gunicorn dashboard:server"
echo ""
echo "✅ All deployment files ready!"
echo "📖 See DEPLOYMENT.md for detailed instructions"
