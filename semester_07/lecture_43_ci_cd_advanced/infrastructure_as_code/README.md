# Infrastructure as Code (IaC)

1. **Name of Algorithm**  
   Infrastructure as Code (IaC)

2. **What problem does it solve? (1 sentence)**  
   Defines and manages infrastructure using code and version control, enabling reproducible, automated, and version-controlled infrastructure provisioning and configuration.

3. **Intuition (plain-language explanation)**  
   Like writing code for servers: instead of manually clicking in cloud console to create servers (error-prone, not repeatable), write code that describes infrastructure (like application code) - run the code to create infrastructure automatically, just like compiling code creates a program.

4. **Inputs & Outputs**  
   - Input: Infrastructure definition files (Terraform, CloudFormation, Ansible, etc.), infrastructure provider (AWS, Azure, GCP, etc.), configuration parameters.  
   - Output: Provisioned infrastructure, version-controlled infrastructure definitions, reproducible infrastructure environments.

5. **Step-by-step description (5–10 lines max)**  
1. Define infrastructure: write code describing desired infrastructure (servers, networks, databases, etc.).
2. Version control: store infrastructure code in Git repository for versioning and collaboration.
3. Initialize: set up infrastructure tool (Terraform init, etc.) and configure provider credentials.
4. Plan: preview infrastructure changes before applying (Terraform plan shows what will be created/modified).
5. Apply: execute infrastructure code to provision actual infrastructure (Terraform apply creates resources).
6. Verify: confirm infrastructure matches definition (servers created, networks configured, etc.).
7. Update: modify infrastructure by changing code and reapplying (infrastructure updated to match code).
8. Destroy: remove infrastructure by destroying resources (Terraform destroy removes all resources).

6. **Tiny example (hand-simulated)**  
   Write Terraform code: 'create 3 EC2 instances, 1 RDS database, 1 VPC' → terraform plan (preview) → terraform apply → AWS creates infrastructure → infrastructure matches code → commit code to Git → infrastructure version-controlled and reproducible.

7. **Time & Space Complexity**  
   - Time: O(P) where P is provisioning time (varies by infrastructure size, typically minutes to hours).  
   - Space: O(C + I) where C is code size (infrastructure definitions), I is infrastructure size (actual resources).

8. **Strengths**  
- Reproducibility: same code creates identical infrastructure every time.
- Version control: infrastructure changes tracked and auditable in Git.
- Automation: eliminates manual infrastructure provisioning and configuration.

9. **Weaknesses / limitations**  
- Learning curve: requires learning infrastructure as code tools and syntax.
- State management: requires managing infrastructure state files carefully.
- Provider lock-in: some tools may be tied to specific cloud providers.

10. **Compare with alternatives**  
    Alternatives: Manual Infrastructure Provisioning, Cloud Console Management, Configuration Management Tools, Container Orchestration

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
