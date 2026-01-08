import matplotlib.pyplot as plt
import numpy as np

class Reporter:
    def __init__(self, env):
        self.env = env
        self.episodes = []
        self.rewards = []
        self.steps = []
        
    def log(self, episode, reward, step_count):
        self.episodes.append(episode)
        self.rewards.append(reward)
        self.steps.append(step_count)
        
    def generate_report(self, value_table, filename="training_report.png"):
        print("📊 Generating Training Report...")
        
        plt.style.use('ggplot')
        fig = plt.figure(figsize=(15, 6))
        
        # --- 1. Learning Curve (Left) ---
        ax1 = fig.add_subplot(121)
        ax1.set_title("Learning Curve (Reward)")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Total Reward")
        
        # Raw Data
        ax1.scatter(self.episodes, self.rewards, s=5, alpha=0.3, color='gray', label='Raw')
        
        # Moving Average
        window = 50
        if len(self.rewards) >= window:
            avg_rewards = np.convolve(self.rewards, np.ones(window)/window, mode='valid')
            ax1.plot(self.episodes[window-1:], avg_rewards, color='blue', linewidth=2, label=f'Avg (N={window})')
            
        ax1.legend()
        
        # --- 2. Brain Map (Right) ---
        ax2 = fig.add_subplot(122)
        ax2.set_title("Final Brain Map (Value Table)")
        im = ax2.imshow(value_table, cmap='RdYlGn', vmin=-10, vmax=10)
        plt.colorbar(im, ax=ax2)
        
        # Annotate Values
        height, width = value_table.shape
        for i in range(height):
            for j in range(width):
                val = value_table[i, j]
                text_color = 'black' if -5 < val < 5 else 'white'
                ax2.text(j, i, f"{val:.1f}", ha='center', va='center', color=text_color, fontweight='bold')
                
        # Markers
        ax2.text(self.env.start[1], self.env.start[0], 'S', ha='left', va='top', color='blue', fontweight='bold', fontsize=12)
        ax2.text(self.env.goal[1], self.env.goal[0], 'G', ha='left', va='top', color='white', fontweight='bold', fontsize=12)
        ax2.text(self.env.trap[1], self.env.trap[0], 'T', ha='left', va='top', color='red', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(filename)
        print(f"✅ Report saved to: {filename}")
        plt.close()
