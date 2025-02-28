def format_percentage(value: float) -> str:
    """
    Format float as percentage string
    """
    return f"{value * 100:.1f}%"

def get_match_feedback(score: float) -> str:
    """
    Get feedback based on match score
    """
    if score >= 0.8:
        return "Excellent Match! Your profile strongly aligns with the job requirements."
    elif score >= 0.6:
        return "Good Match! Your profile matches many of the job requirements."
    elif score >= 0.4:
        return "Fair Match. Consider highlighting more relevant skills and experience."
    else:
        return "Low Match. This position might not be the best fit for your current profile."

def create_match_explanation(matching_terms: list, missing_terms: list) -> str:
    """
    Create explanation text for matching and missing terms
    """
    explanation = []
    
    if matching_terms:
        explanation.append("Matching skills and keywords:\n- " + "\n- ".join(matching_terms[:10]))
    
    if missing_terms:
        explanation.append("\nConsider adding these skills to your resume:\n- " + 
                         "\n- ".join(missing_terms[:10]))
    
    return "\n".join(explanation)
