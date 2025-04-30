from typing import Dict, Any, List
from collections import OrderedDict
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np




client = OpenAI(
    api_key="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"
)
class Memory:

    def load_file(self, filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    def __init__(self, capacity: int, name: str):
        self.capacity = capacity
        self.name = name
        self.memory: Dict[str, Dict[str, Any]] = OrderedDict()
        self.semantic_memory: Dict[str, Dict[str, Any]] = OrderedDict()
        self.procedural_memory: Dict[str, Dict[str, Any]] = OrderedDict()

        self.system_role = self.load_file("systemrole.txt")
#####################################Episodic Memory##################################    
        self.system_role_embedding = self.get_embedding(self.system_role)

#####################################Semantic Memory##################################    
        semantic_path = "semantic.json"

        with open(semantic_path, "r", encoding="utf-8") as f:
            semantic_data = json.load(f)
        for entry_id, entry in semantic_data.items():
            text = entry["text"]
            embedding = self.get_embedding(text)

            self.semantic_memory[entry_id] = {
                "id": entry_id,
                "text": text,
                "embedding": embedding,
                "strength": entry.get("strength", 1.0)
            }
#####################################Procedural Memory##################################    
        procedural_path = "procedural.json"

        with open(procedural_path, "r", encoding="utf-8") as f:
            procedural_data = json.load(f)
        for entry_id, entry in procedural_data.items():
            text = entry["text"]
            embedding = self.get_embedding(text)

            self.procedural_memory[entry_id] = {
                "id": entry_id,
                "text": text,
                "embedding": embedding
            }






#####################################Episodic Memory##################################    
    def calculate_importance(self, event: str,  curtick: int, tick: int) -> float:
        system_role = self.load_file("systemrole.txt")
        time_passed = curtick - tick

        prompt = (
            f"On a scale from 1 to 20, rate how important the following event is to you:\n"
            f"Event: {event}\n"
            f"Now it is tick {curtick}. This event was recorded at tick {tick}.\n"
            f"It has been {time_passed} ticks since the event was recorded.\n"
            f"Only provide a single float number between 1 and 20, 1 is not important to you at all, 20 is really important to you.\n "
            f"need exactly number, nothing else. such answer could be 3"
        )
        classification_context = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=classification_context
            )
            result = response.choices[0].message.content.strip()
            #print(result)
            importance_score = float(result)
        except Exception as e:
            print(f"Error calculating importance: {e}")
            return 1.0
        return importance_score
    
#####################################Semantic Memory##################################    
    # def calculate_importance(self, event: str,  curtick: int, tick: int) -> float:
    #     system_role = self.load_file("systemrole.txt")
    #     time_passed = curtick - tick

    #     prompt = (
    #         f"On a scale from 1 to 20, rate how important the following event is to you:\n"
    #         f"Event: {event}\n"
    #         f"Now it is tick {curtick}. This event was recorded at tick {tick}.\n"
    #         f"It has been {time_passed} ticks since the event was recorded.\n"
    #         f"It may come from repeated experiences or events you've encountered before.\n"
    #         f"Only provide a single float number between 1 and 20, where 1 means not important at all, and 20 means extremely important to your beliefs or decision-making.\n"
    #         f"need exactly number, nothing else. such answer could be 3"
    #     )
    #     classification_context = [
    #         {"role": "system", "content": system_role},
    #         {"role": "user", "content": prompt}
    #     ]

    #     try:
    #         response = client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=classification_context
    #         )
    #         result = response.choices[0].message.content.strip()
    #         #print(result)
    #         importance_score = float(result)
    #     except Exception as e:
    #         print(f"Error calculating importance: {e}")
    #         return 1.0
    #     return importance_score
#####################################Procedural Memory##################################    
    # def calculate_importance(self, event: str,  curtick: int, tick: int) -> float:
    #     system_role = self.load_file("systemrole.txt")
    #     time_passed = curtick - tick

    #     prompt = (
    #         f"On a scale from 1 to 20, rate how important the following event is to you:\n"
    #         f"Event: {event}\n"
    #         f"Now it is tick {curtick}. This event was recorded at tick {tick}.\n"
    #         f"It has been {time_passed} ticks since the event was recorded.\n"
    #         f"It is something you have done repeatedly in the past.\n"
    #         f"Only provide a single float number between 1 and 20, where 1 means it barely affects your routine, and 20 means it's a core.\n"
    #         f"need exactly number, nothing else. such answer could be 3"
    #     )
    #     classification_context = [
    #         {"role": "system", "content": system_role},
    #         {"role": "user", "content": prompt}
    #     ]

    #     try:
    #         response = client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=classification_context
    #         )
    #         result = response.choices[0].message.content.strip()
    #         #print(result)
    #         importance_score = float(result)
    #     except Exception as e:
    #         print(f"Error calculating importance: {e}")
    #         return 1.0
    #     return importance_score






    def get_embedding(self, text: str) -> List[float]:
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
#####################################Episodic Memory##################################    

    def calculate_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        if not emb1 or not emb2:
            return 0.0

        emb1 = np.array(emb1).reshape(1, -1)
        emb2 = np.array(emb2).reshape(1, -1)

        similarity = cosine_similarity(emb1, emb2)[0][0]
        return similarity

    def calculate_relevance(self, event: str, tick: int) -> float:
        event_embedding = self.get_embedding(event)
        relevance_score = self.calculate_similarity(self.system_role_embedding, event_embedding)
        return relevance_score
#####################################Semantic Memory##################################    
    # def calculate_relevance(self, event: str, tick: int) -> float:
    #     event_embedding = self.get_embedding(event)

    #     max_similarity = 0.0
    #     for entry in  self.semantic_memory.values():
    #         semantic_embedding = entry["embedding"]
    #         sim = self.calculate_similarity(event_embedding, semantic_embedding)
    #         max_similarity = max(max_similarity, sim)

    #     return max_similarity
#####################################Procedural Memory##################################    
    # def calculate_relevance(self, event: str, tick: int) -> float:
    #     event_embedding = self.get_embedding(event)

    #     max_similarity = 0.0
    #     for entry in  self.procedural_memory.values():
    #         procedural_embedding = entry["embedding"]
    #         sim = self.calculate_similarity(event_embedding, procedural_embedding)
    #         max_similarity = max(max_similarity, sim)

    #     return 1 - max_similarity




    def calculate_recency(self, curtick: int, tick: int) -> float:
        recency = 1 - ((curtick - tick) / 100)
        return max(0.01, recency)

    def calculate_score(self, recency: float, importance: float, relevance: float = 0) -> float:
        if self.name == "long_term_memory":
            return recency * importance * relevance
        return recency * importance * 0.01
    
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
    
    def migrate(self, target_memory: 'Memory', current_tick: int):
        for key, value in list(self.memory.items()):
            recency = self.calculate_recency(current_tick, value['tick'])
            importance = self.calculate_importance(value['event'], current_tick, value['tick'])
            self.memory[value['event']]['recency'] = recency
            self.memory[value['event']]['importance'] = importance
            if target_memory.name == "long_term_memory":
                relevance = self.calculate_relevance(value['event'], value['tick'])
                self.memory[value['event']]['relevance'] = relevance
                score = self.calculate_score(recency, importance, relevance)
            else:
                score = self.calculate_score(recency, importance)
            
            if len(target_memory.memory) < target_memory.capacity:
                target_memory.memory[key] = value.copy()
                target_memory.memory[key]['score'] = score
            
            else:
                lowest_score_key, lowest_score_value = min(target_memory.memory.items(), key=lambda item: item[1]['score'])
                
                if score > lowest_score_value['score']:
                    del target_memory.memory[lowest_score_key]
                    target_memory.memory[key] = value.copy()
                    target_memory.memory[key]['score'] = score
        
        target_memory.memory = OrderedDict(
            sorted(target_memory.memory.items(), key=lambda item: item[1]['score'], reverse=True)
        )
    
    def add(self, tick: int, event_name: str, importance: float = 0, recency: float = 0, relevance: float = 0):
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
        
    def print_memory(self):
        print(f"\n--- {self.name} Memory (Capacity: {self.capacity}) ---")
        for key, value in self.memory.items():
            print(f"{key}: {value}")

    def get(self) -> Dict[str, Any]:
        return dict(self.memory)

#def main():
    #A = Memory(5, "A")
    #B = Memory(5, "B")
    #C = Memory(5, "long_term_memory")
    #event = "Tommy asking you to play video game with him today at tick 9."
    #importance_score = A.calculate_importance(event, curtick=8, tick=1)
    #print(f"Importance Score: {importance_score}")
    #event = "Tommy asking you to play video game with him today at tick 9."
    #relevance_score = A.calculate_relevance(event, tick=1)
    #print(f"Relevance Score: {relevance_score}")
    #event = "The midterm exam is coming on next month on tick 100."
    #relevance_score = A.calculate_relevance(event, tick=1)
   # print(f"Relevance Score: {relevance_score}")
   # event = "Hi my name is Jeff, nice to meet you."
    #relevance_score = A.calculate_relevance(event, tick=1)
    #print(f"Relevance Score: {relevance_score}")
    #event = "Annual horse racing championship is happening in Dubai next week. The participants are all professional horse riders."
    #relevance_score = A.calculate_relevance(event, tick=1)
    #print(f"Relevance Score: {relevance_score}")
  
    ##for i in range(6):
        #A.add(tick=i+1, event_name=f"event{i+1}")

    #A.print_memory()
    
    #A.migrate(B, current_tick=10)
    #B.print_memory()
    
    #B.migrate(C, current_tick=20)
    #C.print_memory()
    
# if __name__ == "__main__":
#     main()