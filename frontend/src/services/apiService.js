const API_BASE_URL = 'http://localhost:8000';

export async function generateAnimation(prompt) {
  const response = await fetch(`${API_BASE_URL}/generate-animation`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error (${response.status})`);
  }

  const data = await response.json();
  return data.generated_html;
}

/**
 * Generate a GIF from HTML content via backend.
 * @param {string} html - The HTML content to render
 * @returns {Promise<Blob>} - The generated GIF blob
 */
export async function generateGif(html) {
  try {
    console.log("Requesting GIF generation...");
    const response = await fetch(`${API_BASE_URL}/generate-gif`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ html }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`GIF Generation failed with status: ${response.status}`, errorText);
      try {
          const errorData = JSON.parse(errorText);
          throw new Error(errorData.detail || `Server error (${response.status})`);
      } catch (e) {
          throw new Error(`Server error (${response.status}): ${errorText}`);
      }
    }

    console.log("GIF generation successful, receiving blob...");
    return await response.blob();
  } catch (error) {
    console.error("Network or parsing error in generateGif:", error);
    throw error;
  }
}
