import os
import asyncio
import tempfile
import sys
import subprocess
from fastapi import HTTPException

# Path to the standalone script
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "generate_gif_standalone.py")

async def generate_gif_from_html(html_content: str, width: int = 600, height: int = 400, duration: int = 3, fps: int = 30) -> str:
    """
    Generates a GIF by calling a standalone subprocess script.
    This architecture isolates Playwright from the main Uvicorn event loop, 
    preventing "NotImplementedError" crashes on Windows.
    """
    
    # Create temp file for HTML input
    # We use delete=False because the subprocess needs to read it. We clean up later.
    fd_html, html_path = tempfile.mkstemp(suffix=".html", text=True)
    with os.fdopen(fd_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Create temp file for output GIF path
    fd_gif, gif_path = tempfile.mkstemp(suffix=".gif")
    os.close(fd_gif) # Subprocess will write to this
    
    try:
        # Construct command
        cmd = [
            sys.executable,
            SCRIPT_PATH,
            "--input", html_path,
            "--output", gif_path,
            "--width", str(width),
            "--height", str(height),
            "--duration", str(duration),
            "--fps", str(fps)
        ]
        
        print(f"Running standalone generator (threaded): {' '.join(cmd)}")
        
        # Run subprocess via thread pool to avoid blocking and bypass asyncio loop restrictions
        # process = await asyncio.create_subprocess_exec(...) -> REPLACED
        
        def run_sync():
            return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
        result = await asyncio.to_thread(run_sync)
        
        if result.returncode != 0:
            print(f"Subprocess Error: {result.stderr}")
            raise RuntimeError(f"GIF Generation Subprocess Failed: {result.stderr}")
            
        print(f"Subprocess finished successfully. Output GIF size: {os.path.getsize(gif_path)} bytes")
        
        return gif_path

    except Exception as e:
        # Cleanup on failure (on success, route handler handles cleanup, but we can clean input html here)
        if os.path.exists(gif_path):
             try: os.remove(gif_path) 
             except: pass
        raise e
    finally:
        # Always clean up the input HTML file
        if os.path.exists(html_path):
            try: os.remove(html_path)
            except: pass
