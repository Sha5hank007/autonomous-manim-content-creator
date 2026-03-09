
# Autonomous Manim Content Creator

Automatically generate animated explainer videos from a topic using:

* LLMs (Groq, Gemini, OpenRouter)
* Manim for animations
* Edge-TTS for narration
* FFmpeg for video assembly

Provide a topic → the system generates a narrated animated video.

---

## Demo

<!-- Option 1: Clickable YouTube thumbnail -->

<!-- [![Watch the demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) -->

<!-- Option 2: GIF preview (convert a short clip with ffmpeg or ezgif.com) -->

<!-- ![Demo](runs/demo.gif) -->

---

## Features

* Generate educational scripts using LLMs
* Automatically create Manim animations
* Convert narration to speech
* Merge animation + narration into a final video
* Continue generation even if some sections fail
* Save generated code and logs for debugging

---

## Project Structure

```
project/
│
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── manim_client.py
│   ├── tts_client.py
│   ├── video_assembler.py
│   ├── openrouter_client.py
│   └── llm/
│       └── prompts.py
│
├── runs/               # Generated videos (ignored in git)
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-manim-content-creator.git
cd autonomous-manim-content-creator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure FFmpeg is installed and available in your system path.

---

## Environment Setup

Create a `.env` file in the project root:

```env
LLM_PROVIDER=openrouter

OPENROUTER_API_KEY=your_openrouter_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

Only the API key for the selected provider is required.

---

## Selecting the LLM Provider

Set the provider in `.env`:

```env
LLM_PROVIDER=openrouter
```

Supported providers: `openrouter`, `groq`, `gemini`

---

## Running the Project

```bash
python src/main.py
```

Example input:

```
Enter topic: Transformers in Machine Learning
Sections: 3
```

---

## Output Structure

Each run creates a timestamped folder:

```
runs/
└── transformers_20260309_210233/
    ├── transformers_final.mp4
    ├── section_1.py
    ├── section_2.py
    ├── section_3_FAILED.py
    └── llm_log.md
```

Files stored per run:

* Final video
* Generated Manim code
* LLM interaction logs

Intermediate files (renders, audio, temporary clips) are automatically removed.

---

## Example Workflow

1. User enters a topic
2. LLM generates structured sections
3. Manim animations are generated
4. Narration audio is produced
5. Video and audio are combined
6. Final video is saved in `runs/`

---

## Debugging

All LLM interactions and errors are logged in `llm_log.md`.

If a section fails to render, it is saved as `section_N_FAILED.py` for easy inspection and manual debugging.
