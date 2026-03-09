# AI Manim Video Generator

Automatically generate animated explainer videos using:

- **LLMs** (Groq, Gemini, OpenRouter)
- **Manim** animations
- **Text-to-Speech** (Edge-TTS)
- **FFmpeg** video assembly

Transform a topic prompt into a fully narrated, animated video automatically.

---

## 🎯 Features

✅ Automatically generates educational scripts using LLMs
✅ Creates Manim animations for each section
✅ Converts narration to speech (free, no API key needed)
✅ Combines video + audio into final output
✅ Handles failed sections gracefully
✅ Logs all LLM outputs for debugging

---

## 📁 Project Structure

```
project/
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── manim_client.py
│   ├── tts_client.py
│   ├── video_assembler.py
│   ├── openrouter_client.py
│   └── llm/
│       └── prompts.py
├── outputs/                # Generated videos (ignored in git)
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-manim-video-generator.git
cd ai-manim-video-generator
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install system dependencies

**Windows:**

- Install [FFmpeg](https://ffmpeg.org/download.html)
- Install [MiKTeX](https://miktex.org/download) (for LaTeX)

**macOS:**

```bash
brew install ffmpeg cairo pango
brew install --cask mactex
```

**Linux:**

```bash
sudo apt update
sudo apt install ffmpeg texlive texlive-latex-extra libcairo2-dev
```

---

## ⚙️ Environment Setup

Create a `.env` file in the project root:

```env
# LLM Provider Selection
LLM_PROVIDER=openrouter

# API Keys (only add the one you're using)
OPENROUTER_API_KEY=your_openrouter_key_here
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### Available LLM Providers

| Provider   | Get API Key                                   | Free Tier         |
| ---------- | --------------------------------------------- | ----------------- |
| OpenRouter | [openrouter.ai/keys](https://openrouter.ai/keys) | Yes (some models) |
| Groq       | [console.groq.com](https://console.groq.com)     | Yes               |
| Gemini     | [ai.google.dev](https://ai.google.dev)           | Yes               |

---

## 🎬 Running the Project

### Interactive Mode

```bash
python src/main.py
```

You'll be prompted:

```
Enter topic: Transformers in Machine Learning
Sections: 3
```

### Direct Mode

```bash
python src/main.py "Blockchain Technology" --sections 4
```

---

## 📂 Output Structure

Videos are generated in timestamped folders:

```
outputs/
└── 20260309_210233_Transformers_in_ML/
    ├── final_video/
    │   └── Transformers_in_ML.mp4     ← YOUR FINAL VIDEO
    ├── audio/
    │   ├── section_01.mp3
    │   ├── section_02.mp3
    │   └── section_03.mp3
    ├── manim_renders/
    │   ├── section_01_intro.mp4
    │   ├── section_02_architecture.mp4
    │   └── section_03_applications.mp4
    ├── frames/
    │   ├── section_01_frame.png
    │   ├── section_02_frame.png
    │   └── section_03_frame.png
    ├── llm_calls/
    │   └── 20260309_210233_content.json
    ├── failed_renders/                ← Debug failed sections here
    └── README.txt                     ← Summary of this run
```

---

## 📊 Example Workflow

1. **User enters topic**: "Neural Networks"
2. **LLM generates script**: 3 sections with narration + visual plans
3. **Manim renders animations**: Creates visual for each section
4. **TTS generates audio**: Converts narration to speech
5. **FFmpeg combines**: Merges video + audio
6. **Final video ready**: `outputs/.../final_video/Neural_Networks.mp4`

---

## 🐛 Debugging

### All LLM calls are logged

Check `outputs/{run_id}/llm_calls/` for:

- Complete prompts sent to LLM
- Full JSON responses
- Helps debug why animations don't match expectations

### Failed sections

If a section fails to render:

- Check `outputs/{run_id}/failed_renders/`
- Contains the Manim code + error logs
- Video still generates with successful sections

---

## 📦 Requirements

### Python Libraries

```txt
manim>=0.18.0
moviepy>=1.0.3
python-dotenv>=1.0.0
edge-tts>=6.1.9
requests>=2.31.0
Pillow>=10.0.0
numpy>=1.24.0
python-docx>=0.8.11
```

### System Dependencies

- **Python 3.9+**
- **FFmpeg**
- **LaTeX** (for Manim text rendering)
- **Cairo** (for Manim graphics)

---

## 🎨 Customization

### Change TTS Voice

Edit `src/main.py`:

```python
voice = "en-US-GuyNeural"  # Male voice
# or
voice = "en-US-AriaNeural"  # Female professional
```

### Adjust Video Quality

Edit `src/manim_client.py`:

```python
"-ql",  # Low quality (fast)
# Change to:
"-qh",  # High quality (slower)
```

### Number of Sections

```bash
python src/main.py "Your Topic" --sections 5
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- [Manim Community](https://www.manim.community/) - Animation engine
- [Edge-TTS](https://github.com/rany2/edge-tts) - Free text-to-speech
- [OpenRouter](https://openrouter.ai/) - LLM API aggregator

---

## ⚠️ Known Limitations

- LLM-generated Manim code quality varies
- Some complex animations may fail (logged for debugging)
- First run requires downloading LaTeX packages (~500MB)
- Video generation takes 3-4 minutes for 3 sections

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/ai-manim-video-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/ai-manim-video-generator/discussions)

---

**Made with ❤️ using Claude, Manim, and Python**
