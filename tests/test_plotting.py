import pandas as pd
import matplotlib.pyplot as plt

from tennis_career import plot_career_matches


def test_plot():
    data = pd.DataFrame({
        "player_age": [20, 21, 22, 23],
        "age_difference": [-3, 2, -1, 4],
        "result": ["W", "L", "W", "L"]
    })

    fig = plot_career_matches(data)
    ax = fig.axes[0]

    assert ax.get_xlabel() == "Player Age"
    assert ax.get_ylabel() == "Age Difference (Player - Opponent)"
    assert len(ax.collections) == 2

    plt.close(fig)
