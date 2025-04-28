from memory import Memory
from plan import Plan
from event import EventManager
import json

def main():
    long_term_memory = Memory(5, "long_term_memory")
    short_term_memory = Memory(5, "short_term_memory")
    sensory_memory = Memory(10, "sensory_memory")

    weekly_plan = Plan("weekly_init.json")
    daily_plan = Plan()
    daily_plan.set_plan(weekly_plan.get_plan())

    event_manager = EventManager(
        plan=daily_plan,
        memory=sensory_memory,
        fixed_subevents_file="fixed_subevent.json"
    )

    current_day = "Monday"
    curtick = 0
    for tick in range(24):
        print(f"\n--- Tick {tick} (curtick = {curtick}) ---")
        main_event = event_manager.get_main_event(current_day, curtick)
        print(f"Main Event: {main_event}")
        fixed_subevents = event_manager.get_fixed_subevents(tick, main_event)
        fixed_main_event = event_manager.get_fixed_main_event(tick)

        if fixed_subevents and fixed_main_event == main_event:
            subevents = fixed_subevents
        else:
            subevents = [f"{main_event} at tick {tick}"]
        
        print(f"Sub Event: {subevents}")

        for event in subevents:
            sensory_memory.add(tick=tick, event_name=event)
        curtick = (curtick + 1) % 24

        if tick % 24 == 23:
            sensory_memory.migrate(short_term_memory, current_tick=tick)

    

    all_memory = {
        "long_term_memory": long_term_memory.get(),
        "short_term_memory": short_term_memory.get(),
        "sensory_memory": sensory_memory.get()
    }

    with open("long_term_memory.json", "w", encoding="utf-8") as f:
        json.dump(long_term_memory.get(), f, indent=4, ensure_ascii=False)

    with open("short_term_memory.json", "w", encoding="utf-8") as f:
        json.dump(short_term_memory.get(), f, indent=4, ensure_ascii=False)

    with open("sensory_memory.json", "w", encoding="utf-8") as f:
        json.dump(sensory_memory.get(), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
