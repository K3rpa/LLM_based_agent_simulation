from memory import Memory
from plan import Plan
from event import EventManager
import json
from openai import OpenAI

client = OpenAI(
    api_key="your token key"
)
def load_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

def main():
    
    system_role = load_file("systemrole.txt")
    gpt_logs = []
    long_term_memory = Memory(40, "long_term_memory")
    short_term_memory = Memory(50, "short_term_memory")
    sensory_memory = Memory(40, "sensory_memory")

    weekly_plan = Plan("weekly_init.json")
    daily_plan = Plan()
    daily_plan.set_plan(weekly_plan.get_plan())

    event_manager = EventManager(
        plan=daily_plan,
        memory=sensory_memory,
        fixed_subevents_file="fixed_subevent.json"
    )
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    total_days = len(days)

    #run_tick = 168
    run_tick = 335
    for global_tick in range(run_tick):
        current_day_index = global_tick // 24
        curtick = global_tick % 24
        current_day = days[current_day_index % total_days]

        print(f"\n--- Tick {global_tick} (curtick = {curtick}) ---")
        main_event = event_manager.get_main_event(current_day, curtick)
        #print(f"Main Event: {main_event}")
        fixed_subevents = event_manager.get_fixed_subevents(global_tick, main_event)
        fixed_main_event = event_manager.get_fixed_main_event(global_tick)

        if fixed_subevents and fixed_main_event == main_event:
            subevents = fixed_subevents
        else:
            subevents = [f"{main_event} at tick {global_tick}"]
        
        #print(f"Sub Event: {subevents}")

        for event in subevents:
            sensory_memory.add(tick=global_tick, event_name=event)

        if global_tick % 12 == 11:
            sensory_memory.migrate(short_term_memory, current_tick=global_tick)

        if global_tick % 24 == 23:
            short_term_memory.migrate(long_term_memory, current_tick=global_tick)
            
            #############
            # memory_events = short_term_memory.get()
            # memory_json = json.dumps(memory_events, indent=2)
            # daily_plan_json = json.dumps(daily_plan.get_plan(), indent=2)
            # prompt = (
            #     f"Now it is tick {global_tick}. The time starts at tick 0. Tick 8 means first week Monday 8 am.\n"
            #     f"Each day has 24 ticks. For example, tick 25 means Tuesday 1 am.\n\n"

            #     f"Below is the agent's current daily plan. The format is: day → hour → event.\n"
            #     f"Daily Plan JSON:\n{daily_plan_json}\n\n"
            #     f"And here is your memory. Each memory item includes an event description, the tick when it occurred, and some metadata:\n"
            #     f"Memory JSON:\n{memory_json}\n\n"

            #     f"Your task is to revise the daily plan, but ONLY if there is a meaningful reason inferred from the memory.\n"
            #     f"You are not required to make changes—only do so if it's clearly helpful or needed.\n\n"

            #     f"Follow these rules:\n"
            #     f"1. Only consider memory events that occurred before the current tick (tick < {global_tick}). Do NOT use future memory.\n"
            #     f"2. You may use past memory to infer potential follow-up actions, but DO NOT copy past events directly into the plan.\n"
            #     f"3. DO NOT suggest or invent tasks like 'prepare for presentation' unless the memory directly implies such an event.\n"
            #     f"4. Do NOT modify anything before current tick. Only modify future hours: tick >= {global_tick}.\n"
            #     f"5. Only modify planned events if it's truly necessary. Prefer keeping the original daily plan if no strong reason.\n"
            #     f"6. Importance, score, relevance are useful hints, but high numbers alone should NOT cause plan changes.\n"
            #     f"7. You may adjust the plan if a memory suggests things like:\n"
            #     f"   - upcoming commitment with someone\n"
            #     f"   - deadline approaching\n"
            #     f"   - high emotional or psychological impact that may require follow-up\n"
            #     f"   - establishing a habit or consistent routine\n"
            #     f"   (These are examples. Use your own judgment.)\n\n"
            #     f"8. Do NOT modify more than 2 time slots,try to add as less as possible, if there is anything important just keep it 0\n"
            #     f"9. Your output must be a JSON list in the format: [\"Day\", Hour, \"New Event Description\"].\n"
            #     f"10. Only output the final JSON list. No explanations or extra text.\n\n"

            #     f"Example: [[\"Tuesday\", 14, \"Work on Algorithm Homework with Teammate\"]]"
            # )

            # messages = [
            #     {"role": "system", "content": system_role},
            #     {"role": "user", "content": prompt}
            # ]

            # try:
            #     response = client.chat.completions.create(
            #         model="gpt-4",
            #         messages=messages
            #     )
            #     result = response.choices[0].message.content.strip()
            #     #print("\n[GPT Daily Plan Modifications]:\n", result)
            #     gpt_logs.append({
            #         "tick": global_tick,
            #         "type": "daily",
            #         "response": result
            #     })
            #     try:
            #        modifications = json.loads(result)
            #        for mod in modifications:
            #           if len(mod) == 3:
            #                day, hour, new_event = mod
            #                daily_plan.modify_plan(day, int(hour), new_event)
            #                #print(f"Applied modification: {day} {hour} -> {new_event}")
            #     except Exception as e:
            #        print("Failed to parse GPT modifications:", e)

            # except Exception as e:
            #    print("Error querying OpenAI:", str(e))
            #######################
            #check_plan_json = json.dumps(daily_plan.get_plan(), indent=2)
            #print(check_plan_json)
        if global_tick % 168 == 167:
            memory_events = long_term_memory.get()
            memory_json = json.dumps(memory_events, indent=2)
            weekly_plan_json = json.dumps(weekly_plan.get_plan(), indent=2)
            prompt = (
                f"Now it is tick {global_tick}. The time starts at tick 0. Tick 8 means first week Monday 8 am.\n"
                f"Each day has 24 ticks. For example, tick 25 means Tuesday 1 am.\n\n"

                f"Below is the agent's current weekly plan. The format is: day → hour → event.\n"
                f"Daily Plan JSON:\n{weekly_plan_json}\n\n"
                f"And here is your memory. Each memory item includes an event description, the tick when it occurred, and some metadata:\n"
                f"Memory JSON:\n{memory_json}\n\n"

                f"Now, your task is to revise the weekly plan based on the agent’s experience during the week.\n"
                f"This new plan will be used to generate daily schedules for the next week.\n\n"

                f"Follow these rules:\n"
                f"1. Only consider memory events that occurred before the current tick (tick < {global_tick}). Do NOT use future memory.\n"
                f"2. DO NOT suggest or invent tasks like 'prepare for presentation' unless the memory directly implies such an event.\n"
                f"3. Do NOT modify anything before current tick. Only modify future hours: tick >= {global_tick}.\n"
                f"4. Only modify planned events if it's truly necessary. Prefer keeping the original weekly plan if no strong reason.\n"
                f"5. Importance, score, relevance are useful hints, but high numbers alone should NOT cause plan changes.\n"
                f"6. DO NOT change any time slot during Class time.\n"
                f"7. You may adjust the plan if a memory suggests things like:\n"
                f"   - Replace existing time slots with better activities (e.g., more effective routines)\n"
                f"   - Add recurring activities that seem beneficial or emotionally impactful\n"
                f"   (These are examples. Use your own judgment.)\n\n"
                f"8. Do NOT modify more than 4 time slots,try to add as less as possible, if there is anything important just keep it 0\n"
                f"9. Your output must be a JSON list in the format: [\"Day\", Hour, \"New Event Description\"].\n"
                f"10. Only output the final JSON list. No explanations or extra text.\n\n"

                f"Example: [[\"Tuesday\", 14, \"Work on Algorithm Homework with Teammate\"]]"
            )

            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                result = response.choices[0].message.content.strip()
                #print("\n[GPT Weekly Plan Modifications]:\n", result)
                gpt_logs.append({
                    "tick": global_tick,
                    "type": "weekly",
                    "response": result
                })
                try:
                   modifications = json.loads(result)
                   for mod in modifications:
                      if len(mod) == 3:
                           day, hour, new_event = mod
                           weekly_plan.modify_plan(day, int(hour), new_event)
                           #print(f"Applied modification: {day} {hour} -> {new_event}")
                except Exception as e:
                   print("Failed to parse GPT modifications:", e)

            except Exception as e:
               print("Error querying OpenAI:", str(e))
            check_plan_json = json.dumps(weekly_plan.get_plan(), indent=2)
            #print(check_plan_json)
            #daily_plan.set_plan(weekly_plan.get_plan())



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
    
    with open("gpt_response_report.js", "w", encoding="utf-8") as f:
        json.dump(gpt_logs, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
