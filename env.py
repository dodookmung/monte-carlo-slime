
class GridWorld:
    def __init__(self):
        self.width = 5
        self.height = 5
        self.start = (0, 0)
        self.goal = (4, 4)
        self.trap = (2, 2)
        self.agent_pos = self.start
        
        # Actions
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.action_map = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

    def reset(self):
        self.agent_pos = self.start
        return self.agent_pos

    def step(self, action):
        """
        Move the agent.
        Returns: (next_state, reward, done)
        """
        y, x = self.agent_pos
        dy, dx = self.action_map[action]
        
        next_y, next_x = y + dy, x + dx
        
        # Wall collision check
        if next_y < 0 or next_y >= self.height or next_x < 0 or next_x >= self.width:
            next_y, next_x = y, x  # Stay in place
            
        self.agent_pos = (next_y, next_x)
        
        # Check rewards and done status
        if self.agent_pos == self.goal:
            return self.agent_pos, 10, True
        elif self.agent_pos == self.trap:
            return self.agent_pos, -10, True
        else:
            return self.agent_pos, -1, False
