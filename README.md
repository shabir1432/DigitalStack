# 🤖 Agentic AI Blog System

An automated blog posting system using multiple AI agents that researches trending topics, generates high-quality content with media, and publishes to your website - all for **FREE**.

## ✨ Features

- **Multi-Provider AI**: Supports Gemini, Groq, DeepSeek, TogetherAI with automatic fallback
- **Trend Research**: Finds trending topics from Google Trends
- **SEO Optimization**: Generates keywords, hashtags, and meta descriptions
- **Content Generation**: Writes 2000-3000 word blog posts
- **Media Integration**: Pexels stock photos or StabilityAI generated images
- **Auto Publishing**: Publishes directly to your Next.js blog
- **Daily Automation**: GitHub Actions for scheduled posting

## 🛠️ Supported AI Providers

| Provider | Speed | Quality | Free Tier |
|----------|-------|---------|-----------|
| **Gemini** | Fast | Excellent | 60 req/min |
| **Groq** | ⚡ Fastest | Great | Generous |
| **DeepSeek** | Medium | Strong reasoning | Free credits |
| **TogetherAI** | Fast | Multiple models | $25 credits |

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- At least one AI API key

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: At least one AI provider
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here      # Optional but recommended

# Required for images
PEXELS_API_KEY=your_key_here

# Optional: AI image generation
STABILITY_API_KEY=your_key_here

# Configuration
PRIMARY_AI_MODEL=gemini
FALLBACK_AI_MODEL=groq
BLOG_NICHE=technology
```

### 3. Get Free API Keys

| Service | Sign Up |
|---------|---------|
| Google Gemini | https://aistudio.google.com/ |
| Groq | https://console.groq.com/ |
| DeepSeek | https://platform.deepseek.com/ |
| TogetherAI | https://together.ai/ |
| Pexels | https://www.pexels.com/api/ |
| StabilityAI | https://stability.ai/ |

### 4. Run the System

```bash
# Auto-detect trending topic
python main.py

# Specify a topic
python main.py --topic "artificial intelligence"

# Use specific niche
python main.py --niche "health"

# Auto-publish
python main.py --publish
```

### 5. Start Blog Website

```bash
cd blog
npm install
npm run dev
```

Visit http://localhost:3000 🎉

## 📁 Project Structure

```
├── agents/          # AI Agents
│   ├── trend_agent.py      # 🔍 Trend Research
│   ├── keyword_agent.py    # 🏷️ SEO Keywords
│   ├── writer_agent.py     # ✍️ Content Writer
│   ├── publisher_agent.py  # 📤 Publisher
│   └── orchestrator.py     # Coordinator
├── services/        # External APIs
├── core/            # Multi-provider LLM
├── blog/            # Next.js website
├── data/            # Generated content
└── main.py          # Entry point
```

## ⚙️ Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `PRIMARY_AI_MODEL` | Main AI provider | `gemini` |
| `FALLBACK_AI_MODEL` | Backup provider | `groq` |
| `IMAGE_SOURCE` | Image source | `pexels` |
| `BLOG_NICHE` | Blog topic area | `technology` |
| `AUTO_PUBLISH` | Publish immediately | `false` |
| `MIN_WORD_COUNT` | Minimum words | `2000` |

## 🔄 Daily Automation

Enable GitHub Actions for automatic daily posts:

1. Push code to GitHub
2. Add secrets in Settings → Secrets:
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY` (optional)
   - `PEXELS_API_KEY`
3. Workflow runs daily at 8:00 AM UTC

## 💰 Total Cost: $0/month

All services have generous free tiers!

## 📄 License

MIT License
