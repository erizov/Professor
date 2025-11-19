# NER (Named Entity Recognition)

1. **Name of Algorithm**  
   NER (Named Entity Recognition)

2. **What problem does it solve? (1 sentence)**  
   Identifies and classifies named entities (persons, organizations, locations, dates, etc.) in text, enabling information extraction and structured data from unstructured text.

3. **Intuition (plain-language explanation)**  
Like highlighting important names in a document: automatically find and label people, places, companies, dates, etc. so you can extract structured information from text.

4. **Inputs & Outputs**  
   - Input: Text sequences, entity labels (PERSON, ORG, LOC, DATE, etc.), training data with entity annotations.  
   - Output: Tagged text with entity spans and their types (e.g., 'John Smith' → PERSON, 'New York' → LOCATION).

5. **Step-by-step description (5–10 lines max)**  
1. Tokenize input text into words or subwords.
2. Apply sequence labeling model (CRF, BiLSTM-CRF, or Transformer-based).
3. For each token, predict BIO tags: B-PERSON (beginning), I-PERSON (inside), O (outside entity).
4. Use contextual embeddings (BERT, ELMo) to capture word context.
5. Apply CRF layer to enforce valid tag sequences (B must precede I).
6. Extract entity spans from predicted tags and assign entity types.

6. **Tiny example (hand-simulated)**  
   Input: 'Apple Inc. was founded by Steve Jobs in Cupertino, California in 1976.' → Output: [Apple Inc. → ORG], [Steve Jobs → PERSON], [Cupertino, California → LOCATION], [1976 → DATE].

7. **Time & Space Complexity**  
   - Time: O(n·d·l) where n is sequence length, d is embedding dimension, l is number of layers (linear in sequence length).  
   - Space: O(n·d) for embeddings and O(n·c) for tag predictions where c is number of entity classes.

8. **Strengths**  
- Enables structured information extraction from unstructured text.
- Widely used in information retrieval and knowledge graphs.

9. **Weaknesses / limitations**  
- Requires labeled training data (expensive to create).
- May struggle with ambiguous entities or domain-specific terms.

10. **Compare with alternatives**  
    Alternatives: Rule-based NER, Dictionary-based NER, SpaCy NER, BERT-based NER

11. **30-second explanation (your own words)**  
    Identifies and classifies named entities in text using sequence labeling models, extracting structured information like person names, locations, and organizations from unstructured text.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
