from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter
from routes.generate import router as generate_router
import sys
import asyncio

# FORCE Proactor Event Loop on Windows for Playwright compatibility
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(
    title="AI HTML Animation Generator",
    description="Generate animated HTML content from text descriptions using Google Gemini",
    version="1.0.0",
)

# Connect limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(generate_router)


@app.get("/")
@limiter.limit("5/minute")
async def health_check(request):
    return {"status": "ok", "message": "AI HTML Animation Generator API is running"}
