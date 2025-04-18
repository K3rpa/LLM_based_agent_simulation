import json
from typing import List, Dict
from plan import Plan
from memory import Memory

class EventManager:
    def __init__(self, plan: Plan, memory: Memory, fixed_subevents_file: str):
        self.plan = plan
        self.memory = memory
        self.fixed_subevents_file = fixed_subevents_file
        self.fixed_subevents = self.load_fixed_subevents()

    def load_fixed_subevents(self) -> Dict[str, List[str]]:
        with open(self.fixed_subevents_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_main_event(self, day: str, tick: int) -> str:
        plan_dict = self.plan.get_plan()
        return plan_dict.get(day, {}).get(str(tick), "No main event")

    def get_fixed_subevents(self, tick: int) -> List[str]:
        return self.fixed_subevents.get(str(tick), [])

    def simulate_tick(self, day: str, tick: int, curtick: int):
        print(f"\n=== Tick {tick} Simulation ===")
        main_event = self.get_main_event(day, curtick)
        print(f"Main Event: {main_event}")

        fixed = self.get_fixed_subevents(tick)
        subevents = fixed  # Random events are temporarily disabled

        print(f"Subevent Set: {subevents}")