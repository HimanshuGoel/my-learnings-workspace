# Merging & Serving

## The Problem This Solves

You have a fine-tuned model (or LoRA adapter) that passes evaluation. Now you need to serve it efficiently — merge adapters into base weights, quantize for deployment, and set up inference at acceptable latency and cost. The gap between "model works in a notebook" and "model serves production traffic" is substantial.

## How It Works — Conceptual Model

### The Serving Pipeline

```
Training output → Merge (optional) → Quantize (optional) → Deploy → Serve

LoRA adapter (10MB)     → Merge into base → Single model (16GB)
                         ↓
              Quantize to 4-bit → Compressed model (4GB)
                         ↓
              Deploy on GPU/CPU → Serve via API
```

### Three Key Decisions

1. **Merge or not?** — Merge adapter into base for simpler deployment, or keep separate for multi-adapter serving
2. **Quantize or not?** — Compress model for cheaper/faster inference at slight quality cost
3. **Where to deploy?** — GPU cloud, serverless, or managed inference endpoint

## When to Use Which Approach

| Situation | Merge? | Quantize? | Deploy Where? |
|-----------|--------|-----------|---------------|
| Single-task, max quality | Yes | No (bf16) | GPU cloud (A100) |
| Single-task, cost-sensitive | Yes | Yes (4-bit GPTQ/AWQ) | Smaller GPU (T4/L4) |
| Multi-task (swap adapters) | No (keep LoRA) | Base quantized, adapters separate | GPU with adapter swapping |
| Low traffic (< 100 req/day) | Yes | Yes (4-bit) | Serverless (Modal, RunPod) |
| High traffic (> 1K req/day) | Yes | Yes (optimized) | Dedicated GPU with vLLM |
| Just testing/demo | Yes | Optional | HuggingFace Inference Endpoints |

## Implementation Walkthrough

### Step 1: Merge LoRA Adapter into Base Model

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="cpu",  # Merge on CPU to save GPU memory
)

# Load adapter on top of base
model = PeftModel.from_pretrained(base_model, "./lora-adapter")

# Merge adapter weights into base model
merged_model = model.merge_and_unload()

# Save merged model (full weights, no adapter dependency)
merged_model.save_pretrained("./merged-model")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B-Instruct")
tokenizer.save_pretrained("./merged-model")

# Result: ./merged-model/ contains the complete fine-tuned model
# Can be loaded directly without PEFT library
```

### Step 2: Quantize for Efficient Inference

```python
# Option A: GPTQ (offline quantization, best quality for 4-bit)
# Requires: pip install auto-gptq
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False,
)

model = AutoGPTQForCausalLM.from_pretrained(
    "./merged-model",
    quantize_config=quantize_config,
)
model.quantize(calibration_dataset)  # Needs small dataset for calibration
model.save_quantized("./merged-model-4bit-gptq")


# Option B: AWQ (faster quantization, comparable quality)
# Requires: pip install autoawq
from awq import AutoAWQForCausalLM

model = AutoAWQForCausalLM.from_pretrained("./merged-model")
model.quantize(
    tokenizer,
    quant_config={"zero_point": True, "q_group_size": 128, "w_bit": 4},
)
model.save_quantized("./merged-model-4bit-awq")


# Option C: bitsandbytes (on-the-fly quantization, simplest)
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
model = AutoModelForCausalLM.from_pretrained(
    "./merged-model", quantization_config=bnb_config
)
# No separate save step — quantizes at load time
```

### Step 3: Serve with vLLM (Production-Grade)

```python
# vLLM: Fast inference engine with PagedAttention (2-4× faster than HF)
# pip install vllm

# Start server:
# python -m vllm.entrypoints.openai.api_server \
#   --model ./merged-model \
#   --dtype bfloat16 \
#   --max-model-len 4096 \
#   --port 8000

# Or with quantized model:
# python -m vllm.entrypoints.openai.api_server \
#   --model ./merged-model-4bit-awq \
#   --quantization awq \
#   --port 8000

# Client usage (OpenAI-compatible API):
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="./merged-model",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0,
)
```

### Step 4: Deploy on Cloud (Serverless)

```python
# Option A: HuggingFace Inference Endpoints
# 1. Push model to HuggingFace Hub
merged_model.push_to_hub("your-username/your-fine-tuned-model", private=True)
# 2. Create endpoint in HF dashboard
# 3. Call via API: https://api-inference.huggingface.co/models/your-username/...

# Option B: Modal (serverless GPU)
import modal

@modal.function(gpu="T4", image=image)
def generate(prompt: str) -> str:
    model = load_model("./merged-model-4bit")  # Cached across calls
    return model.generate(prompt)

# Option C: RunPod Serverless
# Upload model → Configure endpoint → Auto-scales to zero when idle
```

### Step 5: Multi-Adapter Serving (Advanced)

```python
# Serve one base model with multiple LoRA adapters
# Use LoRAX or vLLM with adapter support

# vLLM with LoRA adapters:
# python -m vllm.entrypoints.openai.api_server \
#   --model meta-llama/Llama-3-8B-Instruct \
#   --enable-lora \
#   --lora-modules customer-support=./adapter-cs code-review=./adapter-cr

# Client switches adapter per request:
response = client.chat.completions.create(
    model="customer-support",  # or "code-review"
    messages=[...],
)
```

## Configuration & Decisions

| Decision | Options | Recommendation |
|----------|---------|---------------|
| Merge adapter? | Merge (simpler) vs Keep separate (multi-task) | Merge unless you need multiple adapters |
| Quantization | None (bf16) / 8-bit / 4-bit (GPTQ/AWQ) | 4-bit AWQ for cost-sensitive deployment |
| Inference engine | HuggingFace / vLLM / TGI | vLLM for production (2-4× faster) |
| Deployment | Dedicated GPU / Serverless / Managed | Serverless for < 1K req/day, dedicated for more |
| Batch inference | vLLM continuous batching | Always enable for throughput |

### Quantization Quality Impact

| Precision | Model Size (8B) | Quality vs bf16 | Speed | Use When |
|-----------|-----------------|-----------------|-------|----------|
| bf16 | ~16 GB | 100% (reference) | 1× | Max quality, have GPU budget |
| int8 | ~8 GB | 99% | 1.2× | Slight savings |
| 4-bit (GPTQ) | ~4 GB | 95-98% | 1.5-2× | Production cost optimization |
| 4-bit (AWQ) | ~4 GB | 96-99% | 1.5-2× | Best 4-bit quality |
| 3-bit | ~3 GB | 90-95% | 2× | Extreme cost savings (risky) |

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Merge changes output quality | Merged model slightly different from adapter model | Usually negligible; if problematic, serve with PEFT directly |
| Quantization degrades quality | Answers worse after 4-bit conversion | Try AWQ instead of GPTQ, or use 8-bit |
| vLLM doesn't support your model | Import errors or unsupported architecture | Check vLLM supported models list, use HF Transformers as fallback |
| Inference too slow | > 2s latency per request | Enable batching, use faster GPU, reduce max_seq_length |
| OOM during inference | CUDA OOM on large prompts | Reduce max_model_len, use quantization, batch smaller |
| Cold start too slow (serverless) | First request takes 30-60s | Use provisioned instances, or keep-alive ping |

## Cost & Resource Planning

| Deployment | GPU | Monthly Cost | Requests/Day | Latency |
|------------|-----|-------------|--------------|---------|
| HF Inference Endpoint (T4) | T4 16GB | ~$50/mo | Up to 1K | 1-5s |
| RunPod Serverless | T4/A100 | Pay per second | Auto-scale | 2-10s (cold start) |
| Modal Serverless | T4/A100 | Pay per second | Auto-scale | 1-5s (warm) |
| Dedicated vLLM (A100) | A100 80GB | ~$2500/mo | 10K+ | 200-500ms |
| Dedicated vLLM (T4, quantized) | T4 16GB | ~$350/mo | 1-5K | 500ms-2s |

## Evaluation

| Check | How | Target |
|-------|-----|--------|
| Merged model matches adapter | Run same test set on both | < 0.5% difference |
| Quantized quality acceptable | Run test set on quantized | < 3% degradation vs bf16 |
| Inference latency | Benchmark 100 requests | < target (e.g., 1s p95) |
| Throughput | Concurrent request test | Handles expected load |
| Cost per 1K requests | Track compute costs | Within budget |

## Decision Checkpoint

- [ ] Adapter merged successfully (if single-task deployment)
- [ ] Quantization tested and quality is acceptable (if using 4-bit)
- [ ] Inference engine chosen (vLLM for production, HF for testing)
- [ ] Deployment target selected (serverless vs dedicated based on traffic)
- [ ] Latency and throughput meet requirements
- [ ] Cost per request estimated and within budget
- [ ] Model uploaded to deployment target (HF Hub, cloud storage)
- [ ] API endpoint tested end-to-end
