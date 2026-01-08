import os
import time

class ConsoleVisualizer:
    def __init__(self, env):
        self.env = env

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, agent_pos, value_table, episode, step, score):
        self.clear_screen()
        print(f"🧪 Monte Carlo Slime - Episode: {episode}, Step: {step}, Score: {score}")
        print("-" * 40)
        
        for i in range(self.env.height):
            line = ""
            for j in range(self.env.width):
                # Determine symbol
                if (i, j) == agent_pos:
                    # Slime emoji based on context
                    if (i, j) == self.env.trap:
                        symbol = "☠️ " 
                    elif (i, j) == self.env.goal:
                        symbol = "😋 "
                    else:
                        symbol = "🟩 "
                elif (i, j) == self.env.goal:
                    symbol = "🍎 "
                elif (i, j) == self.env.trap:
                    symbol = "🕳 "
                else:
                    symbol = "⬜️ "
                
                # Overlay Value
                # Format: Symbol [Value]
                val = value_table[i, j]
                line += f"{symbol}[{val:5.1f}] "
            
            print(line)
            print() # Spacer
            
        print("-" * 40)
