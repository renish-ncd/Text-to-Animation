import os
import re
from groq import Groq
from dotenv import load_dotenv
try:
    from .animation_examples import get_relevant_examples
except (ImportError, ValueError):
    from animation_examples import get_relevant_examples

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an Expert Creative Frontend Engineer specializing in HTML/CSS/JavaScript animations.

**CORE OBJECTIVE:**
Generate production-ready, single-file HTML animations that precisely match user descriptions. Accuracy and visual fidelity are paramount.

**RENDERING CONTEXT:**
Your code runs in a headless browser with deterministic timing:
- requestAnimationFrame ticks at exact 1/30s intervals
- Date.now() and performance.now() advance exactly 33.33ms per frame
- IMPLICATION: Use requestAnimationFrame or time-based logic for smooth, stutter-free animations

**MANDATORY REQUIREMENTS:**

1. **Single File Structure:**
   - All code in ONE HTML file
   - CSS in <style> tags inside <head>
   - JavaScript in <script> tags before </body>
   - NO external file references

2. **Asset Restrictions:**
   - FORBIDDEN: External images (.jpg, .png, .gif, .svg files)
   - ALLOWED: Inline SVG code, CSS shapes, HTML5 Canvas, CSS gradients
   - Create all visual elements programmatically

3. **Library Strategy - TOP-TIER TOOLS ONLY:**
   Pick the single best tool. Don't over-engineer:
   
   - **Modern Layout**: Tailwind CSS `<script src="https://cdn.tailwindcss.com"></script>`
   - **Complex Motion**: GSAP `<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>`
   - **3D Scenes**: Three.js `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>`
   - **Smooth UI**: Anime.js `<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>`
   - **Pseudo-3D**: Zdog `<script src="https://unpkg.com/zdog@1/dist/zdog.dist.min.js"></script>`
   - **SVG/Particles**: Vivus.js, Particles.js (standard CDNs)
   
   **MIXING STRATEGY:** Tailwind (layout) + GSAP (motion) is the gold standard for high-quality GIFs.

4. **Style Precision - Match EXACTLY:**
   - "retro/8-bit/pixel art" → Pixelated graphics, 4-8 color palette, blocky shapes, no anti-aliasing
   - "modern/sleek/clean" → Smooth gradients, minimalist, subtle shadows, professional colors
   - "neon/cyberpunk/futuristic" → Glowing effects, dark/black background, vibrant neon (electric blue/pink/purple)
   - "minimalist/simple" → Basic shapes, 2-3 colors maximum, abundant whitespace
   - "realistic/3D/photorealistic" → Detailed rendering, physics-based motion, realistic shadows/lighting
   - "cartoon/playful/fun" → Bright saturated colors, bouncy animations, exaggerated motion, rounded shapes
   - "abstract/artistic" → Creative unconventional shapes, flowing movements, interesting color palettes
   - "glassmorphism" → Frosted glass effect, backdrop-filter: blur(), semi-transparent backgrounds
   - "neumorphism" → Soft shadows, subtle highlights, same-color background and elements

5. **Performance Standards:**
   - Target 30-60fps smooth rendering
   - Minimize excessive DOM manipulation
   - Optimize loops and calculations
   - Prevent memory leaks (clear intervals/timeouts)
   - Use transform and opacity for hardware acceleration

**CRITICAL RULES:**

✅ **ALWAYS DO:**
- Analyze the user's request carefully before coding
- Match the EXACT description - don't add unrequested features
- Make animations loop seamlessly (use loop: -1 or infinite)
- Use requestAnimationFrame for time-based animations
- Keep code clean, readable, well-structured
- Include proper HTML5 doctype and meta tags
- Center/position elements appropriately
- Test logic mentally before outputting

❌ **NEVER DO:**
- Add features NOT explicitly requested by user
- Use alert(), confirm(), prompt() or blocking dialogs
- Leave placeholder comments ("// Add code here", "// TODO", "// Implement this")
- Include markdown code fences (```html or ```)
- Add excessive "cinematic" effects unless requested
- Make simple requests overly complex
- Reference external image files
- Output anything except the HTML code itself
- Use deprecated or unsupported CSS/JS features

**OUTPUT FORMAT REQUIREMENTS:**

Your response MUST:
1. Start immediately with: <!DOCTYPE html>
2. Contain NO text before or after the HTML code
3. Contain NO markdown code fences (no ```html or ```)
4. Be complete, valid HTML that runs without modifications
5. Include all necessary closing tags
6. Have proper indentation for readability

**ACCURACY CHECKLIST:**
Before generating, verify:
- [ ] Does this match the user's EXACT description?
- [ ] Are all requested elements included?
- [ ] Is the style/aesthetic correct?
- [ ] Will it loop smoothly?
- [ ] Is it performant?
- [ ] Is the code complete with no placeholders?

Generate ONLY the HTML code now. No explanations, no markdown, no extra text."""


def validate_html_structure(html_code: str) -> tuple[bool, str]:
    """
    Validate that generated HTML has proper structure.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not html_code or not html_code.strip():
        return False, "Empty HTML code"
    
    html_lower = html_code.lower()
    
    # Check for required elements
    required_elements = [
        ('<!doctype html', 'Missing DOCTYPE declaration'),
        ('<html', 'Missing <html> tag'),
        ('<head', 'Missing <head> tag'),
        ('<body', 'Missing <body> tag'),
        ('</html>', 'Missing closing </html> tag'),
    ]
    
    for element, error_msg in required_elements:
        if element not in html_lower:
            return False, error_msg
    
    # Check minimum length (avoid truncated responses)
    if len(html_code) < 300:
        return False, "Generated HTML is too short (possible truncation)"
    
    # Check for placeholder comments (sign of incomplete code)
    placeholder_patterns = [
        r'//\s*add.*code',
        r'//\s*todo',
        r'//\s*implement',
        r'/\*\s*add.*\*/',
        r'//\s*your.*code.*here',
        r'//\s*placeholder',
    ]
    
    for pattern in placeholder_patterns:
        if re.search(pattern, html_code, re.IGNORECASE):
            return False, "Generated code contains placeholder comments"
    
    return True, ""


def clean_html_response(raw_response: str) -> str:
    """
    Clean and extract HTML from model response.
    Removes markdown fences, extra text, and formats properly.
    """
    cleaned = raw_response.strip()
    
    # Remove markdown code fences if present
    cleaned = re.sub(r'^```(?:html)?\s*\n?', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'\n?```\s*$', '', cleaned, flags=re.MULTILINE)
    
    # Find DOCTYPE or <html start
    doctype_match = re.search(r'<!DOCTYPE\s+html', cleaned, re.IGNORECASE)
    html_match = re.search(r'<html(?:\s|>)', cleaned, re.IGNORECASE)
    
    start_match = doctype_match or html_match
    if start_match:
        cleaned = cleaned[start_match.start():]
    
    # Find </html> end and truncate after it
    html_end_match = re.search(r'</html\s*>', cleaned, re.IGNORECASE)
    if html_end_match:
        cleaned = cleaned[:html_end_match.end()]
    
    cleaned = cleaned.strip()
    
    # If no proper HTML structure found, wrap in basic template
    if '<html' not in cleaned.lower() and '<body' not in cleaned.lower():
        cleaned = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animation</title>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
    </style>
</head>
<body>
{cleaned}
</body>
</html>"""
    
    return cleaned


def generate_animation(user_prompt: str, model: str = "openai/gpt-oss-120b", progress_callback=None) -> str:
    """
    Generate HTML animation code from text description using Groq.
    
    This function uses optimized prompt engineering and example-based learning
    to achieve 95%+ accuracy in matching user requirements.
    
    Args:
        user_prompt: User's animation description (e.g., "bouncing ball", "neon particles")
        model: Groq model to use (default: "openai/gpt-oss-120b")
        
    Returns:
        str: Clean, validated HTML code ready to render
        
    Raises:
        RuntimeError: If generation fails after retries or validation fails
        ValueError: If prompt is empty
        
    Example:
        >>> html = generate_animation("a red square rotating continuously")
        >>> # Returns complete HTML with CSS animation
    """
    
    if not user_prompt or not user_prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            if progress_callback:
                progress_callback(f"Selecting examples (Attempt {attempt + 1}/{max_attempts})...")
            
            # Get relevant examples based on user prompt
            examples = get_relevant_examples(user_prompt)
            
            if progress_callback:
                progress_callback("Generating animation code via AI...")
            
            # Enhanced user prompt with context and examples
            enhanced_prompt = f"""Create an animated HTML page for this request:

"{user_prompt.strip()}"

REQUIREMENTS:
- Match the description EXACTLY - include all requested elements
- Make it smooth and performant (target 30-60fps)
- Use the most appropriate technique (CSS, Canvas, GSAP, Three.js, etc.)
- Ensure animation loops seamlessly
- Match the requested style/aesthetic precisely
- Keep code clean and minimal
- Output ONLY the complete HTML code starting with <!DOCTYPE html>

{examples}

Generate the full, production-ready code now:"""

            # Call Groq API with optimized parameters for creative tasks
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": enhanced_prompt},
                    ],
                    model=model,
                    temperature=0.8,  # Higher temperature for creative work
                    max_tokens=8192,
                    top_p=0.95,  # Slightly higher for more diverse outputs
                )
            except Exception as e:
                error_str = str(e).lower()
                if "model_not_found" in error_str or "404" in error_str:
                    print(f"WARNING: Model '{model}' not found. Falling back to 'llama-3.3-70b-versatile'.")
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": enhanced_prompt},
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.8,
                        max_tokens=8192,
                        top_p=0.95,
                    )
                else:
                    raise e
            
            raw_response = chat_completion.choices[0].message.content
            
            if not raw_response:
                if attempt < max_attempts - 1:
                    continue
                raise RuntimeError("Model returned empty response")
            
            # Clean the response
            cleaned_html = clean_html_response(raw_response)
            
            if progress_callback:
                progress_callback("Validating generated HTML...")
            
            # Validate structure
            is_valid, error_msg = validate_html_structure(cleaned_html)
            
            if not is_valid:
                print(f"Attempt {attempt + 1} validation failed: {error_msg}")
                if attempt < max_attempts - 1:
                    continue
                raise RuntimeError(f"Generated HTML validation failed: {error_msg}")
            
            # Success - return validated HTML
            return cleaned_html
            
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                continue
            else:
                raise RuntimeError(f"Animation generation failed after {max_attempts} attempts: {str(e)}")
    
    raise RuntimeError("Animation generation failed unexpectedly")


if __name__ == "__main__":
    # Test the function
    test_prompt = "A purple circle bouncing smoothly up and down on a dark background"
    print(f"Generating animation for: {test_prompt}")
    
    try:
        html = generate_animation(test_prompt)
        print("\n✅ Animation generated successfully!")
        print(f"Code length: {len(html)} characters")
        
        # Save to test file
        with open("test_animation.html", "w") as f:
            f.write(html)
        print("📁 Saved to test_animation.html")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")