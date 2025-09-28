#!/bin/bash
# GitHub Repository Setup Script
# Run this after creating your GitHub repository

echo "🚀 Setting up GitHub repository for Healthcare Stamp Generator..."

# Get GitHub username from user
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Add remote origin
echo "📡 Adding remote origin..."
git remote add origin https://github.com/$GITHUB_USERNAME/healthcare-stamp-generator.git

# Push main branch
echo "⬆️ Pushing main branch..."
git push -u origin main

# Push develop branch
echo "⬆️ Pushing develop branch..."
git push -u origin develop

# Push feature branch
echo "⬆️ Pushing feature branch..."
git push -u origin feature/enhanced-stamps

# Verify setup
echo "✅ Repository setup complete!"
echo "🔗 Your repository URL: https://github.com/$GITHUB_USERNAME/healthcare-stamp-generator"
echo "📊 Branches pushed:"
git branch -r

echo ""
echo "🎉 Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Set up branch protection rules for main branch"
echo "3. Enable GitHub Actions if needed"
echo "4. Add collaborators if working in a team"