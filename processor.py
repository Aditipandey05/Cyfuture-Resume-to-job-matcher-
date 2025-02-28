import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple, List, Dict

class TextProcessor:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_md")
        
    def preprocess_text(self, text: str) -> spacy.tokens.Doc:
        """
        Preprocess text using spaCy pipeline
        """
        # Process the text through spaCy pipeline
        doc = self.nlp(text.lower())
        
        # Remove stopwords and punctuation
        return doc

    def get_text_vector(self, doc: spacy.tokens.Doc) -> np.ndarray:
        """
        Get vector representation of text
        """
        return doc.vector

    def calculate_similarity(self, resume_doc: spacy.tokens.Doc, 
                           job_doc: spacy.tokens.Doc) -> float:
        """
        Calculate cosine similarity between resume and job description
        """
        resume_vector = self.get_text_vector(resume_doc)
        job_vector = self.get_text_vector(job_doc)
        
        # Reshape vectors for cosine_similarity
        resume_vector = resume_vector.reshape(1, -1)
        job_vector = job_vector.reshape(1, -1)
        
        return float(cosine_similarity(resume_vector, job_vector)[0][0])

    def get_key_terms(self, doc: spacy.tokens.Doc) -> List[str]:
        """
        Extract key terms from text
        """
        return [token.text for token in doc 
                if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN', 'VERB']]

    def analyze_match(self, resume_doc: spacy.tokens.Doc, 
                     job_doc: spacy.tokens.Doc) -> Dict[str, any]:
        """
        Analyze the match between resume and job description
        """
        # Get similarity score
        similarity = self.calculate_similarity(resume_doc, job_doc)
        
        # Get key terms from both documents
        resume_terms = set(self.get_key_terms(resume_doc))
        job_terms = set(self.get_key_terms(job_doc))
        
        # Find matching terms
        matching_terms = resume_terms.intersection(job_terms)
        missing_terms = job_terms - resume_terms

        return {
            'similarity_score': similarity,
            'matching_terms': list(matching_terms),
            'missing_terms': list(missing_terms)
        }
