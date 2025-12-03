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
        "expected_root_cause": "supplier_reliability_issues",
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
        "expected_root_cause": "equipment_failure",
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
        "expected_root_cause": "inventory_mismatch",
        "hints": [
            "Compare physical inventory counts with system records",
            "Check for timing delays in inventory updates across systems",
            "Analyze order processing workflows and system integrations",
            "Look for patterns in SKU-level discrepancies",
            "Investigate recent system updates or integration changes"
        ],
        "difficulty": "Hard"
    },
    {
        "id": 4,
        "title": "Operation Ghost Network: The Vanishing Shipments",
        "description": """
            A sophisticated anomaly has emerged in your international supply chain network. Over the past six weeks,
            high-value shipments have been mysteriously disappearing between customs clearance and final delivery.
            The losses total $2.3 million, and each incident shows legitimate tracking updates until the cargo
            suddenly goes dark. Security footage is intact, all documentation appears authentic, and carriers
            claim no knowledge of the missing goods. Even more puzzling: some items reappear weeks later at
            unauthorized distribution points. The board suspects either an elaborate theft ring with inside access
            or a critical system vulnerability being exploited. Your forensic analysis could be the difference
            between bankruptcy and catching the perpetrators. Time is running out as the pattern is accelerating.
        """,
        "expected_root_cause": "fraudulent_activity",
        "hints": [
            "Analyze shipment routes and identify common transit points for missing cargo",
            "Cross-reference employee access logs with shipment disappearance timestamps",
            "Look for unusual patterns in carrier switches or route deviations",
            "Check for abnormal authentication attempts or system access from unexpected locations",
            "Investigate relationships between affected shipments - products, values, destinations",
            "Examine the timing: do disappearances correlate with specific shifts or personnel?"
        ],
        "difficulty": "Expert"
    },
    {
        "id": 5,
        "title": "The Cascade Effect: When One Supplier Breaks the Chain",
        "description": """
            Your company's supply chain is experiencing a cascading failure that's threatening to shut down
            production lines across three continents. It started innocuously: a single supplier in Southeast Asia
            missed a delivery deadline by 48 hours. But within two weeks, the ripple effect has caused stockouts,
            production halts, and expedited shipping costs exceeding $800K. What's baffling is the magnitude -
            this supplier only provides 8% of your raw materials, yet the impact is catastrophic. Other suppliers
            are now also missing deadlines, and your alternative sourcing strategies aren't working as planned.
            Manufacturing plants are pointing fingers at procurement, procurement blames logistics, and logistics
            claims the forecasting models are flawed. You need to map the hidden dependencies, identify the
            critical bottleneck, and propose an emergency mitigation strategy before the entire operation collapses.
        """,
        "expected_root_cause": "critical_dependency_failure",
        "hints": [
            "Map the complete dependency network - which products rely on this supplier's materials?",
            "Check if this supplier provides a unique component used across multiple product lines",
            "Analyze lead times and buffer stock levels for alternative suppliers",
            "Look for shared resources or facilities between this supplier and others",
            "Investigate if the delayed component is a prerequisite for just-in-time processes",
            "Examine your supply chain topology - is this a single point of failure?"
        ],
        "difficulty": "Hard"
    }
]


def get_mission(index):
    """
    Get mission by index (0-based).
    
    Args:
        index (int): Zero-based index of the mission (0-4)
        
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
        mission_id (int): Mission ID (1-5)
        
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

