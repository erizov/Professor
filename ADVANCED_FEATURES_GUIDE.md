# Advanced Features Guide
## Advanced Computational Intelligence Techniques

**Purpose**: Guide for advanced features including distributed training, bias/fairness, explainability, and ethical considerations.

---

## Distributed Training

### Data Parallelism

**Example: Distributed Training with Horovod**

```python
# distributed_training_horovod.py
import horovod.torch as hvd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Initialize Horovod
hvd.init()

# Pin GPU to local rank
torch.cuda.set_device(hvd.local_rank())

# Create model
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)
model.cuda()

# Wrap optimizer with Horovod
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
optimizer = hvd.DistributedOptimizer(optimizer)

# Broadcast initial parameters
hvd.broadcast_parameters(model.state_dict(), root_rank=0)

# Distributed data loader
train_dataset = YourDataset()
train_sampler = torch.utils.data.distributed.DistributedSampler(
    train_dataset,
    num_replicas=hvd.size(),
    rank=hvd.rank()
)
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    sampler=train_sampler
)

# Training loop
for epoch in range(10):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = nn.CrossEntropyLoss()(output, target)
        loss.backward()
        optimizer.step()
```

### Model Parallelism

**Example: Large Model Splitting**

```python
# model_parallelism.py
import torch
import torch.nn as nn

class ModelParallel(nn.Module):
    """Model split across multiple GPUs."""
    
    def __init__(self):
        super().__init__()
        # First part on GPU 0
        self.layer1 = nn.Linear(784, 512).cuda(0)
        # Second part on GPU 1
        self.layer2 = nn.Linear(512, 256).cuda(1)
        self.layer3 = nn.Linear(256, 10).cuda(1)
    
    def forward(self, x):
        # Move input to GPU 0
        x = x.cuda(0)
        x = self.layer1(x)
        # Move to GPU 1
        x = x.cuda(1)
        x = self.layer2(x)
        x = self.layer3(x)
        return x
```

---

## Bias and Fairness

### Fairness Metrics

**Example: Demographic Parity and Equalized Odds**

```python
# fairness_metrics.py
import numpy as np
from sklearn.metrics import confusion_matrix

class FairnessMetrics:
    """Calculate fairness metrics."""
    
    def __init__(self, y_true, y_pred, protected_attribute):
        self.y_true = y_true
        self.y_pred = y_pred
        self.protected_attribute = protected_attribute
        self.groups = np.unique(protected_attribute)
    
    def demographic_parity(self) -> dict:
        """Calculate demographic parity (equal positive rate)."""
        metrics = {}
        for group in self.groups:
            mask = self.protected_attribute == group
            positive_rate = np.mean(self.y_pred[mask] == 1)
            metrics[group] = positive_rate
        
        # Calculate difference
        max_rate = max(metrics.values())
        min_rate = min(metrics.values())
        metrics['difference'] = max_rate - min_rate
        
        return metrics
    
    def equalized_odds(self) -> dict:
        """Calculate equalized odds (equal TPR and FPR)."""
        metrics = {}
        for group in self.groups:
            mask = self.protected_attribute == group
            group_true = self.y_true[mask]
            group_pred = self.y_pred[mask]
            
            tn, fp, fn, tp = confusion_matrix(
                group_true, group_pred
            ).ravel()
            
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            
            metrics[group] = {
                'tpr': tpr,
                'fpr': fpr
            }
        
        # Calculate differences
        tprs = [m['tpr'] for m in metrics.values()]
        fprs = [m['fpr'] for m in metrics.values()]
        metrics['tpr_difference'] = max(tprs) - min(tprs)
        metrics['fpr_difference'] = max(fprs) - min(fprs)
        
        return metrics
```

### Bias Mitigation

**Example: Adversarial Debiasing**

```python
# bias_mitigation.py
import torch
import torch.nn as nn

class AdversarialDebiasing(nn.Module):
    """Adversarial debiasing for fairness."""
    
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        # Main predictor
        self.predictor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes)
        )
        # Adversary (tries to predict protected attribute)
        self.adversary = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, x, protected_attribute, adversarial=True):
        # Get representation
        representation = self.predictor[0](x)
        representation = self.predictor[1](representation)
        
        # Main prediction
        prediction = self.predictor[2](representation)
        
        if adversarial:
            # Adversary prediction
            adversary_pred = self.adversary(representation)
            return prediction, adversary_pred
        
        return prediction
```

---

## Explainability

### SHAP Values

**Example: SHAP for Model Explanation**

```python
# explainability_shap.py
import shap
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create SHAP explainer
explainer = shap.TreeExplainer(model)

# Calculate SHAP values
shap_values = explainer.shap_values(X_test)

# Visualize
shap.summary_plot(shap_values, X_test)
shap.waterfall_plot(explainer.expected_value[0], shap_values[0][0], X_test[0])
```

### LIME

**Example: Local Interpretable Model-Agnostic Explanations**

```python
# explainability_lime.py
from lime import lime_tabular
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create LIME explainer
explainer = lime_tabular.LimeTabularExplainer(
    X_train,
    feature_names=feature_names,
    class_names=class_names,
    mode='classification'
)

# Explain single prediction
explanation = explainer.explain_instance(
    X_test[0],
    model.predict_proba,
    num_features=10
)

# Show explanation
explanation.show_in_notebook(show_table=True)
```

### Feature Importance

**Example: Permutation Importance**

```python
# feature_importance.py
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Calculate permutation importance
perm_importance = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,
    random_state=42
)

# Get feature importance
feature_importance = perm_importance.importances_mean
feature_names = X.columns

# Sort by importance
indices = np.argsort(feature_importance)[::-1]

for i in indices:
    print(f"{feature_names[i]}: {feature_importance[i]:.4f}")
```

---

## Ethical Guidelines

### Ethical CI Checklist

**Before Deployment:**
- [ ] Data privacy reviewed
- [ ] Bias assessment completed
- [ ] Fairness metrics calculated
- [ ] Explainability provided
- [ ] Impact assessment done
- [ ] Consent obtained (if needed)
- [ ] Documentation complete

**During Operation:**
- [ ] Monitor for bias
- [ ] Track fairness metrics
- [ ] Review decisions
- [ ] Handle complaints
- [ ] Update documentation

**Ongoing:**
- [ ] Regular audits
- [ ] Bias retesting
- [ ] Model updates
- [ ] Stakeholder feedback

### Ethical Principles

1. **Fairness**: Treat all groups equitably
2. **Transparency**: Explain how decisions are made
3. **Privacy**: Protect user data
4. **Accountability**: Take responsibility for outcomes
5. **Human Oversight**: Maintain human control
6. **Beneficence**: Do good, avoid harm

---

## Best Practices

### 1. Distributed Training
- Use appropriate parallelism strategy
- Monitor communication overhead
- Optimize data loading
- Handle failures gracefully

### 2. Bias and Fairness
- Measure fairness metrics
- Mitigate bias in data and models
- Regular audits
- Diverse teams

### 3. Explainability
- Provide explanations for decisions
- Use multiple explanation methods
- Make explanations accessible
- Document explanation methods

### 4. Ethics
- Follow ethical guidelines
- Regular ethical reviews
- Stakeholder engagement
- Continuous improvement

---

*These advanced features are essential for production-ready, ethical computational intelligence systems.*

