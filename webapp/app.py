"""
MediaCrawler Web Application
A user-friendly web interface for the MediaCrawler tool
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Change to MediaCrawler root directory
import sys
MEDIACRAWLER_ROOT = Path(__file__).parent.parent
os.chdir(MEDIACRAWLER_ROOT)
sys.path.insert(0, str(MEDIACRAWLER_ROOT))

import config
from base.base_crawler import AbstractCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.zhihu import ZhihuCrawler

# Initialize FastAPI app
app = FastAPI(title="MediaCrawler Web Dashboard")

# Setup templates and static files
WEBAPP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(WEBAPP_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(WEBAPP_DIR / "static")), name="static")

# Add custom Jinja2 filters
def datetime_filter(timestamp):
    """Convert Unix timestamp to readable date"""
    try:
        from datetime import datetime
        if timestamp:
            dt = datetime.fromtimestamp(int(timestamp))
            return dt.strftime('%Y-%m-%d %H:%M')
        return 'N/A'
    except:
        return 'N/A'

templates.env.filters['datetime'] = datetime_filter

# Job tracking
active_jobs = {}
job_history = []

# Platform mapping
PLATFORM_CRAWLERS = {
    "xhs": ("小红书 Xiaohongshu", XiaoHongShuCrawler),
    "dy": ("抖音 Douyin", DouYinCrawler),
    "ks": ("快手 Kuaishou", KuaishouCrawler),
    "bili": ("B站 Bilibili", BilibiliCrawler),
    "wb": ("微博 Weibo", WeiboCrawler),
    "tieba": ("百度贴吧 Tieba", TieBaCrawler),
    "zhihu": ("知乎 Zhihu", ZhihuCrawler),
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Dashboard homepage"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "platforms": PLATFORM_CRAWLERS,
            "active_jobs": active_jobs,
            "job_history": job_history[-10:]  # Last 10 jobs
        }
    )


@app.get("/new-job", response_class=HTMLResponse)
async def new_job_page(request: Request):
    """Page to create a new scraping job"""
    return templates.TemplateResponse(
        "new_job.html",
        {
            "request": request,
            "platforms": PLATFORM_CRAWLERS
        }
    )


@app.post("/api/start-job")
async def start_job(
    background_tasks: BackgroundTasks,
    platform: str = Form(...),
    keywords: str = Form(...),
    max_notes: int = Form(15),
    get_comments: bool = Form(False),
    crawler_type: str = Form("search")
):
    """Start a new scraping job"""
    job_id = f"{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    job_config = {
        "job_id": job_id,
        "platform": platform,
        "keywords": keywords,
        "max_notes": max_notes,
        "get_comments": get_comments,
        "crawler_type": crawler_type,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "progress": 0
    }
    
    active_jobs[job_id] = job_config
    
    # Add job to background tasks
    background_tasks.add_task(run_scraping_job, job_id, job_config)
    
    return JSONResponse({
        "success": True,
        "job_id": job_id,
        "message": "Job started successfully!"
    })


async def run_scraping_job(job_id: str, job_config: dict):
    """Background task to run scraping"""
    import logging
    logger = logging.getLogger("MediaCrawler")
    
    try:
        active_jobs[job_id]["status"] = "running"
        active_jobs[job_id]["progress"] = 10
        
        logger.info(f"[WebApp] Starting job {job_id}")
        
        # Update config dynamically
        config.PLATFORM = job_config["platform"]
        config.KEYWORDS = job_config["keywords"]
        config.CRAWLER_MAX_NOTES_COUNT = job_config["max_notes"]
        config.ENABLE_GET_COMMENTS = job_config["get_comments"]
        config.CRAWLER_TYPE = job_config["crawler_type"]
        
        active_jobs[job_id]["progress"] = 30
        
        # Get crawler class
        crawler_class = PLATFORM_CRAWLERS[job_config["platform"]][1]
        crawler = crawler_class()
        
        active_jobs[job_id]["progress"] = 50
        logger.info(f"[WebApp] Running crawler for {job_id}")
        
        # Run crawler
        await crawler.start()
        
        logger.info(f"[WebApp] Job {job_id} completed successfully")
        
        active_jobs[job_id]["status"] = "completed"
        active_jobs[job_id]["progress"] = 100
        active_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
        # Move to history
        job_history.append(active_jobs[job_id].copy())
        
    except Exception as e:
        logger.error(f"[WebApp] Job {job_id} failed: {str(e)}")
        active_jobs[job_id]["status"] = "failed"
        active_jobs[job_id]["error"] = str(e)
        active_jobs[job_id]["progress"] = 0
        job_history.append(active_jobs[job_id].copy())


@app.get("/api/job-status/{job_id}")
async def get_job_status(job_id: str):
    """Get current job status including QR code info"""
    if job_id in active_jobs:
        job_info = active_jobs[job_id].copy()
        
        # Check for QR code files
        qr_code_path = None
        import glob
        qr_files = sorted(glob.glob("/tmp/*.PNG"), key=os.path.getmtime, reverse=True)
        if qr_files:
            # Get the most recent QR code
            qr_code_path = qr_files[0]
            job_info["qr_code_available"] = True
            job_info["qr_code_file"] = os.path.basename(qr_code_path)
        else:
            job_info["qr_code_available"] = False
            
        return JSONResponse(job_info)
    return JSONResponse({"error": "Job not found"}, status_code=404)


@app.get("/api/qrcode/{filename}")
async def get_qrcode(filename: str):
    """Serve QR code image"""
    qr_path = f"/tmp/{filename}"
    if os.path.exists(qr_path):
        return FileResponse(qr_path, media_type="image/png")
    return JSONResponse({"error": "QR code not found"}, status_code=404)


@app.get("/view-data", response_class=HTMLResponse)
async def view_data_page(request: Request, platform: Optional[str] = "xhs", page: int = 1):
    """Page to view scraped data with pagination"""
    data_dir = MEDIACRAWLER_ROOT / "data" / platform / "json"
    
    # Pagination settings
    items_per_page = 50
    
    # Get available data files
    files = []
    if data_dir.exists():
        files = sorted(data_dir.glob("search_contents_*.json"), reverse=True)
    
    # Load data from most recent file
    data = []
    selected_file = None
    if files:
        selected_file = files[0]
        try:
            with open(selected_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Calculate pagination
    total_count = len(data)
    total_pages = max(1, (total_count + items_per_page - 1) // items_per_page)  # Ceiling division
    page = max(1, min(page, total_pages))  # Ensure page is within bounds
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_data = data[start_idx:end_idx]
    
    # Calculate page range for pagination display
    page_range_start = max(1, page - 2)
    page_range_end = min(total_pages + 1, page + 3)
    page_numbers = list(range(page_range_start, page_range_end))
    
    return templates.TemplateResponse(
        "view_data.html",
        {
            "request": request,
            "platform": platform,
            "platforms": PLATFORM_CRAWLERS,
            "data": paginated_data,
            "total_count": total_count,
            "selected_file": selected_file.name if selected_file else None,
            "current_page": page,
            "total_pages": total_pages,
            "items_per_page": items_per_page,
            "start_item": start_idx + 1,
            "end_item": min(end_idx, total_count),
            "page_numbers": page_numbers,
            "show_first": page > 3,
            "show_last": page < total_pages - 2
        }
    )


@app.get("/api/export/{platform}/{format}")
async def export_data(platform: str, format: str = "csv"):
    """Export data in various formats"""
    data_dir = MEDIACRAWLER_ROOT / "data" / platform / "json"
    
    # Get most recent data file
    files = sorted(data_dir.glob("search_contents_*.json"), reverse=True)
    if not files:
        return JSONResponse({"error": "No data found"}, status_code=404)
    
    # Load data
    with open(files[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if format == "json":
        return FileResponse(
            files[0],
            media_type="application/json",
            filename=files[0].name
        )
    
    elif format == "csv":
        import csv
        import io
        
        # Create CSV
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        # Return CSV file
        from fastapi.responses import StreamingResponse
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={platform}_data_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )


@app.get("/api/jobs")
async def get_jobs():
    """Get current jobs status"""
    return JSONResponse({
        "active_jobs": list(active_jobs.values()),
        "job_history": job_history[-20:]
    })


@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str):
    """Get specific job status"""
    if job_id in active_jobs:
        return JSONResponse(active_jobs[job_id])
    
    # Check history
    for job in job_history:
        if job["job_id"] == job_id:
            return JSONResponse(job)
    
    return JSONResponse({"error": "Job not found"}, status_code=404)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MediaCrawler Web Dashboard Starting...")
    print("=" * 60)
    print(f"📱 Access the dashboard at: http://localhost:8000")
    print(f"📱 Or from other computers: http://YOUR-IP:8000")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

