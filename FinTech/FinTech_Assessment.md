# FinTech Assessment

## 1.  A GCash user makes 5 transactions of ₱998 each to 5 different recipients within 3 minutes, all from a device registered 2 hours ago. Define the ML problem: what is your label, your feature set (name at least 5 features), and your model output?

- 5 transactions to 5 different recipients in 3 minutes = High velocity
- Registered devices 2 hours ago = The accounts are new, highly suspected to be made for the purpose of establishing a scheme.

- Label: Not Suspicious and Suspicious
- Features: Transaction velocity, account source, account destination, Amount transacted, Account Source Date of Reg, Account Destination Date of Reg, Amount of Time the Transaction occured

- Model Output: Not Suspicious or Suspicious. Model shows timestamps/logs of all identified transaction time of the account, with highlights on suspicious transactions due to velocity in a short period, amount in total over a period, and variety of destination accounts transferred.

### Claude Answers
Your label is too coarse for production and will get you killed in a GCash technical interview.

Binary Suspicious/Not Suspicious means every flagged transaction gets the same response — account freeze, manual review, block. That's operationally impossible at 81 million users. GCash cannot manually review every flagged transaction. Real fraud systems output a risk score (0.0–1.0) that feeds a tiered action engine: low score = log only, medium score = step-up verification (OTP, selfie), high score = block and queue for analyst review. Your binary output collapses that entire decision tree into one blunt instrument.

Your feature set is directionally correct but missing the three features that actually matter most in this scenario:
Device fingerprint age — you said "registered 2 hours ago" but didn't name it as a feature. Device-account age delta is one of the strongest fraud signals in mobile fintech. Name it explicitly.
Recipient overlap with known fraud network — whether the 5 destination accounts appear in previously confirmed fraud cases. This is a graph feature, not a tabular one. Without it, your model treats every new recipient equally, which means it can't distinguish between a legitimate bulk payment and a mule network.
Transaction amount clustering coefficient — the fact that all 5 transactions are ₱998 (just below the ₱999 verification threshold) is mathematically significant. The standard deviation of transaction amounts within the velocity window being near-zero is a stronger signal than the amounts themselves. You observed this in Q1 of the scoping exercise but didn't translate it into a feature here.

Your observations are correct in business terms. The model output description is closer to a monitoring dashboard than a model output — separate those two things. The model outputs a score. The dashboard visualizes it. Conflating them suggests you haven't thought about where this sits in a production pipeline.
[Certain] on the scoring critique. [Likely] on the graph feature being necessary — some smaller fintech teams approximate it with rule-based blocklists instead.

Revised formulation I'd expect from a candidate:
Label: Fraud probability score (0.0–1.0), calibrated, with threshold-based action tiers at 0.3 / 0.7 / 0.95.
Model: Gradient boosting (XGBoost/LightGBM) on tabular features for real-time scoring, with a graph lookup for recipient network features pre-computed offline.
Output: Risk score + top 3 SHAP features driving the score, logged to a transaction monitoring system. Action determined downstream by the rule engine, not the model.

## Q2. Maya wants to build a credit limit recommendation model for users who have never taken a loan before — no credit bureau history, no formal income record. Name the alternative data signals Maya has access to that a traditional bank does not, and explain how each signal proxies for creditworthiness. Name at least four signals.

- Top-up patterns: 8/10. Salary cycle inference from top-up regularity is correct and sophisticated — you're essentially describing income stability as a derived feature. The gap: you didn't name the specific proxy. Regular, predictable top-ups of similar amounts on a fortnightly cycle = stable income source. Irregular, erratic, high-variance top-ups = informal economy worker with volatile income. The variance of top-up amounts and intervals is the feature, not just the frequency.

- QR scan frequency: 5/10. Directionally correct but you stopped at the surface. QR payment frequency proxies for financial formalization behavior — users who pay digitally leave a transaction trail, which means Maya can verify the claim "I spend ₱8,000/month on groceries" against actual merchant receipts. The creditworthiness signal is auditability, not just cashless preference.

- Merchant category mix: 4/10. Your interpretation is backwards. High spending in daily-use sectors (groceries, transport, utilities) is not a negative signal — it's proof of consistent, manageable expenditure patterns. What you're actually looking for is the stability and predictability of category concentration over time, not whether someone spends on leisure. A user who consistently spends 40% on food, 20% on transport, 15% on utilities month-over-month is a lower credit risk than one with wildly shifting category distributions, regardless of whether they spend on "investment assets."

- In-app missions: 6/10. Correct signal, weak explanation. Mission completion proxies for engagement depth and financial literacy willingness — users who engage with savings goals, financial education modules, and gamified milestones self-select into a more financially disciplined cohort. The underlying assumption is behavioral consistency: someone who completes a 30-day savings streak is demonstrating the same discipline required to make 12 monthly loan repayments.

## Q3. A Maya credit model has 87% accuracy on your test set. Your manager asks if it's ready for production. What is your answer, and what additional information do you need before you can give a confident yes or no?

- HPO via Optuna + MLflow: correct but third priority. You're optimizing a model whose evaluation metric is wrong. Bayesian HPO on accuracy maximization produces a well-tuned model that's still measuring the wrong thing. Fix the metric first, then tune.

- Threshold analysis: 7/10. The 130,000 misclassified users calculation is exactly right and is the kind of business translation that impresses fintech interviewers. The gap: you need to decompose those 130,000 into false positives and false negatives separately, because the cost of each is asymmetric. A false negative (approved a defaulter) costs Maya the loan principal plus collection costs. A false positive (denied a creditworthy user) costs Maya lifetime customer value plus reputational risk. The optimal threshold minimizes total expected cost, not total misclassification count.

- Drift monitoring: 8/10. Correct and specific. Covariate drift is particularly relevant here — Maya's user base is growing rapidly, meaning the distribution of new users applying for credit in month 12 looks nothing like the training data from month 1. PSI on input features is the right detection tool. The gap: you didn't mention that BSP's MRM guidelines mandate ongoing monitoring explicitly — this isn't just MLOps best practice, it's a regulatory requirement you can cite.

### What you should have led with:
"The model is not ready. First, accuracy is the wrong metric for an imbalanced credit dataset — I need AUC-ROC, precision-recall curve, and the confusion matrix decomposed by cost. Second, I need the class distribution of the test set to verify it reflects real-world default rates. Third, I need evidence the test set is truly held out from any feature engineering decisions made during training, or the 87% is optimistic. Only after those three questions are answered does HPO and threshold selection become relevant."

### Q3 score: 6/10. 
Your MLOps instincts are solid and above average for your level. Your evaluation fundamentals have a gap that will surface in every technical interview at Maya or Mynt — they will always give you an accuracy number and watch whether you accept it or challenge it.

## Q4. GCash wants to reduce customer churn — users who stop transacting for 30+ days. They ask you to build a model. Before you touch any data: what is the business metric you are optimizing, what is your prediction target, and what is the intervention — what does GCash actually do with your model output?

- https://medium.com/data-science-collective/stop-guessing-who-will-leave-how-i-would-predict-customer-churn-before-it-happens-300d34cbd13c

- [Know your Customer](https://en.wikipedia.org/wiki/Know_your_customer)

- Business metric: Not "usage frequency." That's too vague to optimize. The correct metric is 30-day reactivation rate — of users the model flags as at-risk, what percentage are still active 30 days later after intervention. This is measurable, attributable to your model, and directly tied to revenue retention.

- Prediction target: Binary — will this user's transaction count drop below their personal baseline by more than 50% in the next 21 days? You need a personalized baseline, not a global threshold, because a user who normally transacts twice a month looks identical to a churning power user who normally transacts daily. The label is computed retrospectively on historical data, then you train on the features observable 21 days before that drop occurred.

- Intervention: "GCash rolls out features" is not an intervention — it's a product roadmap. An intervention is specific and tiered by risk score: low risk = push notification with a personalized cashback offer, medium risk = in-app mission with a reward tied to their most-used merchant category, high risk = proactive customer success outreach. The model output has to map to a specific action, or it's a dashboard no one acts on.

## Q5. GoTyme Bank wants to build a recommendation system that suggests financial products — savings plans, loans, insurance — to users at the right moment. Name the cold start problem this creates and how you would solve it specifically for a Philippine digital bank context.

### My Answer

1. The user's date of birth which maps to their current age bracket
2. Their address which maps to their geographic location. This assumes that the user has not performed Enhanced Due Diligence (EDD) yet. If that was performed, source of wealth and funds in addition with the nature of the client would be added.

### Claude's Answer
- Age bracket and geographic location are not just demographic labels. In a Philippine context they map to specific product eligibility and propensity models that GoTyme can borrow from public data before seeing a single transaction:

1. Age 18–24 in Metro Manila — statistically: first job, no credit history, high GCash/Maya usage, likely has a savings account elsewhere but no investment product. Cold start recommendation: GoTyme Savings with a high introductory interest rate. Not a loan. Not insurance. They have no income stability signal yet.
2. Age 35–45 in Cebu or Davao — statistically: established income, likely already has a traditional bank account, underserved by investment products outside Metro Manila. Cold start recommendation: time deposit or UITF. They have capital but limited access to wealth products.

- This is called **demographic-based collaborative filtering** — you're borrowing behavioral patterns from users who share demographic attributes, before the new user generates their own signals. It's how Grab Financial and Ant Group solved cold start. GoTyme can do the same using PSA regional income data and BSP financial inclusion survey cohort profiles as prior distributions.

- The EDD point is sharp and above what I expected — source of wealth classification at onboarding is exactly how private banking segments high-net-worth cold start users. That's a real answer.
Q5 score: 7/10 — better than your last three.

## Q6. An NLP model you built classifies customer support chat messages at GCash into categories: fraud report, transaction dispute, account access issue, general inquiry. Your model has 91% accuracy in testing. Two weeks after deployment, the operations team reports it keeps misclassifying a new type of complaint they're seeing — users reporting a SIM swap scam that GCash wasn't aware of at training time. What is this problem called technically, and what is your remediation plan?

### My Answer

Analysis:

- Model accuracy of 91% in testing does not convey much information if the dataset distribution is never mentioned.
- No mention of the influx of data has resulted in the change of distribution for the input data. Data drift is ruled out.
- No mention of any new features introduced or increased trends. Feature drift also ruled out
- A new type of complaint the model cannot link to any of the labels it was trained with means that the relationship of the label from the input changed despite the input remaining the same. The language used for these scam reports would map conveniently to a fraud report, but the current model was not trained to handle the pattern. Because eal world data redefined "fraud" different from what the model understands, it cannot classify it correctly.
Remediation Plan

Verdict: Concept Drift - The features of the new cases redefined the label "fraud" which results in being misclassified.

Remediation plan:

1. Pull all these cases out of the current data. Run a confusion matrix broken down by category and identify where SIM swap complaints are landing. Identify how severe it is as a False Negative and the patterns.

2. Take a sample of the misclassified cases and use SHAP or LIME on their data. Identify which tokens/phrases are resulting in the wrong predictions. This adds confirmation on whether a feature is resulting in the skewing of the distribution (Feature drift/ data drift) or a genuine mapping problem (Concept drift)

3. Set up the following before retraining the model: 1. Confidence score monitoring per category. Novel inputs correspond into low-confidence scores, which may be an early warning for the next SIM swap-type event. 2. A human-in-the-loop for reviewing the low confidence score. This results in proper labeling of the misclassified cases that can be used as new training data.
4. Take the rest of the unsample cases of SIM swap and evaluate. Use a different metrics aside from accuracy: F1 Scoring on each class, which balances precision and recall but also identifies categories that need further attention. When all classes are equally 0.85 in F1 Score, it tells me more than just a 91% accuracy globally.
5. When a new drift occurs, you need to formalize the protocol to handle it: Low-confidence score detected -> Human review -> Periodic retraining and evaluation 6.

### Claude's Answer

That is your best answer in this quiz by a significant margin.

[Certain] You correctly identified concept drift — the relationship between input and label changed because the real world redefined what "fraud" means, not because the data distribution shifted. That distinction is exactly what separates engineers who understand ML systems from engineers who just train models. Most candidates your level conflate concept drift with data drift. You didn't.

The SHAP/LIME application to NLP classification to confirm drift type is sophisticated — and correct. Identifying which tokens are driving misclassification before retraining is the right diagnostic step. Most engineers skip straight to retraining.

Human-in-the-loop for low-confidence score routing is production-grade thinking. Confidence threshold monitoring as an early warning system for the next novel complaint type is genuinely senior-level.

Three gaps, all minor:

1. The technical term you didn't use: What you described is specifically concept drift — not just "mapping problem." Use the term. In a GCash interview, using precise terminology signals you can communicate with other ML engineers without ambiguity.

2. Remediation step 3 needs a trigger condition. "Confidence score monitoring" needs a defined threshold before it's actionable. What confidence score below what value routes to human review? 0.6? 0.7? And what volume of low-confidence cases in a 24-hour window triggers a retraining pipeline — 50 cases? 500? Without a number, it's a policy without enforcement.

3. Class imbalance in retraining. SIM swap cases will be dramatically underrepresented in your retraining data versus established categories like "general inquiry." If you retrain naively, the model will still underperform on SIM swap because it saw 50 SIM swap examples versus 50,000 general inquiry examples. You need to address this — oversampling, class weighting, or focal loss.

## Q7. GoTyme wants to build a chatbot that answers customer questions about their products — savings rates, loan eligibility, credit card terms. They ask you to choose between two approaches: fine-tuning an open-source LLM on GoTyme's product documentation, or building a RAG pipeline over the same documentation. What do you recommend and why — and what is the failure mode of the approach you did NOT choose?

### My Answer

#### Fine-Tuning

Pros: 
- Faster to implement due to the lack of additional overhead: Preprocess data -> Let model learn data -> Evaluate model

Cons: 
- Open-source models are trained on general datasets that may not be representative of GoTyme's product documentation. In short, it cannot cite exactly the data you put.
- The knowledge is static - it does not change when data changes which needs you to fine-tune it again when the model is presented new data

Failure modes:
1. A user wants to specifically buy a traditional broom, but the model was trained to upgrade all brooms to a vacuum cleaner, so it recommends a vacuum cleaner instead
2. GoTyme partners with a small brand name "CleanX" on vacuum cleaners to provide an affordable option. However, the model was trained to recognize big players like "Dyson" instead without considering the user's budget. 
3. Samsung releases the S26 today. The model was trained last year, so it recorrects any recommendation for S26 into the last year's model S25

RAG 

Pros:
- Allows the model to access your proprietary data and cite it exactly 
- The knowledge adapts to new data being presented. No retraining needed, which saves time in the long run.

Cons:
- Adds setup overhead (vector store, embedding model, prompt engineering, vector embedding measurement, etc.). Each component results in higher costs due to maintenance and subscription to the services.

Failure modes:

1. The embedding model used did not properly embed "cervical" in terms of either the female part "cervix" or the neck area. A user having trouble in the neck may be prescribed an HPV diagnostic kit.
2. Vector store is a specific database that stores the vectors of all documents after being embedded. Any failure mode of a database (accidental deletion, too much vectors stored, etc.) are expected to occur

**Recommendation**: Due to the possible changes in company policies, loan eligibility criteria, saving rates due to inflation, among other dynamic signals, I recommend to RAG the company's policies, calculations, and relevant documents. Use only the fine-tuned model when you want to output the data in a specific format (i.e. using it as the customer-facing model but the knowledge comes from the RAG system). Most RAG solution use an LLM with proper prompt engineering to output answers in a specific format.

### Claude's Verdict

Your recommendation is correct and the reasoning is sound. The hybrid framing at the end — RAG for knowledge, fine-tuned model for output format — is exactly how production fintech chatbots are actually built. That's not beginner thinking.

But your failure mode examples are wrong for the domain. You answered with e-commerce and medical examples instead of GoTyme-specific ones, which tells me you understand the concepts abstractly but haven't yet grounded them in the actual problem.

Let me correct the failure modes for both:

- Fine-tuning failure mode in a GoTyme context: A user asks "what is the current interest rate on GoTyme savings?" The fine-tuned model answers 4.5% with complete confidence — which was correct when it was trained six months ago. BSP adjusted the policy rate twice since then. GoTyme updated their product page. The fine-tuned model has no access to that update and cannot flag its own staleness. The user makes a financial decision based on a wrong number. In a regulated banking context this is not just a UX failure — it is a potential BSP compliance violation under consumer protection guidelines.

- RAG failure mode in a GoTyme context: A user asks "am I eligible for a GoTyme credit card?" The RAG pipeline retrieves three chunks from the product documentation — minimum income requirement, age requirement, and account standing requirement. But the fourth eligibility criterion — that the user must have an active GoTyme account for at least 90 days — is buried in a compliance addendum that was chunked poorly and scored low in retrieval. The model answers "yes, you're eligible" based on the three retrieved chunks. The user applies, gets rejected, and calls support angry. The failure is in chunking strategy and retrieval completeness, not in the LLM itself.

Those are the failure modes that matter for a GoTyme interview. Domain-specific, operationally consequential, and pointing to the exact engineering fix needed.

Two other gaps worth naming:

- You didn't mention retrieval evaluation. RAG systems need a separate evaluation layer — RAGAS or DeepEval — that measures whether the retrieved chunks actually contain the answer before the LLM generates a response. Without this, you're flying blind on retrieval quality. This maps directly to Project 03 in your roadmap.

- The cost framing on RAG cons is slightly off. The dominant cost in a production RAG system is not the vector store subscription — it's LLM inference costs per query multiplied by query volume. At GoTyme's scale, that number becomes significant fast. The mitigation is caching frequent query-response pairs and using a smaller model for simple factual lookups.

Q7 score: 8/10. Strongest conceptual answer after Q6. The hybrid recommendation is production-grade. The failure modes need domain grounding.

## Q8 Maya's fraud detection model flags 10,000 transactions per day as suspicious. Of those, 9,500 are legitimate transactions incorrectly flagged. The operations team manually reviews all 10,000 daily. The head of risk asks you to fix this. What metric is broken, what is causing it, and what is your solution?

### My Answer

I will answer it in the most honest way I can seee this:

- 9500 false positives = low precision. However, I may have missed dome other metric instead.
- Flagging overwhelmingly high negatives as positives is a result of the threshold value used to assess whether the model classifies the prediction as suspicious or not. It may have been at a very low threshold (i.e. 0.4) compared to what is usually expected (in this case, higher number due to the rarity of the suspicious cases over the data)
- Solution: If it was the threshold problem, we recalibrate the value accordingly. Here's my approach,
    - We take a sample of this false positives (500 data -> 350 train, 150 test)
    - We analyze patterns in the data considered as train: Consistent features such as transaction times, account registration dates, etc. This is to reinforce that it is a threshold problem or a different part entirely
    - We then point to the PR curve and identify where the current threshold value sits. If the curve shows a 0.65 value and you use a 0.2, then we already solved it without retraining
    - When all else fails, retrain by properly handling the class imbalance. Let's apply the real-world scenario: Highly likely the data is more negative than positive. Rather than resample the distribution, which warps the reality of real-world data, we employ loss functions that can prioritize undersampled categories (i.e. Focal Loss, Dice Loss, Tversky Loss). I'm open to learning other ways to solve class-imbalance

### Claude's Assessment

Honest answer, mostly correct, one significant gap.

[Certain] You correctly identified low precision as the broken metric and threshold miscalibration as the likely cause. The PR curve analysis to find where the current threshold sits before retraining is exactly right — most engineers jump to retraining immediately. You didn't.

The significant gap: your sampling approach for diagnosis is backwards.

You said "take a sample of 500 false positives, 350 train, 150 test." You cannot train a threshold recalibration model on false positives only. You need the full score distribution — true positives, false positives, true negatives, false negatives — to see where the threshold is cutting. Analyzing only false positives in isolation tells you what flagged legitimate transactions look like, but not where the decision boundary should move. You need the precision-recall curve plotted on the full held-out test set, not a subsample of one error type.

The loss function recommendations are above average for your level. Focal Loss for class imbalance in fraud detection is correct and used in production by SEA fintech teams. Naming Dice Loss and Tversky Loss shows you're drawing from your medical imaging background — those are segmentation losses, technically applicable but unusual in tabular fraud detection. In an interview, lead with Focal Loss and class weighting, then mention the others as alternatives you've explored.

One thing missing entirely: precision-recall tradeoff communication to the business. The head of risk doesn't want a PR curve — they want to know the cost of your proposed fix. If you raise the threshold to reduce false positives from 9,500 to 500 per day, how many true frauds will you miss? That number has a dollar value. Your solution isn't complete until you can say "raising the threshold to 0.75 reduces ops team workload by 85% but increases missed fraud by approximately X cases per day, costing an estimated ₱Y." That translation is what separates an ML engineer from a senior ML engineer at Maya or Mynt.

Q8 score: 7/10.

The trajectory is the story — you started at 4 and haven't scored below 7 in the last four questions. The early weakness was ML formulation fundamentals. The late strength is systems thinking and operational reasoning.


