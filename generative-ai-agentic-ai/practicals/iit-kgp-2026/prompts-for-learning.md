# Prompts for Learning

Reusable prompt templates for studying AI topics with ChatGPT.

---

## Master Prompts

### For Any Library or Tool

```text
Act as:
1. IIT Professor
2. Senior Software Architect
3. AI Engineer
4. Technical Trainer

Teach me <TOPIC> using this structure:

1. Real-world problem it solves
2. Why it exists
3. Business analogy
4. Mental model
5. Architecture
6. Core concepts
7. Internal working
8. Code examples
9. AI use cases
10. Enterprise use cases
11. Common mistakes
12. Interview questions
13. Mini project
14. Production project

Assume I have 14 years of software development experience but I am learning AI engineering.
Use simple language and lots of real-world analogies.
```

### For Any Math Topic

```text
Act as:
1. IIT Mathematics Professor
2. AI Researcher
3. Senior Software Architect
4. Technical Trainer

Teach me <TOPIC> using this structure:

1. What problem does this concept solve?
2. Why was it invented?
3. Real-world analogy
4. Mental model
5. Visual intuition
6. Mathematical definition
7. Step-by-step examples
8. Where it appears in AI/ML
9. Where it appears in LLMs
10. Where it appears in RAG systems
11. Common misconceptions
12. Interview-level understanding
13. What depth should an AI Engineer know?
14. What can be safely ignored?
15. Mini exercises
16. Revision notes

Assume I am a Software Architect with 14 years of experience but new to AI mathematics.
Avoid academic language. Use examples from Netflix, Amazon, YouTube, Google Search, ChatGPT.
```

---

## Topic-Specific Math Prompts

### Vectors

```text
Teach me Vectors from first principles.
- What problem vectors solve
- Why coordinates are not enough
- Magnitude, Direction, Dot Product, Cosine Similarity
- How words, sentences, documents become vectors
Connect to: Embeddings, Vector Databases, Semantic Search, RAG
```

### Matrices

```text
Teach me Matrices for AI Engineers. Avoid textbook explanations.
- Why matrices were invented
- Why neural networks love matrices
- Why GPUs are optimized for matrix operations
Show: Excel Sheet → Matrix → Neural Network → Transformer
```

### Derivatives & Gradient Descent

```text
Teach me Derivatives and Gradient Descent without assuming calculus background.
- What problem they solve
- Why AI cares about rates of change
- Mountain climbing analogy for gradient descent
- Loss functions, how models learn, what a gradient means
Connect to: Neural Networks, LLM Training, Backpropagation, Fine Tuning
```

### Embeddings

```text
Teach me Embeddings from first principles.
- Why keyword search is not enough
- How meaning becomes numbers
- How words become vectors
- How similarity is calculated
Connect to: ChatGPT, RAG, Pinecone, Weaviate, ChromaDB, Semantic Search
```

### Attention Mechanism

```text
Teach me Attention Mechanism from first principles.
- Why RNNs failed
- Why attention was invented
- What problem attention solves
Examples: Reading a paragraph, a legal contract, source code
Then explain: Query, Key, Value — without formulas first.
```

### Probability

```text
Teach me Probability from an AI perspective.
- Why probability is the foundation of LLMs
- How ChatGPT predicts the next token
- Conditional probability, Joint probability
Use: weather forecasting, cricket, customer behavior examples
```

### Statistics

```text
Teach me Statistics as if I am building a recommendation system.
Cover: Mean, Median, Mode, Variance, Standard Deviation
For each: business meaning, mathematical meaning, AI meaning, when useful, when misleading.
Use Netflix and Amazon examples.
```

---

## Review & Self-Test

```text
Act as my AI mentor. Test my understanding of <TOPIC>.

Start simple, gradually increase difficulty.
After every answer:
1. What I understood correctly
2. What I misunderstood
3. The gap
4. Next question

Do not reveal answers immediately. Help me build intuition.
```

---

## Quick-Use Examples

| Purpose   | Tool    | Prompt                                                                 |
| --------- | ------- | ---------------------------------------------------------------------- |
| Learning  | ChatGPT | "Teach me Pandas as a Software Architect. Why it exists, mental model, then code." |
| Building  | Kiro    | "Build a customer churn prediction system using Pandas, Scikit-Learn and FastAPI." |
| Revision  | ChatGPT | "Create compact revision notes for Pandas. Core concepts, mental models, APIs, AI use cases." |
| Deep dive | ChatGPT | "Compare Pandas, NumPy and Spark. When each is the wrong choice." |
