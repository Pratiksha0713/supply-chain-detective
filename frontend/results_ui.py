"""
Results UI Module

Results screen displaying correctness, explanation, score breakdown,
and option to proceed to next mission.
"""

import streamlit as st
import plotly.graph_objects as go
import sys
sys.path.append('frontend')

from components import kpi_card, render_info_box, submit_button


def render_results(final_score, user_guess, correct_cause, score_breakdown):
    """
    Render complete results screen with score, breakdown, and next steps.
    
    Args:
        final_score (float): The calculated final score
        user_guess (str): User's submitted guess for root cause
        correct_cause (str): The correct root cause answer
        score_breakdown (dict): Detailed breakdown of score components
            - correct (bool): Whether answer was correct
            - base_score (int): Starting score
            - time_taken (float): Time in seconds
            - time_penalty (float): Penalty from time
            - hints_used (int): Number of hints used
            - hint_penalty (int): Penalty from hints
            - total_penalties (float): Sum of all penalties
            - final_score (float): Final calculated score
            - performance_rating (str): Rating category
    
    Returns:
        bool: True if user clicks "Next Mission" button
    """
    # Determine if user passed or failed
    is_correct = score_breakdown.get('correct', False)
    
    # Render pass/fail indicator
    render_result_header(is_correct, final_score)
    
    st.markdown("---")
    
    # Show answer comparison
    render_explanation(correct_cause, user_guess, is_correct)
    
    st.markdown("---")
    
    # Show score breakdown metrics
    st.markdown("### 📊 Score Breakdown")
    render_score_breakdown_metrics(score_breakdown)
    
    st.markdown("---")
    
    # Detailed breakdown table
    render_score_breakdown_detailed(score_breakdown)
    
    st.markdown("---")
    
    # Performance visualization
    render_performance_chart(score_breakdown)
    
    st.markdown("---")
    
    # Next mission button
    next_mission_clicked = render_next_mission_button()
    
    return next_mission_clicked


def render_result_header(is_correct, final_score):
    """
    Render success/failure header with visual indicator.
    
    Args:
        is_correct (bool): Whether the answer was correct
        final_score (float): The final score achieved
    """
    if is_correct:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            ">
                <h1 style="
                    color: white;
                    margin: 0;
                    font-size: 48px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                ">🎉 Mission Complete! 🎉</h1>
                <p style="
                    color: white;
                    margin: 15px 0 0 0;
                    font-size: 24px;
                    opacity: 0.9;
                ">Congratulations, Detective!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show balloons for success
        st.balloons()
        
    else:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            ">
                <h1 style="
                    color: white;
                    margin: 0;
                    font-size: 48px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                ">❌ Incorrect Answer</h1>
                <p style="
                    color: white;
                    margin: 15px 0 0 0;
                    font-size: 24px;
                    opacity: 0.9;
                ">Keep investigating, Detective!</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display final score prominently
    st.markdown(f"""
        <div style="text-align: center; margin: 30px 0;">
            <h2 style="color: #333; margin: 0;">Final Score</h2>
            <p style="
                font-size: 72px;
                font-weight: bold;
                color: {'#28a745' if final_score >= 70 else '#ffc107' if final_score >= 40 else '#dc3545'};
                margin: 10px 0;
            ">{final_score:.1f}</p>
            <p style="color: #666; font-size: 18px;">out of 100</p>
        </div>
    """, unsafe_allow_html=True)


def render_explanation(correct_answer, submitted_answer, is_correct):
    """
    Render explanation of correct answer and comparison with user's answer.
    
    Args:
        correct_answer (str): The correct root cause
        submitted_answer (str): User's submitted answer
        is_correct (bool): Whether answer was correct
    """
    st.markdown("### 🎯 Answer Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Your Answer")
        if is_correct:
            render_info_box(f"✅ {submitted_answer}", type="success")
        else:
            render_info_box(f"❌ {submitted_answer}", type="error")
    
    with col2:
        st.markdown("#### Correct Answer")
        render_info_box(f"✓ {correct_answer}", type="success")
    
    if not is_correct:
        st.info("💡 Review the data and insights to understand the correct root cause. Try again to improve your detective skills!")


def render_score_breakdown_metrics(score_breakdown):
    """
    Render score breakdown as KPI cards.
    
    Args:
        score_breakdown (dict): Score breakdown details
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card("Base Score", f"{score_breakdown.get('base_score', 0)}")
    
    with col2:
        time_taken = score_breakdown.get('time_taken', 0)
        kpi_card("Time Taken", f"{time_taken:.0f}s")
    
    with col3:
        hints_used = score_breakdown.get('hints_used', 0)
        kpi_card("Hints Used", f"{hints_used}")
    
    with col4:
        rating = score_breakdown.get('performance_rating', 'N/A')
        kpi_card("Rating", rating)


def render_score_breakdown_detailed(score_breakdown):
    """
    Render detailed score breakdown table.
    
    Args:
        score_breakdown (dict): Score breakdown details
    """
    st.markdown("### 📋 Detailed Breakdown")
    
    # Create breakdown table
    st.markdown("""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        ">
    """, unsafe_allow_html=True)
    
    # Base score
    base_score = score_breakdown.get('base_score', 0)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
            <span style="font-weight: bold;">Base Score (Answer Correctness)</span>
            <span style="color: #28a745; font-weight: bold;">+{base_score} points</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Time penalty
    time_penalty = score_breakdown.get('time_penalty', 0)
    time_taken = score_breakdown.get('time_taken', 0)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
            <span>Time Penalty ({time_taken:.0f} seconds × 0.1)</span>
            <span style="color: #dc3545; font-weight: bold;">-{time_penalty:.1f} points</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Hint penalty
    hint_penalty = score_breakdown.get('hint_penalty', 0)
    hints_used = score_breakdown.get('hints_used', 0)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
            <span>Hint Penalty ({hints_used} hints × 10)</span>
            <span style="color: #dc3545; font-weight: bold;">-{hint_penalty} points</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Total penalties
    total_penalties = score_breakdown.get('total_penalties', 0)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 2px solid #333;">
            <span style="font-weight: bold;">Total Penalties</span>
            <span style="color: #dc3545; font-weight: bold;">-{total_penalties:.1f} points</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Final score
    final_score = score_breakdown.get('final_score', 0)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 15px; background-color: #f8f9fa;">
            <span style="font-weight: bold; font-size: 18px;">FINAL SCORE</span>
            <span style="font-weight: bold; font-size: 18px; color: {'#28a745' if final_score >= 70 else '#ffc107' if final_score >= 40 else '#dc3545'};">{final_score:.1f} points</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_performance_metrics(time_taken, hints_used):
    """
    Render performance metrics summary.
    
    Args:
        time_taken (float): Time taken in seconds
        hints_used (int): Number of hints used
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("⏱️ Time Taken", f"{time_taken:.0f} seconds")
    
    with col2:
        st.metric("💡 Hints Used", hints_used)


def render_performance_chart(score_breakdown):
    """
    Render visual chart showing score composition.
    
    Args:
        score_breakdown (dict): Score breakdown details
    """
    st.markdown("### 📈 Score Composition")
    
    base_score = score_breakdown.get('base_score', 0)
    time_penalty = score_breakdown.get('time_penalty', 0)
    hint_penalty = score_breakdown.get('hint_penalty', 0)
    final_score = score_breakdown.get('final_score', 0)
    
    # Create waterfall chart
    fig = go.Figure(go.Waterfall(
        name = "Score Breakdown",
        orientation = "v",
        measure = ["absolute", "relative", "relative", "total"],
        x = ["Base Score", "Time Penalty", "Hint Penalty", "Final Score"],
        y = [base_score, -time_penalty, -hint_penalty, final_score],
        text = [f"+{base_score}", f"-{time_penalty:.1f}", f"-{hint_penalty}", f"{final_score:.1f}"],
        textposition = "outside",
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#dc3545"}},
        increasing = {"marker":{"color":"#28a745"}},
        totals = {"marker":{"color":"#667eea"}}
    ))
    
    fig.update_layout(
        title = "How Your Score Was Calculated",
        showlegend = False,
        height = 400,
        yaxis = dict(title="Points"),
        margin = dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance insights
    performance_rating = score_breakdown.get('performance_rating', '')
    
    if performance_rating == 'Excellent':
        st.success("🌟 Outstanding performance! You're a master supply chain detective!")
    elif performance_rating == 'Great':
        st.success("👏 Great job! You solved the case efficiently.")
    elif performance_rating == 'Good':
        st.info("👍 Good work! There's room for improvement in speed or hint usage.")
    elif performance_rating == 'Fair':
        st.warning("💪 Fair effort. Try to work faster and use fewer hints next time.")
    elif performance_rating == 'Poor':
        st.warning("📚 You found the answer, but consider improving your efficiency.")
    else:
        st.error("🔍 Keep practicing! Review the data carefully and try again.")


def render_next_mission_button():
    """
    Render button to proceed to next mission.
    
    Returns:
        bool: True if button is clicked, False otherwise
    """
    st.markdown("### 🚀 Ready for Your Next Mission?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        next_clicked = submit_button("🎯 Next Mission")
    
    if next_clicked:
        return True
    
    # Also add a replay option
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Try This Mission Again", use_container_width=True):
            st.session_state['retry_mission'] = True
            return False
    
    with col2:
        if st.button("🏠 Return to Dashboard", use_container_width=True):
            st.session_state['return_to_dashboard'] = True
            return False
    
    return False


def render_results_screen(is_correct, score, score_details):
    """
    Render complete results screen (legacy wrapper).
    
    Args:
        is_correct (bool): Whether answer was correct
        score (float): Final score
        score_details (dict): Score breakdown
        
    Returns:
        bool: True if user clicks "Next Mission" button
    """
    # Create a compatible score_breakdown from score_details
    score_breakdown = {
        'correct': is_correct,
        'base_score': score_details.get('base_score', 100 if is_correct else 0),
        'time_taken': score_details.get('time_taken', 0),
        'time_penalty': score_details.get('time_penalty', 0),
        'hints_used': score_details.get('hints_used', 0),
        'hint_penalty': score_details.get('hint_penalty', 0),
        'total_penalties': score_details.get('total_penalties', 0),
        'final_score': score,
        'performance_rating': score_details.get('performance_rating', 'N/A')
    }
    
    user_guess = score_details.get('user_guess', 'N/A')
    correct_cause = score_details.get('correct_cause', 'N/A')
    
    return render_results(score, user_guess, correct_cause, score_breakdown)

