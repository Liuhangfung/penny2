# 🎉 MediaCrawler Web Dashboard - Setup Complete!

## ✅ What Was Built

A complete web application with:

### 📁 **New Files Created:**

```
MediaCrawler/
├── START_WEB_APP.bat          # Windows startup script (DOUBLE-CLICK THIS!)
├── QUICK_START_WEB.md          # Quick start guide
├── WEB_APP_SETUP.md            # This file
└── webapp/
    ├── __init__.py
    ├── app.py                   # Main web application
    ├── README.md                # Full documentation
    ├── static/
    │   └── style.css            # Custom styles
    └── templates/
        ├── base.html            # Base template
        ├── index.html           # Dashboard homepage
        ├── new_job.html         # Create job form
        └── view_data.html       # Data viewing page
```

## 🚀 How to Start (3 Steps)

### Step 1: Double-Click START_WEB_APP.bat

Location: `MediaCrawler/START_WEB_APP.bat`

**Just double-click it!** The server will start automatically.

### Step 2: Open Your Browser

Go to: **http://localhost:8000**

### Step 3: Start Scraping!

- Click "New Job"
- Fill in the form  
- Click "Start Scraping"
- Scan QR code (first time only)
- View your data!

---

## 🎨 Features

### ✨ Web Interface Includes:

1. **Dashboard (Homepage)**
   - View active jobs
   - See job history
   - Quick action buttons
   - Auto-refresh when jobs are running

2. **New Job Page**
   - Select platform dropdown
   - Enter keywords
   - Set max posts
   - Choose options (comments, etc.)
   - Beautiful form validation

3. **View Data Page**
   - Browse scraped posts
   - Filter by platform
   - Search within results
   - Export to CSV/JSON
   - View post details with images

4. **Export Functionality**
   - CSV format (for Excel)
   - JSON format (for developers)
   - One-click download

---

## 👥 Sharing with Your Team

### Local Network Access:

**1. Find Your IP Address:**

Windows:
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**2. Share the URL:**

Tell your team to visit:
```
http://YOUR-IP-ADDRESS:8000
```

**Example:**
```
http://192.168.1.100:8000
```

**3. Keep Server Running:**

Leave the computer ON with the web app running!

---

## 🔧 Configuration

All settings in: `config/base_config.py`

**Important Settings:**

```python
# Basic Settings
PLATFORM = "xhs"                    # Default platform
KEYWORDS = "编程副业,Python"         # Default keywords  
CRAWLER_MAX_NOTES_COUNT = 15        # Default posts per job

# Display Settings  
HEADLESS = False                    # Show browser (for QR codes)
ENABLE_CDP_MODE = False             # Use standard mode

# Data Settings
SAVE_DATA_OPTION = "json"           # json, csv, or sqlite
ENABLE_GET_COMMENTS = True          # Scrape comments
ENABLE_GET_MEIDAS = False           # Download images/videos
```

---

## 📊 What Each Page Does

### 🏠 Dashboard (`/`)
- Shows running jobs with progress bars
- Displays recent job history
- Quick links to create jobs and view data
- Auto-refreshes every 10 seconds

### ➕ New Job (`/new-job`)
- Form to configure scraping
- Platform selection
- Keyword input
- Options configuration
- Submits job to background queue

### 📋 View Data (`/view-data`)
- Table display of scraped posts
- Filter by platform
- Search functionality
- Export buttons
- Paginated results (50 per page)

---

## 🛠️ Technical Details

### Stack:
- **Backend:** FastAPI (Python)
- **Frontend:** HTML + Bootstrap 5
- **Templates:** Jinja2
- **Async:** Background tasks with asyncio

### API Endpoints:

```
GET  /                          # Dashboard
GET  /new-job                   # New job form
GET  /view-data                 # View scraped data
POST /api/start-job             # Start scraping job
GET  /api/jobs                  # Get all jobs
GET  /api/job/{job_id}          # Get specific job
GET  /api/export/{platform}/{format}  # Export data
```

### Port:
- Default: **8000**
- Can be changed in `app.py`

### Data Storage:
- Location: `MediaCrawler/data/PLATFORM/json/`
- Format: JSON files with timestamps
- Naming: `search_contents_YYYY-MM-DD.json`

---

## 🔍 Troubleshooting

### ❌ Problem: "Address already in use"

**Solution:** Port 8000 is taken. Either:
- Close other programs using port 8000
- Or edit `app.py` line: `uvicorn.run(app, host="0.0.0.0", port=8000)` 
- Change `8000` to `8001` or another port

### ❌ Problem: "ModuleNotFoundError"

**Solution:** Virtual environment not activated

```bash
cd MediaCrawler
.\venv\Scripts\activate
cd webapp
python app.py
```

### ❌ Problem: Browser doesn't open QR code

**Solution:** In `config/base_config.py` set:
```python
HEADLESS = False
ENABLE_CDP_MODE = False
```

### ❌ Problem: Can't access from other computers

**Solution:** Check Windows Firewall
1. Open Windows Firewall
2. Allow Python through firewall
3. Allow port 8000 (or create inbound rule)

### ❌ Problem: Job fails immediately

**Solution:** 
1. Check you're logged in (scan QR code first time)
2. Try with fewer posts (max_notes = 5)
3. Check keywords are valid
4. View error in dashboard

---

## 🎯 Usage Examples

### Example 1: Scrape Xiaohongshu Posts

1. Open http://localhost:8000
2. Click "New Job"
3. Select: 小红书 Xiaohongshu
4. Keywords: `编程副业,Python教程`
5. Max Posts: `20`
6. Check "Get Comments"
7. Click "Start Scraping"
8. Scan QR code (if first time)
9. View results in "View Data"

### Example 2: Export Data

1. Go to "View Data"
2. Select platform from dropdown
3. Click "Export CSV"
4. Open in Excel

### Example 3: Multiple Jobs

1. Start Job A (Xiaohongshu)
2. While Job A runs, create Job B (Douyin)
3. Both run in background
4. Check progress on dashboard

---

## 📈 Next Steps (Optional Enhancements)

Want to add more features? Consider:

1. **User Authentication**
   - Add login/logout
   - Multiple user accounts
   - Role-based access

2. **Scheduling**
   - Schedule jobs to run at specific times
   - Recurring jobs (daily/weekly)
   - Email notifications

3. **Analytics**
   - Charts and graphs
   - Trend analysis
   - Keyword insights

4. **Advanced Filters**
   - Date range selection
   - Engagement metrics filtering
   - Author filtering

5. **Cloud Deployment**
   - Deploy to DigitalOcean ($6/month)
   - Custom domain
   - HTTPS encryption

**(Contact developer for these features)**

---

## 🔐 Security Notes

**Current Setup:**
- ✅ Local network only (default)
- ✅ No internet exposure
- ⚠️ No authentication (add if sharing widely)

**For Production Use:**
- Add user authentication
- Use HTTPS
- Add rate limiting
- Implement access logs

---

## 📞 Support & Help

**Read First:**
1. `QUICK_START_WEB.md` - Quick start guide
2. `webapp/README.md` - Full documentation
3. This file - Setup and troubleshooting

**Still Need Help?**
- Check terminal output for errors
- Review browser console (F12)
- Check `data/` folder permissions
- Verify virtual environment is activated

---

## ✨ Summary

You now have:
- ✅ A beautiful web dashboard
- ✅ No-code interface for your team
- ✅ Easy data viewing and export
- ✅ Background job processing
- ✅ Local network sharing
- ✅ Complete documentation

**Cost: $0** (runs on your computer)
**Deployment: Local network**
**Access: http://localhost:8000**

---

## 🎉 You're Ready!

**Just double-click:** `START_WEB_APP.bat`

**Then open:** http://localhost:8000

**Start scraping with clicks, not code!** 🚀

---

*Built with ❤️ for your team's internal use*

