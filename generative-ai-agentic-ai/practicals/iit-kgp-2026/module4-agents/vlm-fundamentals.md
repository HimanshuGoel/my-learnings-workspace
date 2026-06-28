# VLM Fundamentals

## What This Enables

Vision-Language Models (VLMs) give LLMs the ability to SEE — process images, screenshots, diagrams, and documents alongside text. This unlocks: document understanding, visual QA, UI interaction, chart analysis, and multimodal RAG systems that handle real-world documents (not just clean text).

## Architecture Overview

### How VLMs Process Images

```
Image Input → Vision Encoder → Patch Embeddings → Projection Layer → LLM (alongside text tokens)

Step 1: Split image into patches (e.g., 14×14 pixel patches, typically 576 patches for 336×336 image)
Step 2: Encode each patch into a vector using a vision encoder (ViT or CLIP)
Step 3: Project patch vectors into the LLM's embedding space (linear projection or MLP)
Step 4: Concatenate image tokens with text tokens → LLM processes both together
```

**Software analogy:** Think of it like a microservice architecture. The vision encoder is a separate service that "translates" images into a language the LLM understands (vectors). The LLM then processes these translated image-tokens alongside normal text-tokens using the same attention mechanism.

### Key Models & Their Architectures

| Model | Vision Encoder | LLM | How They Connect | Max Resolution | Open? |
|-------|---------------|-----|-----------------|---------------|-------|
| GPT-4V/4o | Internal (likely ViT) | GPT-4 | Proprietary fusion | Multiple (tiled) | No (API) |
| Claude 3.5 Sonnet | Internal | Claude | Proprietary | 1568×1568 | No (API) |
| LLaVA 1.6 | CLIP ViT-L/14 | Llama/Mistral | Linear projection | 672×672 (tiled) | Yes |
| Qwen-VL-2 | ViT (custom) | Qwen-2 | Cross-attention | Dynamic | Yes |
| InternVL2 | InternViT-6B | InternLM2 | Dynamic + MLP | Dynamic | Yes |
| Phi-3-Vision | CLIP | Phi-3 | Linear projection | 1344×1344 | Yes |

### The Vision Encoder (CLIP)

```
CLIP training: Given (image, text) pairs from the internet
  → Learn to match images with their descriptions
  → Result: a vision model that produces "semantically meaningful" embeddings
  
Why CLIP for VLMs:
  - Already understands image CONTENT (not just pixels)
  - Produces vectors that are somewhat aligned with text embeddings
  - Pre-trained on 400M+ image-text pairs (massive world knowledge)
  - Different from ImageNet models: CLIP understands concepts, not just objects
```

### Image Tiling (High Resolution)

```
Problem: CLIP trained on 224×224 or 336×336 — can't see fine details in large images

Solution: Image Tiling (used by GPT-4V, LLaVA 1.6, InternVL)
  1. Resize image to fit within max resolution
  2. Split into tiles (e.g., 2×2 or 3×3 grid of 336×336 patches)
  3. Also keep a downscaled "global" view of full image
  4. Encode each tile + global view separately
  5. Concatenate all tile embeddings → LLM sees both details AND big picture

Cost: More tiles = more tokens = more compute + cost
  336×336 (1 tile): ~576 tokens
  672×672 (4 tiles + global): ~2880 tokens
  1344×1344 (16 tiles + global): ~9000+ tokens
```

## Key Patterns & When to Use Each

| Pattern | When | Example |
|---------|------|---------|
| Single image + question | Simple visual QA | "What's in this image?" |
| Image + document text | Multimodal RAG | "Based on this chart and text, what's the trend?" |
| Multi-image comparison | Visual reasoning | "Compare these two screenshots" |
| Image → structured data | Data extraction | "Extract the table from this PDF page" |
| UI screenshot → action | Agent interaction | "Click the submit button" |
| Document image → text | OCR alternative | "Read this scanned document" |

## Implementation with OpenAI (GPT-4o Vision)

```python
from openai import OpenAI
import base64

client = OpenAI()

def analyze_image(image_path: str, question: str) -> str:
    """Send an image to GPT-4o for analysis."""
    # Encode image to base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{image_data}",
                    "detail": "high",  # "low" (fixed 85 tokens) or "high" (tiled, more tokens)
                }},
            ],
        }],
        max_tokens=1000,
    )
    return response.choices[0].message.content


def analyze_image_url(url: str, question: str) -> str:
    """Analyze an image from URL."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": url, "detail": "high"}},
            ],
        }],
        max_tokens=1000,
    )
    return response.choices[0].message.content
```

### With LangChain

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o", max_tokens=1000)

message = HumanMessage(content=[
    {"type": "text", "text": "Describe what you see in this chart"},
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
])

response = llm.invoke([message])
```

### With Open-Source (LLaVA)

```python
from transformers import LlavaForConditionalGeneration, AutoProcessor
from PIL import Image

model = LlavaForConditionalGeneration.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

image = Image.open("chart.png")
prompt = "USER: <image>\nDescribe the trends in this chart.\nASSISTANT:"

inputs = processor(text=prompt, images=image, return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=500)
result = processor.decode(output[0], skip_special_tokens=True)
```

## State Management & Memory

- VLMs are stateless per call (no image memory across turns unless you re-send)
- Multi-turn visual conversations: must re-include the image in each message
- For efficiency: describe the image once, then refer to the description in follow-ups
- Image tokens are expensive: 576-9000 tokens per image (counts toward context window)

## Error Handling & Guardrails

| Failure Mode | Symptom | Fix |
|-------------|---------|-----|
| Hallucinated text in images | VLM "reads" text that isn't there | Cross-check with OCR (Tesseract), ask for confidence |
| Wrong spatial reasoning | Misidentifies left/right, above/below | Use higher detail setting, crop to relevant area |
| Chart misinterpretation | Wrong values read from axes | Extract data programmatically (not visually) for precision |
| Token budget exceeded | Image + text > context window | Use "low" detail, resize images, fewer tiles |
| Refused to process | Safety filter blocks legitimate image | Reframe the prompt, crop out irrelevant content |
| Slow response | High-res images take 5-10s | Use "low" detail for quick screening, "high" for deep analysis |

## Testing & Debugging

```python
# Visual QA test set: image + question + expected answer
vqa_test_set = [
    {"image": "chart_sales_q1.png", "question": "What month had highest sales?", "expected": "March"},
    {"image": "table_specs.png", "question": "What's the RAM specification?", "expected": "16 GB"},
    {"image": "diagram_flow.png", "question": "How many steps are in the process?", "expected": "5"},
]

# Key debugging strategy: Always ask "what do you see?" before "answer my question"
# This reveals if the model is actually perceiving the image correctly
```

## Production Considerations

### Cost
- GPT-4o image input: ~$2.50 per 1000 high-detail images (tiled)
- GPT-4o image input: ~$0.85 per 1000 low-detail images
- Each high-res image ≈ 1000-9000 tokens (at $2.50/1M input tokens)
- Strategy: Use "low" for routing/screening, "high" only when detail matters

### Latency
- Low detail: 1-3s per image
- High detail: 3-8s per image
- Multi-image: Linear scaling (each image adds processing time)

### Scaling
- Batch processing: Send multiple images in sequence (no native batch API)
- For high-volume: Consider local VLM (LLaVA) on GPU for throughput
- Cache results for repeated images (same image = same tokens)

## Integration Points

- **Module 2 (RAG):** VLMs enable multimodal RAG (next topic) — extract info from document images
- **Module 4 (Agents):** VLMs as agent "eyes" — screenshot analysis, UI interaction
- **Capstone:** Document understanding pipeline (PDFs → VLM extraction → RAG)

## Architecture Decision Record

**Decision:** Use GPT-4o for VLM capabilities, with LLaVA as local fallback.

**Why:** GPT-4o has the best visual understanding quality. LLaVA-1.6-7B is good enough for simple extraction tasks and runs locally without API costs.

**Trade-off accepted:** API dependency for quality-critical visual tasks. For production at scale, evaluate moving to larger open-source VLMs (InternVL2, Qwen-VL-2) that approach GPT-4o quality.

**When to reconsider:** If API costs exceed $100/month on image processing, or if latency requirements are < 1s per image, switch to local VLM.
