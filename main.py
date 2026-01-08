import time
from env import GridWorld
from agent import SlimeAgent
from visualizer import ConsoleVisualizer
from reporter import Reporter

def main():
    # Configuration
    EPISODES = 1000
    SHOW_EVERY = 100   # Console visualization frequency
    SLOW_MO = 0.1      # Visualization speed
    
    # Initialization
    env = GridWorld()
    agent = SlimeAgent(env)
    
    # We use both:
    viz = ConsoleVisualizer(env)  # For watching it live (CLI)
    reporter = Reporter(env)      # For the final report (Data)
    
    print("🚀 Starting Monte Carlo Slime Simulation...")
    print(f"   - Episodes: {EPISODES}")
    print("   - You will see the slime learning in the console.")
    print("   - A report image will be saved at the end.")
    time.sleep(2)
    
    for episode in range(1, EPISODES + 1):
        state = env.reset()
        done = False
        score = 0
        step_count = 0
        
        # Decide if we want to visualize this episode in CLI
        show_render = (episode % SHOW_EVERY == 0) or (episode == 1) or (episode > 990)
        
        while not done:
            if show_render:
                viz.render(state, agent.value_table, episode, step_count, score)
                time.sleep(SLOW_MO)
            
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            
            agent.add_step(state, action, reward)
            
            state = next_state
            score += reward
            step_count += 1
            
            if step_count > 100:
                done = True
                
        # End of Episode
        agent.update()
        agent.decay_epsilon()
        
        # Log Data
        reporter.log(episode, score, step_count)
        
        if show_render:
            viz.render(state, agent.value_table, episode, step_count, score)
            print(f"Episode {episode} finished. Score: {score}, Epsilon: {agent.epsilon:.2f}")

    print("\n✅ Simulation Complete!")
    
    # Generate Report
    reporter.generate_report(agent.value_table)

if __name__ == "__main__":
    main()
