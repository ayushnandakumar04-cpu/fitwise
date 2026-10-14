
from google import genai

api_key="AQ.Ab8RN6JuwI_OjKIwuKRbbPl1V05X3SB18NhQdDUQpmclZ4Qj2w"


def get_budget_plan(response_data):
    monthly_total=response_data.get("monthly_total")
    meal_type_summary=response_data.get("meal_type_summary")

    meal_type_summary_text=""

    for di in meal_type_summary:
        meal_type_summary_text += f"{di.get("meal_type")}:{di.get("total")}\n"
    print(meal_type_summary_text)