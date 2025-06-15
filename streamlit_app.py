# D:\path_to_your_new_project\streamlit_app.py
import streamlit as st
from pathlib import Path
from ai_caption_service import get_ai_caption_for_image # Import the main service function

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="✨",
    layout="centered"
)

# --- UI Layout and Components ---

st.title("✨ AI Caption Generator")
st.markdown("This app uses a two-step AI process to generate social media captions. First, it analyzes an image to get a description, then it uses that description along with your preferences to create caption options with a powerful language model.")

st.header("1. Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload an image to generate a caption for. Max size: 10MB"
)

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Your Uploaded Image", use_column_width=True)

st.header("2. Set Your Caption Preferences")

# The "Post Category" input has been removed.
tone = st.text_input("Desired Tone", "sophisticated and exclusive", help="What feeling should the caption evoke? (e.g., funny, inspiring, professional, casual)")

# Create two columns for the checkboxes for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    include_hashtags = st.checkbox("Include Hashtags?", value=True)

with col2:
    include_emojis = st.checkbox("Include Emojis?", value=True)


st.header("3. Generate Your Caption Options")

# The "Generate Caption" button
if st.button("Generate AI Captions", type="primary", use_container_width=True):
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location because our service function requires a file path
        temp_dir = Path("temp_streamlit_uploads")
        temp_dir.mkdir(exist_ok=True)
        temp_file_path = temp_dir / uploaded_file.name

        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Prepare the preferences dictionary (category removed)
        preferences = {
            "tone": tone,
            "include_hashtags": include_hashtags,
            "include_emojis": include_emojis
        }

        # Show a spinner while processing
        with st.spinner("AI is analyzing your image and crafting caption options... Please wait."):
            # Call the main service function
            result = get_ai_caption_for_image(
                image_path=str(temp_file_path),
                preferences=preferences
            )

            # Clean up the temporary file
            temp_file_path.unlink()

            # Display the result
            if result:
                image_description = result.get("description")
                final_captions = result.get("captions") # This is now a list

                st.success("Captions generated successfully!")
                
                # Display the image description used by the AI
                if image_description:
                    with st.expander("View Image Description Used by AI"):
                        st.info(f"{image_description}")
                
                # Display the final captions
                if final_captions and isinstance(final_captions, list):
                    st.subheader("Your Generated Caption Options:")
                    for i, caption in enumerate(final_captions):
                        st.markdown(f"**Option {i+1}:**")
                        st.markdown(f"> {caption}")
                        st.markdown("---")
                else:
                    st.error("AI could not generate valid caption options. Please try again.")

            else:
                st.error("Failed to generate captions. Please check the console logs for more details or try a different image.")

    else:
        st.warning("Please upload an image first to generate captions.")

