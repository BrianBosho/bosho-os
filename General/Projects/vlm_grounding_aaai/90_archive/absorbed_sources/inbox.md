Key Ideas and things I have been exploring:
1) Core Question: Can we measure the amount of visual information at different stages of the VLM:
	1) How much visual information is there in the clip encoder output?
	2) How much goes to the projector?
	3) How does the LLM Process the information to generate the answer?
2) How much does the LLM depend on the visual input to answer the question?
	1) Checking similarity representational between the hidden state of generated tokens and the image patch hidden states at L32
	2) Do we need to inspect the earlier layers of the transformers to check this representational similarity?
	3) What about the counterfactuals: 
		1) Can we identify support patches?
		2) Can we change the support patches? 
3) When we measure the information above? 
	1) How do we measure it?
		1) Can we tell the amount of semantic information? For example can we tell quantitatively that one image has dog and another has a cat? 
		2) Initially we created a basis using samples from the embedding matrix or from a dataset of images and their clip projections: We project hidden states there and embeddings and check if the directions of the basis represents semantic information directions. 
		3) What is the best way to determine a basis and null basis? 
	2) What Can we do with the measured information?
	3) How do we evaluate the measured information?


**On the 3 step formulation** 
Can we really approach the paper with the 3 stage formulation? The 3 stages were initially meant to be exploratory.. SO now we should have a coherent thing that we say we have this signal/ We can still explore the 3 steps and eventually get or narrow down to one single signal or approach of measuring visual grounding. Is that clear? How do we proceed from here? 
Can we actually define the object more clearly and not state the 3 stage or 3 phase approach as a core methodology or contribution? Maybe just as part of the techniques we are exploring. 


**Vault Re-organization**: We need a better structure with:
- No redundancy
- Clear organization and order of information
- Clear separation of concerns; i.e. tasks from ideas from records (Of what has been done), and the next actions and execution steps and so on. 
- What other principle and ideas can we use to organize this vault: 


**Challenge with current paper and recommendations:**
1) Problem with Pope
2) 

