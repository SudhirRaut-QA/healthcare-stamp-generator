# GitHub Repository Setup Script for PowerShell
# Run this after creating your GitHub repository

Write-Host "🚀 Setting up GitHub repository for Healthcare Stamp Generator..." -ForegroundColor Green

# Get GitHub username from user
$GITHUB_USERNAME = Read-Host "Enter your GitHub username"

# Add remote origin
Write-Host "📡 Adding remote origin..." -ForegroundColor Yellow
git remote add origin "https://github.com/$GITHUB_USERNAME/healthcare-stamp-generator.git"

# Push main branch
Write-Host "⬆️ Pushing main branch..." -ForegroundColor Yellow
git push -u origin main

# Push develop branch
Write-Host "⬆️ Pushing develop branch..." -ForegroundColor Yellow
git push -u origin develop

# Push feature branch
Write-Host "⬆️ Pushing feature branch..." -ForegroundColor Yellow
git push -u origin "feature/enhanced-stamps"

# Verify setup
Write-Host "✅ Repository setup complete!" -ForegroundColor Green
Write-Host "🔗 Your repository URL: https://github.com/$GITHUB_USERNAME/healthcare-stamp-generator" -ForegroundColor Cyan
Write-Host "📊 Branches pushed:" -ForegroundColor Yellow
git branch -r

Write-Host ""
Write-Host "🎉 Next steps:" -ForegroundColor Green
Write-Host "1. Visit your repository on GitHub" -ForegroundColor White
Write-Host "2. Set up branch protection rules for main branch" -ForegroundColor White
Write-Host "3. Enable GitHub Actions if needed" -ForegroundColor White
Write-Host "4. Add collaborators if working in a team" -ForegroundColor White