import json
import copy
from typing import Dict, Any, List
from collections import OrderedDict


class Plan:
    def __init__(self, file_path: str = None): 
        self.file_path = file_path
        self.plan = {} 
        if self.file_path: 
            self.plan = self.load_plan()

    def load_plan(self) -> Dict[str, Any]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_plan(self, save_file: str = None):
        file_path = save_file if save_file else self.file_path
        with open(file_path, 'w') as f:
            json.dump(self.plan, f, indent=4)

    def get_plan(self) -> Dict[str, Any]:
        return self.plan

    def set_plan(self, new_plan: Dict[str, Any]):
        self.plan = copy.deepcopy(new_plan)

    def modify_plan(self, day: str, hour: int, event: str):
        if day not in self.plan:
            self.plan[day] = {} 
        if 0 <= hour < 24:
            self.plan[day][str(hour)] = event
        else:
            raise ValueError("Hour must be between 0 and 23")

    def print_plan(self, day: str = None):
        if day:
            if day not in self.plan:
                raise ValueError(f"{day} is not a valid day in the plan")
            print(f"\n{day}:")
            for hour, event in sorted(self.plan[day].items(), key=lambda x: int(x[0])):
                print(f"  {hour}:00 - {event}")
        else:
            for day_name, day_plan in self.plan.items():
                print(f"\n{day_name}:")
                for hour, event in sorted(day_plan.items(), key=lambda x: int(x[0])):
                    print(f"  {hour}:00 - {event}")

class Memory:
    def __init__(self, capacity: int, name: str):
        self.capacity = capacity
        self.name = name
        self.memory: Dict[str, Dict[str, Any]] = OrderedDict()
    
    def calculate_importance(self, event: str,  curtick: int, tick: int) -> float:
        return 1
    
    def calculate_relevance(self, event: str, tick: int) -> float:
        return 1
    
    def calculate_recency(self, curtick: int, tick: int) -> float:
        return 1

    def calculate_score(self, recency: float, importance: float, relevance: float = 1) -> float:
        if self.name == "long_term_memory":
            return recency * importance * relevance
        return recency * importance
    
    def recalculate_all_scores(self, current_tick: int):
        if self.name == "long_term_memory":
            for key, value in self.memory.items():
                importance = self.calculate_importance(value['event'], current_tick, value['tick'])
                self.memory[value['event']]['importance'] = importance
                recency = self.calculate_recency(current_tick, value["tick"])
                self.memory[value['event']]['recency'] = recency
                relevance = self.calculate_relevance(value['event'], value['tick'])
                self.memory[value['event']]['relevance'] = relevance
                value['score'] = self.calculate_score(recency, importance, relevance)
        else:
            for key, value in self.memory.items():
                importance = self.calculate_importance(value['event'], current_tick, value['tick'])
                self.memory[value['event']]['importance'] = importance
                recency = self.calculate_recency(current_tick, value["tick"])
                self.memory[value['event']]['recency'] = recency
                value['score'] = self.calculate_score(recency, importance)
    
    def add(self, tick: int, event_name: str, importance: float = 1, recency: float = 1, relevance: float = 1):
        new_entry = {
            "event": event_name,
            "tick": tick,
            "importance": importance,
            "recency" : recency,
            "relevance" : relevance,
            "score": 0
        }

        if len(self.memory) < self.capacity:
            self.memory[event_name] = new_entry
        else:
            self.memory.popitem(last=False)
            self.memory[event_name] = new_entry


    def delete(self, event_name: str):
        if event_name in self.memory:
            del self.memory[event_name]
        else:
            raise KeyError(f"{event_name} does not exist in memory.")