import glob
import os

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


# ============================================================
# Selected epoch for each fold
# ============================================================

folders = {
    "npy1": 31,
    "npy2": 93,
    "npy3": 69,
    "npy4": 97,
    "npy5": 60,
}

# Alternative epoch settings
# folders = {
#     "npy1": 89,
#     "npy3": 50,
#     "npy4": 58,
#     "npy5": 77,
# }

# folders = {
#     "npy1": 84,
#     "npy4": 94,
# }

# folders = {
#     "npy3": 42,
# }


# ============================================================
# Input and output paths
# ============================================================

base_path = "/Users/apple/Desktop/swin-wavelet/data/ideal/MASS_March"

output_path = (
    "/Users/apple/Desktop/A/old/swin-wavelet/"
    "data/best F1/average_metrics_results_march.xlsx"
)


# ============================================================
# Candidate threshold range
# ============================================================

thresholds = np.arange(0.01, 0.98, 0.01)

# A manually specified threshold can also be used
# thresholds = np.array([0.092])


# ============================================================
# Locate exactly one file matching a wildcard pattern
# ============================================================

def find_single_file(pattern, folder, epoch, file_type):
    """
    Find exactly one file matching the specified wildcard pattern.

    Parameters
    ----------
    pattern : str
        Full file path pattern containing wildcards.
    folder : str
        Name of the current fold folder.
    epoch : int
        Selected epoch number.
    file_type : str
        Description of the expected file type.

    Returns
    -------
    str
        Path of the matched file.

    Raises
    ------
    FileNotFoundError
        If no matching file is found.
    RuntimeError
        If multiple matching files are found.
    """
    matches = sorted(glob.glob(pattern))

    if len(matches) == 0:
        raise FileNotFoundError(
            f"No {file_type} file was found for "
            f"{folder}, epoch {epoch}.\n"
            f"Pattern: {pattern}"
        )

    if len(matches) > 1:
        matched_files = "\n".join(matches)

        raise RuntimeError(
            f"Multiple {file_type} files were found for "
            f"{folder}, epoch {epoch}:\n"
            f"{matched_files}"
        )

    return matches[0]


# ============================================================
# Load prediction scores and ground-truth labels
# ============================================================

def load_fold_data(folder, epoch):
    """
    Load prediction scores and ground-truth labels for one fold.
    """
    folder_path = os.path.join(base_path, folder)

    preds_pattern = os.path.join(
        folder_path,
        f"val_epoch_{epoch}*true_label_preds.npy"
    )

    labels_pattern = os.path.join(
        folder_path,
        f"val_epoch*{epoch}_labels.npy"
    )

    preds_path = find_single_file(
        preds_pattern,
        folder,
        epoch,
        "prediction"
    )

    labels_path = find_single_file(
        labels_pattern,
        folder,
        epoch,
        "label"
    )

    # Flatten arrays to one-dimensional vectors
    preds = np.asarray(
        np.load(preds_path),
        dtype=float
    ).reshape(-1)

    labels = np.asarray(
        np.load(labels_path),
        dtype=int
    ).reshape(-1)

    if len(preds) != len(labels):
        raise ValueError(
            f"Prediction and label lengths do not match for "
            f"{folder}, epoch {epoch}: "
            f"{len(preds)} predictions versus {len(labels)} labels."
        )

    # Create a copy before modifying prediction values
    preds = preds.copy()

    # Flip predictions corresponding to leading negative samples
    first_positive_index = next(
        (
            index
            for index, value in enumerate(labels)
            if value == 1
        ),
        None
    )

    if first_positive_index is not None:
        preds[:first_positive_index] = (
            1 - preds[:first_positive_index]
        )

    return preds, labels, preds_path, labels_path


# ============================================================
# Calculate evaluation metrics
# ============================================================

def calculate_metrics(threshold, preds, true_labels):
    """
    Calculate classification metrics using a specified threshold.
    """
    binary_preds = (preds >= threshold).astype(int)

    # labels=[0, 1] ensures that a 2 x 2 confusion matrix is
    # returned even when one class is absent
    tn, fp, fn, tp = confusion_matrix(
        true_labels,
        binary_preds,
        labels=[0, 1]
    ).ravel()

    accuracy = accuracy_score(
        true_labels,
        binary_preds
    )

    precision = precision_score(
        true_labels,
        binary_preds,
        zero_division=0
    )

    recall = recall_score(
        true_labels,
        binary_preds,
        zero_division=0
    )

    f1 = f1_score(
        true_labels,
        binary_preds,
        zero_division=0
    )

    kappa = cohen_kappa_score(
        true_labels,
        binary_preds
    )

    return {
        "Threshold": threshold,
        "TP": int(tp),
        "FP": int(fp),
        "TN": int(tn),
        "FN": int(fn),
        "ACC": accuracy,
        "Recall": recall,
        "Precision": precision,
        "Kappa": kappa,
        "F1": f1,
    }


# ============================================================
# Load all selected folds
# ============================================================

fold_data = {}

for folder, epoch in folders.items():
    preds, labels, preds_path, labels_path = load_fold_data(
        folder,
        epoch
    )

    fold_data[folder] = {
        "epoch": epoch,
        "preds": preds,
        "labels": labels,
        "preds_path": preds_path,
        "labels_path": labels_path,
    }

    print(
        f"Loaded {folder}, epoch {epoch}: "
        f"{len(labels)} samples"
    )


# ============================================================
# Calculate F1 scores at all candidate thresholds
# ============================================================

f1_results = []

for folder, data in fold_data.items():
    folder_f1_scores = []

    for threshold in thresholds:
        metrics = calculate_metrics(
            threshold,
            data["preds"],
            data["labels"]
        )

        folder_f1_scores.append(metrics["F1"])

    f1_results.append(folder_f1_scores)


# ============================================================
# Select the threshold with the highest average F1 score
# ============================================================

f1_results = np.asarray(f1_results)

average_f1 = np.mean(
    f1_results,
    axis=0
)

best_threshold_index = int(
    np.argmax(average_f1)
)

best_threshold = float(
    thresholds[best_threshold_index]
)

best_average_f1 = float(
    average_f1[best_threshold_index]
)

# A manually specified threshold can be used instead
# best_threshold = 0.0848


# ============================================================
# Calculate fold-level metrics using the shared best threshold
# ============================================================

metrics_results = []

for folder, data in fold_data.items():
    metrics = calculate_metrics(
        best_threshold,
        data["preds"],
        data["labels"]
    )

    metrics["Folder"] = folder
    metrics["Epoch"] = data["epoch"]
    metrics["Predictions Path"] = data["preds_path"]
    metrics["Labels Path"] = data["labels_path"]

    metrics_results.append(metrics)


# ============================================================
# Save evaluation results to an Excel file
# ============================================================

metrics_df = pd.DataFrame(metrics_results)

# Arrange columns in a clearer order
column_order = [
    "Folder",
    "Epoch",
    "Threshold",
    "TP",
    "FP",
    "TN",
    "FN",
    "ACC",
    "Recall",
    "Precision",
    "Kappa",
    "F1",
    "Predictions Path",
    "Labels Path",
]

metrics_df = metrics_df[column_order]

# Create the output directory if it does not exist
os.makedirs(
    os.path.dirname(output_path),
    exist_ok=True
)

metrics_df.to_excel(
    output_path,
    index=False
)


# ============================================================
# Display the final results
# ============================================================

print("\n===== Shared Threshold Selection =====")
print(f"Best threshold: {best_threshold:.3f}")
print(f"Best average F1 score: {best_average_f1:.4f}")

print("\n===== Fold-Level Results =====")

for _, row in metrics_df.iterrows():
    print(
        f"{row['Folder']} | "
        f"Epoch {int(row['Epoch'])} | "
        f"F1 = {row['F1']:.4f} | "
        f"Precision = {row['Precision']:.4f} | "
        f"Recall = {row['Recall']:.4f} | "
        f"Kappa = {row['Kappa']:.4f}"
    )

print("\n===== Average Metrics Across Folds =====")
print(f"ACC:       {metrics_df['ACC'].mean():.4f}")
print(f"Recall:    {metrics_df['Recall'].mean():.4f}")
print(f"Precision: {metrics_df['Precision'].mean():.4f}")
print(f"Kappa:     {metrics_df['Kappa'].mean():.4f}")
print(f"F1:        {metrics_df['F1'].mean():.4f}")

print(f"\nAll metrics have been saved to: {output_path}")
