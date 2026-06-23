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
