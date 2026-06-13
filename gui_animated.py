#!/usr/bin/env python3
"""Space Transport - GUI with Animations"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from game.engine import GameEngine
from game.story import Story
from game.decisions import DecisionHandler

class SpaceTransportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transporte Espacial")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")
        
        # Game logic
        self.engine = GameEngine()
        self.story = Story()
        self.decision_handler = DecisionHandler(self.engine)
        self.current_scene = "intro"
        
        # Animation variables
        self.animation_frame = 0
        self.stars = self.generate_stars()
        self.ship_x = 600
        self.ship_y = 400
        self.ship_angle = 0
        
        # Style
        self.setup_styles()
        
        # Main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create UI elements
        self.create_widgets()
        
        # Start animations
        self.animate()
        
        # Display first scene
        self.display_scene()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#0a0e27')
        style.configure('TLabel', background='#0a0e27', foreground='#00ff88')
        style.configure('Title.TLabel', background='#0a0e27', foreground='#00ff00', font=('Courier', 14, 'bold'))
        style.configure('Status.TLabel', background='#0a0e27', foreground='#ffaa00', font=('Courier', 9))
    
    def generate_stars(self):
        """Generate random stars for space background"""
        stars = []
        for _ in range(150):
            x = random.randint(0, 600)
            y = random.randint(0, 400)
            brightness = random.randint(50, 255)
            stars.append((x, y, brightness))
        return stars
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Title
        title = ttk.Label(self.main_container, text="🚀 TRANSPORTE ESPACIAL 🚀", style='Title.TLabel')
        title.pack(pady=10)
        
        # Main content frame (split view)
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Canvas for animations
        left_frame = ttk.LabelFrame(content_frame, text="VISTA DE LA NAVE", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(
            left_frame,
            width=600,
            height=400,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Story and choices
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Story text area
        text_frame = ttk.LabelFrame(right_frame, text="NARRATIVA", padding=5)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.story_text = tk.Text(
            text_frame,
            height=12,
            width=45,
            bg='#1a1f3a',
            fg='#00ff88',
            font=('Courier', 9),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.story_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.story_text.yview)
        
        # Status frame
        status_frame = ttk.LabelFrame(right_frame, text="ESTADO", padding=5)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.fuel_label = ttk.Label(status_frame, text="Combustible: 100%", style='Status.TLabel')
        self.fuel_label.pack(anchor=tk.W, pady=2)
        
        self.morale_label = ttk.Label(status_frame, text="Moral: 100%", style='Status.TLabel')
        self.morale_label.pack(anchor=tk.W, pady=2)
        
        self.time_label = ttk.Label(status_frame, text="Días: 0", style='Status.TLabel')
        self.time_label.pack(anchor=tk.W, pady=2)
        
        # Choices frame
        choices_label = ttk.Label(right_frame, text="OPCIONES:", style='Title.TLabel')
        choices_label.pack(anchor=tk.W, pady=(5, 2))
        
        self.choices_frame = ttk.Frame(right_frame)
        self.choices_frame.pack(fill=tk.BOTH, expand=True)
        
        self.choice_buttons = []
    
    def draw_space_view(self):
        """Draw outer space view with ship"""
        self.canvas.delete("all")
        
        # Draw stars
        for x, y, brightness in self.stars:
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
            self.canvas.create_oval(x-1, y-1, x+1, y+1, fill=color, outline=color)
        
        # Draw planets in background
        self.canvas.create_oval(50, 50, 120, 120, fill='#ff6b35', outline='#ff8c42')
        self.canvas.create_text(85, 140, text="Marte", fill='#ffaa00', font=('Courier', 9))
        
        self.canvas.create_oval(480, 80, 540, 140, fill='#4ecdc4', outline='#5dd9d0')
        self.canvas.create_text(510, 150, text="Próxima", fill='#ffaa00', font=('Courier', 9))
        
        # Draw ship
        self.draw_ship(300, 200)
        
        # Draw particles for engine
        for i in range(5):
            particle_y = 220 + random.randint(-10, 10)
            particle_x = 280 - random.randint(5, 20)
            self.canvas.create_oval(
                particle_x, particle_y,
                particle_x + 3, particle_y + 3,
                fill='#ff6b35', outline='#ff8c42'
            )
        
        # Draw HUD elements
        self.canvas.create_rectangle(10, 10, 590, 390, outline='#00ff88', width=2)
        self.canvas.create_text(20, 20, text="NAVEGACIÓN ACTIVA", fill='#00ff88', font=('Courier', 8), anchor=tk.NW)
    
    def draw_ship_interior(self):
        """Draw interior of the ship"""
        self.canvas.delete("all")
        
        # Background
        self.canvas.create_rectangle(0, 0, 600, 400, fill='#1a2f4a')
        
        # Walls
        self.canvas.create_rectangle(50, 50, 550, 350, outline='#00ff88', width=3)
        
        # Interior panels
        self.canvas.create_rectangle(60, 60, 200, 150, fill='#0a3d5a', outline='#00ff88')
        self.canvas.create_text(130, 105, text="CONTROL", fill='#00ff88', font=('Courier', 10, 'bold'))
        
        self.canvas.create_rectangle(300, 60, 540, 150, fill='#0a3d5a', outline='#00ff88')
        self.canvas.create_text(420, 105, text="SENSORES", fill='#00ff88', font=('Courier', 10, 'bold'))
        
        self.canvas.create_rectangle(60, 180, 200, 330, fill='#0a3d5a', outline='#00ff88')
        self.canvas.create_text(130, 255, text="MOTOR", fill='#00ff88', font=('Courier', 10, 'bold'))
        
        self.canvas.create_rectangle(300, 180, 540, 330, fill='#0a3d5a', outline='#00ff88')
        self.canvas.create_text(420, 255, text="TRIPULACIÓN", fill='#00ff88', font=('Courier', 10, 'bold'))
        
        # Crew members (simplified)
        crew_positions = [(320, 200), (340, 200), (360, 200), (380, 200),
                          (320, 250), (340, 250), (360, 250), (380, 250)]
        
        for i, (x, y) in enumerate(crew_positions):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='#00ff88', outline='#00ff88')
            if i % 3 == 0:
                self.canvas.create_line(x, y+3, x, y+8, fill='#00ff88', width=1)
        
        # Pulsing lights
        pulse = (self.animation_frame % 20) / 10.0
        light_color = f'#{int(255*pulse):02x}{int(150*pulse):02x}{int(0):02x}'
        
        for x in [85, 130, 175, 160, 140, 120]:
            for y in [80, 100, 120]:
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=light_color, outline=light_color)
        
        # HUD display
        self.canvas.create_text(300, 20, text="INTERIOR DE LA NAVE - VISTA EN TIEMPO REAL", 
                               fill='#00ff88', font=('Courier', 11, 'bold'))
    
    def draw_ship(self, x, y):
        """Draw the spacecraft"""
        # Main hull
        self.canvas.create_polygon(
            x, y-20,          # nose
            x+15, y+15,       # right
            x+10, y+20,       # right bottom
            x-10, y+20,       # left bottom
            x-15, y+15,       # left
            fill='#0088ff', outline='#00ffff', width=2
        )
        
        # Windows
        self.canvas.create_oval(x-3, y-5, x+3, y+5, fill='#ffff00', outline='#ffaa00')
        
        # Engine glow
        self.canvas.create_oval(x-8, y+18, x+8, y+25, fill='#ff6b35', outline='#ff8c42')
    
    def animate(self):
        """Main animation loop"""
        self.animation_frame += 1
        
        # Alternate between space view and interior view every 100 frames
        view_cycle = (self.animation_frame // 100) % 2
        
        if view_cycle == 0:
            self.draw_space_view()
        else:
            self.draw_ship_interior()
        
        # Animate ship movement
        self.ship_x += math.cos(self.animation_frame * 0.02) * 0.5
        self.ship_y += math.sin(self.animation_frame * 0.015) * 0.5
        
        # Schedule next frame
        self.root.after(50, self.animate)
    
    def display_scene(self):
        """Display current scene"""
        scene = self.story.get_scene(self.current_scene)
        
        if not scene:
            self.story_text.config(state=tk.NORMAL)
            self.story_text.delete(1.0, tk.END)
            self.story_text.insert(tk.END, "FIN DEL JUEGO\n\n¡Gracias por jugar!")
            self.story_text.config(state=tk.DISABLED)
            return
        
        # Display story
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
                font=('Courier', 9),
                height=2,
                command=lambda c=choice['id']: self.make_choice(c),
                activebackground='#2a6d9a',
                activeforeground='#00ffaa'
            )
            btn.pack(fill=tk.X, pady=3)
            self.choice_buttons.append(btn)
    
    def update_status(self):
        """Update status labels"""
        fuel = self.engine.game_state['fuel']
        morale = self.engine.game_state['crew_morale']
        time = self.engine.game_state['time_elapsed']
        
        self.fuel_label.config(text=f"Combustible: {fuel}%")
        self.morale_label.config(text=f"Moral: {morale}%")
        self.time_label.config(text=f"Días: {time}")
    
    def make_choice(self, choice_id):
        """Handle player choice"""
        next_scene = self.decision_handler.handle_decision(self.current_scene, choice_id)
        
        if next_scene:
            self.current_scene = next_scene
            self.display_scene()
        
        if self.engine.is_game_over():
            messagebox.showinfo("Fin del Juego", "¡El viaje ha terminado!")
            self.display_scene()

def main():
    root = tk.Tk()
    app = SpaceTransportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
