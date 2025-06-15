# D:\path_to_your_new_project\ai_caption_service.py
import os
from pathlib import Path
import shutil
import logging
from typing import Optional, Dict, Any, List

# Required libraries:
# pip install google-generativeai
# pip install gradio_client
from gradio_client import Client as GradioClient, handle_file as gradio_handle_file
import google.generativeai as genai

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
# Hardcoded values as requested by the user.
HF_SPACE_ID = "uzair-hassan003/SocialAdify"
GEMINI_API_KEY = "AIzaSyAA8rGNOHsQlO98Huc0nYkDxtNswBpAmSs"

# --- Core Functions ---

def get_image_description_from_blip(image_path: str) -> Optional[str]:
    """
    Connects to a Hugging Face Space using Gradio client to get an image description.
    This is a synchronous, blocking function.

    Args:
        image_path: The absolute or relative path to the image file.

    Returns:
        A string containing the image description, or None if an error occurs.
    """
    logger.info(f"Connecting to Hugging Face Space: {HF_SPACE_ID} for image description.")
    
    if not Path(image_path).exists():
        logger.error(f"Image file not found at the specified path: {image_path}")
        return None

    try:
        client = GradioClient(HF_SPACE_ID)
        logger.info(f"Sending image '{image_path}' to HF Space API...")
        
        blip_result = client.predict(
            image=gradio_handle_file(image_path),
            api_name="/predict"
        )
        
        if isinstance(blip_result, str):
            description = blip_result.strip()
            if description:
                logger.info(f"BLIP Image Description received: \"{description}\"")
                return description
            else:
                logger.warning("BLIP service returned an empty description.")
                return None
        else:
            logger.warning(f"Received unexpected result type from BLIP: {type(blip_result)}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while getting BLIP description: {e}", exc_info=True)
        return None

def construct_caption_prompt(
    image_description: str,
    preferences: Dict[str, Any]
) -> str:
    """
    Constructs a detailed prompt for the Gemini API based on image description and user preferences.
    UPDATED to request 3 caption options.
    """
    tone = preferences.get('tone', 'engaging')

    prompt = f"You are an expert social media caption writer.\n"
    prompt += f"Your task is to generate 3 distinct and creative caption options for a social media post with a '{tone}' tone.\n\n"
    prompt += f"The post includes an image with the following description:\n\"{image_description}\"\n\n"

    if preferences.get('include_hashtags'):
        prompt += "Please include 3-5 relevant and effective hashtags at the end of each caption option.\n"
    else:
        prompt += "Do not include any hashtags.\n"

    if preferences.get('include_emojis'):
        prompt += "Please integrate relevant emojis naturally within each caption option to enhance its appeal.\n"
    else:
        prompt += "Do not include any emojis.\n"

    prompt += "\nOutput the 3 captions separated by a newline. Do not include any preamble like \"Here are the captions:\" or numbering like '1.', '2.', '3.'."
    return prompt

def generate_captions_with_gemini(prompt_text: str) -> Optional[List[str]]:
    """
    Sends a prompt to the Gemini API and returns the generated captions as a list of strings.
    UPDATED to handle a multi-caption response.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not configured in the script. Cannot generate caption.")
        return None
        
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        generation_config = genai.types.GenerationConfig(
            temperature=0.8, # Slightly increased temperature for more variety
            max_output_tokens=500 # Increased token limit for multiple captions
        )
        
        logger.info("Sending prompt to Gemini for caption generation...")
        response = model.generate_content(
            prompt_text,
            generation_config=generation_config
        )
        
        generated_text = ""
        if response.parts:
            generated_text = response.parts[0].text.strip()
        elif hasattr(response, 'text'):
            generated_text = response.text.strip()
        
        if not generated_text and response.prompt_feedback and response.prompt_feedback.block_reason:
            logger.warning(f"Gemini content generation blocked. Reason: {response.prompt_feedback.block_reason}")
            return [f"Caption generation blocked: {response.prompt_feedback.block_reason_message}"]
        
        if not generated_text:
            logger.warning("AI returned an empty response.")
            return ["AI returned an empty response."]

        # Split the response by newlines and filter out any empty lines
        captions = [line.strip() for line in generated_text.split('\n') if line.strip()]
        logger.info(f"Successfully parsed {len(captions)} caption(s).")
        return captions

    except Exception as e:
        logger.error(f"An error occurred while communicating with Gemini API: {e}", exc_info=True)
        return None

# --- Main Service Function (UPDATED) ---

def get_ai_caption_for_image(
    image_path: str,
    preferences: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Main function to orchestrate the two-step caption generation process.

    Args:
        image_path: The path to the image file.
        preferences: A dictionary of user preferences for the caption.

    Returns:
        A dictionary containing 'description' and a list of 'captions', or None if a critical step fails.
    """
    # Step 1: Get image description from BLIP
    image_description = get_image_description_from_blip(image_path)
    if not image_description:
        logger.error("Halting process because image description could not be obtained.")
        return None

    # Step 2: Construct the prompt for Gemini
    prompt = construct_caption_prompt(image_description, preferences)
    logger.info(f"Constructed Prompt:\n---\n{prompt}\n---")

    # Step 3: Generate the final captions with Gemini
    final_captions = generate_captions_with_gemini(prompt)
    
    if not final_captions:
        return {"description": image_description, "captions": []}

    # Return both the description and the list of captions
    return {
        "description": image_description,
        "captions": final_captions
    }
