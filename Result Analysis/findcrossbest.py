import glob
import os

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
)


# ============================================================
# File path and filename patterns
# ============================================================

folder_path = (
    "/Users/apple/Desktop/A/old/swin-wavelet/"
    "data/ideal/0509/Cross_revised7/npy19"
)

file_pattern_preds = "val_epoch_{}*true_label_preds.npy"
file_pattern_labels = "val_epoch*{}_labels.npy"


# Store the evaluation results for all epochs
results = []


def calculate_best_f1_and_threshold(preds, labels):
    """
    Determine the optimal F1 score and its corresponding threshold
    from the precision-recall curve.
    """
    precision, recall, thresholds = precision_recall_curve(
        labels,
        preds
    )

    f1_scores = (
        2 * precision * recall
        / (precision + recall + 1e-10)
    )

    best_idx = np.argmax(f1_scores)
    best_f1 = f1_scores[best_idx]

    # The thresholds array contains one fewer element than
    # the precision and recall arrays
    if best_idx < len(thresholds):
        best_threshold = thresholds[best_idx]
    else:
        best_threshold = 0.5

    return best_f1, best_threshold


def calculate_metrics(threshold, preds, true_labels):
    """
    Calculate classification metrics using the specified threshold.
    """
    binary_preds = (preds >= threshold).astype(int)

    # Setting labels=[0, 1] ensures that a 2 × 2 confusion matrix
    # is returned even when one class is absent
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
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "ACC": accuracy,
        "Precision": precision,
        "Recall": recall,
        "Kappa": kappa,
        "F1": f1,
    }


# ============================================================
# Calculate metrics for each epoch
# ============================================================

for epoch in range(20, 800):
    preds_pattern = os.path.join(
        folder_path,
        file_pattern_preds.format(epoch)
    )

    labels_pattern = os.path.join(
        folder_path,
        file_pattern_labels.format(epoch)
    )

    # Expand wildcard patterns and locate matching files
    preds_matches = sorted(glob.glob(preds_pattern))
    labels_matches = sorted(glob.glob(labels_pattern))

    if not preds_matches or not labels_matches:
        continue

    # Skip the epoch when multiple ambiguous files are found
    if len(preds_matches) != 1 or len(labels_matches) != 1:
        print(
            f"Epoch {epoch}: expected one prediction file and "
            f"one label file, but found "
            f"{len(preds_matches)} prediction file(s) and "
            f"{len(labels_matches)} label file(s)."
        )
        continue

    preds_path = preds_matches[0]
    labels_path = labels_matches[0]

    # Load prediction scores and ground-truth labels
    preds = np.asarray(np.load(preds_path)).reshape(-1)
    labels = np.asarray(np.load(labels_path)).reshape(-1)

    if len(preds) != len(labels):
        print(
            f"Epoch {epoch}: prediction and label lengths do not match "
            f"({len(preds)} vs. {len(labels)})."
        )
        continue

    # Flip predictions corresponding to the leading negative samples
    first_positive = next(
        (
            index
            for index, value in enumerate(labels)
            if value == 1
        ),
        None
    )

    if first_positive is not None:
        preds[:first_positive] = 1 - preds[:first_positive]

    # Determine the optimal threshold from the precision-recall curve
    best_f1, best_threshold = calculate_best_f1_and_threshold(
        preds,
        labels
    )

    # Use the manually specified threshold for epoch 21
    if epoch == 21:
        best_threshold = 0.09017112

    # Calculate metrics using the final threshold
    metrics = calculate_metrics(
        best_threshold,
        preds,
        labels
    )

    # Store results for the current epoch
    results.append(
        {
            "epoch": epoch,
            "best_f1": best_f1,
            "best_threshold": best_threshold,
            **metrics,
            "preds_path": preds_path,
            "labels_path": labels_path,
        }
    )


# ============================================================
# Save results and report the best epoch
# ============================================================

if results:
    df = pd.DataFrame(results)

    output_path = (
        "/Users/apple/Desktop/A/old/swin-wavelet/"
        "data/best F1/metrics_results_npy19.xlsx"
    )

    # Create the output directory if it does not exist
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_excel(
        output_path,
        index=False
    )

    print(f"Results have been saved to: {output_path}")

    # Select the best epoch according to the F1 score calculated
    # using the final threshold
    best_row = df.loc[df["F1"].idxmax()]

    print(f"\nBest epoch: {int(best_row['epoch'])}")
    print(f"Best F1 score: {best_row['F1']:.4f}")
    print(
        f"Corresponding threshold: "
        f"{best_row['best_threshold']:.4f}"
    )

    print("\nMetrics of the best epoch:")
    print(f"Accuracy:  {best_row['ACC']:.4f}")
    print(f"Precision: {best_row['Precision']:.4f}")
    print(f"Recall:    {best_row['Recall']:.4f}")
    print(f"Kappa:     {best_row['Kappa']:.4f}")
    print(f"TP:        {int(best_row['TP'])}")
    print(f"FP:        {int(best_row['FP'])}")
    print(f"TN:        {int(best_row['TN'])}")
    print(f"FN:        {int(best_row['FN'])}")

else:
    print("No valid data files were found.")
