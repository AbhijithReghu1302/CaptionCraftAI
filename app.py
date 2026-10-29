
import io
import re

import ollama
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="CaptionCraft AI",
    page_icon="✨",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10101b, #201532);
    color: #f8f5ff;
}
h1 { color: #d8b4fe; }
h2, h3 { color: #c4b5fd; }
.stButton > button {
    border-radius: 10px;
    border: 1px solid #a855f7;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("✨ CaptionCraft AI")
st.subheader("Your photo. Your vibe. Your caption.")
st.write(
    "Turn your photos into captions that express your mood. "
    "Powered by local AI using Gemma 3."
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙️ Caption Settings")

    mood = st.selectbox(
        "Choose your vibe",
        ["Aesthetic", "Funny", "Savage", "Poetic",
         "Romantic", "Motivational", "Casual"]
    )

    style = st.radio(
        "Caption style",
        ["Simple", "Creative", "Both"]
    )

    length = st.selectbox(
        "Caption length",
        ["Short", "Medium", "Long"]
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Hinglish"]
    )

    keywords = st.text_input(
        "Optional keywords",
        placeholder="e.g. memories, sunset, freedom"
    )

# ---------- UPLOAD ----------
left, right = st.columns([1, 1.2])

with left:
    st.markdown("### 📸 Upload your photo")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            image = ImageOps.exif_transpose(image).convert("RGB")

            st.image(
                image,
                caption="Your uploaded photo",
                use_container_width=True
            )
        except Exception:
            st.error("Please upload a valid image.")
            st.stop()
    else:
        image = None
        st.info("Upload a photo to get started.")

# ---------- GENERATION ----------
with right:
    st.markdown("### ✨ Generate your captions")
    st.write(
        "Choose your preferred vibe in the sidebar "
        "and let AI do the creative work."
    )

    generate = st.button(
        "✨ Generate Captions",
        type="primary",
        use_container_width=True
    )

    if generate:
        if image is None:
            st.warning("Please upload an image first.")
        else:
            prompt = f"""
You are CaptionCraft AI, a creative social media assistant.

Analyze the attached image and generate exactly 3 distinct captions.

Mood: {mood}
Style: {style}
Length: {length}
Language: {language}
Optional keywords: {keywords if keywords.strip() else "None"}

Rules:
- Make captions relevant to the visible image.
- Never invent personal details or unseen events.
- Simple captions should sound natural and effortless.
- Creative captions can be expressive, poetic, or witty.
- If style is Both, include simple and creative alternatives.
- Follow the requested language and length.
- Avoid repetitive wording and excessive emojis.
- Add 5 relevant hashtags after the captions.

Use this exact format:

CAPTION 1:
Your first caption

CAPTION 2:
Your second caption

CAPTION 3:
Your third caption

HASHTAGS:
#example #example #example #example #example
"""

            try:
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG")

                with st.spinner(
                    "AI is understanding your photo and creating captions..."
                ):
                    response = ollama.chat(
                        model="gemma3:4b",
                        messages=[{
                            "role": "user",
                            "content": prompt,
                            "images": [buffer.getvalue()]
                        }],
                        options={"temperature": 0.8}
                    )

                result = response["message"]["content"]
                st.session_state["captions"] = result

            except Exception as error:
                st.error(
                    "Could not generate captions. Check that Ollama "
                    "is running and gemma3:4b is installed."
                )
                st.caption(str(error))

# ---------- RESULTS ----------
if st.session_state.get("captions"):
    st.divider()
    st.markdown("## 💜 Your Caption Collection")

    result = st.session_state["captions"]

    # Split the output into individual caption sections.
    sections = re.split(
        r"CAPTION\s+\d+\s*:",
        result,
        flags=re.IGNORECASE
    )

    captions = [
        part.strip()
        for part in sections[1:]
        if part.strip()
    ]

    if captions:
        for index, caption in enumerate(captions[:3], start=1):
            caption_text = re.split(
                r"HASHTAGS\s*:",
                caption,
                flags=re.IGNORECASE
            )[0].strip()

            st.markdown(f"### Caption {index}")
            st.markdown(f"> {caption_text}")

            st.button(
                f"📋 Copy Caption {index}",
                key=f"copy_{index}",
                on_click=lambda text=caption_text: st.session_state.update(
                    copied_caption=text
                )
            )

        if st.session_state.get("copied_caption"):
            st.code(st.session_state["copied_caption"])
            st.caption("Select and copy the caption above.")

    hashtags_match = re.search(
        r"HASHTAGS\s*:\s*(.*)",
        result,
        flags=re.IGNORECASE | re.DOTALL
    )

    if hashtags_match:
        st.markdown("### #️⃣ Suggested Hashtags")
        st.write(hashtags_match.group(1).strip())

    st.download_button(
        "⬇️ Download All Captions",
        data=result,
        file_name="captioncraft_captions.txt",
        mime="text/plain"
    )

    st.caption(
        "AI-generated captions may occasionally be inaccurate. "
        "Review your caption before posting."
    )

st.divider()
st.caption("CaptionCraft AI | Built with Python, Streamlit and Gemma 3")