#!/bin/bash

# Quick Railway Deployment Script
# Run this to deploy your Customer Revenue Intelligence Platform

set -e  # Exit on error

echo "🚀 Customer Revenue Intelligence - Railway Deployment"
echo "======================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found"
    echo ""
    echo "Install it with:"
    echo "  npm install -g @railway/cli"
    echo ""
    exit 1
fi

echo "✓ Railway CLI found"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Customer Revenue Intelligence Platform"
    echo "✓ Git initialized"
else
    echo "✓ Git repository exists"
fi

echo ""
echo "🔐 Logging in to Railway..."
railway login

echo ""
echo "🏗️  Creating Railway project..."
railway init

echo ""
echo "📤 Deploying to Railway..."
railway up

echo ""
echo "======================================================"
echo "✅ Deployment Complete!"
echo "======================================================"
echo ""
echo "Your app is being deployed. It will be available in 2-3 minutes."
echo ""
echo "Next steps:"
echo "1. Get your URL: railway open"
echo "2. View logs: railway logs"
echo "3. Check status: railway status"
echo ""
echo "Test your deployment:"
echo "  curl \$(railway variables get URL)/api/health"
echo ""
echo "======================================================"
