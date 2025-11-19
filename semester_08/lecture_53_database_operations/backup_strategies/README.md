# Database Backup Strategies

1. **Name of Algorithm**  
   Database Backup Strategies

2. **What problem does it solve? (1 sentence)**  
   Creates and manages copies of database data to enable recovery from data loss, corruption, or disasters, ensuring business continuity and data protection.

3. **Intuition (plain-language explanation)**  
Like insurance for data: backup strategies are like having insurance for your data - you regularly make copies (like taking photos of important documents) and store them safely (like keeping photos in a fireproof safe) - if something happens to your original data (like a fire), you can restore from backups (like reprinting photos), ensuring you don't lose everything.

4. **Inputs & Outputs**  
   - Input: Database data, backup configuration, storage location, retention policy, backup schedule.  
   - Output: Backup copies, recovery capability, data protection, business continuity.

5. **Step-by-step description (5–10 lines max)**  
1. Define strategy: choose backup strategy (full, incremental, differential, continuous).
2. Schedule backups: set up backup schedule (daily, hourly, real-time).
3. Perform backup: execute backup operation (full database copy or incremental changes).
4. Store backups: save backups to secure storage (local, remote, cloud).
5. Verify: validate backup integrity and completeness.
6. Test restore: periodically test restoring from backups to ensure they work.
7. Retain: maintain backup retention policy (keep backups for specified period).
8. Monitor: track backup success, storage usage, and restore times.
9. Document: document backup procedures and recovery processes.

6. **Tiny example (hand-simulated)**  
   Database backup strategy: full backup daily at 2 AM → incremental backups every 6 hours → backups stored on local disk and cloud → retention: 30 days daily, 12 months monthly → test restore monthly → disaster recovery: restore from cloud backup → data recovered → business continuity maintained.

7. **Time & Space Complexity**  
   - Time: O(d) for full backup where d is database size, O(c) for incremental where c is changed data size.  
   - Space: O(d·r) where d is database size, r is retention factor (multiple backup copies).

8. **Strengths**  
- Data protection: enables recovery from data loss or corruption.
- Business continuity: ensures business can continue after disasters.
- Compliance: meets regulatory requirements for data retention.

9. **Weaknesses / limitations**  
- Storage cost: requires significant storage for backup copies.
- Time overhead: backup operations consume resources and time.
- Complexity: managing backup schedules and retention can be complex.

10. **Compare with alternatives**  
    Alternatives: Replication, Snapshots, Continuous Backup, Point-in-Time Recovery

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
