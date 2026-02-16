from functools import lru_cache
from difflib import get_close_matches

EXAMPLES = {
    "bouncing": """
**Example: Bouncing Ball Animation**

User Request: "A red circle bouncing up and down"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bouncing Ball</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: #1a1a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let y = 100;
        let velocity = 0;
        const gravity = 0.5;
        const bounce = 0.8;
        const radius = 40;

        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw ball
            ctx.beginPath();
            ctx.arc(canvas.width / 2, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = '#ff3b3b';
            ctx.fill();

            // Physics
            velocity += gravity;
            y += velocity;

            // Bounce
            if (y + radius > canvas.height) {
                y = canvas.height - radius;
                velocity *= -bounce;
            }
        }
        animate();
    </script>
</body>
</html>
""",

    "rotating": """
**Example: Rotating Square**

User Request: "A blue square rotating continuously"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rotating Square</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0f0f23;
        }
        .square {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            animation: rotate 3s linear infinite;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="square"></div>
</body>
</html>
""",

    "particles": """
**Example: Particle System**

User Request: "Floating particles moving randomly"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particles</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: #000;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = (Math.random() - 0.5) * 2;
                this.radius = Math.random() * 3 + 1;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(100, 200, 255, 0.8)`;
                ctx.fill();
            }
        }

        const particles = Array.from({ length: 50 }, () => new Particle());

        function animate() {
            requestAnimationFrame(animate);
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            particles.forEach(p => {
                p.update();
                p.draw();
            });
        }
        animate();
    </script>
</body>
</html>
""",

    "typing": """
**Example: Typing Text Effect**

User Request: "Text that types out letter by letter"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typing Effect</title>
    <script src="https://unpkg.com/typed.js@2.0.16/dist/typed.umd.js"></script>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Courier New', monospace;
        }
        .typing-container {
            font-size: 2rem;
            color: white;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="typing-container">
        <span id="typed"></span>
    </div>
    <script>
        new Typed('#typed', {
            strings: ['Hello World!', 'Welcome to Animations', 'This is Amazing!'],
            typeSpeed: 80,
            backSpeed: 50,
            loop: true
        });
    </script>
</body>
</html>
""",

    "wave": """
**Example: Wave Animation**

User Request: "Smooth wave motion"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wave</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: #0a0a1e;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        let time = 0;

        function drawWave(offset, amplitude, frequency, color) {
            ctx.beginPath();
            ctx.moveTo(0, canvas.height / 2);

            for (let x = 0; x < canvas.width; x++) {
                const y = canvas.height / 2 + 
                         Math.sin((x * frequency) + time + offset) * amplitude;
                ctx.lineTo(x, y);
            }

            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.stroke();
        }

        function animate() {
            requestAnimationFrame(animate);
            ctx.fillStyle = 'rgba(10, 10, 30, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            drawWave(0, 50, 0.01, '#00f5ff');
            drawWave(1, 40, 0.012, '#ff00ff');
            drawWave(2, 60, 0.008, '#00ff00');

            time += 0.05;
        }
        animate();
    </script>
</body>
</html>
""",

    "neon": """
**Example: Neon Glow Effect**

User Request: "Neon glowing text with cyberpunk style"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Glow</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000;
            font-family: 'Arial', sans-serif;
        }
        .neon-text {
            font-size: 4rem;
            font-weight: bold;
            color: #fff;
            text-shadow: 
                0 0 10px #00f5ff,
                0 0 20px #00f5ff,
                0 0 30px #00f5ff,
                0 0 40px #00f5ff,
                0 0 70px #00f5ff,
                0 0 80px #00f5ff,
                0 0 100px #00f5ff;
            animation: flicker 2s infinite;
        }
        @keyframes flicker {
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
                opacity: 1;
            }
            20%, 24%, 55% {
                opacity: 0.4;
            }
        }
    </style>
</head>
<body>
    <div class="neon-text">NEON</div>
</body>
</html>
""",

    "3d_cube": """
**Example: 3D Rotating Cube**

User Request: "A 3D cube rotating in space"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Cube</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            perspective: 1000px;
        }
        .cube {
            width: 200px;
            height: 200px;
            position: relative;
            transform-style: preserve-3d;
            animation: rotate 10s infinite linear;
        }
        .face {
            position: absolute;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            color: white;
        }
        .front  { transform: translateZ(100px); }
        .back   { transform: rotateY(180deg) translateZ(100px); }
        .right  { transform: rotateY(90deg) translateZ(100px); }
        .left   { transform: rotateY(-90deg) translateZ(100px); }
        .top    { transform: rotateX(90deg) translateZ(100px); }
        .bottom { transform: rotateX(-90deg) translateZ(100px); }
        @keyframes rotate {
            from { transform: rotateX(0) rotateY(0); }
            to { transform: rotateX(360deg) rotateY(360deg); }
        }
    </style>
</head>
<body>
    <div class="cube">
        <div class="face front">F</div>
        <div class="face back">B</div>
        <div class="face right">R</div>
        <div class="face left">L</div>
        <div class="face top">T</div>
        <div class="face bottom">B</div>
    </div>
</body>
</html>
""",

    "loading": """
**Example: Loading Spinner**

User Request: "A smooth loading spinner"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Spinner</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #1a1a2e;
        }
        .spinner {
            width: 80px;
            height: 80px;
            border: 8px solid rgba(255, 255, 255, 0.1);
            border-top-color: #00f5ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="spinner"></div>
</body>
</html>
""",

    "gradient": """
**Example: Animated Gradient Background**

User Request: "Smooth animated gradient background"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated Gradient</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
</head>
<body>
</body>
</html>
""",

    "pulse": """
**Example: Pulsing Circle**

User Request: "A circle that pulses/breathes"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pulse</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0f0f23;
        }
        .pulse {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, #ff006e, #8338ec);
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 0 30px rgba(255, 0, 110, 0.5);
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
        }
    </style>
</head>
<body>
    <div class="pulse"></div>
</body>
</html>
""",

    "gsap_timeline": """
**Example: GSAP Timeline Animation**

User Request: "Multiple elements animating in sequence"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GSAP Timeline</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #1a1a2e;
            gap: 30px;
        }
        .box {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="box"></div>
    <div class="box"></div>
    <div class="box"></div>
    <script>
        gsap.timeline({ repeat: -1 })
            .from('.box', {
                y: -100,
                opacity: 0,
                duration: 0.5,
                stagger: 0.2,
                ease: 'bounce.out'
            })
            .to('.box', {
                rotation: 360,
                duration: 1,
                stagger: 0.2,
                ease: 'power2.inOut'
            }, '+=0.5')
            .to('.box', {
                scale: 1.5,
                duration: 0.3,
                stagger: 0.1,
                yoyo: true,
                repeat: 1
            });
    </script>
</body>
</html>
""",

    "text_reveal": """
**Example: Text Reveal Animation**

User Request: "Text that reveals letter by letter with fade in"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Reveal</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            font-family: Arial, sans-serif;
        }
        .text {
            font-size: 3rem;
            color: white;
            font-weight: bold;
        }
        .letter {
            display: inline-block;
            opacity: 0;
        }
    </style>
</head>
<body>
    <div class="text" id="text">HELLO WORLD</div>
    <script>
        const text = document.getElementById('text');
        const letters = text.textContent.split('');
        text.textContent = '';
        
        letters.forEach(letter => {
            const span = document.createElement('span');
            span.textContent = letter === ' ' ? '\u00A0' : letter;
            span.className = 'letter';
            text.appendChild(span);
        });

        gsap.timeline({ repeat: -1, repeatDelay: 1 })
            .to('.letter', {
                opacity: 1,
                y: 0,
                duration: 0.5,
                stagger: 0.05,
                ease: 'power2.out'
            })
            .to('.letter', {
                opacity: 0,
                y: -20,
                duration: 0.3,
                stagger: 0.03,
                delay: 2
            });
    </script>
</body>
</html>
""",

    "morphing": """
**Example: Shape Morphing**

User Request: "A shape that morphs between circle and square"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morphing Shape</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0a0a1e;
        }
        .shape {
            width: 150px;
            height: 150px;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            animation: morph 3s ease-in-out infinite;
            box-shadow: 0 10px 40px rgba(245, 87, 108, 0.4);
        }
        @keyframes morph {
            0%, 100% { border-radius: 50%; transform: rotate(0deg); }
            50% { border-radius: 0%; transform: rotate(180deg); }
        }
    </style>
</head>
<body>
    <div class="shape"></div>
</body>
</html>
""",

    "floating": """
**Example: Floating Elements**

User Request: "Multiple shapes floating up and down smoothly"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floating Shapes</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        .shape {
            width: 60px;
            height: 60px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .shape:nth-child(1) {
            animation: float 3s ease-in-out infinite;
        }
        .shape:nth-child(2) {
            animation: float 3s ease-in-out 0.5s infinite;
            border-radius: 50%;
        }
        .shape:nth-child(3) {
            animation: float 3s ease-in-out 1s infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-30px); }
        }
    </style>
</head>
<body>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</body>
</html>
""",

    "confetti": """
**Example: Confetti Animation**

User Request: "Colorful confetti falling from top"

Complete Code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confetti</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: #1a1a2e;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7d794', '#ff9ff3'];

        class Confetti {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height - canvas.height;
                this.size = Math.random() * 8 + 4;
                this.speedY = Math.random() * 3 + 2;
                this.speedX = Math.random() * 2 - 1;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                this.rotation = Math.random() * 360;
                this.rotationSpeed = Math.random() * 10 - 5;
            }

            update() {
                this.y += this.speedY;
                this.x += this.speedX;
                this.rotation += this.rotationSpeed;

                if (this.y > canvas.height) {
                    this.y = -10;
                    this.x = Math.random() * canvas.width;
                }
            }

            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate(this.rotation * Math.PI / 180);
                ctx.fillStyle = this.color;
                ctx.fillRect(-this.size / 2, -this.size / 2, this.size, this.size);
                ctx.restore();
            }
        }

        const confetti = Array.from({ length: 100 }, () => new Confetti());

        function animate() {
            requestAnimationFrame(animate);
            ctx.fillStyle = 'rgba(26, 26, 46, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            confetti.forEach(c => {
                c.update();
                c.draw();
            });
        }
        animate();
    </script>
</body>
</html>
"""
}


@lru_cache(maxsize=100)
def get_relevant_examples(user_prompt: str, max_examples: int = 2) -> str:
    """
    Select the most relevant examples based on user prompt keywords with fuzzy matching.
    """
    prompt_lower = user_prompt.lower()
    prompt_words = prompt_lower.split()
    
    # Keyword matching for example selection
    keywords_map = {
        "bouncing": ["bounce", "bouncing", "ball", "jump"],
        "rotating": ["rotate", "rotating", "spin", "spinning", "turn"],
        "particles": ["particle", "particles", "dots", "floating random"],
        "typing": ["type", "typing", "typewriter", "letter by letter"],
        "wave": ["wave", "waves", "wavy", "sine", "ocean"],
        "neon": ["neon", "glow", "glowing", "cyberpunk", "futuristic"],
        "3d_cube": ["3d", "cube", "box", "three dimensional"],
        "loading": ["loading", "spinner", "loader", "loading animation"],
        "gradient": ["gradient", "background", "animated background"],
        "pulse": ["pulse", "pulsing", "breathing", "breath", "heartbeat"],
        "gsap_timeline": ["sequence", "timeline", "multiple elements", "one after another"],
        "text_reveal": ["reveal", "text reveal", "fade in text", "appearing text"],
        "morphing": ["morph", "morphing", "shape change", "transform shape"],
        "floating": ["floating", "float", "levitate"],
        "confetti": ["confetti", "falling", "celebration"]
    }
    
    # Flatten keywords for fuzzy matching
    all_keywords = []
    for k_list in keywords_map.values():
        all_keywords.extend(k_list)
    
    # Find matching examples
    matches = []
    for example_key, example_keywords in keywords_map.items():
        # Direct matching first
        if any(kw in prompt_lower for kw in example_keywords):
            matches.append(example_key)
            continue
            
        # Fuzzy matching for each word in prompt
        for word in prompt_words:
            if len(word) < 3: continue
            fuzzy_matches = get_close_matches(word, example_keywords, n=1, cutoff=0.8)
            if fuzzy_matches:
                matches.append(example_key)
                break
    
    # If no matches, return most versatile examples
    if not matches:
        matches = ["bouncing", "rotating"]
    
    # Limit to max_examples while preserving unique keys
    unique_matches = []
    for m in matches:
        if m not in unique_matches:
            unique_matches.append(m)
    
    unique_matches = unique_matches[:max_examples]
    
    # Format examples
    examples_text = "\n\nRELEVANT EXAMPLES FOR REFERENCE:\n"
    examples_text += "=" * 50 + "\n"
    
    for match in unique_matches:
        if match in EXAMPLES:
            examples_text += EXAMPLES[match] + "\n"
            examples_text += "=" * 50 + "\n"
    
    return examples_text


if __name__ == "__main__":
    # Test example selection
    test_prompts = [
        "A red ball bouncing up and down",
        "Neon text with cyberpunk glow",
        "Particles floating randomly",
        "A spinning cube in 3D"
    ]
    
    print("Testing Example Selection:\n")
    for prompt in test_prompts:
        print(f"Prompt: {prompt}")
        examples = get_relevant_examples(prompt, max_examples=1)
        print(f"Selected examples: {len(examples)} characters\n")
