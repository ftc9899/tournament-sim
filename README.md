# tournament-sim

## Purpose

The purpose of this software library is to simulate virtual FIRST Tech Challenge tournaments. Certain parameters of a tournament can be specified:
- Number of teams
- Number of matches per team
- Tiebreaker point (TBP) method
- Score ceiling to simulate scarcity
- Winner-take-all proportion

A simulator is useful for obtaining results that would be difficult or impossible to obtain in real life. We used this simulator to run 10,000 synthetic tournaments for a variety of tournament configurations and tiebreaker point methods. Thus, each data point is based on more tournaments than have happened in the history of FTC. Due to the law of large numbers, we have confidence in the accuracy of the data.

## Results

For several tournament sizes, six TBP methods were tested: losing alliance score (the current method), sum of both alliances' scores, your alliance's score plus the losing alliance's score, your alliance's score, your team's OPR, and randomly generated TBP. The first four methods were chosen because they were proposed and supported by the FTC community. OPR was included as a basis for comparison because it represents the ideal TBP method. Randomly generated TBP is also a basis for comparison because it represents a null TBP method. For each TBP method, we calculated the average root-mean-square deviation between the input rankings and the output rankings of all the teams for 10,000 tournaments. The RMSD represents the input/output difference in ranking for an average team in a given tournament. In the table below, the leftmost two columns indicate the tournament type, while the other columns indicate the corresponding average RMSD for each TBP method.

Teams |Matches per Team|Random|Current| Sum  |U+Lose|Yours | OPR
------|----------------|------|-------|------|------|------|-----
16    |5               |3.415 |2.916  |2.836 |2.773 |2.731 |2.462
24    |5               |5.313 |4.518  |4.406 |4.328 |4.293 |3.939
32    |5               |7.222 |6.150  |6.017 |5.903 |5.872 |5.425
32    |6               |6.722 |5.774  |5.649 |5.561 |5.494 |5.136
40    |8               |7.583 |6.578  |6.466 |6.394 |6.324 |6.023
40    |9               |7.188 |6.276  |6.162 |6.091 |6.053 |5.746
80    |9               |14.864|13.025 |12.816|12.722|12.612|12.090

![Graph of the data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_all_teams.png?raw=true)

Using the TBP method of OPR, any differences in a team's input and output rank are due to RP alone. This is because teams with identical RP will have an output rank order that matches their input rank order. The OPR method can be considered 100% ideal. On the other end of the spectrum, the random method represents no deliberate effort to rank teams and can be considered 0% ideal. A representative percentage on a scale from 0 - 100% can be determined for all the other TBP methods.

![Idealness of different methods for different tournaments sizes: all teams](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_percent_all_teams.png?raw=true)

In a tournament, the top four teams (according to the output rankings) become the alliance captains and have the greatest influence on the tournament's outcome. Tracking only the top four teams (according to the input rankings) and doing the same analysis produces data that has key differences. Note that the RMSD's for these teams are lower than for all teams and are less sensitive to the number of teams. However, these RMSD's decrease more sharply between the different TBP methods.

![Graph of the additional data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_top_4.png?raw=true)

Comparing the top 4 teams to all teams, the idealness of the "sum", "u_plus_lose", and "yours" TBP methods has increased, while the idealness of the current TBP method has _decreased_, creating a significant disparity between the current method and the other methods.

![Idealness of different methods for different tournaments sizes: top 4 teams](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_percent_top_4.png?raw=true)

## Conclusions

Here is what can be concluded from these results:
- Every time the losing alliance's score is a component of TBP, idealness decreases
- Every time an alliance's own score is a component of TBP, idealness increases
- In these simulations, the current TBP method is usually about halfway between the random and ideal TBP methods (50% ideal), while the other methods are often 70-80% ideal
- Using an accurate OPR as the TBP method results in the least difference between input and output rankings
  - However, using OPR as a TBP method is not recommended because the accuracy and convenience of the simulated OPR is not attainable in real life
- Here are the other TBP methods in order of increasing difference between input and output rankings:
  - Your alliance's score
  - Your alliance's score added to the losing alliance's score
  - Sum of both alliances' scores
  - Losing alliance's score
- A tournament with 40 teams each playing 9 matches has an average ranking difference less than half that of a tournament with 80 teams each playing 9 matches
  - Therefore, it may be useful to consider organizing the FTC World Championships as 4 divisions of 40 teams each, though this would add an extra round of playoffs
  - If there is not enough time for such a tournament, note that a division of 40 teams each playing 8 matches has only a slightly larger average ranking difference

## Algorithm Overview

### Generate Teams

This algorithm generates the specified number of teams, each with a scoring potential following a normal distribution generated by NumPy. The distribution has an average that varies based on the tournament size; the standard deviation and range for all tournament sizes follow the 2019 Houston World Championship OPR distribution, which approximated a normal distribution.

### Create Match Schedule

The scheduling algorithm follows the [official algorithm](https://idleloop.com/matchmaker/) when it matters. This is the element of the official algorithm that this algorithm incorporates:
- Pairing Uniformity
  - A given team will not partner with any other team more than once
  - A given team will not face a given opponent more than once

These are the elements of the official algorithm that are not necessary for a simulation:
- Round Uniformity
- Match Separation
- Red/Blue Balancing
- Station Position Balancing

This algorithm only handles tournaments where number of teams is a multiple of 4, so Surrogate Appearances are not needed.

### Simulate the Qualification Matches

After a match schedule has been created, an alliance's score in a given match is calculated by adding the scoring potential of both teams. To simulate the real-life variance of a team's score from match to match, each team's score in a given match is varied by ±10%. When the winner and loser of a match have been determined, RP and TBP are assigned accordingly. For the 'OPR' TBP method, the team's scoring potential (without variance) is added after each match.

To simulate the effects of scarcity as a game feature, the user can specify a ceiling for the total match score.  If the in-progress match score reaches the ceiling, the teams score at a reduced rate for the remainder of the match. The theoretical point at which the match score exceeded the ceiling is determined by scaling the two reported alliance scores by the same factor. After being scaled, the alliance scores sum to the ceiling. Then, each alliance receives 50% of the additional points they would have scored.

To simulate the effects of winner-take-all as a game feature, the user can specify a proportion of the alliance score that is affected by a winner-take-all feature. It is assumed that the stronger alliance will claim more points from any winner-take-all features. Accordingly, the winning alliance's score is increased by the specified proportion, while the losing alliance's score is decreased by the specified proportion.

## Using this library

`main.py` is set up to run any number of tournaments with a specified number of teams and matches per team. The user can select one of six built-in TBP methods. `main.py` is designed to be run from a terminal with the following options:
- `-t` or `--teams` followed by the number of teams
- `-m` or `--matches` followed by the number of matches per team
- `-n` or `--tournaments` followed by the number of tournaments to run
- `-r` or `--ranking` followed by the TBP method to use ('current', 'sum', 'u_plus_lose', 'yours', 'new2019', 'random', 'opr', or 'inv_opr')
- `-c` or `--ceiling` followed by the score ceiling
- `-w` or `--winner-take-all-proportion` followed by the proportion of an alliance's score to be affected by a winner-take-all feature
