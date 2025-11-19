# GitOps

1. **Name of Algorithm**  
   GitOps

2. **What problem does it solve? (1 sentence)**  
   Uses Git as single source of truth for infrastructure and application deployments, enabling declarative, version-controlled, and automated infrastructure management.

3. **Intuition (plain-language explanation)**  
   Like version control for infrastructure: instead of manually configuring servers (error-prone, hard to track), define infrastructure in code (like application code) stored in Git - changes to infrastructure are made via Git commits, automatically applied (like CI/CD for infrastructure).

4. **Inputs & Outputs**  
   - Input: Git repository with infrastructure definitions (Kubernetes manifests, Terraform, etc.), GitOps operator/tool (ArgoCD, Flux, etc.), target infrastructure.  
   - Output: Automated infrastructure deployments, version-controlled infrastructure state, declarative infrastructure management.

5. **Step-by-step description (5–10 lines max)**  
1. Define infrastructure: write infrastructure as code (Kubernetes YAML, Terraform, etc.) in Git repository.
2. Commit changes: make infrastructure changes via Git commits (add/modify/delete infrastructure definitions).
3. GitOps operator detects: operator monitors Git repository for changes.
4. Compare state: operator compares Git state with actual infrastructure state.
5. Reconcile: operator automatically applies changes to match Git state (drift detection and correction).
6. Deploy: infrastructure changes are automatically deployed to target environment.
7. Monitor: track deployment status, infrastructure state, and any drift.
8. Rollback: revert infrastructure by reverting Git commit (operator automatically applies rollback).

6. **Tiny example (hand-simulated)**  
   Update Kubernetes deployment YAML in Git → commit → GitOps operator detects change → compares Git state with cluster → applies changes → deployment updated → infrastructure matches Git state → all changes version-controlled and auditable.

7. **Time & Space Complexity**  
   - Time: O(S + D) where S is sync time (operator reconciliation), D is deployment time (typically minutes for most infrastructure changes).  
   - Space: O(R + I) where R is repository size (infrastructure definitions), I is infrastructure size (actual resources).

8. **Strengths**  
- Version control: all infrastructure changes tracked in Git.
- Automation: eliminates manual infrastructure management.
- Consistency: ensures infrastructure matches declared state (drift prevention).

9. **Weaknesses / limitations**  
- Learning curve: requires understanding of infrastructure as code and GitOps tools.
- Tool dependency: relies on GitOps operator and infrastructure as code tools.
- Initial setup: requires configuring GitOps operator and repository structure.

10. **Compare with alternatives**  
    Alternatives: Manual Infrastructure Management, Infrastructure as Code (without GitOps), Configuration Management Tools, Cloud Console Management

11. **30-second explanation (your own words)**  
    Uses Git as single source of truth for infrastructure and application deployments, enabling declarative, version-controlled, and automated infrastructure management.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
