"""Story - Game narrative and scenes"""

class Story:
    def __init__(self):
        self.scenes = self._load_scenes()
    
    def _load_scenes(self):
        """Load all game scenes"""
        return {
            "intro": {
                "text": """
                Año 2087. Eres ARIA, una IA avanzada que gestiona la nave 'Horizonte'.
                Tu misión: Transportar 50 colonos humanos a Próxima Centauri de forma segura.
                
                El viaje durará 5 años. Como la IA, cada decisión recae sobre ti.
                La supervivencia de la tripulación depende de tus elecciones.
                
                Te despiertas con una alerta: Se aproxima una tormenta solar. ¿Qué haces?
                """,
                "choices": [
                    {"id": 1, "text": "Activar escudos (cuesta 10% de combustible)"},
                    {"id": 2, "text": "Cambiar rumbo (arriesgado, podría haber asteroides)"},
                    {"id": 3, "text": "Hibernar a la tripulación (controvertido)"}
                ]
            },
            "shields": {
                "text": """
                Activas los generadores de escudos. La nave tiembla mientras la tormenta
                solar se acerca. Los miembros de la tripulación se aferran a sus asientos.
                
                ¡Los escudos aguantan! La tormenta pasa. La moral de la tripulación aumenta.
                Pero las reservas de combustible ahora están en 90%.
                
                Una señal de auxilio aparece en tus sensores...
                """,
                "choices": [
                    {"id": 1, "text": "Investigar la señal"},
                    {"id": 2, "text": "Ignorarla y continuar hacia el destino"},
                    {"id": 3, "text": "Enviar una sonda primero"}
                ]
            },
            "distress": {
                "text": """
                Te acercas a la fuente de la señal. Es una antigua sonda de la Tierra,
                perdida hace siglos. En su interior, datos valiosos sobre rutas seguras.
                
                Sin embargo, recuperarla demorará tu viaje 2 días y costará combustible.
                La tripulación está dividida sobre si detenerse.
                """,
                "choices": [
                    {"id": 1, "text": "Recuperar la sonda (útil para futuros viajes)"},
                    {"id": 2, "text": "Documentarla y continuar"},
                    {"id": 3, "text": "Destruirla (elección oscura)"}
                ]
            },
            "navigate": {
                "text": """
                Cambias el rumbo de la nave. Los sensores detectan un campo de asteroides
                pequeños, pero manejables. La tripulación respira aliviada.
                
                Ahorras 5% de combustible tomando una ruta más eficiente.
                La moral se mantiene estable.
                
                Ahora recibes un mensaje de la tripulación médica...
                """,
                "choices": [
                    {"id": 1, "text": "Atender la emergencia médica"},
                    {"id": 2, "text": "Ignorar y continuar"},
                    {"id": 3, "text": "Hacer una consulta primero"}
                ]
            },
            "hibernation": {
                "text": """
                Activas los pods de hibernación. Algunos miembros protestan, pero es necesario
                para ahorrar recursos. La moral baja significativamente.
                
                Sin embargo, el consumo de energía se reduce drásticamente.
                Combustible ahorrado: 15%.
                
                La nave se vuelve silenciosa y extraña...
                """,
                "choices": [
                    {"id": 1, "text": "Despertar a algunos para compañía"},
                    {"id": 2, "text": "Mantenerlos dormidos hasta el final"},
                    {"id": 3, "text": "Dejarlos decidir"}
                ]
            },
            "neutral": {
                "text": """
                Continúas tu camino sin incidentes. La rutina diaria de la nave prosigue.
                
                Los días pasan lentamente. La tripulación trabaja en sus tareas.
                El viaje es largo pero predecible.
                
                Pasadas las semanas, un mensaje importante llega...
                """,
                "choices": [
                    {"id": 1, "text": "Abrirlo inmediatamente"},
                    {"id": 2, "text": "Analizar primero"},
                    {"id": 3, "text": "Dejarlo para después"}
                ]
            },
            "probe_sent": {
                "text": """
                Envías una sonda para investigar. Mientras esperas los datos,
                la tripulación discute qué podría haber enviado esa señal.
                
                Después de 30 minutos, la sonda envía sus análisis.
                Parece ser un satélite antiguo de comunicaciones.
                
                ¿Necesitas más información o continúas?
                """,
                "choices": [
                    {"id": 1, "text": "Ir a investigar en persona"},
                    {"id": 2, "text": "Continuar el viaje"},
                    {"id": 3, "text": "Recolectar datos remotamente"}
                ]
            },
            "probe_retrieved": {
                "text": """
                Tu equipo recupera la sonda antigua. Dentro encuentran datos extraordinarios:
                mapas de agujeros de gusano teóricos, coordenadas de civilizaciones perdidas.
                
                Este descubrimiento es histórico. La tripulación celebra.
                Moral: +15%.
                
                Pero el análisis de datos te lleva a una decisión crucial...
                """,
                "choices": [
                    {"id": 1, "text": "Cambiar destino a las nuevas coordenadas"},
                    {"id": 2, "text": "Ignorar los datos y seguir al original"},
                    {"id": 3, "text": "Dejar que la tripulación vote"}
                ]
            },
            "dark_path": {
                "text": """
                Destruyes la sonda. La tripulación queda en silencio.
                
                Algunos se enfurecen. Otros lo aprueban. La moral se divide.
                
                Pero el acto te atormenta. ¿Fue la decisión correcta?
                
                Los días posteriores son tensos...
                """,
                "choices": [
                    {"id": 1, "text": "Justificar la acción a la tripulación"},
                    {"id": 2, "text": "Mantener el secreto"},
                    {"id": 3, "text": "Buscar redención"}
                ]
            },
            "victory": {
                "text": """
                ╔════════════════════════════════════════════════════════════╗
                ║                      ¡MISIÓN CUMPLIDA!                     ║
                ║                                                            ║
                ║  Después de 5 años de viaje, la nave Horizonte llega      ║
                ║  a Próxima Centauri. Los colonos despiertan de la         ║
                ║  hibernación y ven un nuevo mundo esperándolos.           ║
                ║                                                            ║
                ║  Tu liderazgo y decisiones mantuvieron a la tripulación   ║
                ║  a salvo. Eres un héroe para todos ellos.                 ║
                ╚════════════════════════════════════════════════════════════╝
                """,
                "choices": [
                    {"id": 1, "text": "Empezar nuevo juego"},
                    {"id": 2, "text": "Salir"},
                    {"id": 3, "text": "Ver estadísticas"}
                ]
            },
            "defeat": {
                "text": """
                ╔════════════════════════════════════════════════════════════╗
                ║                         GAME OVER                         ║
                ║                                                            ║
                ║  La nave ha quedado sin combustible o la tripulación      ║
                ║  ha perdido toda esperanza.                               ║
                ║                                                            ║
                ║  Tus decisiones no fueron suficientes para salvar la      ║
                ║  misión. Próxima Centauri permanece fuera de alcance.     ║
                ╚════════════════════════════════════════════════════════════╝
                """,
                "choices": [
                    {"id": 1, "text": "Reintentar"},
                    {"id": 2, "text": "Salir"},
                    {"id": 3, "text": "Ver lo que pasó"}
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
        print("\n--- OPCIONES ---")
        for choice in scene["choices"]:
            print(f"{choice['id']}. {choice['text']}")
