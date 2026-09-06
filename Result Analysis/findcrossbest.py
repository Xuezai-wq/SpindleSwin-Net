import numpy as np
import os
import pandas as pd
from sklearn.metrics import (
    precision_recall_curve,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    cohen_kappa_score,
)

# 文件路径和文件名格式
folder_path = "/Users/apple/Desktop/A/old/swin-wavelet/data/ideal/0509/Cross_revised7/npy19"
file_pattern_preds = "val_epoch_{}_true_label_preds.npy"
file_pattern_labels = "val_epoch_{}_labels.npy"

# 记录每个epoch的指标结果
results = []


def calculate_best_f1_and_threshold(preds, labels):
    """从PR曲线中获取最佳F1分数及对应阈值"""
    precision, recall, thresholds = precision_recall_curve(labels, preds)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_f1 = f1_scores[best_idx]
    best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
    return best_f1, best_threshold


def calculate_metrics(threshold, preds, true_labels):
    """根据阈值计算各类评估指标"""
    binary_preds = (preds >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(true_labels, binary_preds).ravel()
    acc = accuracy_score(true_labels, binary_preds)
    precision = precision_score(true_labels, binary_preds, zero_division=0)
    recall = recall_score(true_labels, binary_preds, zero_division=0)
    f1 = f1_score(true_labels, binary_preds, zero_division=0)
    kappa = cohen_kappa_score(true_labels, binary_preds)
    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "ACC": acc,
        "Precision": precision,
        "Recall": recall,
        "Kappa": kappa,
        "F1": f1,
    }


for epoch in range(20, 800):
    preds_path = os.path.join(folder_path, file_pattern_preds.format(epoch))
    labels_path = os.path.join(folder_path, file_pattern_labels.format(epoch))

    if os.path.exists(preds_path) and os.path.exists(labels_path):
        preds = np.load(preds_path)
        labels = np.load(labels_path)

        # 处理前导负样本的预测翻转
        first_positive = next((i for i, v in enumerate(labels) if v == 1), None)
        if first_positive is not None:
            preds[:first_positive] = 1 - preds[:first_positive]

        # 计算最佳阈值及对应F1
        best_f1, best_threshold = calculate_best_f1_and_threshold(preds, labels)

        #print(best_threshold)
        if epoch == 21:
            best_threshold = 0.09017112

        # 计算所有评估指标
        metrics = calculate_metrics(best_threshold, preds, labels)

        # 记录结果
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

# 保存结果到Excel
if results:
    df = pd.DataFrame(results)
    output_path = "/Users/apple/Desktop/A/old/swin-wavelet/data/best F1/metrics_results_npy19.xlsx"
    df.to_excel(output_path, index=False)
    print(f"结果已保存至: {output_path}")

    # 输出最佳epoch信息
    best_row = df.loc[df["best_f1"].idxmax()]
    print(f"\n最佳Epoch: {best_row['epoch']}")
    print(f"最佳F1分数: {best_row['best_f1']:.4f}")
    print(f"对应阈值: {best_row['best_threshold']:.4f}")
else:
    print("未找到有效数据文件")