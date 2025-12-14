# AI Social Media Caption Generator

A powerful, two-step AI application that automatically generates engaging social media captions for your images.

This tool solves the "writer's block" creators face when posting. Instead of staring at a blank screen, you upload an image, and the AI "sees" it and writes creative caption options for you.

## 🚀 How It Works

This application uses a multi-modal AI pipeline:

1.  **Visual Perception (BLIP):** The uploaded image is sent to a custom Hugging Face Space (`SocialAdify`) running the **BLIP** model. This model analyzes the visual content and returns a textual description.
2.  **Creative Writing (Gemini):** This description, along with your selected tone (e.g., "funny", "professional") and preferences, is fed into **Google Gemini 1.5 Flash**.
3.  **Final Output:** Gemini generates 3 distinct caption options, complete with relevant emojis and hashtags.



## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (for a clean, responsive web interface).
* **Image Analysis:** Hugging Face Gradio Client (connecting to BLIP model).
* **Text Generation:** Google Generative AI (Gemini 1.5 Flash).
* **Logging:** Python's native logging for debugging and tracking API calls.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/ai-caption-generator.git](https://github.com/yourusername/ai-caption-generator.git)
    cd ai-caption-generator
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-generativeai gradio_client streamlit
    ```

3.  **Configuration:**
    * The script is currently configured with hardcoded API keys for demonstration. For production, it is recommended to move `GEMINI_API_KEY` to environment variables or a `.env` file.

## 🏃‍♂️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The web interface will open in your browser at http://localhost:8501.

Upload an image (JPG, PNG, WEBP).

Customize the tone (e.g., "Sarcastic", "Inspirational").

Select if you want emojis or hashtags.

Click Generate and choose from the 3 provided options!

## 🧩 Project Structure

app.py: The main Streamlit frontend application.

ai_caption_service.py: The backend logic containing the API calls to Hugging Face and Google Gemini.

temp_streamlit_uploads/: Temporary directory for handling file uploads (automatically managed).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
