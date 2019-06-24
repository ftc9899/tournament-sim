# tournament-sim

Revision | Description
---------|----------------
1.0      | Initial Release
2.0      | Added "random" TBP method as a baseline and "u_plus_lose" TBP method. Evaluated effects of scarcity and winner-take-all game features. Adjusted average OPR based on tournament size. Conclusion: Adoption of the "yours" TBP method is still recommended.

![9899 logo](https://avatars1.githubusercontent.com/u/36021491?s=100&v=4)

Black Diamond Robotics, FTC Team 9899

## Abstract

There is a desire to improve the FIRST Tech Challenge tiebreaker point (TBP) system. This paper introduces a simulator which can help to quantify the effectiveness of proposed TBP systems. Given a number of teams and matches per team, the simulator is able to generate a large volume of synthetic tournament data that reflects actual tournament data. It applies a root-mean-square deviation analysis to quantify the effectiveness of each proposed TBP system. Based on the results, a TBP system where alliances receive their own score appears to be a promising method.

## Introduction

[FIRST Tech Challenge](https://www.firstinspires.org/robotics/ftc) (FTC) is an international high school robotics competition put on by the FIRST organization. Teams build robots to compete in tournaments within year-long seasons. An FTC tournament consists of two major parts: the qualification matches and the elimination rounds. In the qualification matches, each team participates in an equivalent number of two versus two matches. Teams are paired with a random partner for each match. The match schedule is randomized but set up such that no two teams are paired up more than once or are opponents more than once.

At the conclusion of each match, teams receive ranking points (RP) and tiebreaker points (TBP) dependent on the outcome of said match. The two winning teams (winning alliance) receive two RP, while the two losing teams (losing alliance) receive zero RP. In the event of a tie, all four teams receive one RP.

The current TBP method attempts to rank teams with "tougher" schedules (i.e. they played against "better" opponents) above teams with "easier" schedules. This is accomplished by all four teams receiving TBP equivalent to the losing alliance's score in each match the teams play. At the end of the qualification matches, teams are ranked by RP. The inevitable ties in RP are broken by the aptly-named TBP.

It should be noted that the four highest-ranked teams at the end of the qualification matches become the captains of the four alliances that compete in the elimination rounds. To finish at the top, a team needs to both win as many matches as possible and have the most TBP of any other team with the same number of wins. Therefore, TBP are very important for determining the final ranking of the teams with the most RP.

## Background

What is the motivation to explore new TBP methods? Because of its perceived unfairness and dependence on the performance of other teams, there has been longstanding frustration with the current TBP method. For example, in a tournament where each team plays five matches, if team A wins every match with a score of 200 - 0 and team B wins every match with a score of 20 - 10, the current TBP method ranks team B above team A. Though team B had a "tougher" schedule and team A had an "easier" schedule, should team B be ranked above team A?

On top of that, the current TBP method sometimes causes the controversial behavior of a team scoring for their opponents to inflate their own TBP. In the previous example, if team A realized their predicament and in their final two matches scored 30 points for their opponents, winning each match by a score of 170 - 30, they would rank above team B. Are team A's actions to be encouraged, or is this not gracious professionalism?

Several new TBP methods have been proposed, but it is uncertain which new method is preferable. It would be useful to quantify the performance of the current method and the new methods in order to compare them. Enter the concept of a simulator. Given the match data from a real tournament, a simple simulator can test different TBP methods and report the results. Such a simulator is helpful but limited because the absolute quality of any one TBP method cannot be determined.

Consider a tournament as a transformation of an input ranking of teams to an output ranking of teams. For FTC, this transformation includes RP and TBP. To assess the quality of the transformation, the input and output ranking must be compared. However, the true input ranking for a real tournament is largely unknown. To address this problem, this new simulator creates a set of synthetic teams with known scoring potentials (OPR's) and determines a complete and accurate input ranking of this set of teams by ordering their scoring potentials. This simulator also creates a match schedule, simulates the outcomes of those matches, and ranks the teams using a specified TBP method.

To produce statistically significant results, a sufficiently large number of tournaments must be considered. However, data from real tournaments is limited. For example, there are only four data points for the 80-team qualifying rounds that happen at a World Championship level, which is not a sufficient amount of data for statistical analysis. The simulator solves this problem because it is able to generate large numbers of 80-team tournaments. In fact, the simulator can easily generate more tournaments of any size than have taken place in the history of FTC.

The main disadvantage of a tournament simulated by this software library is that it does not fully incorporate a team's varying performance from match to match as seen at a real tournament. This is mitigated by generating a large number of tournaments so that the [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers) is applicable.

Here is an example of the input rankings for 16 synthetic teams created by the simulator. For convenience, the team numbers correspond to the input ranking.

Team Number |  RP  | TBP | MP | OPR
------------|------|-----|----|-----
1           |     0|    0|   0| 240
2           |     0|    0|   0| 229
3           |     0|    0|   0| 228
4           |     0|    0|   0| 191
5           |     0|    0|   0| 186
6           |     0|    0|   0| 184
7           |     0|    0|   0| 184
8           |     0|    0|   0| 165
9           |     0|    0|   0| 161
10          |     0|    0|   0| 160
11          |     0|    0|   0| 148
12          |     0|    0|   0| 138
13          |     0|    0|   0| 121
14          |     0|    0|   0| 111
15          |     0|    0|   0|  60
16          |     0|    0|   0|  23

And here's an example of the output rankings, or the final rankings after all the qualification matches have been played -- each team has played five matches:

Team Number |  RP  | TBP | MP | OPR
------------|------|-----|----|-----
4           |    10| 1430|   5| 191
1           |    10| 1372|   5| 240
3           |     6| 1611|   5| 228
7           |     6| 1559|   5| 184
6           |     6| 1427|   5| 184
2           |     6| 1425|   5| 229
5           |     6| 1406|   5| 186
14          |     6| 1264|   5| 111
11          |     6| 1259|   5| 148
8           |     6| 1221|   5| 165
9           |     6| 1173|   5| 161
10          |     2| 1540|   5| 160
12          |     2| 1307|   5| 138
13          |     2| 1142|   5| 121
15          |     0| 1011|   5|  60
16          |     0|  813|   5|  23

Looking at the above rankings, a transformation has occurred between the input and output rankings. The method chosen to assess the quality of this transformation is the [root-mean-square deviation](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSD) of the differences D<sub>i</sub> between each team's input and output ranking, calculated using the following equation:

<p align="center">
  <img src="https://github.com/ftc9899/tournament-sim/blob/master/images/rmsd.png?raw=true" alt="RMSD equation">
</p>

Note that the RMSD is a type of standard deviation and follows the [empirical rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule) (the 68-95-99.7 rule). For example, 68% of teams will experience an absolute difference in ranking less than or equal to the RMSD.

In general, the lower the RMSD, the higher the fidelity of the transformation.

### Algorithm Overview

The simulator is written in Python. In order to simulate tens of thousands of tournaments in a relatively short period of time, speed was a priority. The slowest part of the algorithm by far is creating the match schedule, which follows the official algorithm as closely as possible while also being as fast as possible.

#### Generate Teams

This algorithm generates the specified number of teams, each with a scoring potential following a normal distribution generated by NumPy. The distribution has an average that varies based on the tournament size; the standard deviation and range for all tournament sizes follow the 2019 Houston World Championship OPR distribution, which approximated a normal distribution.


#### Create Match Schedule

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

The schedule is populated with teams match by match. As each team is chosen for a given match, the scheduler checks that the match still follows the pairing uniformity rules with the proposed team. If the proposed team causes the match to violate the rules, a different team is selected. The scheduler limits the number of attempts that can be made to find a suitable team, so that if an unusable match schedule has been produced and the scheduler has "painted itself into a corner", the current schedule is abandoned and the scheduler starts over.

#### Simulate the Qualification Matches

After a match schedule has been created, an alliance's score in a given match is calculated by summing the scoring potential of both teams. To simulate the real-life variance of a team's score from match to match, each team's score in a given match is varied by ±10%. When the winner and loser of a match have been determined, RP and TBP are assigned accordingly. (Note: for the 'OPR' TBP method, the team's scoring potential (without variance) is added after each match.)

To simulate the effects of scarcity as a game feature, the user can specify a ceiling for the total match score.  If the in-progress match score reaches the ceiling, the teams score at a reduced rate for the remainder of the match. The theoretical point at which the match score exceeded the ceiling is determined by scaling the two reported alliance scores by the same factor. After being scaled, the alliance scores sum to the ceiling. Then, each alliance receives 50% of the additional points they would have scored.

To simulate the effects of winner-take-all as a game feature, the user can specify a proportion of the alliance score that is affected by a winner-take-all feature. It is assumed that the stronger alliance will claim more points from any winner-take-all features. Accordingly, the winning alliance's score is increased by the specified proportion, while the losing alliance's score is decreased by the specified proportion.

There is no explicit algorithm to simulate the effects of defense; this was a deliberate choice. Defense tends to reduce the scores of both alliances, which subsequently reduces the amount of TBP gained from a match. Therefore, there is less motivation for a team to play defense during the qualification matches than during the elimination rounds. Additionally, few teams practice defensive tactics enough to be effective. When defense is attempted, it can be very successful or it can result in penalties assessed against the defending team. Given these factors, any real-world effects of defense are accounted for by the ±10% variance that is applied to each team's scoring potential in every match.

## Results

For several tournament sizes, six TBP methods were tested: losing alliance score (the current method), sum of both alliances' scores, your alliance's score plus the losing alliance's score, your alliance's score, your team's OPR, and randomly generated TBP. The first four methods were chosen because they were proposed and supported by the FTC community. OPR was included as a basis for comparison because it represents the ideal TBP method. Randomly generated TBP is also a basis for comparison because it represents a null TBP method. For each TBP method, the average RMSD between the input rankings and the output rankings of all the teams for 10,000 tournaments was calculated, a total of 4.2 million tournaments. The RMSD represents the average input/output difference in ranking for each team in a given tournament.

These initial tournaments were run without incoporating scarcity or winner-take-all features. The table below shows the results for all teams. The leftmost two columns indicate the tournament type, while the other columns indicate the corresponding average RMSD for each TBP method.

Teams |Matches per Team|Random|Current| Sum  |U+Lose|Yours | OPR
------|----------------|------|-------|------|------|------|-----
16    |5               |3.415 |2.916  |2.836 |2.773 |2.731 |2.462
24    |5               |5.313 |4.518  |4.406 |4.328 |4.293 |3.939
32    |5               |7.222 |6.150  |6.017 |5.903 |5.872 |5.425
32    |6               |6.722 |5.774  |5.649 |5.561 |5.494 |5.136
40    |8               |7.583 |6.578  |6.466 |6.394 |6.324 |6.023
40    |9               |7.188 |6.276  |6.162 |6.091 |6.053 |5.746
80    |9               |14.864|13.025 |12.816|12.722|12.612|12.090

Note that the RMSD increases as the number of teams increases (for the same number of matches) and decreases as the number of matches increases (for the same number of teams). This indicates that the RMSD can be used to quantify the effect of the number of matches per team on tournament outcomes. Regardless of the tournament configuration, the "current" method has the highest RMSD, followed by "sum", "u_plus_lose", and "yours", respectively.

![Graph of the data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_all_teams.png?raw=true)

Using the TBP method of OPR, any differences in a team's input and output rank are due to RP alone. This is because teams with identical RP will have an output rank order that matches their input rank order. The OPR method can be considered 100% ideal. On the other end of the spectrum, the random method represents no deliberate effort to rank teams and can be considered 0% ideal. A representative percentage on a scale from 0 - 100% can be determined for all the other TBP methods:

<p align="center">
  <img src="https://github.com/ftc9899/tournament-sim/blob/master/images/idealness.png?raw=true" alt="Idealness equation">
</p>

The idealness of a given method for a given tournament size and number of matches per team was calculated by subracting it's RMSD r from the corresponding random RMSD R<sub>random</sub> and dividing by the difference between the random RMSD and the corresponding OPR RMSD R<sub>OPR</sub>.

![Idealness of different methods for different tournaments sizes: all teams](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_percent_all_teams.png?raw=true)

In a tournament, the top four teams (according to the output rankings) become the alliance captains and have the greatest influence on the tournament's outcome. Tracking only the top four teams (according to the input rankings) and doing the same analysis produces data that has key differences:

Teams |Matches per Team|Random|Current| Sum  |U+Lose|Yours | OPR
------|----------------|------|-------|------|------|------|-----
16    |5               |3.233 |2.675  |2.515 |2.428 |2.377 |2.056
24    |5               |4.802 |3.905  |3.578 |3.520 |3.465 |3.049
32    |5               |6.404 |5.158  |4.675 |4.579 |4.535 |4.004
32    |6               |5.680 |4.670  |4.235 |4.134 |4.089 |3.675
40    |8               |5.646 |4.700  |4.343 |4.323 |4.203 |3.878
40    |9               |5.246 |4.421  |4.014 |3.987 |3.954 |3.600
80    |9               |9.210 |7.515  |6.767 |6.770 |6.629 |6.178

Note that the RMSD's for these teams are lower than for all teams and are less sensitive to the number of teams. However, these RMSD's decrease more sharply between the different TBP methods.

![Graph of the additional data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_top_4.png?raw=true)

Comparing the top 4 teams to all teams, the idealness of the "sum", "u_plus_lose", and "yours" TBP methods has increased, while the idealness of the current TBP method has _decreased_, creating a significant disparity between the current method and the other methods.

![Idealness of different methods for different tournaments sizes: top 4 teams](https://github.com/ftc9899/tournament-sim/blob/master/images/vanilla_percent_top_4.png?raw=true)

After the initial data was collected, the additions of scarcity and winner-take-all features were tested independently. The graph below shows the effect of a low score ceiling (i.e. a high scarcity scenario) on TBP for all teams. Each tournament had a ceiling equal to four times the average team OPR. In this configuration, teams were affected by the ceiling in about 50% of matches, according to match statistics. This is an extreme case because scarcity has rarely been a factor in qualification matches in past FTC games, even at the World Championship level. When compared to the previous results for all teams, scarcity appears to significantly reduce the idealness of the current TBP method, while the other methods are relatively unaffected.

![Idealness of different methods in a high-scarcity scenario: all teams](https://github.com/ftc9899/tournament-sim/blob/master/images/low_ceiling_all_teams.png?raw=true)

For the top 4 teams, a high scarcity game causes the idealness of the current method to decrease by 5-15 percentage points as compared to a game where scarcity is not a factor. The other methods are still relatively unaffected.

![Idealness of different methods in a high-scarcity scenario: top 4 teams](https://github.com/ftc9899/tournament-sim/blob/master/images/low_ceiling_top_4.png?raw=true)

The graph below shows the effect of a relatively large winner-take-all proportion (0.3) on TBP for all teams. This is also an extreme case because winner-take-all elements of previous FTC games have not contributed this large of a proportion to an alliance's final score. When compared to the initial results for all teams, winner-take-all game elements do not significantly change the results.

![Idealness of different methods in an extreme winner-take-all scenario: all teams](https://github.com/ftc9899/tournament-sim/blob/master/images/extreme_wta_all_teams.png?raw=true)

For the top 4 teams, a game with extreme winner-take-all elements also does not significantly change the results.

![Idealness of different methods in an extreme winner-take-all scenario: top 4 teams](https://github.com/ftc9899/tournament-sim/blob/master/images/extreme_wta_top_4.png?raw=true)

The following two graphs represent tournaments where the game has a high score ceiling (low scarcity) and a relatively small winner-take-all proportion (0.1). The high ceiling was the same for all tournament sizes: four times the OPR of a team that is one standard deviation above the mean at a World Championship. These added elements did not change the results significantly compared to the initial results.

![Idealness of different methods in a low-scarcity, realistic winner-take-all scenario: all teams](https://github.com/ftc9899/tournament-sim/blob/master/images/all_factors_all_teams.png?raw=true)

The story is the same for the top 4 teams: the added elements did not change the results significantly compared to the initial results.

![Idealness of different methods in a low-scarcity, realistic winner-take-all scenario: top 4 teams](https://github.com/ftc9899/tournament-sim/blob/master/images/all_factors_top_4.png?raw=true)

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

### Recommendations

It has been observed that the RP system rewards both the offensive and defensive capability of an alliance. Offense scores the points required to win a match, while defense can slow down a strong opponent enough to win a match. Contrary to this, the only capability rewarded by the current TBP method is the audacity and the ability to score for one's opponent. And finally, the data shows that rewarding strength of schedule through TBP (the current method) is not as effective as rewarding offense (i.e. receiving your alliance's score as TBP each match). This assertion is still true for games that incorporate scarcity and/or winner-take-all features. Therefore, adopting the TBP method of each alliance receiving TBP equivalent to their alliance's score in each match is recommended.
