import random
import numpy as np

class SlimeAgent:
    def __init__(self, env):
        self.env = env
        self.value_table = np.zeros((env.height, env.width))
        self.returns = {(i, j): [] for i in range(env.height) for j in range(env.width)}
        self.epsilon = 0.9  # Initial exploration rate
        self.gamma = 1.0    # Discount factor (no discount for now as per rules)
        self.episode_history = []  # Stores (state, action, reward)

    def get_action(self, state):
        """
        Epsilon-greedy policy.
        """
        # Exploration
        if random.random() < self.epsilon:
            return random.choice(self.env.actions)
        
        # Exploitation
        # Look at neighbors and pick the one with highest value
        y, x = state
        best_action = None
        max_val = -float('inf')
        
        candidates = []
        
        for action in self.env.actions:
            dy, dx = self.env.action_map[action]
            next_y, next_x = y + dy, x + dx
            
            # If out of bounds, value is essentially -inf (or just current cell's value to discourage wall bashing)
            # Actually, the agent "peeks" at the next state's value
            if 0 <= next_y < self.env.height and 0 <= next_x < self.env.width:
                val = self.value_table[next_y, next_x]
            else:
                val = -float('inf') # Wall
                
            if val > max_val:
                max_val = val
                candidates = [action]
            elif val == max_val:
                candidates.append(action)
                
        return random.choice(candidates) if candidates else random.choice(self.env.actions)

    def update(self):
        """
        Monte Carlo Update
        G_t = R_{t+1} + gamma * R_{t+2} + ...
        """
        G = 0
        visited_states = set()
        
        # Backtrack
        for state, action, reward in reversed(self.episode_history):
            G = self.gamma * G + reward
            
            if state not in visited_states:
                visited_states.add(state)
                self.returns[state].append(G)
                self.value_table[state] = np.mean(self.returns[state])
                
        # Clear history
        self.episode_history = []
        
    def add_step(self, state, action, reward):
        self.episode_history.append((state, action, reward))

    def decay_epsilon(self, decay_rate=0.999):
        self.epsilon = max(0.01, self.epsilon * decay_rate)
