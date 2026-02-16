import sys
import os
import time
import tempfile
import argparse
from playwright.sync_api import sync_playwright
from PIL import Image

# Script to hijack time and animation frames for deterministic rendering
TIME_HIJACK_SCRIPT = """
try {
    console.log("Initializing Time Hijacker...");
    window.__virtualTime = 0;
    window.__rafCallbacks = [];
    window.__originalDate = window.Date;
    window.__originalPerf = window.performance;

    // Hijack Date
    class HijackedDate extends window.__originalDate {
        constructor(...args) {
            if (args.length) return new window.__originalDate(...args);
            return new window.__originalDate(window.__virtualTime + 1700000000000);
        }
        static now() {
            return window.__virtualTime + 1700000000000;
        }
    }
    window.Date = HijackedDate;

    // Hijack performance.now
    window.performance.now = () => window.__virtualTime;

    // Hijack requestAnimationFrame
    window.requestAnimationFrame = (callback) => {
        const id = window.__rafCallbacks.length;
        window.__rafCallbacks.push({ id, callback, cancelled: false });
        return id;
    };

    window.cancelAnimationFrame = (id) => {
        const cb = window.__rafCallbacks.find(c => c.id === id);
        if (cb) cb.cancelled = true;
    };

    // Function to advance time
    window.advanceTime = (ms) => {
        window.__virtualTime += ms;
        const callbacks = window.__rafCallbacks.filter(c => !c.cancelled);
        window.__rafCallbacks = [];
        callbacks.forEach(({ callback }) => {
            try { callback(window.performance.now()); } catch(e) { console.error(e); }
        });
    };
    console.log("Time Hijacker Initialized Successfully");
} catch (e) {
    console.error("Time Hijacker Initialization Failed:", e);
}
"""

def generate_gif(input_html_path: str, output_gif_path: str, width: int = 600, height: int = 400, duration: int = 3, fps: int = 30):
    """
    Generates a GIF from an HTML file using Playwright (Synchronous) in a standalone process.
    """
    try:
        with open(input_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        print(f"Starting generation for {input_html_path} -> {output_gif_path}")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height})
            
            # Debug console logs
            page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}", file=sys.stderr))
            
            # Inject time hijacker
            page.add_init_script(TIME_HIJACK_SCRIPT)
            
            # Set content directly or load file via file:// url? set_content is safer for strings
            # But here we have content string
            page.set_content(html_content, wait_until="load")
            
            # Verify injection
            is_injected = page.evaluate("() => typeof window.advanceTime === 'function'")
            if not is_injected:
                print("WARNING: Time hijacker not found after load. Re-injecting...", file=sys.stderr)
                page.evaluate(TIME_HIJACK_SCRIPT)
            
            # Warmup
            time.sleep(0.5)
            
            frames = []
            total_frames = duration * fps
            frame_interval_ms = 1000.0 / fps
            
            with tempfile.TemporaryDirectory() as temp_dir:
                for i in range(total_frames):
                    if i > 0:
                        page.evaluate(f"window.advanceTime({frame_interval_ms})")
                    
                    screenshot_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
                    page.screenshot(path=screenshot_path, type="png")
                    
                    with Image.open(screenshot_path) as img:
                        frames.append(img.copy().convert("RGB"))
                
                browser.close()
                
                if not frames:
                    raise RuntimeError("No frames captured")

                # Save GIF
                frames[0].save(
                    output_gif_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=int(frame_interval_ms),
                    loop=0,
                    optimize=True,
                    disposal=2 # Clear background
                )
                print(f"GIF saved successfully to {output_gif_path}")

    except Exception as e:
        print(f"Error in standalone generator: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate GIF from HTML using Playwright")
    parser.add_argument("--input", required=True, help="Path to input HTML file")
    parser.add_argument("--output", required=True, help="Path to output GIF file")
    parser.add_argument("--width", type=int, default=600)
    parser.add_argument("--height", type=int, default=400)
    parser.add_argument("--duration", type=int, default=3)
    parser.add_argument("--fps", type=int, default=30)
    
    args = parser.parse_args()
    
    generate_gif(args.input, args.output, args.width, args.height, args.duration, args.fps)
