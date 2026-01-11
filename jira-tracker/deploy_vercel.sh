#!/bin/bash

# ===================================
# Vercel Deployment Script (Frontend)
# ===================================

echo "🚀 Deploying Frontend to Vercel..."
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found."
    echo "Install it with: npm install -g vercel"
    exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "⚠️  .env.production not found"
    echo "Creating from example..."

    if [ -f ".env.production.example" ]; then
        cp .env.production.example .env.production
        echo "✅ Created .env.production"
        echo "⚠️  IMPORTANT: Update REACT_APP_API_URL with your backend URL"
        echo ""
        read -p "Press Enter to continue or Ctrl+C to cancel..."
    else
        echo "❌ .env.production.example not found"
        echo "Create .env.production with:"
        echo "   REACT_APP_API_URL=https://your-backend.railway.app"
        exit 1
    fi
fi

# Build the project
echo "📦 Building project..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your app should be live at: https://your-app.vercel.app"
echo ""
echo "⚙️  To set environment variables in Vercel:"
echo "   vercel env add REACT_APP_API_URL"
echo ""
echo "Or via Vercel Dashboard:"
echo "   Project Settings → Environment Variables"
echo ""
