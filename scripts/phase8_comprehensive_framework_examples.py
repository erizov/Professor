#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 8: Comprehensive Framework Examples Expansion
Add framework examples to 200+ additional files focusing on graduate-level topics
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

ROOT = Path(__file__).resolve().parents[1]


# Comprehensive framework examples for graduate-level topics
COMPREHENSIVE_FRAMEWORK_EXAMPLES: Dict[str, Dict[str, str]] = {
    # Operating Systems
    'container_runtimes': {
        'docker': '''# Docker - Container Runtime
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3
COPY app.py /app/
WORKDIR /app
CMD ["python3", "app.py"]

# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    runtime: runc
    ports:
      - "8080:8080"''',
        'kubernetes': '''# Kubernetes - Container Runtime Interface (CRI)
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  runtimeClassName: runc
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"''',
    },
    'microkernel_architecture': {
        'kubernetes': '''# Kubernetes - Microkernel-like Architecture
# Core API server (kernel) with pluggable components
apiVersion: v1
kind: ConfigMap
metadata:
  name: system-config
data:
  scheduler: "default-scheduler"
  kube-proxy: "iptables"
  cni: "calico"

# Pluggable components as separate pods
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-scheduler
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: scheduler
        image: custom-scheduler:latest''',
    },
    'cpu_scheduling_advanced': {
        'kubernetes': '''# Kubernetes - Advanced CPU Scheduling
apiVersion: v1
kind: Pod
metadata:
  name: high-priority-pod
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "4"
        memory: "8Gi"
    # CPU affinity
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
          - matchExpressions:
            - key: cpu-type
              operator: In
              values: ["intel"]''',
    },
    
    # Concurrency & Parallel Computing
    'actor_model': {
        'python': '''# Python - Actor Model with Akka-style
from typing import Protocol
from dataclasses import dataclass

@dataclass
class Message:
    content: str

class Actor:
    def __init__(self, name: str):
        self.name = name
        self.mailbox = []
    
    def send(self, message: Message):
        self.mailbox.append(message)
    
    def receive(self):
        if self.mailbox:
            return self.mailbox.pop(0)
        return None

# Usage
actor = Actor("worker")
actor.send(Message("process data"))
message = actor.receive()''',
        'java': '''// Java - Akka Actor Model
import akka.actor.AbstractActor;
import akka.actor.Props;

public class WorkerActor extends AbstractActor {
    public static Props props() {
        return Props.create(WorkerActor.class);
    }
    
    @Override
    public Receive createReceive() {
        return receiveBuilder()
            .match(String.class, message -> {
                System.out.println("Received: " + message);
            })
            .build();
    }
}''',
    },
    'lock_free_data_structures': {
        'java': '''// Java - Lock-free ConcurrentHashMap
import java.util.concurrent.ConcurrentHashMap;

public class LockFreeExample {
    private ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
    
    public void increment(String key) {
        map.compute(key, (k, v) -> v == null ? 1 : v + 1);
    }
    
    public Integer get(String key) {
        return map.get(key);
    }
}''',
        'python': '''# Python - Lock-free with atomic operations
from threading import Lock
from collections import defaultdict

class LockFreeCounter:
    def __init__(self):
        self._counters = defaultdict(int)
        self._locks = defaultdict(Lock)
    
    def increment(self, key: str):
        with self._locks[key]:
            self._counters[key] += 1
    
    def get(self, key: str) -> int:
        return self._counters[key]''',
    },
    'gpu_computing': {
        'python': '''# Python - GPU Computing with CuPy
import cupy as cp

# GPU array operations
x_gpu = cp.array([1, 2, 3, 4, 5])
y_gpu = cp.array([6, 7, 8, 9, 10])
result_gpu = x_gpu + y_gpu

# Transfer back to CPU
result_cpu = cp.asnumpy(result_gpu)''',
        'cuda': '''// CUDA - GPU Kernel
__global__ void vectorAdd(float *A, float *B, float *C, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        C[i] = A[i] + B[i];
    }
}

// Host code
int main() {
    int N = 1000;
    size_t size = N * sizeof(float);
    
    float *h_A = (float*)malloc(size);
    float *h_B = (float*)malloc(size);
    float *h_C = (float*)malloc(size);
    
    // Allocate device memory
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);
    
    // Copy to device
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);
    
    // Launch kernel
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
    
    // Copy result back
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);
    
    return 0;
}''',
    },
    
    # Distributed Systems
    'consensus_algorithms': {
        'kubernetes': '''# Kubernetes - Raft Consensus (etcd)
# etcd uses Raft for consensus
apiVersion: v1
kind: ConfigMap
metadata:
  name: etcd-config
data:
  etcd.conf: |
    name: etcd-0
    initial-cluster: etcd-0=http://etcd-0:2380,etcd-1=http://etcd-1:2380,etcd-2=http://etcd-2:2380
    initial-cluster-state: new
    initial-cluster-token: etcd-cluster-1''',
        'python': '''# Python - Raft Consensus Implementation
class RaftNode:
    def __init__(self, node_id: int, peers: List[int]):
        self.node_id = node_id
        self.peers = peers
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []
    
    def request_vote(self, term: int, candidate_id: int):
        if term > self.current_term:
            self.current_term = term
            self.voted_for = candidate_id
            return True
        return False''',
    },
    'vector_clocks': {
        'python': '''# Python - Vector Clocks
from typing import Dict

class VectorClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}
    
    def tick(self):
        self.clock[self.node_id] += 1
    
    def update(self, other_clock: Dict[str, int]):
        for node, time in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), time)
        self.tick()
    
    def happens_before(self, other: 'VectorClock') -> bool:
        return all(self.clock.get(k, 0) <= other.clock.get(k, 0) 
                  for k in set(self.clock.keys()) | set(other.clock.keys()))''',
    },
    'crdt': {
        'python': '''# Python - CRDT (Conflict-free Replicated Data Type)
from typing import Dict, Set

class GSet:
    """Grow-only Set CRDT"""
    def __init__(self):
        self.elements: Set[str] = set()
    
    def add(self, element: str):
        self.elements.add(element)
    
    def merge(self, other: 'GSet'):
        self.elements.update(other.elements)
    
    def contains(self, element: str) -> bool:
        return element in self.elements

# Usage
set1 = GSet()
set1.add("a")
set1.add("b")

set2 = GSet()
set2.add("c")

set1.merge(set2)  # {a, b, c}''',
    },
    
    # Cloud Native
    'service_mesh': {
        'istio': '''# Istio - Service Mesh
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2''',
        'kubernetes': '''# Kubernetes - Service Mesh with Linkerd
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    linkerd.io/inject: enabled
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080''',
    },
    'serverless_architecture': {
        'aws': '''# AWS Lambda - Serverless Function
import json
import boto3

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    # Process event
    records = event.get('Records', [])
    
    for record in records:
        # Process each record
        data = json.loads(record['body'])
        process_data(data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

def process_data(data):
    # Your processing logic
    pass''',
        'kubernetes': '''# Kubernetes - Knative Serverless
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: serverless-app
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containers:
      - image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENV_VAR
          value: "value"''',
    },
    'function_as_service': {
        'kubernetes': '''# Kubernetes - FaaS with OpenFaaS
apiVersion: openfaas.com/v1
kind: Function
metadata:
  name: my-function
spec:
  name: my-function
  image: my-function:latest
  handler: handler
  language: python3
  fprocess: python3 index.py
  environment:
    write_debug: "true"''',
        'python': '''# Python - FaaS Handler
def handler(event, context):
    """
    FaaS function handler
    """
    # Extract data from event
    data = event.get('data', {})
    
    # Process
    result = process(data)
    
    # Return response
    return {
        'statusCode': 200,
        'body': result
    }

def process(data):
    # Your processing logic
    return {"processed": True}''',
    },
    
    # Observability
    'distributed_tracing': {
        'opentelemetry': '''# OpenTelemetry - Distributed Tracing
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Usage
with tracer.start_as_current_span("operation"):
    # Your code
    with tracer.start_as_current_span("sub-operation"):
        # Nested span
        pass''',
        'kubernetes': '''# Kubernetes - Distributed Tracing with Jaeger
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-tracing
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: JAEGER_AGENT_HOST
          value: jaeger-agent
        - name: JAEGER_AGENT_PORT
          value: "6831"''',
    },
    'metrics_collection': {
        'prometheus': '''# Prometheus - Metrics Collection
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Usage
@request_duration.time()
def handle_request():
    request_count.inc()
    # Your request handling logic
    time.sleep(0.1)

# Start metrics server
start_http_server(8000)''',
        'kubernetes': '''# Kubernetes - Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics''',
    },
    'apm': {
        'elastic': '''# Elastic APM - Application Performance Monitoring
from elasticapm import Client

# Initialize APM client
apm_client = Client(
    service_name='my-service',
    server_url='http://apm-server:8200',
    environment='production'
)

# Transaction tracking
with apm_client.begin_transaction('request'):
    # Your code
    apm_client.capture_message('Processing request')
    
    try:
        # Your logic
        pass
    except Exception as e:
        apm_client.capture_exception()''',
    },
    
    # Data Engineering
    'data_mesh': {
        'kubernetes': '''# Kubernetes - Data Mesh Architecture
apiVersion: v1
kind: Namespace
metadata:
  name: data-mesh
---
apiVersion: v1
kind: Service
metadata:
  name: data-product-api
  namespace: data-mesh
spec:
  selector:
    app: data-product
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-product
  namespace: data-mesh
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-product
  template:
    metadata:
      labels:
        app: data-product
    spec:
      containers:
      - name: api
        image: data-product:latest
        ports:
        - containerPort: 8080''',
    },
    'stream_processing_advanced': {
        'kafka': '''# Apache Kafka - Stream Processing
from kafka import KafkaConsumer, KafkaProducer
import json

# Consumer
consumer = KafkaConsumer(
    'input-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stream processing
for message in consumer:
    data = message.value
    # Process
    result = process_data(data)
    # Produce to output topic
    producer.send('output-topic', result)''',
        'kubernetes': '''# Kubernetes - Kafka Streams
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-streams-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: streams
        image: kafka-streams:latest
        env:
        - name: KAFKA_BOOTSTRAP_SERVERS
          value: "kafka:9092"
        - name: APPLICATION_ID
          value: "streams-app"''',
    },
    'lambda_architecture': {
        'kafka': '''# Lambda Architecture - Batch + Stream
# Batch Layer (Hadoop/Spark)
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BatchProcessing").getOrCreate()
df = spark.read.parquet("s3://data/batch/")
batch_results = df.groupBy("key").agg({"value": "sum"})

# Speed Layer (Kafka Streams)
from kafka import KafkaConsumer
consumer = KafkaConsumer('stream-topic')
for message in consumer:
    # Real-time processing
    process_stream(message)

# Serving Layer - Merge batch + stream results''',
    },
    
    # Databases
    'query_optimization': {
        'postgresql': '''-- PostgreSQL - Query Optimization
-- Create indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Analyze query plan
EXPLAIN ANALYZE
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;

-- Use covering index
CREATE INDEX idx_covering ON orders(customer_id, created_at, total)
INCLUDE (id, status);''',
    },
    'database_sharding': {
        'postgresql': '''-- PostgreSQL - Database Sharding
-- Shard by user_id (modulo 4)
CREATE TABLE orders_shard_0 (
    CHECK (user_id % 4 = 0)
) INHERITS (orders);

CREATE TABLE orders_shard_1 (
    CHECK (user_id % 4 = 1)
) INHERITS (orders);

CREATE TABLE orders_shard_2 (
    CHECK (user_id % 4 = 2)
) INHERITS (orders);

CREATE TABLE orders_shard_3 (
    CHECK (user_id % 4 = 3)
) INHERITS (orders);

-- Routing function
CREATE OR REPLACE FUNCTION route_to_shard(user_id INT)
RETURNS TEXT AS $$
BEGIN
    RETURN 'orders_shard_' || (user_id % 4);
END;
$$ LANGUAGE plpgsql;''',
    },
    
    # LLM & AI
    'llm_architecture': {
        'pytorch': '''# PyTorch - Transformer Architecture
import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

class TransformerModel(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        encoder_layers = TransformerEncoderLayer(d_model, nhead)
        self.transformer = TransformerEncoder(encoder_layers, num_layers)
        self.fc = nn.Linear(d_model, vocab_size)
    
    def forward(self, src):
        src = self.embedding(src)
        output = self.transformer(src)
        return self.fc(output)''',
        'huggingface': '''# Hugging Face - LLM Architecture
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

inputs = tokenizer("Hello world", return_tensors="pt")
outputs = model(**inputs)''',
    },
    'fine_tuning_llm': {
        'huggingface': '''# Hugging Face - Fine-tuning LLM
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()''',
    },
    'rag_advanced': {
        'langchain': '''# LangChain - Advanced RAG
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

result = qa_chain.run("What is the main topic?")''',
    },
}


def find_readme_files_for_expansion() -> List[Tuple[Path, str, str]]:
    """Find README files in graduate semesters that need framework examples."""
    candidates = []
    
    for readme_path in ROOT.rglob("**/README.md"):
        if "supporting_documents" in str(readme_path):
            continue
        if readme_path.name == "README.md" and readme_path.parent.name != "Professor":
            # Check if in graduate semester (9-16)
            path_str = str(readme_path.relative_to(ROOT))
            if any(f'semester_{i}' in path_str for i in range(9, 17)):
                try:
                    content = readme_path.read_text(encoding='utf-8')
                    algorithm_name = readme_path.parent.name
                    lecture_name = readme_path.parent.parent.name
                    
                    # Check if has Examples section
                    has_examples = (
                        "## Examples of Implementation" in content or
                        "## Examples of Deployment" in content or
                        "## Examples" in content
                    )
                    
                    if has_examples:
                        # Check framework count (want to add more if < 3)
                        framework_count = sum(1 for fw in [
                            'Kubernetes', 'Docker', 'Terraform', 'Prometheus',
                            'Istio', 'Kafka', 'Redis', 'PostgreSQL', 'PyTorch',
                            'Hugging Face', 'LangChain', 'OpenTelemetry', 'AWS',
                            'CUDA', 'Akka', 'Jaeger', 'Elastic'
                        ] if fw in content)
                        
                        if framework_count < 3:
                            candidates.append((readme_path, algorithm_name, lecture_name))
                except Exception:
                    continue
    
    return candidates


def get_framework_examples(algorithm_name: str, lecture_name: str) -> Dict[str, str]:
    """Get appropriate framework examples for algorithm."""
    algo_lower = algorithm_name.lower()
    lecture_lower = lecture_name.lower()
    
    # Try exact match
    examples = COMPREHENSIVE_FRAMEWORK_EXAMPLES.get(algorithm_name, {})
    if examples:
        return examples
    
    # Try partial match
    for key, ex in COMPREHENSIVE_FRAMEWORK_EXAMPLES.items():
        if key in algo_lower or algo_lower in key:
            return ex
    
    # Try lecture-based matching
    if 'os' in lecture_lower or 'operating' in lecture_lower:
        if 'container' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('container_runtimes', {})
        elif 'scheduling' in algo_lower or 'cpu' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('cpu_scheduling_advanced', {})
        elif 'microkernel' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('microkernel_architecture', {})
    
    elif 'concurrency' in lecture_lower or 'parallel' in lecture_lower:
        if 'actor' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('actor_model', {})
        elif 'lock' in algo_lower or 'free' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('lock_free_data_structures', {})
        elif 'gpu' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('gpu_computing', {})
    
    elif 'distributed' in lecture_lower:
        if 'consensus' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('consensus_algorithms', {})
        elif 'vector' in algo_lower or 'clock' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('vector_clocks', {})
        elif 'crdt' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('crdt', {})
    
    elif 'cloud' in lecture_lower or 'native' in lecture_lower:
        if 'service' in algo_lower and 'mesh' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('service_mesh', {})
        elif 'serverless' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('serverless_architecture', {})
        elif 'function' in algo_lower or 'faas' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('function_as_service', {})
    
    elif 'observability' in lecture_lower or 'monitoring' in lecture_lower:
        if 'tracing' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('distributed_tracing', {})
        elif 'metric' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('metrics_collection', {})
        elif 'apm' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('apm', {})
    
    elif 'data' in lecture_lower and 'engineering' in lecture_lower:
        if 'mesh' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('data_mesh', {})
        elif 'stream' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('stream_processing_advanced', {})
        elif 'lambda' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('lambda_architecture', {})
    
    elif 'llm' in lecture_lower or 'ai' in lecture_lower:
        if 'architecture' in algo_lower or 'transformer' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('llm_architecture', {})
        elif 'fine' in algo_lower or 'tuning' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('fine_tuning_llm', {})
        elif 'rag' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('rag_advanced', {})
    
    elif 'database' in lecture_lower or 'sql' in lecture_lower:
        if 'optimization' in algo_lower or 'query' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('query_optimization', {})
        elif 'sharding' in algo_lower:
            return COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('database_sharding', {})
    
    # Generic examples based on lecture category
    if 'os' in lecture_lower or 'operating' in lecture_lower:
        return {'kubernetes': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('container_runtimes', {}).get('kubernetes', '')}
    elif 'concurrency' in lecture_lower or 'parallel' in lecture_lower:
        return {'python': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('actor_model', {}).get('python', '')}
    elif 'distributed' in lecture_lower:
        return {'kubernetes': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('consensus_algorithms', {}).get('kubernetes', '')}
    elif 'cloud' in lecture_lower or 'native' in lecture_lower:
        return {'kubernetes': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('service_mesh', {}).get('kubernetes', '')}
    elif 'observability' in lecture_lower or 'monitoring' in lecture_lower:
        return {'prometheus': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('metrics_collection', {}).get('prometheus', '')}
    elif 'data' in lecture_lower and 'engineering' in lecture_lower:
        return {'kubernetes': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('data_mesh', {}).get('kubernetes', '')}
    elif 'llm' in lecture_lower or 'ai' in lecture_lower:
        return {'huggingface': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('llm_architecture', {}).get('huggingface', '')}
    elif 'database' in lecture_lower or 'sql' in lecture_lower:
        return {'postgresql': COMPREHENSIVE_FRAMEWORK_EXAMPLES.get('query_optimization', {}).get('postgresql', '')}
    
    return {}


def add_framework_examples_to_readme(readme_path: Path, algorithm_name: str, lecture_name: str) -> bool:
    """Add framework examples to README."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        
        # Get examples
        examples = get_framework_examples(algorithm_name, lecture_name)
        
        # Filter out empty examples
        examples = {k: v for k, v in examples.items() if v and v.strip()}
        
        if not examples:
            return False
        
        # Find Examples section
        examples_patterns = [
            r'(## Examples of Implementation\s*\n\s*\n)(.*?)(?=\n##|\Z)',
            r'(## Examples of Deployment\s*\n\s*\n)(.*?)(?=\n##|\Z)',
            r'(## Examples of Impl[^\n]*\s*\n\s*\n)(.*?)(?=\n##|\Z)',
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
        
        # Build new examples
        new_examples = ""
        
        # Determine code block language and framework name
        framework_map = {
            'docker': ('dockerfile', 'Docker'),
            'kubernetes': ('yaml', 'Kubernetes'),
            'terraform': ('hcl', 'Terraform'),
            'python': ('python', 'Python'),
            'java': ('java', 'Java'),
            'cuda': ('cuda', 'CUDA'),
            'istio': ('yaml', 'Istio'),
            'aws': ('python', 'AWS Lambda'),
            'opentelemetry': ('python', 'OpenTelemetry'),
            'prometheus': ('python', 'Prometheus'),
            'elastic': ('python', 'Elastic APM'),
            'kafka': ('python', 'Apache Kafka'),
            'postgresql': ('sql', 'PostgreSQL'),
            'pytorch': ('python', 'PyTorch'),
            'huggingface': ('python', 'Hugging Face'),
            'langchain': ('python', 'LangChain'),
        }
        
        for key, code in examples.items():
            if key in framework_map:
                lang, framework_name = framework_map[key]
                
                # Check if already exists
                if framework_name in existing_section:
                    continue
                
                new_examples += f"### {framework_name}\n\n"
                new_examples += f"```{lang}\n{code}\n```\n\n"
                
                # Add purpose based on framework
                purposes = {
                    'Docker': 'Docker uses this for containerization and runtime management.',
                    'Kubernetes': 'Kubernetes uses this for container orchestration and cluster management.',
                    'Terraform': 'Terraform uses this for infrastructure as code and cloud provisioning.',
                    'Python': 'Python libraries provide implementations for this pattern/algorithm.',
                    'Java': 'Java frameworks use this for enterprise application development.',
                    'CUDA': 'CUDA enables GPU-accelerated computing for this algorithm.',
                    'Istio': 'Istio service mesh uses this for traffic management and observability.',
                    'AWS Lambda': 'AWS Lambda provides serverless execution for this pattern.',
                    'OpenTelemetry': 'OpenTelemetry provides distributed tracing capabilities.',
                    'Prometheus': 'Prometheus collects and stores metrics for monitoring.',
                    'Elastic APM': 'Elastic APM provides application performance monitoring.',
                    'Apache Kafka': 'Apache Kafka enables stream processing and event-driven architectures.',
                    'PostgreSQL': 'PostgreSQL database uses this for data management and optimization.',
                    'PyTorch': 'PyTorch provides deep learning capabilities for this algorithm.',
                    'Hugging Face': 'Hugging Face provides pre-trained models and fine-tuning tools.',
                    'LangChain': 'LangChain provides RAG and LLM integration capabilities.',
                }
                
                new_examples += f"**Purpose**: {purposes.get(framework_name, 'Framework-specific implementation.')}\n\n"
        
        if new_examples:
            # Clean existing section
            if '*Note: Framework-specific examples will be added' in existing_section:
                existing_section = existing_section.replace(
                    '*Note: Framework-specific examples will be added based on actual implementations.*',
                    ''
                ).replace(
                    '*Note: Framework-specific examples will be added*',
                    ''
                ).strip()
            
            # Append new examples
            section_start = match.start(2)
            section_end = match.end(2)
            
            if existing_section.strip() and existing_section.strip() != '':
                new_section = existing_section.rstrip() + "\n\n" + new_examples.strip()
            else:
                new_section = new_examples.strip()
            
            content = content[:section_start] + new_section + "\n\n" + content[section_end:]
            readme_path.write_text(content, encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Execute Phase 8: Comprehensive Framework Examples Expansion."""
    print("=" * 70)
    print("Phase 8: Comprehensive Framework Examples Expansion")
    print("=" * 70)
    
    candidates = find_readme_files_for_expansion()
    print(f"\nFound {len(candidates)} README files that could use more framework examples")
    
    updated_count = 0
    framework_counts = {}
    
    for i, (readme_path, algo_name, lecture_name) in enumerate(candidates, 1):
        if add_framework_examples_to_readme(readme_path, algo_name, lecture_name):
            updated_count += 1
            
            # Track frameworks added
            content = readme_path.read_text(encoding='utf-8')
            for fw in ['Kubernetes', 'Docker', 'Terraform', 'Prometheus', 'Istio', 
                       'Kafka', 'PostgreSQL', 'PyTorch', 'Hugging Face', 'LangChain']:
                if fw in content:
                    framework_counts[fw] = framework_counts.get(fw, 0) + 1
            
            if updated_count % 50 == 0:
                print(f"[PROGRESS] Processed {i}/{len(candidates)} files, updated {updated_count}...")
    
    print(f"\n[COMPLETE] Processed {len(candidates)} files")
    print(f"Updated {updated_count} files with framework examples")
    print("\nFrameworks added:")
    for fw, count in sorted(framework_counts.items(), key=lambda x: -x[1]):
        print(f"  - {fw}: {count} files")
    print("\nCoverage areas:")
    print("  - Operating Systems (container runtimes, scheduling)")
    print("  - Concurrency & Parallel Computing (actors, lock-free, GPU)")
    print("  - Distributed Systems (consensus, vector clocks, CRDTs)")
    print("  - Cloud Native (service mesh, serverless, FaaS)")
    print("  - Observability (tracing, metrics, APM)")
    print("  - Data Engineering (data mesh, stream processing)")
    print("  - Databases (query optimization, sharding)")
    print("  - LLM & AI (transformers, fine-tuning, RAG)")


if __name__ == "__main__":
    main()

