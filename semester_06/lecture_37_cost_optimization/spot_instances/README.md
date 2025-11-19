# Spot Instances

1. **Name of Algorithm**  
   Spot Instances

2. **What problem does it solve? (1 sentence)**  
   Uses spare cloud compute capacity available at significantly discounted prices (up to 90% off) for fault-tolerant workloads, enabling cost-effective ML training and batch inference with the trade-off of potential interruption.

3. **Intuition (plain-language explanation)**  
   Like buying airline tickets at the last minute: cloud providers have unused capacity they sell at huge discounts, but they can take it back if someone pays full price - perfect for jobs that can handle interruptions (like training that can checkpoint and resume).

4. **Inputs & Outputs**  
   - Input: Workload (training jobs, batch inference), spot instance configuration (instance type, max price, interruption handling), checkpointing strategy.  
   - Output: Cost-optimized compute resources with potential for interruption, significant cost savings.

5. **Step-by-step description (5–10 lines max)**  
1. Identify fault-tolerant workloads: choose workloads that can handle interruptions (training with checkpoints, batch inference).
2. Configure spot instances: select instance type, set maximum bid price (willing to pay), choose availability zones.
3. Request spot instances: submit spot instance requests to cloud provider.
4. Monitor spot prices: track current spot prices vs. on-demand prices to optimize bidding strategy.
5. Handle interruptions: implement checkpointing (save model state periodically) and resume logic.
6. Run workload: execute training or inference on spot instances, save checkpoints regularly.
7. Recover from interruption: if instance terminated, restore from checkpoint and resume on new spot instance.
8. Track savings: monitor cost savings compared to on-demand instances.

6. **Tiny example (hand-simulated)**  
   ML training: ResNet-50 training on 4 GPUs → on-demand: $10/hour → spot instances: $1/hour (90% discount) → training with checkpoints every epoch → instance interrupted after 2 hours → resume from checkpoint → total training: 8 hours → cost: $8 (vs $80 on-demand, 90% savings).

7. **Time & Space Complexity**  
   - Time: O(T + R·C) where T is total training time, R is number of interruptions, C is checkpoint restore time (may take longer than on-demand due to interruptions).  
   - Space: O(M) for model checkpoints, O(M) for model state in memory (same as on-demand).

8. **Strengths**  
- Significant cost savings: up to 90% cheaper than on-demand instances.
- Suitable for fault-tolerant workloads: training and batch jobs can handle interruptions.
- High availability: can use multiple availability zones to reduce interruption risk.

9. **Weaknesses / limitations**  
- Interruptions: instances can be terminated with short notice (2 minutes on AWS).
- Not suitable for real-time: interruptions make spot instances unsuitable for production inference.
- Complexity: requires checkpointing and resume logic.

10. **Compare with alternatives**  
    Alternatives: On-Demand Instances, Reserved Instances, Savings Plans, Preemptible Instances

11. **30-second explanation (your own words)**  
    Uses spare cloud compute capacity at discounted prices for fault-tolerant ML workloads, enabling significant cost savings (up to 90%) with the trade-off of potential interruption, requiring checkpointing and resume strategies.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
