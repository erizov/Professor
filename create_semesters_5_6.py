#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Semesters 5 and 6 with AI/ML focus."""

import json
from pathlib import Path


SEMESTERS_5_6 = {
    "semester_5": {
        "lecture_21_transfer_learning": [
            {"folder": "transfer_learning", "name": "Transfer Learning", 
             "category": "Deep Learning", "time": "O(n*d*h)", 
             "space": "O(d*h)"},
            {"folder": "fine_tuning", "name": "Fine-Tuning Pre-trained Models", 
             "category": "Deep Learning", "time": "O(n*d)", 
             "space": "O(d*h)"},
            {"folder": "feature_extraction", "name": "Feature Extraction", 
             "category": "Deep Learning", "time": "O(n*d)", 
             "space": "O(d)"},
        ],
        "lecture_22_cnn_architectures": [
            {"folder": "resnet", "name": "ResNet Architecture", 
             "category": "Deep Learning", "time": "O(n*d*layers)", 
             "space": "O(d*layers)"},
            {"folder": "vgg", "name": "VGG Network", 
             "category": "Deep Learning", "time": "O(n*d*depth)", 
             "space": "O(d*depth)"},
            {"folder": "inception", "name": "Inception Network", 
             "category": "Deep Learning", "time": "O(n*d*modules)", 
             "space": "O(d*modules)"},
            {"folder": "efficientnet", "name": "EfficientNet", 
             "category": "Deep Learning", "time": "O(n*d*scale)", 
             "space": "O(d*scale)"},
        ],
        "lecture_23_object_detection": [
            {"folder": "yolo", "name": "YOLO Object Detection", 
             "category": "Computer Vision", "time": "O(S²*B*C)", 
             "space": "O(S²*B)"},
            {"folder": "rcnn", "name": "R-CNN", 
             "category": "Computer Vision", "time": "O(n*proposals)", 
             "space": "O(proposals)"},
            {"folder": "ssd", "name": "Single Shot Detector", 
             "category": "Computer Vision", "time": "O(n*anchors)", 
             "space": "O(anchors)"},
        ],
        "lecture_24_segmentation": [
            {"folder": "unet", "name": "U-Net Segmentation", 
             "category": "Computer Vision", "time": "O(n*H*W)", 
             "space": "O(H*W*channels)"},
            {"folder": "fcn", "name": "Fully Convolutional Networks", 
             "category": "Computer Vision", "time": "O(n*H*W)", 
             "space": "O(H*W)"},
            {"folder": "mask_rcnn", "name": "Mask R-CNN", 
             "category": "Computer Vision", "time": "O(n*proposals)", 
             "space": "O(proposals*mask)"},
        ],
        "lecture_25_transformers": [
            {"folder": "transformer", "name": "Transformer Architecture", 
             "category": "NLP", "time": "O(n²*d)", 
             "space": "O(n*d)"},
            {"folder": "bert", "name": "BERT Language Model", 
             "category": "NLP", "time": "O(n²*d)", 
             "space": "O(n*d)"},
            {"folder": "gpt", "name": "GPT Architecture", 
             "category": "NLP", "time": "O(n²*d)", 
             "space": "O(n*d)"},
            {"folder": "attention", "name": "Attention Mechanism", 
             "category": "NLP", "time": "O(n²*d)", 
             "space": "O(n²)"},
        ],
        "lecture_26_ensemble_methods": [
            {"folder": "bagging", "name": "Bagging", 
             "category": "Ensemble Learning", "time": "O(n*m*trees)", 
             "space": "O(n*trees)"},
            {"folder": "boosting", "name": "Boosting", 
             "category": "Ensemble Learning", "time": "O(n*m*iterations)", 
             "space": "O(n*iterations)"},
            {"folder": "stacking", "name": "Stacking", 
             "category": "Ensemble Learning", "time": "O(n*m*models)", 
             "space": "O(n*models)"},
        ],
        "lecture_27_hyperparameter_optimization": [
            {"folder": "grid_search", "name": "Grid Search", 
             "category": "Optimization", "time": "O(n*combinations)", 
             "space": "O(n)"},
            {"folder": "random_search", "name": "Random Search", 
             "category": "Optimization", "time": "O(n*iterations)", 
             "space": "O(n)"},
            {"folder": "bayesian_optimization", 
             "name": "Bayesian Optimization", 
             "category": "Optimization", "time": "O(n*iterations)", 
             "space": "O(iterations)"},
            {"folder": "optuna", "name": "Optuna Framework", 
             "category": "Optimization", "time": "O(n*trials)", 
             "space": "O(trials)"},
        ],
        "lecture_28_reinforcement_learning": [
            {"folder": "q_learning", "name": "Q-Learning", 
             "category": "Reinforcement Learning", "time": "O(states*actions)", 
             "space": "O(states*actions)"},
            {"folder": "dqn", "name": "Deep Q-Network", 
             "category": "Reinforcement Learning", "time": "O(episodes*steps)", 
             "space": "O(replay_buffer)"},
            {"folder": "policy_gradient", "name": "Policy Gradient", 
             "category": "Reinforcement Learning", "time": "O(episodes*steps)", 
             "space": "O(network_params)"},
            {"folder": "actor_critic", "name": "Actor-Critic", 
             "category": "Reinforcement Learning", "time": "O(episodes*steps)", 
             "space": "O(2*network_params)"},
            {"folder": "ppo", "name": "Proximal Policy Optimization", 
             "category": "Reinforcement Learning", "time": "O(episodes*steps)", 
             "space": "O(network_params)"},
        ],
        "lecture_29_nlp_advanced": [
            {"folder": "word2vec", "name": "Word2Vec", 
             "category": "NLP", "time": "O(V*d*corpus)", 
             "space": "O(V*d)"},
            {"folder": "glove", "name": "GloVe Embeddings", 
             "category": "NLP", "time": "O(V²*iterations)", 
             "space": "O(V*d)"},
            {"folder": "seq2seq", "name": "Sequence-to-Sequence", 
             "category": "NLP", "time": "O(n*m*d)", 
             "space": "O(n*d)"},
            {"folder": "ner", "name": "Named Entity Recognition", 
             "category": "NLP", "time": "O(n*d)", 
             "space": "O(n)"},
        ],
        "lecture_30_time_series": [
            {"folder": "arima", "name": "ARIMA", 
             "category": "Time Series", "time": "O(n*p*d*q)", 
             "space": "O(n)"},
            {"folder": "lstm_timeseries", "name": "LSTM for Time Series", 
             "category": "Time Series", "time": "O(n*timesteps*d)", 
             "space": "O(timesteps*d)"},
            {"folder": "prophet", "name": "Facebook Prophet", 
             "category": "Time Series", "time": "O(n*iterations)", 
             "space": "O(n)"},
        ],
    },
    "semester_6": {
        "lecture_31_mlops": [
            {"folder": "model_versioning", "name": "Model Versioning", 
             "category": "MLOps", "time": "O(1)", 
             "space": "O(model_size)"},
            {"folder": "ab_testing", "name": "A/B Testing for ML", 
             "category": "MLOps", "time": "O(requests)", 
             "space": "O(metrics)"},
            {"folder": "feature_store", "name": "Feature Store Pattern", 
             "category": "MLOps", "time": "O(features)", 
             "space": "O(features*time)"},
            {"folder": "model_monitoring", "name": "Model Monitoring", 
             "category": "MLOps", "time": "O(predictions)", 
             "space": "O(logs)"},
            {"folder": "data_drift", "name": "Data Drift Detection", 
             "category": "MLOps", "time": "O(n*features)", 
             "space": "O(n)"},
        ],
        "lecture_32_distributed_ml": [
            {"folder": "data_parallelism", "name": "Data Parallelism", 
             "category": "Distributed ML", "time": "O(n/workers)", 
             "space": "O(model + n/workers)"},
            {"folder": "model_parallelism", "name": "Model Parallelism", 
             "category": "Distributed ML", "time": "O(n*layers/workers)", 
             "space": "O(model/workers)"},
            {"folder": "parameter_server", "name": "Parameter Server", 
             "category": "Distributed ML", "time": "O(sync_overhead)", 
             "space": "O(params)"},
            {"folder": "allreduce", "name": "AllReduce Algorithm", 
             "category": "Distributed ML", "time": "O(log(workers))", 
             "space": "O(params)"},
            {"folder": "federated_learning", "name": "Federated Learning", 
             "category": "Distributed ML", "time": "O(rounds*clients)", 
             "space": "O(model)"},
        ],
        "lecture_33_model_optimization": [
            {"folder": "quantization", "name": "Model Quantization", 
             "category": "Optimization", "time": "O(params)", 
             "space": "O(params/bits)"},
            {"folder": "pruning", "name": "Model Pruning", 
             "category": "Optimization", "time": "O(params)", 
             "space": "O(remaining_params)"},
            {"folder": "knowledge_distillation", 
             "name": "Knowledge Distillation", 
             "category": "Optimization", "time": "O(n*student)", 
             "space": "O(student_model)"},
            {"folder": "nas", "name": "Neural Architecture Search", 
             "category": "Optimization", "time": "O(search_space*trials)", 
             "space": "O(candidates)"},
            {"folder": "tensorrt", "name": "TensorRT Optimization", 
             "category": "Optimization", "time": "O(inference)", 
             "space": "O(optimized_model)"},
            {"folder": "onnx", "name": "ONNX Model Conversion", 
             "category": "Optimization", "time": "O(model_size)", 
             "space": "O(model_size)"},
        ],
        "lecture_34_edge_ai": [
            {"folder": "edge_deployment", "name": "Edge AI Deployment", 
             "category": "Edge Computing", "time": "O(inference)", 
             "space": "O(compressed_model)"},
            {"folder": "tflite", "name": "TensorFlow Lite", 
             "category": "Edge Computing", "time": "O(inference)", 
             "space": "O(lite_model)"},
            {"folder": "mobile_optimization", "name": "Mobile Optimization", 
             "category": "Edge Computing", "time": "O(inference)", 
             "space": "O(mobile_model)"},
            {"folder": "iot_ml", "name": "IoT Machine Learning", 
             "category": "Edge Computing", "time": "O(inference)", 
             "space": "O(tiny_model)"},
        ],
        "lecture_35_deployment_patterns": [
            {"folder": "blue_green_ml", "name": "Blue-Green ML Deployment", 
             "category": "Deployment", "time": "O(1)", 
             "space": "O(2*model)"},
            {"folder": "canary_ml", "name": "Canary Deployment", 
             "category": "Deployment", "time": "O(1)", 
             "space": "O(model)"},
            {"folder": "shadow_deployment", "name": "Shadow Deployment", 
             "category": "Deployment", "time": "O(2*requests)", 
             "space": "O(2*model)"},
            {"folder": "multi_armed_bandit", 
             "name": "Multi-Armed Bandit", 
             "category": "Deployment", "time": "O(requests)", 
             "space": "O(arms)"},
        ],
        "lecture_36_inference_optimization": [
            {"folder": "batch_inference", "name": "Batch Inference", 
             "category": "Inference", "time": "O(n/batch)", 
             "space": "O(batch_size)"},
            {"folder": "model_caching", "name": "Model Caching", 
             "category": "Inference", "time": "O(1)", 
             "space": "O(cache_size)"},
            {"folder": "inference_pipeline", "name": "Inference Pipeline", 
             "category": "Inference", "time": "O(stages)", 
             "space": "O(pipeline)"},
            {"folder": "gpu_optimization", "name": "GPU Optimization", 
             "category": "Inference", "time": "O(n/parallelism)", 
             "space": "O(vram)"},
        ],
        "lecture_37_cost_optimization": [
            {"folder": "spot_instances", "name": "Spot Instance Training", 
             "category": "Cost Optimization", "time": "O(variable)", 
             "space": "O(checkpoints)"},
            {"folder": "autoscaling", "name": "Auto-scaling for ML", 
             "category": "Cost Optimization", "time": "O(dynamic)", 
             "space": "O(dynamic)"},
            {"folder": "serverless_ml", "name": "Serverless ML", 
             "category": "Cost Optimization", "time": "O(requests)", 
             "space": "O(0)"},
            {"folder": "cost_analysis", "name": "ML Cost Analysis", 
             "category": "Cost Optimization", "time": "O(resources)", 
             "space": "O(logs)"},
        ],
        "lecture_38_monitoring_production": [
            {"folder": "prometheus_ml", "name": "Prometheus for ML", 
             "category": "Monitoring", "time": "O(metrics)", 
             "space": "O(time_series)"},
            {"folder": "grafana_dashboards", "name": "Grafana Dashboards", 
             "category": "Monitoring", "time": "O(queries)", 
             "space": "O(dashboards)"},
            {"folder": "alerting", "name": "ML Alerting Systems", 
             "category": "Monitoring", "time": "O(rules)", 
             "space": "O(alerts)"},
            {"folder": "performance_profiling", 
             "name": "Performance Profiling", 
             "category": "Monitoring", "time": "O(profiling_overhead)", 
             "space": "O(profiles)"},
        ],
    }
}


def create_algorithm(semester: str, lecture: str, 
                    algo_info: dict) -> None:
    """Create algorithm structure."""
    base_path = Path(semester) / lecture / algo_info['folder']
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Metadata with resource info
    metadata = {
        "name": algo_info['name'],
        "category": algo_info['category'],
        "complexity": {
            "time": algo_info['time'],
            "space": algo_info['space']
        },
        "resources": {
            "memory_requirement": "varies",
            "cpu_intensive": True if 'Deep Learning' in algo_info['category'] else False,
            "gpu_recommended": True if 'Deep Learning' in algo_info['category'] or 'ML' in algo_info['category'] else False,
            "network_bandwidth": "low" if 'Edge' in algo_info['category'] else "medium"
        }
    }
    
    with open(base_path / "metadata.json", 'w', 
             encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Enhanced README
    readme = f"# {algo_info['name']}\n\n"
    readme += f"**Category**: {algo_info['category']}\n\n"
    readme += f"**Time Complexity**: {algo_info['time']}\n\n"
    readme += f"**Space Complexity**: {algo_info['space']}\n\n"
    readme += "## Resource Requirements\n\n"
    readme += f"- **Memory**: {metadata['resources']['memory_requirement']}\n"
    readme += f"- **CPU Intensive**: {'Yes' if metadata['resources']['cpu_intensive'] else 'No'}\n"
    readme += f"- **GPU Recommended**: {'Yes' if metadata['resources']['gpu_recommended'] else 'No'}\n"
    readme += f"- **Network**: {metadata['resources']['network_bandwidth']}\n\n"
    readme += "## Implementation\n\n"
    readme += "See algorithm.py and Algorithm.java for implementations.\n\n"
    readme += "## Performance Considerations\n\n"
    readme += f"This algorithm is part of {algo_info['category']} and requires "
    readme += "careful consideration of resource constraints.\n"
    
    with open(base_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    
    # Python with timing
    func_name = algo_info['folder']
    py_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""{algo_info['name']} implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def {func_name}():
    """
    Implement {algo_info['name']}.
    
    Category: {algo_info['category']}
    Time Complexity: {algo_info['time']}
    Space Complexity: {algo_info['space']}
    """
    print("==" * 35)
    print("{algo_info['name']}")
    print("==" * 35)
    print(f"Category: {algo_info['category']}")
    print(f"Time Complexity: {algo_info['time']}")
    print(f"Space Complexity: {algo_info['space']}")
    print()
    print("Resource Requirements:")
    print("  - GPU: {'Recommended' if 'Deep Learning' in algo_info['category'] else 'Optional'}")
    print("  - Memory: {'High' if 'Deep Learning' in algo_info['category'] else 'Medium'}")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("{algo_info['name']}")
    _, metrics = timer.measure({func_name})
    print(f"\\nExecution time: {{metrics['execution_time_ms']:.3f}} ms")
    print(f"Memory used: {{metrics['memory_peak_kb']:.2f}} KB")
'''
    
    with open(base_path / "algorithm.py", 'w', 
             encoding='utf-8') as f:
        f.write(py_code)
    
    # Java
    java_code = f'''/**
 * {algo_info['name']} implementation.
 * 
 * Category: {algo_info['category']}
 * Time Complexity: {algo_info['time']}
 * Space Complexity: {algo_info['space']}
 */
public class Algorithm {{
    public static void main(String[] args) {{
        long startTime = System.nanoTime();
        
        System.out.println("==".repeat(35));
        System.out.println("{algo_info['name']}");
        System.out.println("==".repeat(35));
        System.out.println("Category: {algo_info['category']}");
        System.out.println("Time: {algo_info['time']}");
        System.out.println("Space: {algo_info['space']}");
        System.out.println();
        System.out.println("Resource Requirements:");
        System.out.println("  - GPU: {'Recommended' if 'Deep Learning' in algo_info['category'] else 'Optional'}");
        System.out.println("  - Memory: {'High' if 'Deep Learning' in algo_info['category'] else 'Medium'}");
        System.out.println("==".repeat(35));
        
        long endTime = System.nanoTime();
        double durationMs = (endTime - startTime) / 1_000_000.0;
        System.out.println(String.format("\\nExecution time: %.3f ms", durationMs));
    }}
}}
'''
    
    with open(base_path / "Algorithm.java", 'w', 
             encoding='utf-8') as f:
        f.write(java_code)


def main() -> None:
    """Generate semesters 5 and 6."""
    total = 0
    
    for semester, lectures in SEMESTERS_5_6.items():
        for lecture, algorithms in lectures.items():
            for algo in algorithms:
                create_algorithm(semester, lecture, algo)
                total += 1
                print(f"Created: {semester}/{lecture}/{algo['folder']}")
    
    print(f"\nSemesters 5-6 algorithms created: {total}")


if __name__ == "__main__":
    main()

