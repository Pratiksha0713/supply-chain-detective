"""
Missions Module

Manages mission configurations, scenarios, and correct answers
for the Supply Chain Detective game.
"""

MISSIONS = [
    {
        "id": 1,
        "title": "The Mystery of Late Deliveries",
        "description": """
            Your company has been experiencing an unusual spike in delivery delays over the past two months.
            Customer complaints have increased by 45%, and several major clients are threatening to switch suppliers.
            The operations team is baffled - everything seems normal on paper, but packages are consistently
            arriving 3-5 days late. Your mission: investigate the supply chain data, identify patterns,
            and determine the root cause of these delays before the company loses more business.
        """,
        "expected_root_cause": "supplier_capacity_shortage",
        "hints": [
            "Check if delays correlate with specific suppliers or regions",
            "Look at supplier performance metrics and capacity utilization",
            "Analyze seasonal patterns and demand spikes",
            "Examine the relationship between order quantities and delivery times"
        ],
        "difficulty": "Easy"
    },
    {
        "id": 2,
        "title": "The Phantom Quality Issues",
        "description": """
            A series of quality defects have been detected in products shipped from your distribution centers.
            The defect rate has jumped from 2% to 12% in just three weeks. Interestingly, the defects only
            appear in certain product categories, and internal quality checks at manufacturing sites show
            no issues. Returns are piling up, and the quality assurance team suspects something is happening
            during transportation or storage. Dive into the data to uncover what's causing these quality anomalies.
        """,
        "expected_root_cause": "improper_storage_conditions",
        "hints": [
            "Investigate temperature-sensitive products and storage conditions",
            "Check warehouse locations and their environmental controls",
            "Look for patterns in transportation routes and handling procedures",
            "Analyze the time products spend in different storage facilities"
        ],
        "difficulty": "Medium"
    },
    {
        "id": 3,
        "title": "The Inventory Paradox",
        "description": """
            Your company is facing a bizarre situation: inventory records show sufficient stock levels,
            but order fulfillment is failing at an alarming rate. Warehouses report they have the items,
            yet 30% of orders are being marked as 'out of stock' and delayed. The finance team is concerned
            about potential inventory write-offs, and operations suspects a systematic issue with either
            inventory tracking, demand forecasting, or warehouse management. This is a complex puzzle that
            requires deep analysis of multiple data sources to solve.
        """,
        "expected_root_cause": "inventory_system_synchronization_error",
        "hints": [
            "Compare physical inventory counts with system records",
            "Check for timing delays in inventory updates across systems",
            "Analyze order processing workflows and system integrations",
            "Look for patterns in SKU-level discrepancies",
            "Investigate recent system updates or integration changes"
        ],
        "difficulty": "Hard"
    }
]


def get_mission(index):
    """
    Get mission by index (0-based).
    
    Args:
        index (int): Zero-based index of the mission (0-2)
        
    Returns:
        dict: Mission configuration dictionary or None if index is invalid
    """
    if 0 <= index < len(MISSIONS):
        return MISSIONS[index]
    return None


def load_mission(mission_id):
    """
    Load mission configuration by ID.
    
    Args:
        mission_id (int): Mission ID (1-3)
        
    Returns:
        dict: Mission configuration dictionary or None if not found
    """
    for mission in MISSIONS:
        if mission["id"] == mission_id:
            return mission
    return None


def get_mission_data(mission_id):
    """
    Get filtered dataset for specific mission.
    
    Args:
        mission_id (int): Mission ID
        
    Returns:
        dict: Mission data configuration
    """
    mission = load_mission(mission_id)
    if mission:
        return {
            "id": mission["id"],
            "title": mission["title"],
            "description": mission["description"],
            "difficulty": mission["difficulty"]
        }
    return None


def get_mission_narrative(mission_id):
    """
    Get story/narrative text for mission.
    
    Args:
        mission_id (int): Mission ID
        
    Returns:
        str: Mission description/narrative
    """
    mission = load_mission(mission_id)
    return mission["description"] if mission else None


def get_correct_answer(mission_id):
    """
    Get correct root cause answer for mission.
    
    Args:
        mission_id (int): Mission ID
        
    Returns:
        str: Expected root cause identifier
    """
    mission = load_mission(mission_id)
    return mission["expected_root_cause"] if mission else None


def get_mission_hints(mission_id):
    """
    Get available hints for mission.
    
    Args:
        mission_id (int): Mission ID
        
    Returns:
        list: List of hint strings
    """
    mission = load_mission(mission_id)
    return mission["hints"] if mission else []


def get_all_missions():
    """
    Get list of all available missions.
    
    Returns:
        list: List of all mission dictionaries
    """
    return MISSIONS


def get_mission_count():
    """
    Get total number of available missions.
    
    Returns:
        int: Number of missions
    """
    return len(MISSIONS)


def validate_mission_answer(mission_id, user_answer):
    """
    Validate if user's answer matches the expected root cause.
    
    Args:
        mission_id (int): Mission ID
        user_answer (str): User's proposed root cause
        
    Returns:
        bool: True if answer is correct, False otherwise
    """
    correct_answer = get_correct_answer(mission_id)
    if correct_answer and user_answer:
        return user_answer.lower().strip() == correct_answer.lower().strip()
    return False

