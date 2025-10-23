# MediaCrawler Web Dashboard

A user-friendly web interface for MediaCrawler - No coding required!

## 🎯 What is This?

This web application provides an easy-to-use interface for the MediaCrawler tool. Your team can scrape social media data through a simple web browser without writing any code.

## 🚀 Quick Start

### For Windows Users:

1. **Double-click** `START_WEB_APP.bat` in the MediaCrawler folder
2. Wait for the server to start (you'll see "Application startup complete")
3. Open your browser and go to: `http://localhost:8000`
4. Start scraping!

### For Other Team Members:

If the server is running on Computer A, other team members can access it at:
```
http://COMPUTER-A-IP:8000
```

To find the IP address:
- On Windows: Open Command Prompt and type `ipconfig`
- Look for "IPv4 Address" (e.g., 192.168.1.100)

## 📱 How to Use

### 1. Dashboard (Home Page)

- View active scraping jobs
- See job history
- Quick access to all features

### 2. Create New Job

**Steps:**
1. Click "New Job" in the navigation
2. Select a platform (Xiaohongshu, Douyin, Bilibili, etc.)
3. Enter keywords to search (separated by commas)
4. Set maximum number of posts to scrape
5. Choose options (comments, images, etc.)
6. Click "Start Scraping"

**First Time Login:**
- A browser window will open with a QR code
- Scan with your phone to login
- The login state will be saved for future use

### 3. View Data

**Features:**
- Browse all scraped data
- Filter by platform
- Search within results
- Export to CSV or JSON
- View post details

### 4. Export Data

**Available Formats:**
- **CSV** - For Excel and data analysis
- **JSON** - For developers and APIs

## 🔧 Configuration

The web app uses the same configuration as the command-line tool.

Edit settings in: `config/base_config.py`

**Common Settings:**
```python
HEADLESS = False  # Show browser (for QR code scanning)
SAVE_DATA_OPTION = "json"  # json, csv, or sqlite
ENABLE_GET_COMMENTS = True  # Scrape comments
CRAWLER_MAX_NOTES_COUNT = 15  # Default posts per job
```

## 👥 Team Access

### Local Network Only (Default):

1. Start the web app on one computer
2. Find the computer's IP address
3. Share the URL with team: `http://IP-ADDRESS:8000`
4. Everyone on the same network can access it

**Example:**
- Server computer IP: 192.168.1.100
- Team members visit: `http://192.168.1.100:8000`

### Security Notes:

- The web app is designed for internal use only
- Only accessible within your office network
- No authentication required (add if needed)
- Keep the computer with the server running

## 📊 Understanding the Interface

### Dashboard Icons:

- 🟢 **Running** - Job is currently scraping
- ✅ **Completed** - Job finished successfully  
- ❌ **Failed** - Job encountered an error
- ⏸️ **Queued** - Job waiting to start

### Data View:

- **Title** - Post title/content preview
- **Author** - Creator username and avatar
- **Engagement** - Likes, comments, shares
- **Date** - When the post was created
- **Actions** - View original post, export, etc.

## 🛠️ Troubleshooting

### Problem: Can't access web app

**Solution:**
1. Check if the server is running
2. Try `http://localhost:8000` on the server computer
3. Make sure Windows Firewall allows port 8000
4. Verify you're on the same network

### Problem: QR code won't scan

**Solution:**
1. Make sure `HEADLESS = False` in config
2. Browser window should open automatically
3. If not, manually open the platform website and login
4. Check `ENABLE_CDP_MODE` setting

### Problem: Job fails

**Solution:**
1. Check the error message in the dashboard
2. Verify keywords are correct
3. Make sure you're logged in to the platform
4. Try with fewer posts first (max_notes = 5)

## 📝 Technical Details

**Built with:**
- FastAPI (Python web framework)
- Bootstrap 5 (UI framework)
- Jinja2 (Template engine)

**Port:** 8000 (default)

**Data Storage:** `MediaCrawler/data/` folder

**Logs:** Check terminal/console where you started the app

## 🔐 Adding Authentication (Optional)

If you want to add user login:

1. Edit `webapp/app.py`
2. Add authentication middleware
3. Create user database
4. Add login/logout pages

(Contact developer for assistance)

## 📞 Support

**Common Questions:**

**Q: Can I run multiple jobs at once?**
A: Yes, jobs run in the background. You can start new jobs while others are running.

**Q: Where is the data saved?**
A: In `MediaCrawler/data/PLATFORM/json/` folder

**Q: Can I schedule automatic scraping?**
A: Not yet, but you can start jobs manually anytime through the web interface.

**Q: What platforms are supported?**
A: Xiaohongshu (小红书), Douyin (抖音), Kuaishou (快手), Bilibili (B站), Weibo (微博), Zhihu (知乎), Baidu Tieba (百度贴吧)

## 🎓 Tips for Best Results

1. **Start Small**: Test with 5-10 posts first
2. **Login First**: Complete QR code scan before large jobs
3. **Check Data**: Review results in "View Data" before exporting
4. **Save Login**: Keep browser window open to maintain login
5. **Export Regularly**: Download CSV backups of important data

## 🔄 Updating

To update the web app:
1. Stop the server (Ctrl+C in the terminal)
2. Update the code
3. Restart by running `START_WEB_APP.bat`

## 📧 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Look at the terminal output for error messages
3. Contact your IT administrator
4. Review the main MediaCrawler documentation

---

**Happy Scraping! 🚀**

For internal use only. Please respect platform terms of service and use responsibly.

