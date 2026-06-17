Note there is a current problem with Figure 2 (The diagram showing the Fedprop process). We need to redraw it.

Our primary contribution is a communication-free algorithm:
- We illustrate our results by showing we can attain significant improvement in the results when we have FP Without incurring communication cost
	- This is easy to demonstrate as a recovery in performance where we show that in the case where there was initial performance degradation, we have significant results recovery.
		- We can show the recovery percentage for the L1 & L2 results
		- This recovery can be improved by RPE (Random positional encoding)
		- Topology and Amazon problem
			- We however need to show that there are datasets where this performance degradation between Central/Full and zero hop is not significant. For These circumstances, our results are not significant. 
			- This kind of datasets also then invite a broader Question into the impact of topology in the performance of GNNs in federated graph learning:
			- How does topology affect? Is it only in node classification? How is performance affected for other tasks? 
- In addition to recovery we need to show how our results compare to the SOTA techniques: In this case we have FedGCN/FedGAT and FedSage:
	- Here we can compare the raw performance with ours and show that our results are competitive with their results.  This is what we did initially and still got some criticisms
	- We can also compare them and illustrate them in the context if performance/Communication trade-off and show where we stand in the chart
- Finally we can also review the reconstruction errors:
	- This was recommended by the reviews at some point which is: Assuming I make a certain claim about the generation of new data, can I illustrate the recovery for the features in the new data. i.e. show that after n propagation steps, we have recovered X% of the data? i.e. similarity or some other error metrics:
		- How does partition regime affect the reconstruction error? How does IID and non-IID regime affect reconstruction error?
		- How does reconstruction error affect performance on the down stream task: In this case node classification
		- How do different propagation algorithms affect the reconstruction features?
	- A more interesting and important task is to actually evaluate the theoretical formulation. Can we show that the reconstruction error is a function of the graph topology and show that more heterolytic graphs have higher reconstruction errors? Or that this partitioning scheme would work diffe3rently for different datasets with different graph topology ro partitioning regimes? 
- We proceed to illustrate a a few additional things such as:
	- Model agnostic framework: This system works for both GAT and GCN structures
	- Robustness to the number of clients: We increase the number of clients and show how the performance is preserved by the fedprop algos (For this we have to choose the datasets)
	- We show how this is immune to changes in partition regimes: For instance we can set IID partitions like: 0.1/1/10/100/1K/10K and show how performance changes across that. 
		- This though raises an additional level of analysis: What does changing the partition regime mean? How can we describe it in terms of graph structure? What are we doing to the graph as we change the partitioning regime?

### Issues on Experimental settings:
**Datasets**
So far we ahve solid and consistent results on:
- Planetoid (Cora/Citeseer/Pubmed)
- OGBN Arxiv
For these datasets we have pretty consistent results in how fed prop recovers performance and how we remain competitive with other SOTA models.

Problems with other datasets
**Other homophilic datasets**
- OGBN products seems too big to run when I initially tried. I am not sure if I should trye it and what it would benefit me: Primarily it might be good for showing the algorithm scales to bigger datasets. 
- Amazon computers and photos: These are still homophylic: Problem with these is that the gap between the Zero hop and full is already very thin so that we do not have any meaningful recovery in between when we use fed prop. 
	- This is also an opportunity to understand and explore topology and assumptions that graph learning (GCNs & GATs) makes that breaks when topology changes.
- The pressure to add the amazon datasets is because we need to show that this technique or approach works even for non citation based datasets.
**Heterophylic**:
The problem with these datasets is some weird inconsistence: 
- In these case, zero hop do not give bad performance. If anything in most cases zero hop provides performance that is better than full graph data. 
- This makes it difficult to say what FedProp is doing:
	- Ideally we would need it to show that the recovery of performance is not as good in Heterophilic as it is in homophylic graphs. 
	- The natural thing to day here is that although our solution is tailored for homophylic graphs, the problem we solve does not exist in heterophylic settings. An example is that we do not have a performance degradation to recover from in the first place. 
	- This is also an opportunity to understand and explore topology and assumptions that graph learning (GCNs & GATs) makes that breaks when topology changes. 


**L1/L2**
Our algorithm makes certain assumptions about what we know. 
- The most natural settings are such that we know 1 hop neighbourhood structure even though we have no features. In this setting we get reasonable recovery in most of our results however we are still preforming slightly less than the SOTA on most of the datasets and experimental settings
- In 2 hop neighbourhood however, We have significantly between performance and competitive with SOTA in both models (GCN & GAT), however, we have to make the assumption that the 2 hop structure will be provided and this provides an additional communication issue/cost and privacy implications.  

**Partitioning**
We have a small problem here:
-  We use partitions of 1/10 and 10K as the bets parameters
- The natural expectation is that performance in higher in IID than non-IID settings but this is not always true:
	-  Check how the performance of Fedprop full changes between IID and non-IID (So far the difference is not really significant which shows that the difference in performance is due to feature propagation)
		- We may need to show how the reconstruction error varies between IID and non-IID results.
	- We only added \beta=10 because for PubMed the performance at beta =1 was terrible even for full data. 


**SOTA comparison**
- In this case the big question is do we re-run the sota experiments that we can or do we just run ours and pick the sota results from literature? 
- The FedGCN codebase allows us to run it
- I think I can make changes to the fedGAT codebase to be able to run it but it will need some modifications. 
	- is it worth the effort?
- For FedSage and Fedsage+ the partitioning scheme used is different from ours so we can do an head to head comparison of the results. 



**Possible next Steps**
1) Based everything I currently have: No new experiments and no new analysis put together a complete paper. In this case, we are re-organizing and editing. 
2) Identify all the gaps that we have. i.e. what else can we add then define the next scopes
3) Determine what goes to the TMLR Journal paper and what ends up being a separate paper. 
So we will end up with:
- P1 - > A complete version of the paper based on what we currently have
- P2: a improved version on the paper with more analysis and more results
- P3: A follow up paper. 


