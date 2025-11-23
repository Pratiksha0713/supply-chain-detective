"""
Scoring System Module

Evaluates player performance based on correctness, time taken,
and hints used to calculate final mission score.
"""

# Scoring constants
BASE_SCORE_CORRECT = 100
BASE_SCORE_WRONG = 0
TIME_PENALTY_PER_SECOND = 0.1
HINT_PENALTY_PER_HINT = 10


def score_submission(user_guess, correct_cause, time_taken, hints_used):
    """
    Score a user's mission submission based on correctness, time, and hints used.
    
    Scoring Rules:
    - Correct answer: 100 points
    - Wrong answer: 0 points
    - Time penalty: -0.1 points per second
    - Hint penalty: -10 points per hint used
    
    Args:
        user_guess (str): User's guessed root cause
        correct_cause (str): Correct root cause answer
        time_taken (int/float): Time taken in seconds
        hints_used (int): Number of hints used
        
    Returns:
        tuple: (final_score, breakdown_dict)
            - final_score (float): The calculated final score (minimum 0)
            - breakdown_dict (dict): Detailed breakdown of score components
    """
    # Check if answer is correct
    is_correct = check_answer(user_guess, correct_cause)
    
    # Calculate base score
    base_score = BASE_SCORE_CORRECT if is_correct else BASE_SCORE_WRONG
    
    # Calculate penalties
    time_penalty = calculate_time_penalty(time_taken)
    hint_penalty = calculate_hint_penalty(hints_used)
    
    # Calculate final score (cannot go below 0)
    final_score = max(0, base_score - time_penalty - hint_penalty)
    
    # Create breakdown dictionary
    breakdown = {
        "correct": is_correct,
        "base_score": base_score,
        "time_taken": time_taken,
        "time_penalty": time_penalty,
        "hints_used": hints_used,
        "hint_penalty": hint_penalty,
        "total_penalties": time_penalty + hint_penalty,
        "final_score": final_score,
        "performance_rating": get_performance_rating(final_score)
    }
    
    return final_score, breakdown


def check_answer(submitted_answer, correct_answer):
    """
    Check if submitted answer matches correct answer.
    
    Args:
        submitted_answer (str): User's submitted answer
        correct_answer (str): Correct answer
        
    Returns:
        bool: True if answers match (case-insensitive), False otherwise
    """
    if not submitted_answer or not correct_answer:
        return False
    
    return submitted_answer.lower().strip() == correct_answer.lower().strip()


def calculate_time_penalty(time_taken):
    """
    Calculate penalty based on time taken to solve.
    
    Args:
        time_taken (int/float): Time taken in seconds
        
    Returns:
        float: Time penalty amount
    """
    return time_taken * TIME_PENALTY_PER_SECOND


def calculate_hint_penalty(hints_used):
    """
    Calculate penalty based on number of hints used.
    
    Args:
        hints_used (int): Number of hints used
        
    Returns:
        int: Hint penalty amount
    """
    return hints_used * HINT_PENALTY_PER_HINT


def calculate_final_score(correctness, time_taken, hints_used):
    """
    Calculate final mission score from all factors.
    
    Args:
        correctness (bool): Whether answer was correct
        time_taken (int/float): Time taken in seconds
        hints_used (int): Number of hints used
        
    Returns:
        float: Final calculated score (minimum 0)
    """
    base_score = BASE_SCORE_CORRECT if correctness else BASE_SCORE_WRONG
    time_penalty = calculate_time_penalty(time_taken)
    hint_penalty = calculate_hint_penalty(hints_used)
    
    return max(0, base_score - time_penalty - hint_penalty)


def get_score_breakdown(correctness, time_taken, hints_used):
    """
    Get detailed breakdown of score components.
    
    Args:
        correctness (bool): Whether answer was correct
        time_taken (int/float): Time taken in seconds
        hints_used (int): Number of hints used
        
    Returns:
        dict: Breakdown of all score components
    """
    base_score = BASE_SCORE_CORRECT if correctness else BASE_SCORE_WRONG
    time_penalty = calculate_time_penalty(time_taken)
    hint_penalty = calculate_hint_penalty(hints_used)
    final_score = max(0, base_score - time_penalty - hint_penalty)
    
    return {
        "correct": correctness,
        "base_score": base_score,
        "time_taken": time_taken,
        "time_penalty": time_penalty,
        "hints_used": hints_used,
        "hint_penalty": hint_penalty,
        "total_penalties": time_penalty + hint_penalty,
        "final_score": final_score,
        "performance_rating": get_performance_rating(final_score)
    }


def get_performance_rating(score):
    """
    Get performance rating based on final score.
    
    Args:
        score (float): Final score
        
    Returns:
        str: Performance rating category
    """
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Great"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    elif score > 0:
        return "Poor"
    else:
        return "Incorrect"


def get_performance_feedback(score):
    """
    Get performance feedback message based on score.
    
    Args:
        score (float): Final score
        
    Returns:
        str: Feedback message
    """
    if score >= 90:
        return "Outstanding work! You're a master supply chain detective!"
    elif score >= 75:
        return "Great job! You identified the root cause quickly and efficiently."
    elif score >= 60:
        return "Good work! You found the answer, but there's room for improvement."
    elif score >= 40:
        return "Fair effort. Try using fewer hints and working faster next time."
    elif score > 0:
        return "You found the answer, but took too long or used too many hints."
    else:
        return "Incorrect answer. Review the data and try again!"


def format_score_report(breakdown):
    """
    Format a detailed score report from breakdown data.
    
    Args:
        breakdown (dict): Score breakdown dictionary
        
    Returns:
        str: Formatted score report
    """
    report = [
        "=" * 50,
        "MISSION SCORE REPORT",
        "=" * 50,
        f"Answer: {'CORRECT' if breakdown['correct'] else 'INCORRECT'}",
        f"Base Score: {breakdown['base_score']} points",
        "",
        "Penalties:",
        f"  Time taken: {breakdown['time_taken']:.1f}s (-{breakdown['time_penalty']:.1f} points)",
        f"  Hints used: {breakdown['hints_used']} (-{breakdown['hint_penalty']} points)",
        f"  Total penalties: -{breakdown['total_penalties']:.1f} points",
        "",
        f"FINAL SCORE: {breakdown['final_score']:.1f} / 100",
        f"Rating: {breakdown['performance_rating']}",
        "",
        f"Feedback: {get_performance_feedback(breakdown['final_score'])}",
        "=" * 50
    ]
    
    return "\n".join(report)

