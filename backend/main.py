from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pathlib import Path
import os
from .products import products
from .config import settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Tienda Online API",
    description="API segura para tienda de productos infantiles",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    if settings.ENABLE_SECURITY_HEADERS:
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Enable XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data: http: https: blob:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Permissions Policy
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

# API Endpoints
@app.get("/api/products")
@limiter.limit(settings.RATE_LIMIT_PER_MINUTE)
async def get_products(request: Request):
    """Get all products with rate limiting"""
    return products

@app.get("/api/config")
@limiter.limit("30/minute")
async def get_config(request: Request):
    """Get public configuration (contact info)"""
    return {
        "whatsappNumber": settings.WHATSAPP_NUMBER,
        "contactEmail": settings.CONTACT_EMAIL
    }

# Mount the frontend directory to serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

# Serve images from img directory
@app.get("/img/{filename}")
async def serve_image(filename: str):
    """
    Serve image files from the img directory with security validation
    """
    # Strict validation to prevent directory traversal
    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Whitelist allowed image extensions
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.avif'}
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Construct safe file path
    img_dir = Path("frontend/img").resolve()
    file_path = (img_dir / filename).resolve()
    
    # Ensure the resolved path is within img directory
    try:
        file_path.relative_to(img_dir)
    except ValueError:
        # Path is outside img directory
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file exists
    if file_path.is_file():
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="File not found")


# Serve other static files with improved security
@app.get("/{filename}")
async def serve_frontend_file(filename: str):
    """
    Serve frontend files with enhanced path traversal protection
    """
    # Strict validation to prevent directory traversal
    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Whitelist allowed file extensions
    allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.avif'}
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        # Return index.html for potential SPA routing
        return FileResponse('frontend/index.html')
    
    # Construct safe file path
    frontend_dir = Path("frontend").resolve()
    file_path = (frontend_dir / filename).resolve()
    
    # Ensure the resolved path is within frontend directory
    try:
        file_path.relative_to(frontend_dir)
    except ValueError:
        # Path is outside frontend directory
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file exists
    if file_path.is_file():
        return FileResponse(file_path)
    
    # Fallback to index.html
    return FileResponse('frontend/index.html')

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Custom error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler that doesn't leak information"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Custom 500 handler that doesn't expose internal details"""
    # Log the actual error internally (you should add proper logging)
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

