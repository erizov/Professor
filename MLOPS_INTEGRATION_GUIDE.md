# MLOps Integration Guide
## Production-Ready Computational Intelligence Deployment

**Purpose**: Guide for deploying computational intelligence systems to production with monitoring, CI/CD, and best practices.

---

## Overview

MLOps (Machine Learning Operations) combines CI/CD, monitoring, and DevOps practices for computational intelligence systems. This guide covers production deployment patterns for CI algorithms.

---

## Model Serving

### TensorFlow Serving

**Example: Serving a Neural Network**

```python
# model_serving_tensorflow.py
import tensorflow as tf
from tensorflow import keras
import numpy as np

class ModelServer:
    """TensorFlow Serving wrapper."""
    
    def __init__(self, model_path: str):
        """Load model for serving."""
        self.model = keras.models.load_model(model_path)
        self.model.compile()
    
    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.model.predict(input_data)
    
    def health_check(self) -> dict:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "model_loaded": self.model is not None
        }

# Usage
server = ModelServer("models/neural_network.h5")
predictions = server.predict(input_data)
```

### TorchServe

**Example: Serving PyTorch Models**

```python
# model_serving_pytorch.py
import torch
import torch.nn as nn
from torchvision import transforms

class PyTorchModelServer:
    """PyTorch model serving."""
    
    def __init__(self, model_path: str):
        """Load PyTorch model."""
        self.model = torch.load(model_path)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
    
    def predict(self, input_data):
        """Make predictions."""
        with torch.no_grad():
            input_tensor = self.transform(input_data)
            output = self.model(input_tensor)
            return output.numpy()
```

### REST API Serving

**Example: Flask API for Model Serving**

```python
# api_serving.py
from flask import Flask, request, jsonify
import numpy as np
from model_server import ModelServer

app = Flask(__name__)
model_server = ModelServer("models/model.h5")

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint."""
    try:
        data = request.json
        input_data = np.array(data['input'])
        predictions = model_server.predict(input_data)
        return jsonify({
            'predictions': predictions.tolist(),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify(model_server.health_check())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## Monitoring

### Prometheus Metrics

**Example: Model Performance Monitoring**

```python
# monitoring_prometheus.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
prediction_counter = Counter(
    'model_predictions_total',
    'Total number of predictions',
    ['model_name', 'status']
)

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency',
    ['model_name']
)

model_accuracy = Gauge(
    'model_accuracy',
    'Current model accuracy',
    ['model_name']
)

def monitor_prediction(model_name: str, func):
    """Decorator to monitor predictions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            prediction_counter.labels(
                model_name=model_name,
                status='success'
            ).inc()
            return result
        except Exception as e:
            prediction_counter.labels(
                model_name=model_name,
                status='error'
            ).inc()
            raise
        finally:
            latency = time.time() - start_time
            prediction_latency.labels(model_name=model_name).observe(latency)
    return wrapper

# Usage
@monitor_prediction('neural_network')
def predict(input_data):
    return model.predict(input_data)
```

### Grafana Dashboards

**Key Metrics to Monitor:**
- Prediction latency (p50, p95, p99)
- Prediction throughput (requests/second)
- Error rate
- Model accuracy (if ground truth available)
- Resource usage (CPU, memory, GPU)
- Data drift detection

---

## CI/CD for Models

### GitHub Actions Workflow

**Example: Model Training and Deployment Pipeline**

```yaml
# .github/workflows/mlops.yml
name: MLOps Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Train model
        run: |
          python train_model.py
      - name: Run tests
        run: |
          pytest tests/
      - name: Evaluate model
        run: |
          python evaluate_model.py
      - name: Upload model
        uses: actions/upload-artifact@v2
        with:
          name: model
          path: models/

  deploy:
    needs: train
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Deployment steps
          kubectl apply -f k8s/deployment.yaml
```

### MLflow Integration

**Example: Model Versioning and Tracking**

```python
# mlflow_tracking.py
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Start MLflow run
with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("plots/confusion_matrix.png")
```

---

## Deployment Patterns

### Blue-Green Deployment

**Strategy**: Run two identical production environments, switch traffic between them.

**Benefits:**
- Zero-downtime deployments
- Easy rollback
- Safe testing in production

**Implementation:**
```python
# blue_green_deployment.py
class BlueGreenDeployer:
    """Blue-green deployment manager."""
    
    def __init__(self):
        self.blue_version = "v1.0"
        self.green_version = "v2.0"
        self.active = "blue"
    
    def deploy_green(self, new_model):
        """Deploy new model to green environment."""
        # Deploy to green
        # Run smoke tests
        # If successful, switch traffic
        if self._validate_green(new_model):
            self.active = "green"
            return True
        return False
    
    def rollback(self):
        """Rollback to previous version."""
        self.active = "blue" if self.active == "green" else "green"
```

### Canary Deployment

**Strategy**: Gradually roll out new version to small percentage of traffic.

**Benefits:**
- Risk mitigation
- Gradual rollout
- Real-world testing

**Implementation:**
```python
# canary_deployment.py
class CanaryDeployer:
    """Canary deployment manager."""
    
    def __init__(self):
        self.canary_percentage = 0
        self.max_canary = 50  # 50% max
    
    def deploy_canary(self, new_model, percentage: int):
        """Deploy canary version."""
        self.canary_percentage = min(percentage, self.max_canary)
        # Route percentage of traffic to canary
        # Monitor metrics
        # Gradually increase if successful
    
    def promote(self):
        """Promote canary to full deployment."""
        self.canary_percentage = 100
```

### A/B Testing

**Strategy**: Test two versions simultaneously with different user groups.

**Implementation:**
```python
# ab_testing.py
import random

class ABTester:
    """A/B testing for models."""
    
    def __init__(self):
        self.model_a = None
        self.model_b = None
        self.split = 0.5  # 50/50 split
    
    def get_model(self, user_id: str):
        """Get model for user based on A/B test."""
        # Consistent assignment based on user_id
        if hash(user_id) % 100 < self.split * 100:
            return self.model_a
        return self.model_b
    
    def evaluate(self, metrics_a: dict, metrics_b: dict):
        """Evaluate A/B test results."""
        # Statistical significance testing
        # Choose winner
        if metrics_b['accuracy'] > metrics_a['accuracy']:
            return 'B'
        return 'A'
```

---

## Data Drift Detection

**Example: Detecting Distribution Changes**

```python
# data_drift_detection.py
from scipy import stats
import numpy as np

class DataDriftDetector:
    """Detect data drift in production."""
    
    def __init__(self, reference_data: np.ndarray):
        """Initialize with reference data."""
        self.reference_data = reference_data
        self.reference_dist = self._compute_distribution(reference_data)
    
    def _compute_distribution(self, data: np.ndarray) -> dict:
        """Compute data distribution."""
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'min': np.min(data),
            'max': np.max(data)
        }
    
    def detect_drift(self, new_data: np.ndarray, threshold: float = 0.05) -> bool:
        """Detect if data has drifted."""
        new_dist = self._compute_distribution(new_data)
        
        # Kolmogorov-Smirnov test
        statistic, p_value = stats.ks_2samp(
            self.reference_data,
            new_data
        )
        
        return p_value < threshold
```

---

## Model Retraining

**Example: Automated Retraining Pipeline**

```python
# model_retraining.py
class ModelRetrainingPipeline:
    """Automated model retraining."""
    
    def __init__(self, model_class, retrain_threshold: float = 0.05):
        self.model_class = model_class
        self.retrain_threshold = retrain_threshold
        self.current_model = None
        self.reference_accuracy = None
    
    def should_retrain(self, current_accuracy: float) -> bool:
        """Determine if model should be retrained."""
        if self.reference_accuracy is None:
            self.reference_accuracy = current_accuracy
            return False
        
        accuracy_drop = self.reference_accuracy - current_accuracy
        return accuracy_drop > self.retrain_threshold
    
    def retrain(self, new_data, new_labels):
        """Retrain model with new data."""
        # Combine old and new data
        # Retrain model
        # Validate new model
        # Deploy if better
        new_model = self.model_class()
        new_model.fit(new_data, new_labels)
        return new_model
```

---

## Best Practices

### 1. Version Control
- Version all models
- Track model lineage
- Document model changes

### 2. Testing
- Unit tests for model code
- Integration tests for pipelines
- Performance tests for latency

### 3. Monitoring
- Monitor prediction latency
- Track error rates
- Detect data drift
- Monitor model accuracy

### 4. Security
- Secure model endpoints
- Encrypt model artifacts
- Control access to models
- Audit model usage

### 5. Documentation
- Document model architecture
- Document deployment process
- Document monitoring setup
- Document rollback procedures

---

*This guide provides production-ready patterns for deploying computational intelligence systems. Adapt based on your specific infrastructure and requirements.*

