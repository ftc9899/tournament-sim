# tournament-sim

![9899 logo](https://avatars1.githubusercontent.com/u/36021491?s=100&v=4)

Black Diamond Robotics, FTC Team 9899

## Abstract

There is a desire to improve the FIRST Tech Challenge tiebreaker point (TBP) system. This paper introduces a simulator which can help to quantify proposed TBP methods. The simulator does not rely on any external data and is able to generate a large volume of synthetic tournament data that reflects actual tournament data. It applies a root-mean-square deviation analysis to quantify each proposed TBP system. Based on the results, a TBP system where alliances receive their own score appears to be a promising method.

## Introduction

FIRST Tech Challenge (FTC) is an international high school robotics competition put on by the FIRST organization. Teams build robots to compete in tournaments within year-long seasons. An FTC tournament consists of two major parts: the qualification matches and the elimination rounds. In the qualification matches, each team participates in an equivalent number of two versus two matches. Teams are paired with a random partner for each match. The match schedule is set up such that no two teams are paired up more than once or are opponents more than once.

At the conclusion of each match, teams receive ranking points (RP) and tiebreaker points (TBP) dependent on the outcome of said match. The two winning teams (winning alliance) receive two RP, while the two losing teams (losing alliance) receive zero RP. In the event of a tie, all four teams receive one RP.

The current TBP method attempts to rank teams with "tougher" schedules (i.e. they played against "better" opponents) above teams with "easier" schedules. This is accomplished by all four teams receiving TBP equivalent to the losing alliance's score in each match the teams play. At the end of the qualification matches, teams are ranked by RP. The inevitable ties in RP are broken by the aptly-named TBP.

It should be noted that the four highest-ranked teams at the end of the qualification matches become the captains of the four alliances that compete in the elimination rounds. To finish at the top, a team needs to both win as many matches as possible and have the most TBP of any other team with the same number of wins. Therefore, TBP are very important for determining the final ranking of the teams with the most RP.

What is the motivation to explore new TBP methods? Because of its perceived unfairness and dependence on the performance of other teams, there has been longstanding frustration with the current TBP method. On top of that, it causes the controversial behavior of a team scoring for their opponents to inflate their own TBP. Even worse, there have been accusations of cheating with the intent to manipulate TBP.

## Background

Several new TBP methods have been proposed, but it is uncertain which new method is preferable. It would be useful to quantify the performance of the current method and the new methods in order to compare them. Enter the concept of a simulator. Given the match data from a real tournament, a simple simulator can test different TBP methods and report the results. Such a simulator is helpful but limited because the absolute quality of any one TBP method cannot be determined.

Consider a tournament as a transformation of an input ranking of teams to an output ranking of teams. For FTC, this transformation includes RP and TBP. To assess the quality of the transformation, the input and output ranking must be compared. However, the input ranking for a real tournament is largely unknown. To address this problem, this new simulator creates a set of synthetic teams with known scoring potentials (OPR's) and determines a complete and accurate input ranking of this set of teams by ordering their scoring potentials. This simulator also creates a match schedule, simulates the outcomes of those matches, and ranks the teams with a specified TBP method.

To produce statistically significant results, a sufficiently large number of tournaments must be considered. However, data from real tournaments is limited. For example, there are only four data points for the 80-team qualifying rounds that happen at a World Championship level, which is not a sufficient amount of data for statistical analysis. The simulator solves this problem because it is able to generate large numbers of 80-team tournaments. In fact, the simulator can easily generate more tournaments of any size than have taken place in the history of FTC.

The main disadvantage of a tournament simulated by this software library is that it does not fully incorporate a team's varying performance from match to match as seen at a real tournament. This is mitigated by generating a large number of tournaments so that the law of large numbers is applicable.

Here is an example of the input rankings for 16 synthetic teams created by the simulator:

Team Name |  RP  | TBP | MP | OPR
----------|------|-----|----|-----
1         |     0|    0|   0| 240
2         |     0|    0|   0| 229
3         |     0|    0|   0| 228
4         |     0|    0|   0| 191
5         |     0|    0|   0| 186
6         |     0|    0|   0| 184
7         |     0|    0|   0| 184
8         |     0|    0|   0| 165
9         |     0|    0|   0| 161
10        |     0|    0|   0| 160
11        |     0|    0|   0| 148
12        |     0|    0|   0| 138
13        |     0|    0|   0| 121
14        |     0|    0|   0| 111
15        |     0|    0|   0|  60
16        |     0|    0|   0|  23

And here's an example of the output rankings, or the final rankings after all the qualification matches have been played -- each team has played five matches:

Team Name |  RP  | TBP | MP | OPR
----------|------|-----|----|-----
4         |    10| 1430|   5| 191
1         |    10| 1372|   5| 240
3         |     6| 1611|   5| 228
7         |     6| 1559|   5| 184
6         |     6| 1427|   5| 184
2         |     6| 1425|   5| 229
5         |     6| 1406|   5| 186
14        |     6| 1264|   5| 111
11        |     6| 1259|   5| 148
8         |     6| 1221|   5| 165
9         |     6| 1173|   5| 161
10        |     2| 1540|   5| 160
12        |     2| 1307|   5| 138
13        |     2| 1142|   5| 121
15        |     0| 1011|   5|  60
16        |     0|  813|   5|  23

Looking at the above rankings, a transformation has occurred between the input and output rankings. The method chosen to assess the quality of this transformation is the [root-mean-square deviation](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSD) of the differences between each team's input and output ranking (D<sub>i</sub>), calculated using the following equation:

<p align="center">
  <img src="https://github.com/ftc9899/tournament-sim/blob/master/rmsd.png?raw=true" alt="RMSD equation">
</p>

Note that the RMSD is a type of standard deviation and follows the [empirical rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule) (the 68-95-99.7 rule). Specifically, 68% of teams will experience an absolute difference in ranking less than or equal to the RMSD.

In general, the lower the RMSD, the higher the fidelity of the transformation.

### Algorithm Overview

In order to simulate tens of thousands of tournaments in a relatively short period of time, speed was a priority. The slowest part of the algorithm by far is creating the match schedule, which follows the official algorithm as closely as possible while also being as fast as possible.

#### Generate Teams

This algorithm generates the specified number of teams, each with a scoring potential following a normal distribution generated by NumPy. The distribution has an average, standard deviation, and range that follow the 2019 Houston World Championship OPR distribution, which approximated a normal distribution. 

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

After a match schedule has been created, an alliance's score in a given match is calculated by adding the scoring potential of both teams. To simulate the real-life variance of a team's score from match to match, each team's score in a given match is varied by ±10%. When the winner and loser of a match have been determined, RP and TBP are assigned accordingly. For the 'OPR' TBP method, the team's scoring potential (without variance) is added after each match.

## Results

For several tournament sizes, four TBP methods were tested: losing alliance score (the current method), sum of both alliances' scores, your alliance's score, and your team's OPR. The first three methods were chosen because they were proposed and supported by the FTC community. OPR was included as a basis for comparison because it represents the ideal TBP method. For each TBP method, the average RMSD between the input rankings and the output rankings of all the teams for 10,000 tournaments was calculated, a total of 2.8 million tournaments. The RMSD represents the average input/output difference in ranking for each team in a given tournament.

The table below shows the results for all teams. The leftmost two columns indicate the tournament type, while the rightmost four columns indicate the corresponding average RMSD for each TBP method.

Teams |Matches per Team|Current| Sum  |Yours | OPR
------|----------------|-------|------|------|------
16    |5               |2.972  |2.876 |2.781 |2.489
24    |5               |4.600  |4.477 |4.360 |4.010
32    |5               |6.195  |6.063 |5.901 |5.437
32    |6               |5.798  |5.682 |5.549 |5.177
40    |8               |6.586  |6.461 |6.340 |6.003
40    |9               |6.285  |6.165 |6.039 |5.761
80    |9               |13.043 |12.812|12.630|12.111

Note that the RMSD increases as the number of teams increases (for the same number of matches) and decreases as the number of matches increases (for the same number of teams). This indicates that the RMSD can be used to quantify the effect of the number of matches per team on tournament outcomes. Regardless of the tournament configuration, the "current" method has the highest RMSD, followed by "sum" and "yours", respectively.

![A nice graph of the data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/tbp_comparison.PNG?raw=true)

Using the TBP method of OPR, any differences in a team's input and output rank are due to RP alone. This is because teams with identical RP will have an output rank order that matches their input rank order. The contribution of a TBP method to the RMSD is the difference in RMSD from the OPR method to the TBP method, which is expressed as a percent in the graph below.

![Another graph](https://github.com/ftc9899/tournament-sim/blob/master/tbp_percent_comparison.PNG?raw=true)

In a tournament, the top four teams (according to the output rankings) become the alliance captains and have the greatest influence on the tournament's outcome. Tracking only the top four teams (according to the input rankings) and doing the same analysis produces data that has key differences:

Teams |Matches per Team|Current| Sum  |Yours | OPR
------|----------------|-------|------|------|------
16    |5               |2.822  |2.614 |2.525 |2.132
24    |5               |4.078  |3.740 |3.612 |3.219
32    |5               |5.255  |4.766 |4.588 |4.066
32    |6               |4.732  |4.349 |4.174 |3.731
40    |8               |4.731  |4.330 |4.268 |3.888
40    |9               |4.379  |4.032 |3.899 |3.620
80    |9               |7.586  |6.815 |6.569 |6.162

Note that the RMSD's for these teams are lower than for all teams and are less sensitive to the number of teams. However, these RMSD's decrease more sharply between the different TBP methods.

![A nice graph of the additional data from the above table](https://github.com/ftc9899/tournament-sim/blob/master/top_4_tbp_comparison.PNG?raw=true)

Comparing the top 4 teams to all teams, the contribution of a TBP method to the RMSD is magnified, as shown in the graph below.

![Yet another graph](https://github.com/ftc9899/tournament-sim/blob/master/top_4_tbp_percent_comparison.PNG?raw=true)

## Conclusions

Here is what can be concluded from this data:
- In these simulations, tiebreaker points contributed up to 24% of the difference between a team's input and output ranking
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