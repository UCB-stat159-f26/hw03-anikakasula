import matplotlib.pyplot as plt


def plot_career_matches(data):
    fig, ax = plt.subplots(figsize=(10, 6))

    wins = data[data["result"] == "W"]
    losses = data[data["result"] == "L"]

    ax.scatter(wins["player_age"], wins["age_difference"],
               color="teal", s=10, alpha=0.6, label="Win")
    ax.scatter(losses["player_age"], losses["age_difference"],
               color="purple", s=10, alpha=0.6, label="Loss")

    ax.axhline(0, color="gray", linestyle="--")
    ax.set_xlabel("Player Age")
    ax.set_ylabel("Age Difference (Player - Opponent)")
    ax.set_title("Career Matches by Age Difference")
    ax.legend()

    return fig
