import time
import random


class BuoyAgent:
    def __init__(self):
        self.baseline_color = 0.35
        self.baseline_flex = 0.25
        self.risk_score = 0.0
        self.state = "NORMAL"

    def observe(self):
        """
        Simulated sensor inputs
        """
        return {
            "color": random.uniform(0.2, 0.9),   # oil / chemical indicator
            "flex": random.uniform(0.1, 0.8),    # object disturbance
            "location": (11.02, 76.96)            # lake coordinate
        }

    def reason(self, obs):
        """
        Attention-based reasoning
        """
        color_shift = abs(obs["color"] - self.baseline_color)
        flex_shift = abs(obs["flex"] - self.baseline_flex)

        # Attention weights (dynamic importance)
        attention_color = 0.6
        attention_flex = 0.4

        self.risk_score = (
            attention_color * color_shift +
            attention_flex * flex_shift
        )

    def decide(self):
        if self.risk_score > 0.25:
            self.state = "FLAGGED_ZONE"
        else:
            self.state = "NORMAL"

    def act(self, obs):
        if self.state == "FLAGGED_ZONE":
            print("\n🚨 POLLUTION ZONE FLAGGED")
            print(f"Risk Score : {self.risk_score:.2f}")
            print(f"Location   : {obs['location']}")
            print("Action     : Geo-fence marked, authority node notified\n")
        else:
            print("✅ Lake condition normal")

    def step(self):
        obs = self.observe()
        self.reason(obs)
        self.decide()
        self.act(obs)


# ---------- RUN AGENT ----------
agent = BuoyAgent()

print("🌊 Autonomous Buoy Agent Started\n")

for _ in range(5):
    agent.step()
    time.sleep(2)
