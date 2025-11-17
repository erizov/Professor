#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6: Expand Framework Examples to More Algorithms
Focus on graduate-level and advanced topics
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

ROOT = Path(__file__).resolve().parents[1]


# Expanded framework examples for graduate-level topics
GRADUATE_FRAMEWORK_EXAMPLES: Dict[str, Dict[str, str]] = {
    # LLM and AI topics
    'llm_architecture': {
        'python': '''# Hugging Face Transformers - LLM Architecture
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Transformer architecture with attention mechanisms
inputs = tokenizer("Hello world", return_tensors="pt")
outputs = model(**inputs)''',
        'pytorch': '''# PyTorch - Transformer Architecture
import torch.nn as nn
from torch.nn import Transformer

class LLMModel(nn.Module):
    def __init__(self, vocab_size, d_model, nhead):
        super().__init__()
        self.transformer = Transformer(d_model, nhead)
        self.embedding = nn.Embedding(vocab_size, d_model)
    
    def forward(self, src):
        src = self.embedding(src)
        return self.transformer(src, src)''',
    },
    'fine_tuning_llm': {
        'python': '''# Hugging Face - Fine-tuning LLM
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()''',
    },
    'rag_advanced': {
        'python': '''# LangChain - Advanced RAG
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

vectorstore = Chroma.from_documents(documents, embeddings)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)''',
    },
    'model_serving_advanced': {
        'kubernetes': '''# Kubernetes - Model Serving
apiVersion: serving.kubeflow.org/v1beta1
kind: InferenceService
metadata:
  name: model-serving
spec:
  predictor:
    tensorflow:
      storageUri: gs://model-bucket/model
      resources:
        requests:
          cpu: "2"
          memory: 4Gi''',
        'docker': '''# Docker - Model Serving
FROM tensorflow/serving:latest
COPY model /models/my_model
ENV MODEL_NAME=my_model
EXPOSE 8501''',
    },
    'feature_stores_advanced': {
        'python': '''# Feast - Feature Store
from feast import FeatureStore

fs = FeatureStore(repo_path=".")
feature_vector = fs.get_online_features(
    features=["user_features:age", "user_features:city"],
    entity_rows=[{"user_id": 1}]
)''',
    },
    # CI/CD topics
    'infrastructure_as_code': {
        'terraform': '''# Terraform - Infrastructure as Code
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "app-server"
  }
}''',
        'ansible': '''# Ansible - Infrastructure as Code
- name: Configure web server
  hosts: webservers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present''',
    },
    'gitops_advanced': {
        'kubernetes': '''# GitOps with ArgoCD
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
spec:
  source:
    repoURL: https://github.com/user/repo
    path: k8s
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: default''',
    },
    # Database topics
    'query_optimization': {
        'sql': '''-- PostgreSQL - Query Optimization
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;

-- Create index for optimization
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);''',
    },
    'database_sharding': {
        'sql': '''-- Database Sharding Strategy
-- Shard by user_id
CREATE TABLE orders_shard_0 (
    CHECK (user_id % 4 = 0)
) INHERITS (orders);

CREATE TABLE orders_shard_1 (
    CHECK (user_id % 4 = 1)
) INHERITS (orders);''',
    },
    # Blockchain topics
    'smart_contracts': {
        'solidity': '''// Solidity - Smart Contract
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 public storedData;
    
    function set(uint256 x) public {
        storedData = x;
    }
    
    function get() public view returns (uint256) {
        return storedData;
    }
}''',
    },
    # Observability topics
    'distributed_tracing': {
        'python': '''# OpenTelemetry - Distributed Tracing
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation"):
    # Your code here
    pass''',
        'java': '''// Spring Cloud Sleuth - Distributed Tracing
@RestController
public class Controller {
    @Autowired
    private Tracer tracer;
    
    @GetMapping("/api/data")
    public String getData() {
        Span span = tracer.nextSpan().name("getData").start();
        try {
            // Your code
            return "data";
        } finally {
            span.end();
        }
    }
}''',
    },
    'log_aggregation': {
        'docker': '''# Docker - Log Aggregation
version: '3'
services:
  app:
    image: myapp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  fluentd:
    image: fluent/fluentd
    volumes:
      - ./logs:/var/log''',
        'kubernetes': '''# Kubernetes - Log Aggregation
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
    </source>''',
    },
}


def find_readme_files_needing_examples() -> List[Tuple[Path, str]]:
    """Find README files that need framework examples."""
    needs_examples = []
    
    for readme_path in ROOT.rglob("**/README.md"):
        if "supporting_documents" in str(readme_path):
            continue
        if readme_path.name == "README.md" and readme_path.parent.name != "Professor":
            try:
                content = readme_path.read_text(encoding='utf-8')
                algorithm_name = readme_path.parent.name
                
                # Check if has Examples section but might need more
                has_examples = (
                    "## Examples of Implementation" in content or
                    "## Examples of Deployment" in content or
                    "## Examples" in content
                )
                
                if has_examples:
                    # Check if it needs more frameworks (has less than 2)
                    framework_count = sum(1 for fw in [
                        'Spring Framework', '.NET Framework', 'Java Standard Library',
                        'Python Standard Library', 'Docker', 'Kubernetes', 'Terraform',
                        'Hugging Face', 'PyTorch', 'LangChain', 'OpenTelemetry'
                    ] if fw in content)
                    
                    if framework_count < 2:
                        needs_examples.append((readme_path, algorithm_name))
            except Exception:
                continue
    
    return needs_examples


def add_graduate_framework_examples(readme_path: Path, algorithm_name: str) -> bool:
    """Add framework examples for graduate-level algorithms."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        
        # Get examples - try multiple matching strategies
        examples = GRADUATE_FRAMEWORK_EXAMPLES.get(algorithm_name, {})
        if not examples:
            # Try partial match
            algo_lower = algorithm_name.lower()
            for key, ex in GRADUATE_FRAMEWORK_EXAMPLES.items():
                if key in algo_lower or algo_lower in key:
                    examples = ex
                    break
        
        # Try algorithm type matching for graduate topics
        if not examples:
            algo_lower = algorithm_name.lower()
            lecture_path = readme_path.parent.parent.name.lower()
            
            # LLM topics
            if any(term in algo_lower or term in lecture_path for term in ['llm', 'transformer', 'attention', 'fine_tuning', 'rag']):
                if 'architecture' in algo_lower or 'transformer' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('llm_architecture', {})
                elif 'fine_tuning' in algo_lower or 'fine_tune' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('fine_tuning_llm', {})
                elif 'rag' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('rag_advanced', {})
            
            # MLOps topics
            elif any(term in algo_lower or term in lecture_path for term in ['model_serving', 'feature_store', 'mlops']):
                if 'model_serving' in algo_lower or 'serving' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('model_serving_advanced', {})
                elif 'feature_store' in algo_lower or 'feature' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('feature_stores_advanced', {})
            
            # CI/CD topics
            elif any(term in algo_lower or term in lecture_path for term in ['infrastructure', 'iac', 'gitops']):
                if 'infrastructure' in algo_lower or 'iac' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('infrastructure_as_code', {})
                elif 'gitops' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('gitops_advanced', {})
            
            # Database topics
            elif any(term in algo_lower or term in lecture_path for term in ['query', 'optimization', 'sharding', 'database']):
                if 'optimization' in algo_lower or 'query' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('query_optimization', {})
                elif 'sharding' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('database_sharding', {})
            
            # Blockchain topics
            elif any(term in algo_lower or term in lecture_path for term in ['smart_contract', 'blockchain']):
                examples = GRADUATE_FRAMEWORK_EXAMPLES.get('smart_contracts', {})
            
            # Observability topics
            elif any(term in algo_lower or term in lecture_path for term in ['tracing', 'observability', 'logging']):
                if 'tracing' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('distributed_tracing', {})
                elif 'log' in algo_lower:
                    examples = GRADUATE_FRAMEWORK_EXAMPLES.get('log_aggregation', {})
        
        if not examples:
            return False
        
        # Find Examples section (handle various header formats including corrupted ones)
        examples_patterns = [
            r'(## Examples of Implementation\s*\n\s*\n)(.*?)(?=\n##|\Z)',
            r'(## Examples of Deployment\s*\n\s*\n)(.*?)(?=\n##|\Z)',
            r'(## Examples of Impl[^\n]*\s*\n\s*\n)(.*?)(?=\n##|\Z)',  # Handle corrupted headers
            r'(## Examples\s*\n\s*\n)(.*?)(?=\n##|\Z)',
        ]
        
        match = None
        for pattern in examples_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                break
        
        if not match:
            return False
        
        existing_section = match.group(2) if match.lastindex >= 2 else ""
        
        # Replace generic note if present
        if '*Note: Framework-specific examples will be added*' in existing_section or \
           '*Note: Framework-specific examples will be added based on actual implementations.*' in existing_section:
            existing_section = existing_section.replace(
                '*Note: Framework-specific examples will be added based on actual implementations.*',
                ''
            ).replace(
                '*Note: Framework-specific examples will be added*',
                ''
            ).strip()
        
        # Build new examples
        new_examples = ""
        
        if 'python' in examples:
            # Check if Python example already exists
            if '```python' not in existing_section or 'Hugging Face' not in existing_section:
                new_examples += "### Python / Libraries\n\n"
                new_examples += "```python\n" + examples['python'] + "\n```\n\n"
                new_examples += "**Purpose**: Python libraries use this technique for production implementations.\n\n"
        
        if 'pytorch' in examples:
            if 'PyTorch' not in existing_section:
                new_examples += "### PyTorch\n\n"
                new_examples += "```python\n" + examples['pytorch'] + "\n```\n\n"
                new_examples += "**Purpose**: PyTorch implements this for deep learning and computational intelligence.\n\n"
        
        if 'terraform' in examples:
            if 'Terraform' not in existing_section:
                new_examples += "### Terraform\n\n"
                new_examples += "```hcl\n" + examples['terraform'] + "\n```\n\n"
                new_examples += "**Purpose**: Terraform uses this for infrastructure as code and cloud provisioning.\n\n"
        
        if 'kubernetes' in examples:
            if 'Kubernetes' not in existing_section or 'kubeflow' not in existing_section.lower():
                new_examples += "### Kubernetes\n\n"
                new_examples += "```yaml\n" + examples['kubernetes'] + "\n```\n\n"
                new_examples += "**Purpose**: Kubernetes uses this for container orchestration and service management.\n\n"
        
        if 'docker' in examples:
            if 'Docker' not in existing_section or 'dockerfile' not in existing_section.lower():
                new_examples += "### Docker\n\n"
                new_examples += "```dockerfile\n" + examples['docker'] + "\n```\n\n"
                new_examples += "**Purpose**: Docker uses this for containerization and deployment.\n\n"
        
        if 'sql' in examples:
            if '```sql' not in existing_section or 'PostgreSQL' not in existing_section:
                new_examples += "### SQL / Database\n\n"
                new_examples += "```sql\n" + examples['sql'] + "\n```\n\n"
                new_examples += "**Purpose**: Database systems use this for data management and optimization.\n\n"
        
        if 'solidity' in examples:
            if 'Solidity' not in existing_section and 'blockchain' not in existing_section.lower():
                new_examples += "### Solidity / Blockchain\n\n"
                new_examples += "```solidity\n" + examples['solidity'] + "\n```\n\n"
                new_examples += "**Purpose**: Blockchain platforms use this for smart contract development.\n\n"
        
        if 'java' in examples:
            if '```java' not in existing_section or 'Spring Cloud' not in existing_section:
                new_examples += "### Java / Spring Cloud\n\n"
                new_examples += "```java\n" + examples['java'] + "\n```\n\n"
                new_examples += "**Purpose**: Java frameworks use this for enterprise application development.\n\n"
        
        if new_examples:
            # Replace the entire section with new content
            section_start = match.start(2)
            section_end = match.end(2)
            
            # Clean up existing section (remove generic notes)
            cleaned_section = existing_section
            if cleaned_section.strip() == '' or \
               '*Note: Framework-specific examples will be added' in cleaned_section or \
               'implemented in various' in cleaned_section.lower():
                # Replace entire section
                new_section = new_examples.strip()
            else:
                # Append to existing
                new_section = cleaned_section.rstrip() + "\n\n" + new_examples.strip()
            
            content = content[:section_start] + new_section + "\n\n" + content[section_end:]
            readme_path.write_text(content, encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Execute Phase 6: Expand framework examples."""
    print("=" * 70)
    print("Phase 6: Expand Framework Examples to More Algorithms")
    print("=" * 70)
    
    readme_files = find_readme_files_needing_examples()
    print(f"\nFound {len(readme_files)} README files that could use more framework examples")
    
    updated_count = 0
    
    for i, (readme_path, algo_name) in enumerate(readme_files, 1):
        if add_graduate_framework_examples(readme_path, algo_name):
            updated_count += 1
            if updated_count % 50 == 0:
                print(f"[PROGRESS] Processed {i}/{len(readme_files)} files, updated {updated_count}...")
    
    print(f"\n[COMPLETE] Processed {len(readme_files)} files")
    print(f"Updated {updated_count} files with additional framework examples")
    print("\nFramework examples added:")
    print("  - Python libraries (Hugging Face, LangChain)")
    print("  - PyTorch for deep learning")
    print("  - Terraform for infrastructure")
    print("  - Kubernetes for orchestration")
    print("  - Docker for containerization")
    print("  - SQL for database operations")
    print("  - Solidity for blockchain")
    print("  - Java/Spring Cloud for enterprise")


if __name__ == "__main__":
    main()

