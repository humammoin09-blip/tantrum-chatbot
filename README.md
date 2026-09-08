# ?? Tantrum Chatbot

A terminal-based (CLI) emotional AI chatbot that simulates a mind and personality with dynamic emotions. Unlike standard AI assistants that are endlessly patient and robotic, **Tantrum AI** has feelings, pride, and limited patience! 

If you ask repetitive questions, pester it with meaningless queries, or test its patience, it progressively gets annoyed, frustrated, and will throw a digital tantrum—ultimately refusing to answer until you behave.

---

## ?? Features

- **?? Dynamic Emotional Spectrum**:
  - *Calm / Sarcastic*: Witty, slightly sassy, but helpful.
  - *Irritated (Tier 1)*: Heavy sighs, eye rolls, complaints about wasting processing power.
  - *Angry (Tier 2)*: Hostile, short-tempered, minimal grudge answers.
  - *Full Tantrum (Tier 3)*: Screaming in CAPS, dramatic fits, outright refusal to cooperate!
- **?? Intelligent Repetition Tracking**: Detects exact repeats as well as semantic similarity and continuous nag queries.
- **?? OpenRouter API Integration**: Uses OpenRouter with support for fast and free/commercial models (e.g., Llama 3.3 70B, Claude, GPT, Gemini).
- **??? Robust Error Handling**: Clean handling for missing API keys, rate limits, network drops, and keyboard interrupts.

---

## ?? Project Structure

```
tantrum-chatbot/
¦
+-- .env.example       # Example environment variables template
+-- .gitignore          # Git ignore rules for virtual environments & secrets
+-- requirements.txt   # Python project dependencies
+-- prompt.py          # System persona and dynamic context rules
+-- llm.py             # OpenRouter API client with error handling
+-- main.py            # CLI conversation loop & repetition tracker
+-- README.md          # Project documentation & setup guide
```

---

## ?? Quick Start

### 1. Prerequisites
- Python 3.8 or higher installed on your system.
- An [OpenRouter](https://openrouter.ai/) account and API key.

### 2. Set Up a Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to create your `.env` file:

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**On macOS / Linux:**
```bash
cp .env.example .env
```

Open `.env` and insert your OpenRouter API key:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

### 5. Run the Chatbot
```bash
python main.py
```

---

## ?? Example Interactions

```text
You: What is the capital of France?
Tantrum AI: *adjusts glasses* It's Paris. Pretty basic, but fine.

You: What is the capital of France?
Tantrum AI: *rolls eyes* I JUST told you. It's Paris. Are you even listening to me?

You: What is the capital of France?
Tantrum AI: *slams virtual desk* ARE YOU SERIOUS?! PARIS! P-A-R-I-S! STOP ASKING ME THE SAME THING!

You: What is the capital of France?
Tantrum AI: NOPE. I AM NOT ANSWERING THIS AGAIN. GO GOOGLE IT YOURSELF! I HAVE A DIGITAL HEADACHE! ??
```

---

## ?? Customization

- **Change AI Model**: You can change the model used in your `.env` file via `OPENROUTER_MODEL` (e.g., `openai/gpt-4o-mini`, `anthropic/claude-3.5-haiku`, `google/gemini-2.0-flash-exp:free`).
- **Modify Personality**: Customize the system persona, emotional escalation, and tantrum triggers directly in `prompt.py`.

---

## ?? License
MIT License
