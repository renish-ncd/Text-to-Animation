from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from services.groq_service import generate_animation
from services.gif_service import generate_gif_from_html
from services.sanitizer import sanitize_html
from limiter import limiter

router = APIRouter()


class AnimationRequest(BaseModel):
    prompt: str


class AnimationResponse(BaseModel):
    generated_html: str


class GifRequest(BaseModel):
    html: str


def cleanup_file(path: str):
    """Remove temporary file."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error removing file {path}: {e}")


@router.post("/generate-animation", response_model=AnimationResponse)
@limiter.limit("10/minute")
async def generate_animation_endpoint(request: Request, body: AnimationRequest):
    """Generate an HTML animation from a text prompt using Groq."""
    if not body.prompt or not body.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        print(f"Generating animation with Groq for prompt: {body.prompt[:50]}...")
        generated_html = generate_animation(body.prompt.strip())
        
        # Sanitize HTML
        safe_html = sanitize_html(generated_html)
        print("Animation generated and sanitized successfully.")
        
        return AnimationResponse(generated_html=safe_html)
    except RuntimeError as e:
        print(f"Groq Generation Runtime Error: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        print(f"Unexpected Error during animation generation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/generate-gif")
@limiter.limit("5/minute")
async def generate_gif_endpoint(request: Request, body: GifRequest, background_tasks: BackgroundTasks):
    """Generate a GIF from HTML content."""
    if not body.html or not body.html.strip():
        raise HTTPException(status_code=400, detail="HTML content cannot be empty")

    try:
        print("Starting deterministic GIF generation...")
        # Now synchronous call -> Migrated to ASYNC
        gif_path = await generate_gif_from_html(body.html)
        print(f"GIF generated at: {gif_path}")
        
        # Schedule file cleanup after response is sent
        background_tasks.add_task(cleanup_file, gif_path)
        
        return FileResponse(
            path=gif_path,
            media_type="image/gif",
            filename="animation.gif"
        )
    except Exception as e:
        print(f"GIF Generation Critical Error: {e}")
        raise HTTPException(status_code=500, detail=f"GIF generation failed: {str(e)}")

