
# HW3: Tennis Career Package

This Python package retrieves career match data from Tennis Abstract and creates scatter plots showing the age difference between a player and their opponents.

## Installation

Install the package directly from GitHub:
pip install git+https://github.com/UCB-stat159-f26/hw03-anikakasula.git

## Usage
The package has two main functions:

- `get_career_matches()` retrieves and processes a player's career matches.
- `plot_career_matches()` creates a scatter plot of age differences, with wins and losses shown in different colors.

### Serena Williams
from tennis_career import get_career_matches, plot_career_matches

serena = get_career_matches("Serena Williams")
plot_career_matches(serena)

### Rafael Nadal
rafa = get_career_matches("Rafael Nadal")
plot_career_matches(rafa)

If the player name is invalid or no career data is available, the package returns an error message.

## Data Processing
The match data comes from Tennis Abstract's career JavaScript files. The package extracts the match dates, results, and opponent information.

The female and male files store opponent ages differently. Female files contain opponents' birth dates, while male files already contain their ages.

Player birth dates are retrieved from the tennis player datasets in the tennis-point-by-point archive.

The cleaned data contains:

- `match_date`
- `player_age`
- `opponent_age`
- `age_difference`
- `result`

Age difference is calculated as the player's age minus the opponent's age.

## Testing
The package uses pytest to test data processing and plotting.

The tests use sample match records instead of requesting data from the live website.

To run the tests:
python -m pytest tests/ -v

## Reflections
One thing I learned from this assignment was how to turn code from an earlier assignment into a Python package that other people can install and use. Instead of working with just Serena Williams' data, I had to make the functions work with different players.

The most challenging part was handling the differences between male and female match records. I initially expected the data to have the same structure, but the opponent age information was stored differently. I also ran into issues retrieving player birth dates and had to find another way to access them.

Writing tests helped me understand why it is useful to separate downloading data from processing it. By using sample JavaScript files, I could check whether the cleaning functions worked without repeatedly accessing the website.

## Data Sources
- [Tennis Abstract](https://www.tennisabstract.com/)
- [Tennis point-by-point archive](https://github.com/micahp/tennis-point-by-point-archive)
