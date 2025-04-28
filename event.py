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

    def get_fixed_subevents(self, tick: int, main_event: str) -> List[str]:
        tick_str = str(tick)
        return self.fixed_subevents.get(tick_str, {}).get(main_event, [])
    
    def get_fixed_main_event(self, tick: int) -> str:
        tick_str = str(tick)
        entry = self.fixed_subevents.get(tick_str, {})
        if isinstance(entry, dict) and len(entry) == 1:
            return list(entry.keys())[0]
        return None


    def simulate_tick(self, day: str, tick: int, curtick: int):
        print(f"\n=== Tick {tick} Simulation ===")
        main_event = self.get_main_event(day, curtick)
        print(f"Main Event: {main_event}")

        fixed = self.get_fixed_subevents(tick, main_event)
        
        if fixed:
            subevents = fixed
        else:
            subevents = [f"{main_event} at tick {tick}"]

        print(f"Subevent Set: {subevents}")