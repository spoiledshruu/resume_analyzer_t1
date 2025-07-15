import matplotlib.pyplot as plt
import torch
import numpy as np

def plot_role_prediction_confidence(roles, confidences):
    """
    Return a Matplotlib figure showing role prediction confidence scores.
    Args:
        roles (list[str]): List of role names.
        confidences (torch.Tensor or list[float]): Corresponding confidence scores (0-1).
    Returns:
        matplotlib.figure.Figure
    """
    # Convert to numpy array if tensor
    if isinstance(confidences, torch.Tensor):
        confidences = confidences.numpy()
    
    # Sort roles by confidence descending
    sorted_indices = np.argsort(confidences)[::-1]
    roles_sorted = [roles[i] for i in sorted_indices]
    confidences_sorted = confidences[sorted_indices]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(roles_sorted, confidences_sorted, color='mediumseagreen')
    ax.set_xlabel('Confidence Score')
    ax.set_title('Role Prediction Confidence')
    ax.set_xlim(0, 1)

    # Add confidence labels on bars
    for bar, score in zip(bars, confidences_sorted):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, f'{score:.2f}', va='center')

    ax.invert_yaxis()  # Highest confidence on top
    fig.tight_layout()
    
    return fig
