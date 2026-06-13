"""Decisions - Handle player choices and consequences"""

class DecisionHandler:
    def __init__(self, engine):
        self.engine = engine
        self.consequences = {
            ("intro", 1): {
                "description": "You increase shields",
                "fuel_change": -10,
                "morale_change": 5,
                "next_scene": "shields"
            },
            ("intro", 2): {
                "description": "You change course",
                "fuel_change": -5,
                "morale_change": 0,
                "next_scene": "navigate"
            },
            ("intro", 3): {
                "description": "You hibernate the crew",
                "fuel_change": 0,
                "morale_change": -15,
                "next_scene": "hibernation"
            },
            ("shields", 1): {
                "description": "You investigate the signal",
                "fuel_change": -5,
                "morale_change": 10,
                "next_scene": "distress"
            },
            ("shields", 2): {
                "description": "You ignore the signal and continue",
                "fuel_change": 0,
                "morale_change": -5,
                "next_scene": "neutral"
            },
            ("shields", 3): {
                "description": "You send a probe first",
                "fuel_change": -3,
                "morale_change": 8,
                "next_scene": "probe_sent"
            },
            ("distress", 1): {
                "description": "You retrieve the ancient probe",
                "fuel_change": -8,
                "morale_change": 15,
                "next_scene": "probe_retrieved"
            },
            ("distress", 2): {
                "description": "You document and move on",
                "fuel_change": -2,
                "morale_change": 5,
                "next_scene": "neutral"
            },
            ("distress", 3): {
                "description": "You destroy the probe",
                "fuel_change": 0,
                "morale_change": -20,
                "next_scene": "dark_path"
            }
        }
    
    def handle_decision(self, scene_id, choice_id):
        """Process a player decision"""
        key = (scene_id, choice_id)
        
        if key not in self.consequences:
            print("Invalid choice.")
            return None
        
        consequence = self.consequences[key]
        
        # Apply consequences
        print(f"\n>>> {consequence['description']}")
        
        self.engine.game_state['fuel'] += consequence['fuel_change']
        self.engine.game_state['morale_change'] += consequence['morale_change']
        self.engine.save_choice(choice_id)
        
        return consequence['next_scene']
    
    def validate_choice(self, choice_id):
        """Validate if choice is valid"""
        return 1 <= choice_id <= 3
