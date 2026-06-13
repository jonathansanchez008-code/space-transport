#!/usr/bin/env python3
"""Space Transport - GUI Version with Tkinter"""

import tkinter as tk
from tkinter import ttk, messagebox
from game.engine import GameEngine
from game.story import Story
from game.decisions import DecisionHandler

class SpaceTransportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Transport")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0e27")
        
        # Game logic
        self.engine = GameEngine()
        self.story = Story()
        self.decision_handler = DecisionHandler(self.engine)
        self.current_scene = "intro"
        
        # Style
        self.setup_styles()
        
        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create UI elements
        self.create_widgets()
        
        # Start game
        self.display_scene()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark theme
        style.configure('TFrame', background='#0a0e27')
        style.configure('TLabel', background='#0a0e27', foreground='#00ff88')
        style.configure('Title.TLabel', background='#0a0e27', foreground='#00ff00', font=('Courier', 14, 'bold'))
        style.configure('Status.TLabel', background='#0a0e27', foreground='#ffaa00', font=('Courier', 9))
        style.configure('TButton', font=('Courier', 10))
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Title
        title = ttk.Label(self.main_frame, text="🚀 SPACE TRANSPORT 🚀", style='Title.TLabel')
        title.pack(pady=10)
        
        # Story text area
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.story_text = tk.Text(
            text_frame,
            height=15,
            width=100,
            bg='#1a1f3a',
            fg='#00ff88',
            font=('Courier', 10),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.story_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.story_text.yview)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.main_frame, text="SHIP STATUS", padding=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.fuel_label = ttk.Label(status_frame, text="Fuel: 100%", style='Status.TLabel')
        self.fuel_label.pack(side=tk.LEFT, padx=20)
        
        self.morale_label = ttk.Label(status_frame, text="Crew Morale: 100%", style='Status.TLabel')
        self.morale_label.pack(side=tk.LEFT, padx=20)
        
        self.time_label = ttk.Label(status_frame, text="Days: 0", style='Status.TLabel')
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        # Choices frame
        self.choices_frame = ttk.Frame(self.main_frame)
        self.choices_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.choice_buttons = []
    
    def display_scene(self):
        """Display current scene"""
        scene = self.story.get_scene(self.current_scene)
        
        if not scene:
            self.story_text.config(state=tk.NORMAL)
            self.story_text.delete(1.0, tk.END)
            self.story_text.insert(tk.END, "GAME OVER\n\nThanks for playing Space Transport!")
            self.story_text.config(state=tk.DISABLED)
            return
        
        # Clear and display story
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, scene["text"])
        self.story_text.config(state=tk.DISABLED)
        
        # Update status
        self.update_status()
        
        # Clear previous buttons
        for btn in self.choice_buttons:
            btn.destroy()
        self.choice_buttons = []
        
        # Create choice buttons
        for choice in scene["choices"]:
            btn = tk.Button(
                self.choices_frame,
                text=f"{choice['id']}. {choice['text']}",
                bg='#1a4d7a',
                fg='#00ff88',
                font=('Courier', 10),
                height=2,
                command=lambda c=choice['id']: self.make_choice(c),
                activebackground='#2a6d9a',
                activeforeground='#00ffaa'
            )
            btn.pack(fill=tk.X, pady=5)
            self.choice_buttons.append(btn)
    
    def update_status(self):
        """Update status labels"""
        fuel = self.engine.game_state['fuel']
        morale = self.engine.game_state['crew_morale']
        time = self.engine.game_state['time_elapsed']
        
        self.fuel_label.config(text=f"Fuel: {fuel}%")
        self.morale_label.config(text=f"Crew Morale: {morale}%")
        self.time_label.config(text=f"Days: {time}")
    
    def make_choice(self, choice_id):
        """Handle player choice"""
        next_scene = self.decision_handler.handle_decision(self.current_scene, choice_id)
        
        if next_scene:
            self.current_scene = next_scene
            self.display_scene()
        
        # Check game over
        if self.engine.is_game_over():
            messagebox.showinfo("Game Over", "Game Over! Your journey has ended.")
            self.display_scene()

def main():
    root = tk.Tk()
    app = SpaceTransportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
