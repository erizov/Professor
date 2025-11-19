# File Systems

1. **Name of Algorithm**  
   File Systems

2. **What problem does it solve? (1 sentence)**  
Organizes and manages data storage on disk devices by providing hierarchical directory structure, file metadata, and access control, enabling efficient storage, retrieval, and organization of files and directories.

3. **Intuition (plain-language explanation)**  
   Like a library's filing system: the file system organizes data on disk like a library organizes books - files are like books (data), directories are like shelves (organization), and the file system keeps track of where everything is (metadata) so you can find and access files quickly.

4. **Inputs & Outputs**  
   - Input: File operations (create, read, write, delete), directory operations, file paths, file metadata (name, size, permissions).  
   - Output: Organized file storage on disk, directory hierarchies, file access through paths, metadata management.

5. **Step-by-step description (5–10 lines max)**  
1. Format disk: initialize file system structure on disk (superblock, inode table, data blocks).
2. Create directory structure: build hierarchical tree of directories (root, subdirectories).
3. Allocate storage: when file created, allocate disk blocks to store file data.
4. Store metadata: record file information in inode (size, permissions, timestamps, block pointers).
5. Map paths: translate file paths (/home/user/file.txt) to inode numbers using directory entries.
6. Handle file operations: read (find blocks, read data), write (allocate blocks, write data), delete (free blocks, remove inode).
7. Manage free space: track free disk blocks using bitmap or free list.
8. Maintain consistency: use journaling or other techniques to ensure file system integrity after crashes.

6. **Tiny example (hand-simulated)**  
   Create file /home/user/document.txt: file system finds free inode → allocates inode #1234 → creates directory entry 'document.txt' → inode #1234 in /home/user → allocates disk blocks 100-105 → writes file data to blocks → updates inode with block pointers → file created.

7. **Time & Space Complexity**  
   - Time: O(d) for path lookup where d is directory depth, O(b) for reading/writing b blocks, O(1) for metadata operations (with caching).  
   - Space: O(F) for storing F files' metadata (inodes), O(D) for directory structures, O(B) for data blocks where B is total blocks used.

8. **Strengths**  
- Organized storage: provides logical organization of data.
- Efficient access: enables fast file lookup and retrieval.
- Abstraction: hides disk complexity from applications.

9. **Weaknesses / limitations**  
- Overhead: metadata and directory structures consume disk space.
- Fragmentation: files may be stored non-contiguously, affecting performance.
- Complexity: requires careful design to handle concurrent access and crashes.

10. **Compare with alternatives**  
    Alternatives: Raw Disk Access, Database Storage, Object Storage, Network File Systems

11. **30-second explanation (your own words)**  
Organizes and manages data storage on disk devices by providing hierarchical directory structure, file metadata, and access control, enabling efficient storage, retrieval, and organization of files and directories.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
