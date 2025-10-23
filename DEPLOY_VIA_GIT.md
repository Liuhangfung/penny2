# 🚀 Deploy MediaCrawler via Git (EASIEST METHOD)

## ✅ Why Use Git?
- One command deployment: `git clone`
- Easy updates: `git pull`
- Version control included
- Works everywhere

---

## STEP 1: Push to GitHub (One-time setup)

### A. Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `MediaCrawler-Internal`
3. **Choose: Private** (to keep it internal)
4. Click "Create repository"

### B. Push Your Code (on your PC)

```powershell
# Navigate to MediaCrawler folder
cd "C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler"

# Initialize Git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - MediaCrawler web app"

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important Files to Exclude:**

Create `.gitignore` file before pushing:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
venv/
env/

# Browser data
browser_data/
account.db
account.json

# Data files
data/
*.csv
*.json
*.db

# OS files
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/
```

---

## STEP 2: Deploy to Server (Super Easy!)

### On Windows Server:

```powershell
# Clone repository
cd C:\
git clone https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git MediaCrawler

# If Git not installed, download from: https://git-scm.com/download/win

# Then continue with normal setup
cd C:\MediaCrawler
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt jinja2 python-multipart
playwright install

# Open firewall
New-NetFirewallRule -DisplayName "MediaCrawler" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

# Start app
.\START_WEB_APP.bat
```

### On Linux Server:

```bash
# Clone repository
cd ~
git clone https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git MediaCrawler

# If Git not installed:
sudo apt install git -y

# Then continue with normal setup
cd ~/MediaCrawler
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt jinja2 python-multipart
playwright install

# Open firewall
sudo ufw allow 8000/tcp

# Create systemd service (see DEPLOY_TO_SERVER.md)
# Or run manually:
python webapp/app.py
```

---

## 🔄 UPDATE CODE ON SERVER (Future Updates)

When you make changes and want to update server:

### 1. Push changes from your PC:
```powershell
cd "C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler"
git add .
git commit -m "Updated pagination and date display"
git push
```

### 2. Pull changes on server:
```powershell
# Windows Server
cd C:\MediaCrawler
git pull

# Restart app
# If using service: nssm restart MediaCrawler
# If running manually: Ctrl+C then .\START_WEB_APP.bat
```

```bash
# Linux Server
cd ~/MediaCrawler
git pull

# Restart service
sudo systemctl restart mediacrawler
```

---

## 🔒 SECURITY: Using Private Repository

**If repository is PRIVATE, you'll need authentication:**

### Option A: Personal Access Token (Recommended)

1. **Create token on GitHub:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (all)
   - Generate token
   - **COPY TOKEN NOW** (you won't see it again!)

2. **Clone with token:**
   ```bash
   git clone https://YOUR-TOKEN@github.com/YOUR-USERNAME/MediaCrawler-Internal.git
   ```

3. **Or configure Git credential helper:**
   ```bash
   git config --global credential.helper store
   git clone https://github.com/YOUR-USERNAME/MediaCrawler-Internal.git
   # Enter username and token when prompted
   ```

### Option B: SSH Keys (More Secure)

1. **Generate SSH key on server:**
   ```bash
   ssh-keygen -t ed25519 -C "server@yourcompany.com"
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste public key

3. **Clone with SSH:**
   ```bash
   git clone git@github.com:YOUR-USERNAME/MediaCrawler-Internal.git
   ```

---

## 📦 ALTERNATIVE: Direct Download (No Git on Server)

If you don't want to install Git on server:

1. **On GitHub:**
   - Go to your repository
   - Click "Code" → "Download ZIP"

2. **Transfer ZIP to server:**
   - Copy via RDP/SCP
   - Extract on server
   - Continue with normal setup

---

## ✅ COMPLETE WORKFLOW SUMMARY

### Initial Setup (One time):
```
Your PC → Git → GitHub → Server (git clone) → Setup & Run
```

### Future Updates:
```
Your PC (make changes) → git push → GitHub
Server → git pull → restart app
```

---

## 🎯 RECOMMENDED WORKFLOW

1. ✅ Use **private GitHub repository**
2. ✅ Use `.gitignore` to exclude sensitive data
3. ✅ Use Personal Access Token for authentication
4. ✅ Update server with `git pull` (takes 5 seconds!)

---

## 🔧 TROUBLESHOOTING

### Git not installed on server?

**Windows:**
Download from: https://git-scm.com/download/win

**Linux:**
```bash
sudo apt install git -y
```

### Authentication failed?

Make sure you're using Personal Access Token, not password.
GitHub doesn't accept passwords anymore.

### "Permission denied" on Linux?

```bash
# Fix permissions
sudo chown -R $USER:$USER ~/MediaCrawler
```

---

## 🎉 DONE!

Now you can:
- ✅ Deploy to any server with one command
- ✅ Update server in seconds
- ✅ Keep version history
- ✅ Team members can deploy easily too

**Next step:** See `DEPLOY_TO_SERVER.md` for complete server setup after cloning.

