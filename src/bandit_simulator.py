"""
ListingCraft AI Multi-Armed Bandit (MAB) Thompson Sampling Simulator.
Applies Bayesian reinforcement learning (Beta-Bernoulli conjugate priors)
to model A/B/C listing headline performance over simulated consumer traffic.
"""

from typing import Dict, Any, List
import numpy as np


def run_thompson_sampling_simulation(
    variants: List[Dict[str, str]],
    total_impressions: int = 1500,
    random_seed: int = 42
) -> Dict[str, Any]:
    """
    Runs Monte Carlo simulation of Bayesian Thompson Sampling across 3 listing copy variations.
    Each arm represents a copywriting hypothesis:
    - Arm A: Keyword-Dense SEO Focus
    - Arm B: Emotional Artisanal Storytelling
    - Arm C: Scarcity & Fast Turnaround Angle
    """
    np.random.seed(random_seed)
    n_arms = len(variants)

    # Latent true conversion rates (ground truth unknown to the agent)
    # Typical e-commerce CTR ranges from 2.5% to 5.2%
    true_ctrs = [0.032, 0.048, 0.039] if n_arms == 3 else [0.035] * n_arms

    # Beta prior parameters: alpha = successes + 1, beta = failures + 1
    alphas = np.ones(n_arms)
    betas = np.ones(n_arms)

    arm_pulls = np.zeros(n_arms, dtype=int)
    arm_rewards = np.zeros(n_arms, dtype=int)

    # Simulation rounds
    for _ in range(total_impressions):
        # Sample theta from posterior Beta(alpha, beta) for each arm
        sampled_thetas = np.random.beta(alphas, betas)
        chosen_arm = int(np.argmax(sampled_thetas))

        # Simulate user click
        reward = int(np.random.rand() < true_ctrs[chosen_arm])

        # Bayesian update
        arm_pulls[chosen_arm] += 1
        arm_rewards[chosen_arm] += reward
        alphas[chosen_arm] += reward
        betas[chosen_arm] += (1 - reward)

    # Probability of each arm being optimal via 5000 posterior draws
    posterior_draws = np.random.beta(alphas[:, None], betas[:, None], size=(n_arms, 5000))
    best_arm_counts = np.sum(np.argmax(posterior_draws, axis=0) == np.arange(n_arms)[:, None], axis=1)
    win_probabilities = np.round((best_arm_counts / 5000.0) * 100.0, 1)

    results = []
    for i in range(n_arms):
        empirical_ctr = round((arm_rewards[i] / max(1, arm_pulls[i])) * 100.0, 2)
        results.append({
            "variant_label": variants[i].get("label", f"Headline {chr(65+i)}"),
            "headline_text": variants[i].get("text", ""),
            "allocated_traffic": int(arm_pulls[i]),
            "simulated_clicks": int(arm_rewards[i]),
            "posterior_ctr_pct": empirical_ctr,
            "win_probability_pct": float(win_probabilities[i])
        })

    # Identify champion variant
    champion_idx = int(np.argmax(win_probabilities))
    champion = results[champion_idx]

    return {
        "total_simulated_impressions": total_impressions,
        "champion_variant": champion["variant_label"],
        "champion_win_probability": champion["win_probability_pct"],
        "arm_results": results,
        "recommendation": f"Thompson Sampling converged: '{champion['variant_label']}' dominates with {champion['win_probability_pct']}% posterior confidence."
    }
