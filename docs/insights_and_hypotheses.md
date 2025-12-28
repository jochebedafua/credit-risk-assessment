# Insights and Hypothesis Generation

## 3.1 Why Are Clients Defaulting?

Exploratory Data Analysis (EDA) reveals that loan defaults are not driven by a single dominant factor, but rather by the interaction of factors. These risk factors interact in non-linear ways.
Given that defaults represent approximately **12% of the dataset**, default behavior tends to occur at the **extremes of risk exposure** rather than along simple linear trends.

The key observations and hypotheses are summarized below.

### Credit Utilization and Liquidity Pressure

**Observation**  
Clients who default tend to exhibit higher credit utilization ratios, particularly at the upper tails of the distribution.

**Interpretation**  
Credit utilization reflects how much of a borrower’s available financial buffer is being consumed by the loan. High utilization indicates limited liquidity and reduced capacity to absorb unexpected expenses or income disruptions.

**Hypothesis**  
Borrowers with limited liquid reserves are more vulnerable to short-term financial shocks, increasing the likelihood of repayment failure.

### Income-to-Loan Ratio and Affordability

**Observation**  
Defaulters consistently display lower income-to-loan ratios compared to non-defaulters.

**Interpretation**  
When loan amounts represent a large proportion of annual income, repayment obligations exert sustained pressure on monthly cash flow.

**Hypothesis**  
Borrowers whose income is insufficient relative to loan size face structural affordability challenges that elevate default risk, even in the absence of adverse events.

### Credit Score and Historical Behavior

**Observation**  
Lower credit score buckets are associated with higher default rates, although credit score alone does not clearly separate defaulters from non-defaulters.

**Interpretation**  
While credit scores capture historical repayment behavior, they do not fully reflect a borrower’s current liquidity position or loan affordability.

**Hypothesis**  
Defaults are more strongly influenced by **current financial stress** than by historical credit behavior alone.


## 3.2 Actionable Recommendations to Reduce Loan Defaults

### Income-Based Loan Caps

**Action**  
Implement income-based loan limits (e.g., maximum loan-to-income thresholds) to reduce structural over-borrowing and improve repayment sustainability.

### Liquidity-Aware Credit Decisions

**Action**  
Explicitly incorporate account balance and deposit behavior into loan eligibility assessments to prevent lending to borrowers with insufficient financial buffers.

### Early Warning Monitoring

**Action**  
Monitor post-loan indicators such as declining deposits or increasing credit utilization to enable proactive intervention before delinquency occurs.


## 3.3 Additional Data Points for Improved Credit Risk Assessment

While the current dataset captures core financial attributes, additional variables that would relevant for loan eligibility are:

### Repayment Behavior Metrics

- Number of missed payments  
- Days past due on prior loans  


### Household and Financial Obligations

- Rent or mortgage payments  
- Number of dependents  