# Feedforward Neural Network

1. **Name of Algorithm**  
   Feedforward Neural Network

2. **What problem does it solve? (1 sentence)**  
   Approximates complex non-linear mappings between inputs and outputs using layered compositions of linear transformations and activation functions.

3. **Intuition (plain-language explanation)**  
   Stack perceptrons: each layer learns increasingly abstract features, enabling the network to model intricate patterns beyond linear decision boundaries.

4. **Inputs & Outputs**  
   - Input: Training data (features X, labels y), network architecture (layers, neurons), activation functions, loss function, optimizer hyperparameters.  
   - Output: Trained network weights/biases capable of inference on unseen data; predicted outputs for inputs.

5. **Step-by-step description (5–10 lines max)**  
1. Define architecture: input layer, one or more hidden layers, output layer.
2. Initialize weights/biases (Xavier/He random).
3. Forward pass: compute activations layer by layer.
4. Compute loss between predictions and targets.
5. Backpropagate gradients via chain rule and update weights with optimizer.

6. **Tiny example (hand-simulated)**  
   MNIST digit classifier: 784→128→64→10 network with ReLU activations and softmax output trained via cross-entropy loss.

7. **Time & Space Complexity**  
   - Time: O(k · Σ layer_multiplications) roughly O(k · n · Σ (d_{l-1}·d_l)) for k epochs over n samples.  
   - Space: O(Σ (d_{l-1}·d_l)) for weights plus activations stored during backprop.

8. **Strengths**  
- Universal function approximators with sufficient width/depth.
- Can learn hierarchical representations automatically.

9. **Weaknesses / limitations**  
- Require large datasets and careful regularization to avoid overfitting.
- Training can be unstable (vanishing/exploding gradients).

10. **Compare with alternatives**  
    Alternatives: Convolutional Neural Networks, Recurrent Neural Networks, Gradient Boosting Machines

11. **30-second explanation (your own words)**  
    Layered neurons perform affine transformations followed by non-linear activations, and training adjusts weights via backpropagation to minimize loss on labeled data.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
