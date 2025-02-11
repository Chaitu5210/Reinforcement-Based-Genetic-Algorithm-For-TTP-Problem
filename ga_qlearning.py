# ga_qlearning.py

import numpy as np
from collections import namedtuple
import random

class GAQLearning:
    def __init__(self, num_strategies=4, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.num_strategies = num_strategies
        # Define num_components first before using it
        self.num_components = 4  # Parent Selection, Crossover, Mutation, Replacement
        
        # Now initialize Q-table after num_components is defined
        self.q_table = np.zeros((num_strategies**4, self.num_components * num_strategies))
        
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        
        # Define named tuple for state representation
        self.State = namedtuple('State', ['parent_selection', 'crossover', 'mutation', 'replacement'])
        
        # Strategy names for each component
        self.strategy_names = {
            'parent_selection': ['truncation', 'tournament', 'roulette_wheel', 'rank'],
            'crossover': ['single_point', 'two_point', 'uniform', 'arithmetic'],
            'mutation': ['bit_flip', 'swap', 'scramble', 'inversion'],
            'replacement': ['bottom_20_percent', 'lowest_fitness', 'fitness_probability', 'elitism']
        }
    
    def state_to_index(self, state):
        """Convert state tuple to single integer index"""
        return (state.parent_selection * self.num_strategies**3 +
                state.crossover * self.num_strategies**2 +
                state.mutation * self.num_strategies +
                state.replacement)
    
    def index_to_state(self, index):
        """Convert integer index to state tuple"""
        parent_selection = index // (self.num_strategies**3)
        remainder = index % (self.num_strategies**3)
        crossover = remainder // (self.num_strategies**2)
        remainder = remainder % (self.num_strategies**2)
        mutation = remainder // self.num_strategies
        replacement = remainder % self.num_strategies
        return self.State(parent_selection, crossover, mutation, replacement)
    
    def get_possible_actions(self, state):
        """Get all possible actions from current state"""
        actions = []
        for component in range(self.num_components):
            for new_strategy in range(self.num_strategies):
                if new_strategy != getattr(state, self.State._fields[component]):
                    actions.append((component, new_strategy))
        return actions
    
    def get_next_state(self, state, action):
        """Apply action to state and return new state"""
        state_list = list(state)
        component, new_strategy = action
        state_list[component] = new_strategy
        return self.State(*state_list)
    
    def choose_action(self, state):
        """Choose action using epsilon-greedy strategy"""
        if random.random() < self.epsilon:
            # Exploration: choose random action
            return random.choice(self.get_possible_actions(state))
        else:
            # Exploitation: choose best action
            state_idx = self.state_to_index(state)
            possible_actions = self.get_possible_actions(state)
            q_values = [self.q_table[state_idx][component * self.num_strategies + new_strategy]
                       for component, new_strategy in possible_actions]
            max_q_idx = np.argmax(q_values)
            return possible_actions[max_q_idx]
    
    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value using Q-learning update rule"""
        state_idx = self.state_to_index(state)
        next_state_idx = self.state_to_index(next_state)
        
        # Calculate maximum Q-value for next state
        next_q_max = np.max(self.q_table[next_state_idx])
        
        # Current Q-value
        component, new_strategy = action
        current_q = self.q_table[state_idx][component * self.num_strategies + new_strategy]
        
        # Update Q-value
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_q_max - current_q)
        self.q_table[state_idx][component * self.num_strategies + new_strategy] = new_q
    
    def get_optimal_strategies(self):
        """Get the optimal combination of strategies based on Q-values"""
        best_state_idx = np.argmax(np.max(self.q_table, axis=1))
        best_state = self.index_to_state(best_state_idx)
        
        return {
            'parent_selection': self.strategy_names['parent_selection'][best_state.parent_selection],
            'crossover': self.strategy_names['crossover'][best_state.crossover],
            'mutation': self.strategy_names['mutation'][best_state.mutation],
            'replacement': self.strategy_names['replacement'][best_state.replacement]
        }