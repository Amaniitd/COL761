Contribution of Team Members
1. Sohail Khan (2021MCS2153) :-  33%
2. Aman Kumar (2019CS10324) :- 33%
3. Nitin Kumar (2021MCS2142) :- 33%

Task 1:
1. Size of node embeddings for node is 12
2. For each timestamp each node aggregates the node embeddings of its neighbours
3. Current embeddings of node is concatenated with aggregated embeddings
4. Then this is passed through an RNN that gives the new user embeddings
5. Then new emebddings are passed through MLP that predicts the traffic at that junction

Task 2:
Similar approach is implemented as mentioned in below link:-
https://medium.com/stanford-cs224w/predicting-los-angeles-traffic-with-graph-neural-networks-52652bc643b1