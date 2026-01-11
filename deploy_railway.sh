#!/bin/bash

# ===================================
# Railway Deployment Script
# ===================================

echo "🚀 Deploying to Railway..."
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found."
    echo "Install it with: npm install -g @railway/cli"
    echo "Or deploy from: https://railway.app"
    exit 1
fi

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Logging in to Railway..."
    railway login
fi

# Check if project is linked
if ! railway status &> /dev/null; then
    echo "🔗 Linking to Railway project..."
    railway link
fi

# Deploy
echo "📦 Deploying backend to Railway..."
railway up

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📊 View deployment status:"
echo "   railway status"
echo ""
echo "📝 View logs:"
echo "   railway logs"
echo ""
echo "🌐 Open in browser:"
echo "   railway open"
echo ""
echo "⚙️  Set environment variables:"
echo "   railway variables set KEY=value"
echo ""
echo "📋 Required environment variables:"
echo "   - SECRET_KEY"
echo "   - JWT_SECRET_KEY"
echo "   - DATABASE_URL (if using PostgreSQL)"
echo "   - CORS_ORIGINS"
echo ""
