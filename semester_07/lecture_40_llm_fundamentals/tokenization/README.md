# Tokenization

1. **Name of Algorithm**  
   Tokenization

2. **What problem does it solve? (1 sentence)**  
Converts raw text into discrete tokens (subwords, words, or characters) that can be processed by language models, enabling efficient representation and handling of vocabulary limitations.

3. **Intuition (plain-language explanation)**  
   Like breaking a sentence into building blocks: tokenization splits text into smaller pieces (tokens) - instead of storing every possible word (huge vocabulary), it breaks words into subword pieces (like 'un-happy', 'play-ing') that can be recombined, making the vocabulary manageable.

4. **Inputs & Outputs**  
   - Input: Raw text string, tokenizer (BPE, WordPiece, SentencePiece), vocabulary, special tokens.  
   - Output: List of token IDs, token-to-text mapping, attention masks, special token markers.

5. **Step-by-step description (5–10 lines max)**  
1. Normalize text: lowercase, remove extra spaces, handle Unicode (optional, depends on tokenizer).
2. Split into subwords: apply tokenization algorithm (BPE: merge frequent pairs, WordPiece: split by subword units, SentencePiece: learn optimal splits).
3. Map to IDs: convert tokens to integer IDs using vocabulary dictionary.
4. Add special tokens: prepend/append special tokens (BOS, EOS, SEP, PAD, etc.) as needed.
5. Handle unknown: map out-of-vocabulary words to UNK token or split into subwords.
6. Truncate/pad: truncate to max length or pad to fixed length for batching.
7. Create masks: generate attention masks to ignore padding tokens.
8. Return tokenized: output token IDs, attention masks, and token-to-text mapping.

6. **Tiny example (hand-simulated)**  
   Text: 'Hello world!' → BPE tokenizer → ['Hello', 'Ġworld', '!'] → vocabulary lookup → [15496, 1917, 0] → add special tokens → [50256, 15496, 1917, 0, 50256] (BOS, Hello, world, !, EOS) → pad to length 10 → [50256, 15496, 1917, 0, 50256, 50256, 50256, 50256, 50256, 50256].

7. **Time & Space Complexity**  
   - Time: O(n) where n is text length (linear scan and dictionary lookups), O(v) for vocabulary operations where v is vocabulary size.  
   - Space: O(v) for vocabulary storage, O(t) for tokenized output where t is number of tokens (typically 1-2 tokens per word).

8. **Strengths**  
- Handles OOV: subword tokenization handles out-of-vocabulary words.
- Efficient: smaller vocabulary than word-level, fewer parameters.
- Language agnostic: works across languages with appropriate tokenizers.

9. **Weaknesses / limitations**  
- Information loss: splitting words may lose some semantic information.
- Tokenization artifacts: model must learn to handle subword boundaries.
- Length variation: same word may tokenize differently in different contexts.

10. **Compare with alternatives**  
    Alternatives: Character-level, Word-level, Byte-level, Sentence-level

11. **30-second explanation (your own words)**  
Converts raw text into discrete tokens using subword tokenization algorithms, enabling efficient representation and handling of vocabulary limitations while preserving semantic information.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
