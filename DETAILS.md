# Abstract

# Background

A FIRST Tech Challenge tournament consists of two major parts: the qualification matches and the elimination rounds. Currently, this simulator only considers the qualification matches, where each team participates in an equivalent number of two versus two matches. Teams are paired with a random partner for each match. The match schedule is set up such that no two teams are paired up more than once or are opponents more than once.

At the conclusion of each match, teams receive ranking points (RP) and tiebreaker points (TBP) dependent on the outcome of said match. The two winning teams (winning alliance) receive two RP, while the two losing teams (losing alliance) receive zero RP. In the event of a tie, all four teams receive one RP. Under the current system, all four teams receive TBP equivalent to the losing alliance's score. Teams are then ranked by RP. The inevitable ties in RP are broken by the aptly-named TBP.

# Results

For several tournament sizes, four TBP methods were tested: losing alliance score (the current method), sum of both alliances' scores, your alliance's score, and your team's OPR. For each TBP method, the average root-mean-square deviation between the input rankings and the output rankings of all the teams for 10,000 tournaments was calculated. The RMSD represents the input/output difference in ranking for an average team in a given tournament. In the table below, the leftmost two columns indicate the tournament type, while the rightmost four columns indicate the corresponding average RMSD for each TBP method.

Teams |Matches per Team|Current| Sum  |Yours | OPR
------|----------------|-------|------|------|------
16    |5               |2.972  |2.876 |2.781 |2.489
24    |5               |4.600  |4.477 |4.360 |4.010
32    |5               |6.195  |6.063 |5.901 |5.437
32    |6               |5.798  |5.682 |5.549 |5.177
40    |8               |6.586  |6.461 |6.340 |6.003
40    |9               |6.285  |6.165 |6.039 |5.761
80    |9               |13.043 |12.812|12.630|12.111

![A nice graph of the data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/tbp_comparison.PNG?raw=true)

![Another graph](https://github.com/ftc9899/tournament-sim/blob/master/tbp_percent_comparison.PNG?raw=true)

# Conclusions

Here is what can be concluded from this data:
- In these simulations, tiebreaker points contributed up to 24% of the difference between a team's input and output ranking
  - Using the TBP method of OPR, any differences in a team's input and output rank are due to RP alone
  - The contribution of RP to the RMSD is shown by the OPR TBP method
  - The contribution of a TBP method to the RMSD is the change in RMSD from the OPR method to the TBP method
- The chosen TBP method has a greater effect on the output ranking of high-scoring teams as compared to all teams
  - In the case of a Worlds-level tournament, the RP contribute an average difference of 6.162 ranking positions
  - The current TBP method contributes an additional average difference of 1.424 ranking positions, which is 18.77% of the total difference
  - The 'yours' TBP method contributes an additional average difference of 0.407 ranking positions, which is 6.20% of the total difference
- Using an accurate OPR as the TBP method results in the least difference between input and output rankings
  - However, using OPR as a TBP method is not recommended because the accuracy and convenience of the simulated OPR is not attainable in real life
- Here are the other TBP methods in order of increasing difference between input and output rankings:
  - Your alliance's score
  - Sum of both alliances' scores
  - Losing alliance's score
- A tournament with 40 teams each playing 9 matches has an average ranking difference less than half that of a tournament with 80 teams each playing 9 matches
  - Therefore, it may be useful to consider organizing the FTC World Championships as 4 divisions of 40 teams each, though this would add an extra round of playoffs
  - If there is not enough time for such a tournament, note that a division of 40 teams each playing 8 matches has only a slightly larger average ranking difference