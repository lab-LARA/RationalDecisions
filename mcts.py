import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os


class Country:
    def __init__(self, name, resources, relationship):
        self.name = name
        self.resources = resources  # Dictionary of resource types and quantities
        self.relationship = relationship

    def get_actions(self):
        return ['Trade', 'Hoard', 'Manipulate', 'Negotiate']

    def evaluate_payoff(self, action1, action2, resource):
        if action1 == 'Trade' and action2 == 'Trade':
            return (3 + self.resources.get(resource, 0) / 10 + self.relationship,
                    3 + self.resources.get(resource, 0) / 10 + self.relationship)
        elif action1 == 'Trade' and action2 == 'Hoard':
            return (0, 5 + self.relationship)
        elif action1 == 'Hoard' and action2 == 'Trade':
            return (5 + self.relationship, 0)
        elif action1 == 'Manipulate':
            return (2 + self.resources.get(resource, 0) / 20 + self.relationship,
                    2 + self.relationship)
        elif action1 == 'Negotiate' and action2 == 'Negotiate':
            return (6 + self.resources.get(resource, 0) / 15 + self.relationship,
                    6 + self.relationship)
        elif action1 == 'Negotiate' or action2 == 'Negotiate':
            return (4 + self.resources.get(resource, 0) / 15 + self.relationship,
                    4 + self.relationship)
        else:
            return (1 + self.relationship, 1 + self.relationship)

    def manipulate_resources(self, resource, quantity):
        """Modify resources to influence negotiations."""
        if resource in self.resources:
            self.resources[resource] += quantity

    def negotiate_trade(self, resource, desired_resource, quantity):
        """Propose a negotiation involving resources."""
        if resource in self.resources and self.resources[resource] >= quantity:
            return f"Propose exchange: {quantity} of {resource} for {desired_resource}"
        return "No viable negotiation."

# Check Nash Equilibrium
def is_nash_equilibrium(country1, country2, action1, action2, resource):
    current_payoff1, current_payoff2 = country1.evaluate_payoff(action1, action2, resource)

    for a1 in country1.get_actions():
        payoff1, _ = country1.evaluate_payoff(a1, action2, resource)
        if payoff1 > current_payoff1:
            return False

    for a2 in country2.get_actions():
        _, payoff2 = country2.evaluate_payoff(action1, a2, resource)
        if payoff2 > current_payoff2:
            return False

    return True

# Monte Carlo Tree Search Implementation
def monte_carlo_tree_search(country1, country2, resource, simulations=1000):
    actions = country1.get_actions()
    action_counts = {action: 0 for action in actions}
    action_rewards = {action: 0 for action in actions}

    intermediate_steps = []

    for _ in range(simulations):
        action1 = random.choice(actions)
        action2 = random.choice(actions)

        if action1 == 'Manipulate':
            country1.manipulate_resources(resource, random.randint(-5, 5))
        if action2 == 'Manipulate':
            country2.manipulate_resources(resource, random.randint(-5, 5))

        payoff1, payoff2 = country1.evaluate_payoff(action1, action2, resource)
        intermediate_steps.append((action1, action2, payoff1, payoff2))

        action_counts[action1] += 1
        action_rewards[action1] += payoff1

        if is_nash_equilibrium(country1, country2, action1, action2, resource):
            print("Intermediate steps:")
            for step in intermediate_steps:
                print(f"Actions: {step[0]} vs {step[1]}, Payoffs: {step[2]} vs {step[3]}")
            return action1, action2, True

    best_action = max(actions, key=lambda a: action_rewards[a] / (action_counts[a] + 1e-6))

    # Consider potential retaliation
    retaliation_rewards = {}
    for opponent_action in actions:
        retaliation_payoff = 0
        for _ in range(simulations // len(actions)):
            action1 = best_action
            if opponent_action == 'Manipulate':
                country2.manipulate_resources(resource, random.randint(-5, 5))
            payoff1, _ = country1.evaluate_payoff(action1, opponent_action, resource)
            retaliation_payoff += payoff1
        retaliation_rewards[opponent_action] = retaliation_payoff / (simulations // len(actions))

    worst_case = min(retaliation_rewards.values())
    print("Intermediate steps:")
    for step in intermediate_steps:
        print(f"Actions: {step[0]} vs {step[1]}, Payoffs: {step[2]} vs {step[3]}")
    return best_action, worst_case, False

# Simulate Conflict Resolution
def resolve_conflict(country1, country2, resource, max_iterations=10):
    iteration = 0
    while iteration < max_iterations:
        action1, action2, is_nash = monte_carlo_tree_search(country1, country2, resource)
        if is_nash:
            print(f"Nash equilibrium reached: {action1} vs {action2}")
            return
        iteration += 1
        print(f"Iteration {iteration}: Best action {action1}")

    print("Conflict unresolved after max iterations.")

# Example Usage
russia = Country("Russia", resources={'gas': 100, 'oil': 200, 'prisoners': 10}, relationship=-1)
usa = Country("USA", resources={'gas': 50, 'oil': 150, 'sanctions': 1}, relationship=0)

# Simulate conflict resolution
resolve_conflict(russia, usa, resource='gas')
