# 🚀 Deploy MediaCrawler to Local Server - Complete Guide

## 📦 STEP 1: Prepare Your Files

### On Your Current PC:

1. **Stop any running web server** (Ctrl+C in terminal)

2. **Create a deployment package:**
   - The entire `MediaCrawler` folder is ready to deploy
   - Location: `C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler`

3. **Optional: Clean up (remove unnecessary files):**
   ```powershell
   cd "C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler"
   
   # Remove browser cache (optional - will regenerate)
   # Remove-Item -Recurse -Force browser_data
   
   # Remove Python cache
   Remove-Item -Recurse -Force __pycache__
   Remove-Item -Recurse -Force *\__pycache__
   ```

---

## 🪟 METHOD A: Windows Server Deployment

### STEP 2: Copy Files to Server

**Option A: Using Remote Desktop (RDP)**

1. **Connect to server:**
   - Press `Win + R`
   - Type: `mstsc`
   - Enter server IP address
   - Login with credentials

2. **Copy MediaCrawler folder:**
   - On your PC: Copy entire `MediaCrawler` folder
   - On server: Paste to `C:\MediaCrawler\`
   
   OR
   
   - Use network share: `\\SERVER-IP\C$\MediaCrawler`

**Option B: Using File Copy (if on same network)**

```powershell
# On your PC, run:
xcopy "C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler" "\\SERVER-IP\C$\MediaCrawler\" /E /I /Y
```

### STEP 3: Setup Python Environment on Server

**Connect to server via RDP, then:**

```powershell
# Open PowerShell on server
cd C:\MediaCrawler

# Check Python version
python --version
# Should be Python 3.9 or higher

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install web app dependencies
pip install jinja2 python-multipart

# Install Playwright browsers
playwright install
```

### STEP 4: Configure Firewall

```powershell
# Allow port 8000
New-NetFirewallRule -DisplayName "MediaCrawler Web" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

# OR use Windows Firewall GUI:
# Control Panel → Windows Defender Firewall → Advanced Settings
# → Inbound Rules → New Rule → Port → TCP → 8000
```

### STEP 5: Start the Web App

**Option A: Manual Start (for testing)**

```powershell
cd C:\MediaCrawler
.\START_WEB_APP.bat
```

**Option B: Run as Windows Service (24/7 - Recommended)**

1. **Download NSSM (Non-Sucking Service Manager):**
   - Visit: https://nssm.cc/download
   - Download and extract to `C:\nssm\`

2. **Install as service:**
   ```powershell
   cd C:\nssm\win64
   
   # Install service
   .\nssm install MediaCrawler "C:\MediaCrawler\venv\Scripts\python.exe" "C:\MediaCrawler\webapp\app.py"
   
   # Set working directory
   .\nssm set MediaCrawler AppDirectory "C:\MediaCrawler"
   
   # Start service
   .\nssm start MediaCrawler
   
   # Check status
   .\nssm status MediaCrawler
   ```

3. **Service management:**
   ```powershell
   # Stop service
   .\nssm stop MediaCrawler
   
   # Restart service
   .\nssm restart MediaCrawler
   
   # Remove service (if needed)
   .\nssm remove MediaCrawler confirm
   ```

### STEP 6: Find Server IP Address

```powershell
# On server, run:
ipconfig

# Look for "IPv4 Address"
# Example: 192.168.1.100
```

### STEP 7: Access from Your Team

**Share this URL with your team:**
```
http://SERVER-IP:8000
```

**Example:**
```
http://192.168.1.100:8000
```

---

## 🐧 METHOD B: Linux Server Deployment

### STEP 2: Copy Files to Server

**Option A: Using SCP (Secure Copy)**

```bash
# On your PC (if you have WSL or Git Bash):
scp -r "C:\Users\USER\Desktop\trading analysis\penny\MediaCrawler" username@SERVER-IP:/home/username/

# OR use WinSCP (GUI tool) - download from: https://winscp.net
```

**Option B: Using SFTP**

1. Install FileZilla or WinSCP
2. Connect to SERVER-IP via SFTP
3. Upload entire `MediaCrawler` folder to `/home/username/`

### STEP 3: Setup on Linux Server

**SSH into server:**

```bash
ssh username@SERVER-IP
```

**Install dependencies:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install python3 python3-pip python3-venv git -y

# Install Playwright system dependencies
sudo apt install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
```

**Setup MediaCrawler:**

```bash
# Navigate to MediaCrawler
cd ~/MediaCrawler

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install jinja2 python-multipart

# Install Playwright browsers
playwright install
```

### STEP 4: Create Systemd Service (for 24/7 running)

```bash
# Create service file
sudo nano /etc/systemd/system/mediacrawler.service
```

**Add this content:**

```ini
[Unit]
Description=MediaCrawler Web Dashboard
After=network.target

[Service]
Type=simple
User=YOUR-USERNAME
WorkingDirectory=/home/YOUR-USERNAME/MediaCrawler
Environment="PATH=/home/YOUR-USERNAME/MediaCrawler/venv/bin"
ExecStart=/home/YOUR-USERNAME/MediaCrawler/venv/bin/python webapp/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Replace `YOUR-USERNAME` with your actual username!**

**Enable and start service:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable mediacrawler

# Start service
sudo systemctl start mediacrawler

# Check status
sudo systemctl status mediacrawler

# View logs
sudo journalctl -u mediacrawler -f
```

### STEP 5: Configure Firewall (Linux)

```bash
# Allow port 8000
sudo ufw allow 8000/tcp
sudo ufw reload

# Check firewall status
sudo ufw status
```

### STEP 6: Find Server IP

```bash
# On server:
hostname -I
# OR
ip addr show | grep inet
```

### STEP 7: Access from Team

Share URL: `http://SERVER-IP:8000`

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Server is running (check with `systemctl status mediacrawler` or NSSM)
- [ ] Port 8000 is open in firewall
- [ ] Can access `http://localhost:8000` from server itself
- [ ] Can access `http://SERVER-IP:8000` from your PC
- [ ] Team members can access from their computers
- [ ] QR code login works
- [ ] Scraping jobs work
- [ ] Data is saved to server

---

## 🔧 TROUBLESHOOTING

### Can't connect from other computers?

**Windows Server:**
```powershell
# Check if app is running
netstat -an | findstr 8000

# Check firewall
Get-NetFirewallRule -DisplayName "MediaCrawler*"

# Test from server browser
Start http://localhost:8000
```

**Linux Server:**
```bash
# Check if app is running
sudo netstat -tulpn | grep 8000

# Check firewall
sudo ufw status

# Check service logs
sudo journalctl -u mediacrawler --since today
```

### App crashes on startup?

**Check logs:**
```bash
# Linux
sudo journalctl -u mediacrawler -n 50

# Windows (in PowerShell where you ran it)
# Errors will show in console
```

**Common fixes:**
1. Make sure Python 3.9+ is installed
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check working directory is correct
4. Ensure all files copied correctly

### Port 8000 already in use?

**Change port in `webapp/app.py`:**

Find line 261 and change:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

To:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Or any other port
```

Then update firewall rules for new port.

---

## 🎯 QUICK START SUMMARY

### Fastest path to deployment:

**Windows Server (5 minutes):**
1. Copy MediaCrawler folder to `C:\MediaCrawler\`
2. Run: `python -m venv venv`
3. Run: `.\venv\Scripts\activate`
4. Run: `pip install -r requirements.txt jinja2 python-multipart`
5. Run: `playwright install`
6. Run: `.\START_WEB_APP.bat`
7. Share: `http://YOUR-SERVER-IP:8000`

**Linux Server (10 minutes):**
1. Copy MediaCrawler folder to server
2. Run setup commands (see STEP 3)
3. Create systemd service (see STEP 4)
4. Start service: `sudo systemctl start mediacrawler`
5. Share: `http://YOUR-SERVER-IP:8000`

---

## 📞 SUPPORT

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check firewall and network settings
4. Review application logs

---

## 🎉 SUCCESS!

Once deployed, your team can access:
```
http://SERVER-IP:8000
```

Everyone on your network can now:
- ✅ Create scraping jobs
- ✅ View scraped data
- ✅ Export to CSV/JSON
- ✅ No coding required!

**Server stays on 24/7 = Team has 24/7 access!**

