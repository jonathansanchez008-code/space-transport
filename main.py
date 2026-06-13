#!/usr/bin/env python3
"""Space Transport - Main Game Loop"""

from game.engine import GameEngine
from game.story import Story
from game.decisions import DecisionHandler

def main():
    """Main game loop"""
    engine = GameEngine()
    story = Story()
    decision_handler = DecisionHandler(engine)
    
    # Start the game
    engine.start_game()
    input("\nPress Enter to begin your journey...")
    
    current_scene = "intro"
    
    while not engine.is_game_over():
        print("\n" + "="*60)
        
        # Display current scene
        scene = story.get_scene(current_scene)
        if not scene:
            print("Game Over - No more scenes available.")
            break
        
        story.display_scene(scene)
        
        # Display game status
        engine.show_status()
        
        # Get player choice
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if not decision_handler.validate_choice(choice):
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue
            
            # Process decision and get next scene
            next_scene = decision_handler.handle_decision(current_scene, choice)
            
            if next_scene:
                current_scene = next_scene
            else:
                print("Invalid transition.")
                break
        
        except ValueError:
            print("Please enter a valid number.")
            continue
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
    
    # Game over
    print("\n" + "="*60)
    print("GAME OVER")
    engine.show_status()
    print(f"Total decisions made: {len(engine.player_choices)}")
    print("Thanks for playing Space Transport!")

if __name__ == "__main__":
    main()
