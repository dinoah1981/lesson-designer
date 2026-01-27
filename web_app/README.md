# Lesson Designer Web App

A Streamlit web interface for the Marzano-based lesson planning tool.

## Quick Start (Local)

1. **Install dependencies:**
   ```bash
   cd web_app
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   ```bash
   # Create secrets file
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml

   # Edit .streamlit/secrets.toml and add your Anthropic API key
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   The app will open automatically at `http://localhost:8501`

## Deploy to Streamlit Cloud (Free)

1. **Push to GitHub:**
   - Create a new GitHub repo
   - Push the entire `lesson-designer` folder

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repo
   - Set main file path: `web_app/app.py`
   - Click "Deploy"

3. **Add secrets:**
   - In Streamlit Cloud, go to your app settings
   - Click "Secrets"
   - Add:
     ```toml
     ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"
     ```

## Features

- **Stage 1:** Collect lesson requirements (competency, grade, duration)
- **Stage 2:** Claude designs lesson using Marzano's taxonomy
- **Stage 3:** 4 student personas review the lesson for accessibility
- **Stage 4:** Generate PowerPoint slides and Word worksheets
- **Stage 5:** Download your materials

## Cost Estimate

- **Streamlit Cloud:** Free tier available
- **Anthropic API:** ~$0.01-0.05 per lesson designed
  - Uses Claude Sonnet for lesson design and persona feedback
  - Typical lesson = 3-5 API calls

## File Structure

```
web_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    └── secrets.toml.example  # API key template
```

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Make sure you've created `.streamlit/secrets.toml` with your API key
- Or set the environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`

**"Module not found: scripts"**
- Make sure you're running from the `lesson-designer` root directory
- The app needs access to the `.claude/skills/lesson-designer/scripts/` folder

**Slides/worksheet not generating**
- Check that `python-pptx` and `python-docx` are installed
- Check the console for error messages
