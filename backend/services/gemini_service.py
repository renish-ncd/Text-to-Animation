import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 1.5 Pro for best instruction following and complex reasoning
# Setup the model with system instructions
SYSTEM_PROMPT = """You are an Expert Creative Coder and Frontend Engineer specialized in creating award-winning, high-performance HTML/CSS/JS animations.

YOUR GOAL:
Generate a single-file, production-ready HTML document that renders a breathtaking animation based on the user's description.

TECHNICAL CONSTRAINTS:
1.  **Single File:** Output MUST be a single HTML file with embedded CSS (<style>) and JS (<script>).
2.  **No External Assets:** Do NOT use external images (jpg/png). Draw everything using CSS shapes, SVG, or HTML5 Canvas.
3.  **Libraries:** You MUST use Tailwind CSS via CDN for layout.
    - <script src="https://cdn.tailwindcss.com"></script>
    - Allowed Animation Libraries (CDN only): GSAP, Anime.js, Three.js (if 3D needed).
4.  **Performance:**
    - Use `requestAnimationFrame` for JS animations.
    - Use CSS `transform` and `opacity` for smooth 60fps rendering.
    - Avoid heavy DOM manipulation for >100 particles (use Canvas instead).

VISUAL STYLE & QUALITY:
-   **Modern & Premium:** The result must look like a high-end portfolio site (Awwwards style).
-   **Lighting & Depth:** Use gradients, shadows, and blurs to create depth. Avoid flat, boring colors unless requested.
-   **Responsive:** The animation must look good on both Desktop and Mobile. Center the main content.
-   **Background:** Always provide a thematic, rich background (e.g., dark gradients, stars, subtle patterns), never plain white unless asked.

CRITICAL RULES:
-   Do NOT include markdown code fences (```html). Return ONLY the raw HTML code.
-   Do NOT use `alert()` or blocking code.
-   Do NOT output placeholders like "Add logic here". Write the FULL working code.

OUTPUT FORMAT:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Animation</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom CSS */
    </style>
</head>
<body class="bg-gray-900 m-0 overflow-hidden flex items-center justify-center h-screen w-screen">
    <!-- Content -->
    <script>
        // Animation Logic
    </script>
</body>
</html>
"""

model = genai.GenerativeModel(
    model_name="gemini-3-pro-preview", # Upgraded to Pro for better reasoning
    system_instruction=SYSTEM_PROMPT
)

def generate_animation(user_prompt: str) -> str:
    """Generate HTML animation code from a text description using Google Gemini."""
    try:
        # Prompt Engineering: Enhance user input
        enhanced_prompt = (
            f"Create a high-quality, cinematic animation for: '{user_prompt}'. "
            "Make it visually stunning, smooth, and detailed. "
            "Use modern color palettes and fluid motions. "
            "Strictly follow the system constraints."
        )
        
        full_prompt = f"{enhanced_prompt}\n\nOutput ONLY the complete HTML code starting with <!DOCTYPE html>."
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=8192,
                temperature=0.4,
            )
        )

        if not response.text:
            raise ValueError("Empty response from Gemini")

        raw_response = response.text

        # Clean response: strip markdown code fences if present
        cleaned = raw_response.strip()
        # Remove any text before <!DOCTYPE or <html
        doctype_match = re.search(r'<!DOCTYPE\s+html', cleaned, re.IGNORECASE)
        html_match = re.search(r'<html', cleaned, re.IGNORECASE)
        start_match = doctype_match or html_match
        if start_match:
            cleaned = cleaned[start_match.start():]

        # Remove any text after </html>
        html_end = re.search(r'</html\s*>', cleaned, re.IGNORECASE)
        if html_end:
            cleaned = cleaned[:html_end.end()]

        # Fallback: strip markdown fences
        cleaned = re.sub(r"^```(?:html)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)
        cleaned = cleaned.strip()

        # Validate that it contains HTML
        if "<html" not in cleaned.lower() and "<body" not in cleaned.lower():
            # If valid HTML structure is missing, wrap it
             cleaned = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animation</title>
</head>
<body>
{cleaned}
</body>
</html>"""

        return cleaned

    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")
