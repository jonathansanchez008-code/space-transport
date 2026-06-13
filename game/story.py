"""Story - Game narrative and scenes"""

class Story:
    def __init__(self):
        self.scenes = self._load_scenes()
    
    def _load_scenes(self):
        """Load all game scenes"""
        return {
            "intro": {
                "text": """
                Year 2087. You are ARIA, an advanced AI managing the spacecraft 'Horizon'.
                Your mission: Transport 50 human colonists to Proxima Centauri safely.
                
                The journey will take 5 years. As the AI, every decision falls on you.
                The crew's survival depends on your choices.
                
                You wake up to an alert: A solar storm approaches. What do you do?
                """,
                "choices": [
                    {"id": 1, "text": "Increase shields (costs 10% fuel)"},
                    {"id": 2, "text": "Change course (risky, may encounter asteroids)"},
                    {"id": 3, "text": "Hibernate crew (controversial)"}
                ]
            },
            "shields": {
                "text": """
                You activate the shield generators. The ship trembles as the solar storm
                approaches. Crew members brace themselves.
                
                The shields hold! The storm passes. Crew morale increases slightly.
                But fuel reserves are now at 90%.
                
                A distress signal appears on your sensors...
                """,
                "choices": [
                    {"id": 1, "text": "Investigate the signal"},
                    {"id": 2, "text": "Ignore it and continue to destination"},
                    {"id": 3, "text": "Send a probe first"}
                ]
            },
            "distress": {
                "text": """
                You approach the signal source. It's an ancient probe from Earth, lost
                for centuries. Inside, valuable data about safe routes through space.
                
                However, retrieving it will delay your journey by 2 days and cost fuel.
                The crew is divided on whether to stop.
                """,
                "choices": [
                    {"id": 1, "text": "Retrieve the probe (helps future journeys)"},
                    {"id": 2, "text": "Document it and move on"},
                    {"id": 3, "text": "Destroy it (dark choice)"}
                ]
            }
        }
    
    def get_scene(self, scene_id):
        """Get a specific scene"""
        return self.scenes.get(scene_id, None)
    
    def display_scene(self, scene):
        """Display a scene to the player"""
        if not scene:
            return
        
        print(scene["text"])
        print("\n--- OPTIONS ---")
        for choice in scene["choices"]:
            print(f"{choice['id']}. {choice['text']}")
