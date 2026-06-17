### Outstanding issues
**Pope limitation**
- We are exploring token level grounding but the POPE dataset does not give us freeform generation to assess how token level grounding is done. We do not do token level grounding
- 
**Problems with other datasets**
- If we find VQA datasets that have some elements of hallucination in evaluation we also get a problem in trying to detect hallucinations in cases where we do not have a proper dataset:
	- Example suppose we have a dataset with 5 items, but then we have only 3 labelled items. If our free form generation describes 2 of the items not labelled in the dataset then we can conclude we hallucinated 2. 
- 
**Contrastive decoding baseline**
- Our closes signal looks like a  contrastive decoding signal: The null/real counterfactual. is mostly from contrastive decoding. So what do we do for this? What are we adding that is new or Unique?
**VAUQ Review**
- What are the main techniques here and how is evaluation done?
**Other Lit review Questions**
- What are the closes papers we have to our methodology?
- Can we do a review of each of the papers that are close or foundational to what we are doing?
**General Questions:**
- How do we get a signal? Is that Unique? What literature sources can we look into? 
- How is vlm and llm self evalualtion done? 
