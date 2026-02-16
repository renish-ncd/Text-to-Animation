import sys
import os

# Add backend root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gif_service import generate_gif_from_html

html_content = """
<!DOCTYPE html>
<html>
<body style="margin:0; overflow:hidden;">
<div id="box" style="width:50px;height:50px;background:red;position:absolute;top:0;left:0;"></div>
<script>
let x = 0;
function animate() {
    requestAnimationFrame(animate);
    x += 5;
    document.getElementById('box').style.left = x + 'px';
}
animate();
</script>
</body>
</html>
"""

import asyncio

async def test():
    try:
        print("Testing GIF generation...")
        gif_path = await generate_gif_from_html(html_content, duration=1, fps=30)
        print(f"Success! GIF created at: {gif_path}")
        
        if os.path.exists(gif_path) and os.path.getsize(gif_path) > 0:
            print("File size is valid.")
        else:
            print("Error: File is empty or missing.")
            
    except Exception as e:
        print(f"Test Failed: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(test())
