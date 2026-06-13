"""Game Engine - Core game logic"""

class GameEngine:
    def __init__(self):
        self.current_scene = None
        self.player_choices = []
        self.game_state = {
            "fuel": 100,
            "crew_morale": 100,
            "destination": None,
            "time_elapsed": 0
        }
    
    def start_game(self):
        """Initialize the game"""
        self.current_scene = "intro"
        self.display_intro()
    
    def display_intro(self):
        """Display game introduction"""
        intro_text = """
        ╔════════════════════════════════════════════════════════════╗
        ║           WELCOME TO SPACE TRANSPORT                       ║
        ║                                                            ║
        ║  You are an AI managing a spacecraft carrying 50 humans   ║
        ║  to a distant star system. Your decisions will determine  ║
        ║  whether they reach their destination safely.             ║
        ╚════════════════════════════════════════════════════════════╝
        """
        print(intro_text)
    
    def show_status(self):
        """Display game status"""
        print(f"\n--- SHIP STATUS ---")
        print(f"Fuel: {self.game_state['fuel']}%")
        print(f"Crew Morale: {self.game_state['crew_morale']}%")
        print(f"Destination: {self.game_state['destination'] or 'Not set'}")
        print(f"Time Elapsed: {self.game_state['time_elapsed']} days")
    
    def save_choice(self, choice):
        """Save player choice"""
        self.player_choices.append(choice)
    
    def is_game_over(self):
        """Check if game is over"""
        return (self.game_state['fuel'] <= 0 or 
                self.game_state['crew_morale'] <= 0)
