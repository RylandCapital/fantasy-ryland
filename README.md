# fantasy-ryland

INTRO:

Fantasy-Ryland is a automated machine learning pipeline for fantasy sports. check out our twitter @shippersdfs

Currently Fanduel Mainline (fd_mainline) is our premier NFL pipeline and will be under construction as we add the newest
functionality and feature construction techniques that we developed in our premier NHL model -> Fanduel Get Pucks Deep (fd_gpd). 

Fanduel Mainline will be offline and underconstruction until the start of the 2023-24 season. All our pipelines are currently built for 
large slates and mostly for GPPs, so there isnt much left to do NFL wise until 2023-24. 

We are currently sharpening our NHL model (GPD) on fanduel in the nickel and quarter contests. It has done amazingly. In only 5 slates
we have won one contest and placed multiple entries in the top 10 in 2 others.. the hit rate has been phenomal. 

TOP LEVEL METHODOLOGY:

Our approach is a team based approach. we have collected player data (fantasylabs) from 60 or so historical slates. from there....
1. Build millions of teams from these historical slates 
2. Flag each team a 1 or 0 (1 = would have one the GPP, 2 = would have lost the GPP)
3. Build between 100-300 custom TEAM LEVEL FEATURES (i.e. team projected points, team time on ice, salary variance etc etc...)
4. Train the algorithm to learn which teams are winners and which are losers (Dataiku for our ML visualizations)

5. On gameday, we then feed the algorithm 5 million teams to chose from, optimize a contest specific ticket of teams based on the models output
6. Upload and have a rum and coke while I watch how we do. 

all the code I use will always be available here along with the historical datasets I used to build my teams. 

any questions->
email: rylandmathews1@gmail.com


