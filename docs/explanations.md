# Mandatory Explanations

## Chunk Size Choice
We chose a chunk size of 500 tokens. This size balances the need for enough context for the LLM to answer questions accurately, while keeping retrieval granular enough to avoid irrelevant information. Too small chunks lose context; too large chunks reduce retrieval precision.

## Retrieval Failure Case
One observed failure case: when a user asks a question that is semantically related but uses very different vocabulary from the document, the retrieval step may not surface the most relevant chunk, leading to poor answers.

## Metric Tracked
We track retrieval latency (time from query to answer) and similarity score (cosine similarity between query and top chunk). These help us monitor system responsiveness and retrieval quality.
