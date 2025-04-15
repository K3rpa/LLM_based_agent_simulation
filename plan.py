import json
import copy
from typing import Dict, Any

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

#if __name__ == "__main__":
#    weekly = Plan('weekly_init.json')
 #   daily = Plan()
#    daily.set_plan(weekly.get_plan())
 #   weekly.modify_plan('Monday', 10, "Modified Weekly Event")

#    daily.modify_plan('Monday', 10, "Modified Daily Event")

    # Print plans
#    weekly.print_plan('Monday')
    #daily.print_plan()
