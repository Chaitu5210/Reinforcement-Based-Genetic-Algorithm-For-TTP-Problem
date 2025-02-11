import numpy as np
import random

class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        # Four components: parent selection, crossover, mutation, replacement
        # Each component has 4 possible strategies (0,1,2,3)
        self.num_strategies = 4
        
        # Initialize Q-table: state space = 256 (4^4), action space = 16 (4 components * 4 strategies)
        self.q_table = np.zeros((256, 16))
        
        self.learning_rate = learning_rate    # How much to update Q-values (0 to 1)
        self.discount_factor = discount_factor  # How much to value future rewards (0 to 1)
        self.epsilon = epsilon    # Exploration rate (0 to 1)

    def get_state_index(self, strategies):
        """Convert current strategies to state index
        strategies: tuple of (parent_selection, crossover, mutation, replacement)
        each value is 0-3 representing which strategy is currently being used"""
        p, c, m, r = strategies
        return p * 64 + c * 16 + m * 4 + r

    def get_strategies_from_index(self, index):
        """Convert state index back to strategy numbers"""
        p = index // 64
        remainder = index % 64
        c = remainder // 16
        remainder = remainder % 16
        m = remainder // 4
        r = remainder % 4
        return (p, c, m, r)

    def choose_action(self, current_state):
        """Choose an action using epsilon-greedy strategy
        Returns: (component_to_change, new_strategy_value)"""
        if random.random() < self.epsilon:
            # Exploration: randomly choose component and new strategy
            component = random.randint(0, 3)  # Choose which component to change
            new_value = random.randint(0, 3)  # Choose new strategy value
            return (component, new_value)
        else:
            # Exploitation: choose best action based on Q-values
            state_idx = self.get_state_index(current_state)
            action_idx = np.argmax(self.q_table[state_idx])
            component = action_idx // 4
            new_value = action_idx % 4
            return (component, new_value)

    def get_next_state(self, current_state, action):
        """Apply action to current state to get next state"""
        component, new_value = action
        next_state = list(current_state)
        next_state[component] = new_value
        return tuple(next_state)

    def update(self, current_state, action, reward, next_state):
        """Update Q-value based on action and reward"""
        # Get indices
        current_idx = self.get_state_index(current_state)
        next_idx = self.get_state_index(next_state)
        component, new_value = action
        action_idx = component * 4 + new_value

        # Current Q-value
        current_q = self.q_table[current_idx][action_idx]
        
        # Maximum Q-value for next state
        next_max_q = np.max(self.q_table[next_idx])
        
        # Update Q-value using Q-learning formula
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q)
        
        self.q_table[current_idx][action_idx] = new_q

    def get_best_strategies(self):
        """Get the best performing combination of strategies"""
        # Find state with highest Q-value
        best_state_idx = np.argmax(np.max(self.q_table, axis=1))
        return self.get_strategies_from_index(best_state_idx)