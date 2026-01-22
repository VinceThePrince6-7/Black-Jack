import random
from collections import defaultdict
from BJ_final import BlackjackEnv

# ==================================================
# ACTIONS
# ==================================================
STAND = 0
HIT = 1
ACTIONS = [STAND, HIT]

# ==================================================
# EPSILON-GREEDY
# ==================================================
def epsilon_greedy(Q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)

    qvals = [Q[(state, a)] for a in ACTIONS]
    max_q = max(qvals)
    best = [a for a, q in zip(ACTIONS, qvals) if q == max_q]

    return random.choice(best)

# ==================================================
# TRÆNING
# ==================================================
def train(
    episodes=3_000_000,
    alpha=0.1,
    gamma=0.99,
    eps_start=1.0,
    eps_min=0.05,
    eps_decay=0.999995,
    eval_episodes=500_000,
):
    env = BlackjackEnv()
    Q = defaultdict(float)
    epsilon = eps_start

    wins = losses = pushes = 0

    # ---------------- TRÆN ----------------
    for ep in range(1, episodes + 1):
        state = env.reset()
        done = False

        while not done:
            action = epsilon_greedy(Q, state, epsilon)
            next_state, reward, done = env.step(action)

            target = reward
            if not done:
                target += gamma * max(Q[(next_state, a)] for a in ACTIONS)

            Q[(state, action)] += alpha * (target - Q[(state, action)])
            state = next_state

        if reward > 0:
            wins += 1
        elif reward < 0:
            losses += 1
        else:
            pushes += 1

        epsilon = max(eps_min, epsilon * eps_decay)

        if ep % 1_000_000 == 0:
            # print(f"Training episode {ep}, epsilon={epsilon:.3f}")
            print(f"{wins / ep:.3f}")

    # ---------------- EVALUERING ----------------
    wins = losses = pushes = 0
    total_reward = 0

    for _ in range(eval_episodes):
        state = env.reset()
        done = False

        while not done:
            action = epsilon_greedy(Q, state, 0.0)  # epsilon = 0
            state, reward, done = env.step(action)

        total_reward += reward

        if reward > 0:
            wins += 1
        elif reward < 0:
            losses += 1
        else:
            pushes += 1

    total = wins + losses + pushes

    print("\nEVALUATION RESULTS")
    print("Hands played:", total)
    print("Win rate:", wins / total)

    return Q

# ==================================================
# RUN
# ==================================================
if __name__ == "__main__":

    train()
