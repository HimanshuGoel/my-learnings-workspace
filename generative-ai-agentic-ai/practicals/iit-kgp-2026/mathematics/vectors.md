# Stage 4 â€” Linear Algebra & Vectors

## One-Line Summary

> Linear Algebra teaches how AI represents meaning as vectors, measures similarity and distance between them, combines them into richer concepts, and discovers the fundamental directions that efficiently describe information.

---

## Why This Matters for AI

- Modern AI converts everything (words, sentences, images, users, products) into vectors called **embeddings** â€” without vectors, AI has no way to represent knowledge
- Similarity search, recommendations, and transformer attention all rely on vector operations like dot products
- Neural networks are fundamentally linear algebra machines â€” every single layer performs vector transformations
- Dimensionality reduction techniques (PCA, t-SNE, UMAP) use basis, span, and orthogonality concepts to compress high-dimensional data
- Understanding vectors is a prerequisite for matrices, calculus gradients, backpropagation, and ultimately understanding how LLMs learn

---

## Core Concepts

### 4.1 Understanding Vectors

Everything in AI starts with representing information as numbers in space. This section builds the foundation: what vectors are, how they live in coordinate spaces, and what their basic properties mean.

### 1. 3D Coordinate Space

- **Meaning** â€” A coordinate system assigns a unique numerical address to every point in space. In 1D it's a single number on a line, in 2D it's a pair `(x, y)` on a flat plane, and in 3D it's a triple `(x, y, z)` in physical space.
- **Why It Exists** â€” Without coordinates, we have no way to precisely describe where something is. Coordinates give us a shared language for location and position.
- **Formula** â€” `(x)` for 1D, `(x, y)` for 2D, `(x, y, z)` for 3D, and `(xâ‚, xâ‚‚, ..., xâ‚™)` for n-dimensional space
- **Example** â€” The point `(3, 5)` in 2D means "go 3 units along the x-axis and 5 units along the y-axis." In a 768-dimensional embedding space, a word like "king" would be a point with 768 coordinates.
- **Mental Model** â€” Think of coordinates as a postal address. Just like "Block 3, Floor 5" tells you exactly where an apartment is, `(3, 5)` tells you exactly where a point is in 2D space.
- **AI Connection** â€” AI embeddings are positions in high-dimensional meaning-space. When GPT converts the word "cat" into a vector, it's assigning it coordinates in a 1536-dimensional space. Similar words end up at nearby coordinates.
- **Common Mistake** â€” Don't confuse the number of dimensions with physical space. AI routinely works in 768, 1536, or 4096+ dimensions â€” these aren't physical directions, they're abstract meaning directions.

### 2. Vectors as Arrows

- **Meaning** â€” A vector represents movement with both a direction (which way) and a magnitude (how far). Unlike a point which just marks a location, a vector describes a displacement or relationship.
- **Why It Exists** â€” Points tell us "where," but many real problems need "which way and how much." Velocity, force, and semantic relationships all require both direction and size.
- **Formula** â€” A vector `(3, 2)` looks identical to a point `(3, 2)` in notation, but the interpretation is different: the vector means "move 3 right and 2 up."
- **Example** â€” The point `(3, 2)` says "I am at position (3,2)." The vector `(3, 2)` says "move 3 units in the x-direction and 2 units in the y-direction from wherever you start."
- **Mental Model** â€” A vector is a movement instruction or an arrow. It doesn't care where it starts â€” only the direction and length matter.
- **AI Connection** â€” Word embeddings behave like directional meaning vectors. The vector from "king" to "queen" captures the concept of gender, regardless of where those words sit in absolute space.

### 3. Plotting Vectors

- **Meaning** â€” A vector is visually represented as an arrow drawn from a starting point (tail) to an ending point (head). By convention, vectors are usually drawn from the origin `(0, 0)`.
- **Why It Exists** â€” Humans understand pictures better than numbers. Plotting vectors lets us see relationships, similarities, and patterns that would be invisible in raw coordinate lists.
- **Example** â€” Vector `(4, 3)` is drawn as an arrow from `(0,0)` to `(4,3)`. You can immediately see it points roughly northeast and is about 5 units long.
- **Mental Model** â€” Imagine a dashboard where each arrow represents a concept. Arrows pointing in similar directions mean similar things.
- **AI Connection** â€” Tools like PCA, t-SNE, and UMAP take high-dimensional embeddings (768D) and project them down to 2D/3D arrows so humans can visualize which concepts cluster together.

### 4. Magnitude of a Vector

- **Meaning** â€” The magnitude (or length) of a vector measures how far the arrow stretches. It tells you the "amount" or "strength" of the vector, independent of its direction.
- **Why It Exists** â€” Sometimes we need to know not just which way something points, but how strong or intense it is. Speed vs. velocity: magnitude strips away direction and gives pure size.
- **Formula** â€” For a 2D vector `(x, y)`: magnitude `|v| = âˆš(xÂ² + yÂ²)`. For 3D: `|v| = âˆš(xÂ² + yÂ² + zÂ²)`.
- **Example** â€” Vector `(3, 4)` has magnitude `âˆš(9 + 16) = âˆš25 = 5`. This is just the Pythagorean theorem applied to vectors.
- **Mental Model** â€” Direction answers "which way?" and magnitude answers "how much?" Together they fully describe a vector.
- **AI Connection** â€” In neural networks, the magnitude of an activation vector indicates confidence or signal strength. A larger embedding magnitude can indicate a more "certain" representation.

### 5. Unit Vector

- **Meaning** â€” A unit vector is a vector whose magnitude equals exactly 1. It preserves direction while removing any notion of size. You create it by dividing a vector by its own magnitude.
- **Why It Exists** â€” Without unit vectors, we can't compare directions independently of magnitude. If we want to ask "are these two concepts pointing the same way?" we need to strip away their different sizes first.
- **Formula** â€” `vÌ‚ = v / |v|` (divide each coordinate by the magnitude)
- **Example** â€” Vector `(3, 4)` has magnitude 5. Its unit vector is `(3/5, 4/5) = (0.6, 0.8)`. Same direction, length exactly 1.
- **Mental Model** â€” A compass needle. It only tells you direction â€” north, south, east â€” it doesn't tell you how far to walk.
- **AI Connection** â€” Before computing cosine similarity, embeddings are often normalized to unit length. This ensures the comparison measures only directional alignment, not magnitude.
- **Common Mistake** â€” The zero vector `(0, 0)` has no unit vector because you can't divide by zero magnitude. It has no direction to preserve.

### 6. Zero Vector

- **Meaning** â€” The zero vector `(0, 0)` or `(0, 0, 0)` has no direction, no magnitude, and represents "no movement at all." It's the vector equivalent of the number zero.
- **Why It Exists** â€” Just as zero is needed in arithmetic (what happens when you add nothing?), the zero vector is needed for vector algebra to work consistently. It's the identity element for vector addition.
- **Formula** â€” `0 = (0, 0, ..., 0)` in any dimension
- **Example** â€” `(5, 3) + (0, 0) = (5, 3)`. Adding the zero vector changes nothing, just like adding zero to a number.
- **Mental Model** â€” Standing completely still. No direction to face, no distance to travel.
- **AI Connection** â€” In neural networks, a zero activation vector means "this neuron contributes nothing." Padding tokens in NLP are often represented as zero vectors.

---

## 4.2 Vector Operations

Now that we understand what vectors are, the next question is: what can we do with them? Vector operations let us combine, compare, and transform vectors â€” which is exactly what neural networks do millions of times during a forward pass.

### 7. Vector Addition

- **Meaning** â€” Adding two vectors combines their movements by adding corresponding coordinates. The result is a new vector that represents both movements applied together.
- **Why It Exists** â€” In the real world, forces combine. In AI, features combine. Vector addition is how we merge information from multiple sources into a single representation.
- **Formula** â€” `(a, b) + (c, d) = (a+c, b+d)`
- **Example** â€” Walking `(2, 3)` then `(1, 4)` lands you at `(3, 7)`. The combined movement is the sum of both vectors.
- **Mental Model** â€” Walking two legs of a journey. First go east 2 and north 3, then east 1 and north 4. Your total displacement is east 3, north 7.
- **AI Connection** â€” Residual connections in ResNet and Transformers literally add vectors: `output = layer(x) + x`. This "skip connection" is just vector addition, and it's one of the key innovations that made deep networks trainable.

### 8. Vector Subtraction

- **Meaning** â€” Subtracting vectors finds the difference between them â€” the vector you'd need to add to one to reach the other. It answers: "what's the gap between these two?"
- **Why It Exists** â€” Subtraction reveals relationships. The difference between two embeddings captures what makes them distinct from each other.
- **Formula** â€” `(a, b) - (c, d) = (a-c, b-d)`
- **Example** â€” `(7, 5) - (2, 3) = (5, 2)`. To get from point `(2,3)` to point `(7,5)`, you need to move `(5,2)`.
- **Mental Model** â€” "What change is needed to get from A to B?" Subtraction gives you the arrow pointing from A toward B.
- **AI Connection** â€” The famous word embedding arithmetic: `vector("king") - vector("man") + vector("woman") â‰ˆ vector("queen")`. Subtraction extracts the "gender" relationship. Gradients in training are also computed via subtraction (predicted - actual = error).

### 9. Scalar Multiplication

- **Meaning** â€” Multiplying a vector by a single number (called a scalar) stretches or shrinks the vector without changing its direction. A negative scalar flips the direction.
- **Why It Exists** â€” We often need to control the intensity of a vector without changing what it represents. "Same direction, but louder" or "same direction, but quieter."
- **Formula** â€” `k(x, y) = (kx, ky)` where k is any real number
- **Example** â€” `2 Ã— (3, 2) = (6, 4)` (same direction, doubled length). `-1 Ã— (3, 2) = (-3, -2)` (opposite direction, same length).
- **Mental Model** â€” A volume knob on a speaker. Turn it up (k > 1) to amplify, turn it down (0 < k < 1) to reduce, flip it negative to reverse.
- **AI Connection** â€” Every weight in a neural network is a scalar. When the network multiplies an input feature by weight 0.8, it's saying "keep this information but reduce its influence by 20%." Learning is the process of finding the right scalars.
- **Common Mistake** â€” Scalar multiplication changes magnitude but not direction (unless the scalar is negative). It cannot rotate a vector â€” that requires matrix multiplication (â†’ See matrices.md Â§ Matrix-Vector Multiplication).

---

## 4.3 Similarity & Direction

The most powerful question in AI is: "how similar are these two things?" In vector space, similarity is measured by how closely two vectors point in the same direction. This section covers the mathematical tools for answering that question.

### 10. Dot Product

- **Meaning** â€” The dot product takes two vectors and produces a single number that measures how much they point in the same direction. It's computed by multiplying corresponding coordinates and summing the results.
- **Why It Exists** â€” We need a mathematical way to ask "how similar are these two vectors?" The dot product is the simplest and most efficient answer to that question.
- **Formula** â€” Algebraic: `AÂ·B = xâ‚xâ‚‚ + yâ‚yâ‚‚`. Geometric: `AÂ·B = |A||B|cosÎ¸` where Î¸ is the angle between them.
- **Example** â€” `(1, 0)Â·(0, 1) = 1Ã—0 + 0Ã—1 = 0` (perpendicular vectors, zero similarity). `(1, 0)Â·(1, 0) = 1Ã—1 + 0Ã—0 = 1` (identical vectors, maximum similarity). `(2, 3)Â·(4, 1) = 8 + 3 = 11` (somewhat similar directions).
- **Mental Model** â€” Imagine shining a flashlight along vector A. The dot product tells you how much of vector B's shadow falls along A's direction. More shadow = more similarity.
- **AI Connection** â€” Transformer attention scores are computed as dot products between query and key vectors. Semantic search ranks results by the dot product between the query embedding and document embeddings. This single operation is the engine of modern AI.
- **Interpretation:**
  - **Positive** â†’ vectors point in similar directions (similar meaning)
  - **Zero** â†’ vectors are perpendicular (completely independent)
  - **Negative** â†’ vectors point in opposite directions (opposite meaning)

### 11. Orthogonal Vectors

- **Meaning** â€” Two vectors are orthogonal (perpendicular) when the angle between them is exactly 90Â°. Their dot product equals zero, meaning they share absolutely no directional information.
- **Why It Exists** â€” Orthogonality tells us when two pieces of information are completely independent. If features are orthogonal, knowing one tells you nothing about the other â€” this is the ideal for efficient representations.
- **Formula** â€” `AÂ·B = 0` means A and B are orthogonal
- **Example** â€” `(1, 0)` and `(0, 1)` are orthogonal: `1Ã—0 + 0Ã—1 = 0`. They point along completely different axes. But `(1, 1)` and `(1, 0)` are NOT orthogonal: `1Ã—1 + 1Ã—0 = 1 â‰  0`.
- **Mental Model** â€” North and East are orthogonal directions. Knowing how far north you are tells you nothing about how far east you are. They carry completely independent information.
- **AI Connection** â€” PCA produces orthogonal principal components so each captures unique information with zero redundancy. Well-trained embeddings tend to have near-orthogonal directions for unrelated concepts.
- **Common Mistake** â€” Orthogonal does NOT mean opposite. Opposite vectors have a dot product of -1 (negative, pointing away from each other). Orthogonal means the dot product is exactly 0 (completely unrelated).

---

## 4.4 Measuring Vectors

We can now add, subtract, and compare direction â€” but how do we measure the "distance" between vectors? Different problems need different distance measures. This section covers norms: the mathematical rulers we use to measure vector size and distance.

### 12. Norms

- **Meaning** â€” A norm is a function that assigns a non-negative "size" to any vector. Different norms define "size" differently, and the choice of norm affects how we measure distance and similarity.
- **Why It Exists** â€” There's no single "correct" way to measure size. Is the distance between two cities the straight-line distance, or the driving distance? Different norms answer different versions of this question.
- **Formula** â€” General notation: `||v||` (double bars around the vector)
- **Mental Model** â€” A norm is a ruler for vectors. A tailor's tape measure, a straight ruler, and a GPS all measure "distance" differently â€” norms are the mathematical version of this.
- **AI Connection** â€” The choice of norm affects loss functions (L1 vs L2 loss), regularization (Lasso vs Ridge), and distance metrics (nearest neighbor search). Picking the right norm is a design decision in ML.

### 13. Euclidean Norm (L2)

- **Meaning** â€” The Euclidean norm measures straight-line distance â€” the shortest path between two points. It's the most intuitive and commonly used norm, equivalent to the magnitude we defined earlier.
- **Why It Exists** â€” It matches our physical intuition of distance. When we think "how far apart are these two things?", we usually mean straight-line distance.
- **Formula** â€” `||v||â‚‚ = âˆš(xÂ² + yÂ²)` for 2D; `âˆš(xâ‚Â² + xâ‚‚Â² + ... + xâ‚™Â²)` for nD
- **Example** â€” Distance between `(1, 2)` and `(4, 6)`: `âˆš((4-1)Â² + (6-2)Â²) = âˆš(9 + 16) = âˆš25 = 5`
- **Mental Model** â€” "As the crow flies" â€” the straight-line distance ignoring all obstacles.
- **AI Connection** â€” Used in K-Nearest Neighbors, K-Means clustering, and as the default distance metric in most ML algorithms. L2 loss (mean squared error) uses this norm to measure prediction errors.

### 14. Manhattan Distance (L1)

- **Meaning** â€” The Manhattan distance measures how far you'd travel along grid lines (sum of absolute differences in each coordinate). No diagonals allowed â€” only horizontal and vertical moves.
- **Why It Exists** â€” In many real scenarios, you can't travel in straight lines. A taxi in Manhattan must follow streets. Similarly, in high-dimensional spaces, L1 distance is often more robust to outliers than L2.
- **Formula** â€” `||v||â‚ = |xâ‚| + |xâ‚‚| + ... + |xâ‚™|`; between two points: `|xâ‚-xâ‚‚| + |yâ‚-yâ‚‚|`
- **Example** â€” Vector `(3, 4)` has L1 norm = `|3| + |4| = 7`. Compare with L2 norm = `âˆš(9+16) = 5`. L1 is always â‰¥ L2.
- **Mental Model** â€” "As the taxi drives" â€” following a city grid, you can only go along blocks, never cut through diagonally.
- **AI Connection** â€” L1 regularization (Lasso) encourages sparsity â€” it pushes many weights to exactly zero, performing automatic feature selection. L1 loss (mean absolute error) is more robust to outliers than L2 loss.

### 15. p-Norms

- **Meaning** â€” The p-norm is a generalized family where the parameter p controls how size is measured. L1 and L2 are just special cases of the p-norm with p=1 and p=2 respectively.
- **Why It Exists** â€” Different values of p give different trade-offs. Low p (like p=1) emphasizes all coordinates equally. High p (like p=âˆž) emphasizes only the largest coordinate. This flexibility lets us tune distance to our problem.
- **Formula** â€” `||v||â‚š = (|xâ‚|áµ– + |xâ‚‚|áµ– + ... + |xâ‚™|áµ–)^(1/p)`
- **Example** â€” For vector `(3, 4)`: L1 = 7, L2 = 5, Lâˆž = max(3,4) = 4. The same vector has different "sizes" under different norms.
- **Mental Model** â€” Changing p changes the shape of what "equal distance from the origin" looks like. p=2 gives a circle, p=1 gives a diamond, p=âˆž gives a square.
- **AI Connection** â€” p=1 for sparsity-inducing regularization (Lasso), p=2 for smooth optimization (Ridge), p=âˆž for minimax/worst-case scenarios. The choice of p is a model design decision.

| p | Name | Shape of Unit Ball | AI Use Case |
| - | ---- | ------------------ | ----------- |
| 1 | Manhattan | Diamond | Sparsity, feature selection (Lasso) |
| 2 | Euclidean | Circle | Standard distance, Ridge regularization |
| âˆž | Chebyshev | Square | Worst-case bounds |

---

## 4.5 Vector Spaces

So far we've worked with individual vectors. But AI works with entire spaces of vectors â€” learned worlds where concepts live. This section introduces the structures that make vector spaces meaningful: how vectors combine, what they can reach, when they're redundant, and how to find the most efficient set of building blocks.

### 16. Linear Combinations

- **Meaning** â€” A linear combination creates a new vector by scaling existing vectors by different amounts and adding them together. It's the most fundamental operation for building new vectors from old ones.
- **Why It Exists** â€” Most vectors we encounter aren't "basic" â€” they're mixtures of simpler directions. Linear combinations give us the formal language for describing these mixtures.
- **Formula** â€” `câ‚A + câ‚‚B + câ‚ƒC + ...` where câ‚, câ‚‚, câ‚ƒ are scalars (any real numbers)
- **Example** â€” Given vectors `A = (1, 0)` and `B = (0, 1)`, the linear combination `3A + 2B = 3(1,0) + 2(0,1) = (3, 2)`. We built `(3, 2)` by mixing A and B.
- **Mental Model** â€” Mixing paint colors. You can create orange by combining some amount of red and some amount of yellow. The "amounts" are your scalars, the base colors are your vectors.
- **AI Connection** â€” Every single neuron in a neural network computes a linear combination: `output = wâ‚xâ‚ + wâ‚‚xâ‚‚ + ... + wâ‚™xâ‚™ + bias`. The weights are scalars, the inputs are vectors. The entire forward pass is linear combinations followed by nonlinear activations.

### 17. Span

- **Meaning** â€” The span of a set of vectors is the collection of ALL possible vectors you can create using linear combinations of them. It defines the "reachable world" from those vectors.
- **Why It Exists** â€” We need to know: given some vectors, what's the full set of things they can represent? If two vectors span a plane, any point on that plane is reachable. If they only span a line, the plane is beyond reach.
- **Example** â€” One vector `(1, 0)` spans only the x-axis (a line). Two independent vectors `(1, 0)` and `(0, 1)` span the entire 2D plane. Any point `(a, b)` can be built as `a(1,0) + b(0,1)`.
- **Mental Model** â€” The "reachable world." One vector gives you a line (1D world). Two independent vectors give you a plane (2D world). Three independent vectors give you a 3D world. n independent vectors give you nD space.
- **AI Connection** â€” An embedding space is the span of the model's learned direction vectors. If the model only learned 50 independent directions, it can only represent concepts in that 50-dimensional span â€” everything else is invisible to it.
- **Common Mistake** â€” Adding more vectors doesn't always increase the span. If the new vector is a linear combination of existing ones (dependent), the span stays the same. Only genuinely new directions expand the reachable world.

### 18. Linear Dependence

- **Meaning** â€” A vector is linearly dependent on others if it can be perfectly recreated using a linear combination of them. It adds no new information â€” it's mathematically redundant.
- **Why It Exists** â€” Identifying dependence tells us which vectors are genuine new information and which are just repackaged versions of what we already have. This is critical for efficiency.
- **Example** â€” Given `A = (1, 0)` and `B = (0, 1)`, the vector `C = (2, 3)` is dependent because `C = 2A + 3B`. But `A` and `B` are independent â€” neither can be built from the other.
- **Mental Model** â€” A duplicate tool in your toolbox. If you have a hammer and a mallet that do the same job, one is redundant. Dependent vectors are "redundant directions."
- **AI Connection** â€” PCA identifies and removes dependent/redundant directions in data. If two features are perfectly correlated (one is a linear combination of the other), PCA will collapse them into a single direction, compressing the representation.

**In plain English:** If you can build vector C by combining vectors A and B, then C doesn't teach you anything new. It's just A and B in disguise.

### 19. Basis Vectors

- **Meaning** â€” A basis is the minimum set of independent vectors that spans an entire space. Every vector in the space can be uniquely expressed as a linear combination of basis vectors, and no basis vector is redundant.
- **Why It Exists** â€” A basis answers: "What's the smallest toolkit I need to represent everything?" It's the most efficient description of a space â€” no gaps (spans everything) and no waste (nothing redundant).
- **Formula** â€” For n-dimensional space, a basis has exactly n vectors. Standard basis for 2D: `{(1,0), (0,1)}`. Standard basis for 3D: `{(1,0,0), (0,1,0), (0,0,1)}`.
- **Example** â€” In 2D, `{(1,0), (0,1)}` is a basis: any point `(a,b) = a(1,0) + b(0,1)`. But `{(1,0), (2,0)}` is NOT a basis for 2D because both vectors point along the x-axis â€” they can't reach any y-direction.
- **Mental Model** â€” The smallest set of LEGO building blocks that can construct anything in the space. You need exactly enough â€” too few and you can't build everything, too many and some are redundant.
- **AI Connection** â€” Each dimension of an embedding space corresponds to a learned basis direction. A 768-dimensional embedding has 768 basis directions, each capturing some aspect of meaning. The quality of these learned directions determines how well the model understands language.

### 20. Change of Basis

- **Meaning** â€” Change of basis means expressing the same vector using a different coordinate system. The vector itself doesn't change â€” only how we describe it changes, like translating a sentence from English to Hindi.
- **Why It Exists** â€” Some coordinate systems reveal structure better than others. Data that looks random in the standard basis might show clear patterns in a better-chosen basis. Choosing the right basis simplifies problems dramatically.
- **Example** â€” Vector `(3, 4)` in the standard basis `{(1,0), (0,1)}` could also be written as `(5, 0)` in a rotated basis that aligns with the vector's direction. Same arrow, different description.
- **Mental Model** â€” Changing language. The Taj Mahal is the same building whether you describe it in English, Hindi, or French. The thing is unchanged; only the description system changes.
- **AI Connection** â€” PCA is fundamentally a change-of-basis operation. It finds a new coordinate system where the first axis captures the most variance, the second captures the next most, and so on. This reveals the hidden structure in data that the original coordinates obscured.

### 21. Orthogonal Basis

- **Meaning** â€” An orthogonal basis is one where all basis vectors are perpendicular to each other (pairwise dot product = 0). An orthonormal basis goes further: orthogonal AND each vector has unit length.
- **Why It Exists** â€” Orthogonal bases are the "cleanest" possible descriptions of a space. Each basis direction captures completely independent information with zero overlap. This makes computation simpler and representations more interpretable.
- **Formula** â€” For basis vectors eâ‚, eâ‚‚, ..., eâ‚™: `eáµ¢ Â· eâ±¼ = 0` for all i â‰  j (orthogonal). Additionally `|eáµ¢| = 1` for all i (orthonormal).
- **Example** â€” The standard basis `{(1,0), (0,1)}` is orthonormal: the vectors are perpendicular and each has length 1. The basis `{(1,1), (1,-1)}` is orthogonal (dot product = 0) but not orthonormal (each has length âˆš2).
- **Mental Model** â€” Think of perfectly independent building blocks with zero overlap. North, East, and Up are orthogonal â€” moving North tells you absolutely nothing about your East or Up position.
- **AI Connection** â€” PCA produces orthogonal principal components, ensuring each captured direction is completely independent. Well-designed latent spaces (like those in VAEs) aim for orthogonal dimensions so each slider controls a single independent attribute.

**In plain English:** An orthogonal basis gives you the cleanest possible set of independent directions. Each direction captures unique information that no other direction duplicates.

---

## Quick Reference Tables

### Table 1 â€” Core Concepts Overview

| # | Concept | Core Question | Key Idea | AI Connection |
| - | ------- | ------------- | -------- | ------------- |
| 1 | Coordinate Space | Where is something? | Numerical address in space | Embeddings are positions in meaning-space |
| 2 | Vectors as Arrows | How do I move? | Direction + magnitude | Directional meaning vectors |
| 3 | Plotting Vectors | How do I visualize? | Arrow from tail to head | PCA, t-SNE, UMAP visualization |
| 4 | Magnitude | How strong is a vector? | Vector length via Pythagorean theorem | Activation strength, confidence |
| 5 | Unit Vector | What if only direction matters? | Normalize to length = 1 | Embedding normalization before comparison |
| 6 | Zero Vector | What if nothing happens? | No direction, no magnitude | Empty/inactive/padding representation |
| 7 | Vector Addition | How do movements combine? | Add coordinates element-wise | Residual connections in Transformers |
| 8 | Vector Subtraction | What's the difference? | Subtract coordinates | Embedding arithmetic, gradient = error |
| 9 | Scalar Multiplication | How do I adjust intensity? | Multiply all coordinates by k | Neural network weights |
| 10 | Dot Product | How similar are two vectors? | Multiply-and-sum coordinates | Attention scores, semantic search |
| 11 | Orthogonal Vectors | Are directions independent? | Dot product = 0 | Independent features, no redundancy |
| 12 | Norms | How do we measure size? | Function assigning size to vectors | Loss functions, distance metrics |
| 13 | Euclidean Norm (L2) | Straight-line distance? | âˆš(sum of squares) | KNN, clustering, MSE loss |
| 14 | Manhattan Distance (L1) | Grid distance? | Sum of absolute values | Lasso regularization, robust distance |
| 15 | p-Norms | Can distance be generalized? | Family parameterized by p | Tunable loss/regularization |
| 16 | Linear Combinations | How do we build new vectors? | Scale and add existing vectors | Every neuron computes one |
| 17 | Span | What can these vectors reach? | All possible linear combinations | Model's representable concept space |
| 18 | Linear Dependence | Is a vector redundant? | Can be built from others | Feature redundancy, PCA compression |
| 19 | Basis | What's the minimum building set? | Smallest independent spanning set | Embedding dimensions |
| 20 | Change of Basis | Better coordinate system? | Same vector, new description | PCA finds a better basis |
| 21 | Orthogonal Basis | Cleanest possible basis? | All perpendicular, zero overlap | PCA components, clean latent spaces |

---

### Table 2 — Formula Cheat Sheet

| Topic | Formula | What It Computes |
| ----- | ------- | ---------------- |
| Magnitude (2D) | `|v| = √(x² + y²)` | Vector length |
| Magnitude (3D) | `|v| = √(x² + y² + z²)` | 3D vector length |
| Unit Vector | `v̂ = v / |v|` | Normalize to length 1 |
| Vector Addition | `(a,b) + (c,d) = (a+c, b+d)` | Combine two vectors |
| Vector Subtraction | `(a,b) - (c,d) = (a-c, b-d)` | Difference between vectors |
| Scalar Multiplication | `k(x,y) = (kx, ky)` | Scale a vector |
| Dot Product (Algebraic) | `A·B = x₁x₂ + y₁y₂` | Similarity measure |
| Dot Product (Geometric) | `A·B = |A||B|cosθ` | Angle relationship |
| Orthogonal Test | `A·B = 0` | Confirms perpendicularity |
| Manhattan Distance (L1) | `|x₁| + |x₂| + ... + |xₙ|` | Grid-walk distance |
| Euclidean Distance (L2) | `√(x₁² + x₂² + ... + xₙ²)` | Straight-line distance |
| p-Norm | `(Σ|xᵢ|ᵖ)^(1/p)` | Generalized distance |
| Linear Combination | `c₁A + c₂B + ...` | Build new vector from existing |

---

### Table 3 — AI Translation Table

| Math Concept | AI Interpretation | Specific Example |
| ------------ | ----------------- | ---------------- |
| Coordinate | Position in embedding space | Word "cat" → coordinates in 1536D space |
| Vector | Embedding | A sentence embedding from OpenAI |
| Magnitude | Confidence / activation strength | High magnitude = strong signal |
| Unit Vector | Pure semantic direction | Normalized embedding for cosine similarity |
| Zero Vector | Empty / inactive representation | Padding token embedding |
| Vector Addition | Feature combination | ResNet skip connection: `output = F(x) + x` |
| Vector Subtraction | Relationship extraction | `king - man + woman ≈ queen` |
| Scalar Multiplication | Weight application | Network weight × input feature |
| Dot Product | Similarity score | Attention: `score = Q · K` |
| Orthogonal Vectors | Independent features | Uncorrelated PCA components |
| Euclidean Distance | Dissimilarity measure | KNN finds closest training examples |
| Manhattan Distance | Robust dissimilarity | Lasso pushes weights to exactly 0 |
| Linear Combination | Neuron computation | `w₁x₁ + w₂x₂ + ... + bias` |
| Span | Model's concept coverage | What the embedding space can represent |
| Linear Dependence | Redundant information | Correlated features = wasted capacity |
| Basis | Fundamental learned directions | 768 dimensions in BERT = 768 basis directions |
| Change of Basis | Better representation | PCA rotates data to reveal structure |
| Orthogonal Basis | Efficient latent space | VAE dimensions controlling independent attributes |

---

### Table 4 — Mental Models Summary

| Concept | Mental Model | Why It Helps |
| ------- | ------------ | ------------ |
| Coordinate | Postal address | Gives exact location |
| Vector | Arrow with direction + length | Captures movement/relationship |
| Magnitude | Length of the arrow | "How much" independent of direction |
| Unit Vector | Compass needle | Pure direction, no distance |
| Zero Vector | Standing still | No contribution |
| Addition | Walking two journey legs | Combining movements |
| Subtraction | Gap between two points | "What's needed to get from A to B" |
| Scalar Multiplication | Volume knob | Louder/quieter without changing station |
| Dot Product | Shadow cast by flashlight | How much one aligns with another |
| Orthogonal | North vs East | Completely independent |
| L2 Norm | Crow flying straight | Shortest path |
| L1 Norm | Taxi on grid streets | Restricted path |
| Linear Combination | Mixing paint colors | Blend existing things into new |
| Span | Reachable world | Everything you can build |
| Dependence | Duplicate tool in toolbox | Adds nothing new |
| Basis | Minimum LEGO set | Smallest kit to build everything |
| Change of Basis | Translating languages | Same meaning, different words |
| Orthogonal Basis | Independent building blocks | Zero overlap between blocks |

---

### Table 5 — Most Important Takeaways (Ranked)

| Rank | Insight |
| ---- | ------- |
| 1 | AI represents all meaning using vectors (embeddings) |
| 2 | Similar meanings have similar vector directions |
| 3 | Dot product is the fundamental similarity operation in AI |
| 4 | Every neuron computes a linear combination |
| 5 | Norms measure size/distance — choice matters for ML |
| 6 | Span defines what a model can possibly represent |
| 7 | Dependence means wasted capacity — redundant features |
| 8 | Basis gives the minimum building blocks for a space |
| 9 | Change of basis (PCA) reveals hidden data structure |
| 10 | Orthogonal bases create the cleanest, most efficient representations |
| 11 | Modern AI is largely geometry in high-dimensional vector spaces |


---

## Memory Map

```text
Coordinates (Where things are)
      ↓
Vectors (Direction + Magnitude)
      ↓
Vector Operations
  ├── Addition (Combine)
  ├── Subtraction (Difference)
  └── Scalar Multiplication (Scale)
      ↓
Similarity & Direction
  ├── Dot Product (How similar?)
  └── Orthogonality (Completely independent?)
      ↓
Distance & Size
  ├── L2 Norm (Straight line)
  ├── L1 Norm (Grid walk)
  └── p-Norm (Generalized)
      ↓
Building Spaces
  ├── Linear Combinations (Mix vectors)
  ├── Span (Reachable world)
  └── Linear Dependence (Redundancy check)
      ↓
Efficient Representations
  ├── Basis (Minimum building blocks)
  ├── Change of Basis (Better coordinates)
  └── Orthogonal Basis (Cleanest representation)
      ↓
AI Applications
  ├── Embeddings (vectors representing meaning)
  ├── PCA (finding better basis)
  ├── Attention (dot product similarity)
  └── Neural Networks (linear combinations + activation)
```

---

## Interview / Revision Summary

| Concept | Remember This |
| ------- | ------------- |
| Vector | Direction + magnitude; AI calls them embeddings |
| Magnitude | Vector length = √(sum of squares) |
| Unit Vector | Normalize to length 1; strips away magnitude, keeps direction |
| Dot Product | Multiply-and-sum = similarity score; powers attention and search |
| Orthogonal | Dot product = 0 means completely independent directions |
| L2 Norm | Straight-line distance; most common in ML |
| L1 Norm | Grid distance; promotes sparsity, robust to outliers |
| Linear Combination | Scale + add = every neuron's computation |
| Span | All vectors reachable from a set = model's representable world |
| Linear Dependence | Redundant = can be built from others = wasted capacity |
| Basis | Minimum independent vectors spanning the whole space |
| Change of Basis | Same vectors described in better coordinates (PCA) |
| Orthogonal Basis | Cleanest possible basis: zero redundancy between directions |
| The Big Picture | Modern AI is geometry in high-dimensional vector spaces |

---

### If Someone Asks: "What role does Linear Algebra play in AI?"

> Linear Algebra provides the mathematical foundation for how AI represents and processes information. Everything in modern AI — words, images, users, products — gets converted into vectors called embeddings that live in high-dimensional spaces. Neural networks transform these vectors through matrix multiplications (which are just organized linear combinations). The dot product measures similarity between vectors, which is how attention mechanisms in Transformers decide what to focus on. Concepts like span and basis determine what a model can represent, while orthogonality ensures efficiency with minimal redundancy. Techniques like PCA use change-of-basis to find better coordinate systems that reveal hidden patterns. In essence, AI "thinks" in vectors and "acts" through linear transformations.
