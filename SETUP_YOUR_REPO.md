# 🎯 Setup Your Own Repository for Deployment

## Current Situation:
You're connected to: https://github.com/NanmiCoder/MediaCrawler.git (original)
You need: Your own repository to deploy from

---

## STEP-BY-STEP SETUP:

### STEP 1: Create Your GitHub Repository

1. Go to: https://github.com/new
2. Fill in:
   - Repository name: `MediaCrawler-Internal` (or any name you like)
   - Description: "Internal scraping tool with web dashboard"
   - Choose: **🔒 Private** (to keep it internal to your team)
3. Click "Create repository"

**DO NOT** initialize with README, .gitignore, or license (we already have these)

---

### STEP 2: Change Remote to Your Repository

Copy your repository URL from GitHub (looks like):
```
https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git
```

Then run these commands:

```powershell
# Navigate to MediaCrawler folder
cd "C:\Users\USER\Desktop\trading analysis\penny"

# Remove old remote (original repo)
git remote remove origin

# Add YOUR repository as new remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git

# Verify it changed
git remote -v
```

---

### STEP 3: Commit Your Changes

```powershell
# Add all your new files and changes
git add .

# Commit everything
git commit -m "Add web dashboard and deployment guides"

# Push to YOUR repository
git push -u origin main
```

If prompted for credentials:
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your GitHub password)

**Create token at:** https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scope: `repo` (all repo permissions)
- Generate and copy token
- Use token as password

---

### STEP 4: Verify on GitHub

Go to your repository URL:
```
https://github.com/YOUR-USERNAME/MediaCrawler-Internal
```

You should see all your files including:
- ✅ webapp/ folder
- ✅ DEPLOY_TO_SERVER.md
- ✅ DEPLOY_VIA_GIT.md
- ✅ START_WEB_APP.bat
- ✅ All other files

---

### STEP 5: Deploy to Server

Now you can deploy to your server easily:

**Windows Server:**
```powershell
cd C:\
git clone https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git MediaCrawler
cd MediaCrawler
# Continue with setup (see DEPLOY_TO_SERVER.md)
```

**Linux Server:**
```bash
cd ~
git clone https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git MediaCrawler
cd MediaCrawler
# Continue with setup (see DEPLOY_TO_SERVER.md)
```

---

## 🔄 FUTURE UPDATES

When you make changes:

**On your PC:**
```powershell
cd "C:\Users\USER\Desktop\trading analysis\penny"
git add .
git commit -m "Description of changes"
git push
```

**On server:**
```powershell
# Windows
cd C:\MediaCrawler
git pull
# Restart app

# Linux
cd ~/MediaCrawler
git pull
sudo systemctl restart mediacrawler
```

---

## 🔒 SECURITY: Private Repository

Since you chose **Private**, only YOU can access it.

**To give team members access:**
1. Go to: https://github.com/YOUR-USERNAME/MediaCrawler-Internal/settings/access
2. Click "Add people"
3. Add team members' GitHub usernames
4. Choose permission level (usually "Read" or "Write")

---

## 📝 QUICK REFERENCE

**Your repository structure:**
```
MediaCrawler-Internal/
├── webapp/              ← Web dashboard (YOUR addition)
├── DEPLOY_TO_SERVER.md  ← Deployment guide (YOUR addition)
├── DEPLOY_VIA_GIT.md    ← Git guide (YOUR addition)
├── START_WEB_APP.bat    ← Start script (YOUR addition)
├── config/              ← Original + your modifications
├── media_platform/      ← Original scraping code
└── ... (rest of original files)
```

---

## ✅ DONE!

Once setup is complete, you have:
- ✅ Your own private repository
- ✅ All your custom code saved
- ✅ Easy deployment to any server
- ✅ Easy updates via `git pull`
- ✅ Version control for your changes

Next step: Follow DEPLOY_TO_SERVER.md to deploy to your server!

