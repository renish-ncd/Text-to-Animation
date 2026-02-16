📄 Project Documentation
AI HTML Animation & GIF Preview Generator
1. Project Overview
1.1 Purpose

The objective of this project is to develop a web-based AI-powered tool that allows users to input text descriptions and generate animated HTML content using the Groq kimi-k2 model. The generated content will be previewed visually and optionally converted into GIF format.

1.2 Core Features

Text-to-HTML animation generation using AI

Live preview rendering using iframe

Toggle panel to switch between:

Generated HTML code view

Animation / GIF preview

Secure backend AI processing

Optional GIF export functionality

2. Technology Stack
2.1 Frontend

React.js

CSS / Tailwind CSS (recommended)

Axios or Fetch API

iframe sandbox rendering

2.2 Backend

Python

FastAPI (Recommended) OR Flask

Groq API Integration

GIF generation service (optional)

2.3 AI Model

Groq kimi-k2

3. High-Level Architecture
User Interface (React Frontend)
        ↓
API Request (User Prompt)
        ↓
Python Backend (FastAPI)
        ↓
Groq kimi-k2 Model
        ↓
Generated HTML Animation Code
        ↓
Frontend Rendering
        ├── Code View Panel
        └── iframe Preview Panel
                ↓
        Optional GIF Generation
4. Functional Requirements
4.1 Input Module
Description

Allows users to provide animation or UI description in plain text.

UI Components

Textarea Input Field

Submit Button

Loading Indicator

4.2 Output Module
Toggle Panels
Panel 1: Code Viewer

Displays AI-generated HTML + CSS + JS animation code.

Panel 2: Preview Panel

Renders animation inside iframe.

4.3 AI Processing
Input

User natural language description.

Output

Pure HTML animation code without explanations.

4.4 GIF Generation (Optional Phase 2)
Methods

html2canvas + gif.js (Frontend)

Puppeteer rendering (Backend – Recommended)

5. UI Layout Specification
5.1 Screen Split Layout
Panel	Width	Content
Left Panel	40%	Text Input
Right Panel	60%	Toggle Output
5.2 Right Panel Tabs

Generated Code

Preview / GIF

6. Frontend Design Specification
6.1 Component Structure
src/
 ├── components/
 │     ├── InputPanel.jsx
 │     ├── OutputPanel.jsx
 │     ├── CodeViewer.jsx
 │     ├── PreviewFrame.jsx
 │     └── ToggleTabs.jsx
 ├── services/
 │     └── apiService.js
 └── App.jsx
6.2 Preview Rendering Logic

Inject generated HTML into iframe.

Use sandbox security.

Example:

<iframe sandbox="allow-scripts allow-same-origin"></iframe>
7. Backend Design Specification
7.1 API Endpoints
POST /generate-animation
Request Body
{
  "prompt": "User animation description"
}
Response
{
  "generated_html": "<html>...</html>"
}
7.2 Backend Folder Structure
backend/
 ├── main.py
 ├── routes/
 │     └── generate.py
 ├── services/
 │     └── groq_service.py
 └── models/
8. Groq AI Integration
8.1 Prompt Engineering Template
You are an expert frontend animation developer.


Generate complete HTML animation code based on the user description.


Rules:
- Return only valid HTML, CSS, and JS code.
- Do not provide explanation.
- Ensure animation is visually appealing.
- Ensure the code runs independently.


User Description:
{USER_PROMPT}
8.2 Response Handling

Validate output

Remove markdown wrappers if present

Return clean HTML

9. GIF Generation Architecture
9.1 Frontend Approach

Capture iframe using html2canvas

Convert frames using gif.js

9.2 Backend Approach (Recommended)

Use Puppeteer

Render HTML animation

Capture frames

Export GIF

10. Security Requirements

Never expose Groq API key in frontend

Use backend proxy

Use iframe sandbox restrictions

Sanitize AI-generated HTML

11. Performance Considerations

Use request throttling

Add loading state UI

Cache repeated prompts (optional)

Use streaming AI responses (future)

12. Error Handling

System should handle:

AI response failure

Invalid HTML generation

Network errors

Rendering failure

13. Future Enhancements

Download GIF button

Animation template library

Prompt history

Multi-theme support

Real-time AI streaming

Multi-format export (MP4, PNG sequence)

14. Development Phases
Phase 1 – Core MVP

Text input

Groq integration

HTML code generation

iframe preview

Toggle UI

Phase 2 – GIF Support

GIF generation

Download feature

Phase 3 – Advanced Features

Prompt templates

Animation editor

History storage

15. Environment Variables
GROQ_API_KEY=your_key_here
BACKEND_URL=http://localhost:8000
16. Deployment Suggestions
Frontend

Vercel / Netlify

Backend

AWS / Render / Railway

17. Testing Strategy

Unit Testing → API + Services

UI Testing → Component Rendering

Integration Testing → AI + Rendering Flow

18. Acceptance Criteria

✔ User can input text
✔ AI generates animation HTML
✔ User can view code
✔ User can preview animation
✔ Toggle panels work correctly
✔ Backend securely calls Groq API

19. Estimated Complexity

Frontend: Medium

Backend: Medium

AI Integration: Medium

GIF Generation: Medium-High