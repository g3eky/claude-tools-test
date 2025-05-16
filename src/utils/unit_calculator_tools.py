from typing import List, Dict, Any

# Static data: 10 sample appliances with approximate cost per hour (in USD)
APPLIANCES = [
    {"name": "Refrigerator", "cost_per_hour": 0.03},
    {"name": "Air Conditioner", "cost_per_hour": 0.50},
    {"name": "Washing Machine", "cost_per_hour": 0.15},
    {"name": "Microwave Oven", "cost_per_hour": 0.12},
    {"name": "Television", "cost_per_hour": 0.05},
    {"name": "Laptop", "cost_per_hour": 0.02},
    {"name": "Electric Kettle", "cost_per_hour": 0.10},
    {"name": "Ceiling Fan", "cost_per_hour": 0.01},
    {"name": "Heater", "cost_per_hour": 0.40},
    {"name": "Dishwasher", "cost_per_hour": 0.20},
]

# Module-level hashmap to store user appliance usage
user_appliance_usages: Dict[str, Dict[str, Any]] = {}

def add_or_update_appliance_usage(name: str, hours_per_day: float, count: int) -> Dict[str, Any]:
    """
    Add or update an appliance usage entry in the hashmap.
    """
    valid_names = {a["name"] for a in APPLIANCES}
    if name not in valid_names:
        return {"status": "error", "message": f"'{name}' is not a recognized appliance."}
    user_appliance_usages[name] = {
        "name": name,
        "hours_per_day": hours_per_day,
        "count": count
    }
    return {"status": "success", "message": f"Usage for '{name}' updated.", "current": user_appliance_usages[name]}

def calculate_monthly_appliance_cost() -> Dict[str, Any]:
    """
    Calculate the total monthly cost for all appliance usages in the hashmap.
    """
    breakdown = []
    total = 0.0
    appliance_cost_map = {a["name"]: a["cost_per_hour"] for a in APPLIANCES}
    for usage in user_appliance_usages.values():
        name = usage["name"]
        hours = usage.get("hours_per_day", 0)
        count = usage.get("count", 0)
        cost_per_hour = appliance_cost_map.get(name)
        if cost_per_hour is None:
            continue  # skip unknown appliances
        monthly = cost_per_hour * hours * count * 30
        breakdown.append({
            "name": name,
            "monthly_cost": round(monthly, 2),
            "hours_per_day": hours,
            "count": count,
            "cost_per_hour": cost_per_hour
        })
        total += monthly
    return {
        "breakdown": breakdown,
        "total_monthly_cost": round(total, 2)
    }

def list_user_appliances() -> Dict[str, Any]:
    """
    List all appliances currently in the user's hashmap.
    """
    return {
        "appliances": list(user_appliance_usages.keys()),
        "count": len(user_appliance_usages)
    }

unit_calculator_tools = [
    {
        "name": "add_or_update_appliance_usage",
        "function": add_or_update_appliance_usage,
        "description": "Add or update an appliance usage entry (hours per day and count) in the user's appliance list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the appliance (must match one of the sample appliances)"
                },
                "hours_per_day": {
                    "type": "number",
                    "description": "Number of hours per day the appliance is used"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of such appliances"
                }
            },
            "required": ["name", "hours_per_day", "count"]
        }
    },
    {
        "name": "calculate_monthly_appliance_cost",
        "function": calculate_monthly_appliance_cost,
        "description": "Calculate the total monthly cost for all appliances in the user's appliance list.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "list_user_appliances",
        "function": list_user_appliances,
        "description": "List all appliances currently in the user's appliance list.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
] 