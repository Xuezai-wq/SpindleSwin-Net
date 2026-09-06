import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score, cohen_kappa_score

# 文件夹对应的epoch
folders = {'npy1': 31, 'npy2': 93, 'npy3': 69, 'npy4': 97, 'npy5': 60}
#folders = {'npy1': 89, 'npy3': 50, 'npy4': 58, 'npy5': 77}

#folders = {'npy1': 84,'npy4': 94}
#folders = {'npy3': 42}
base_path = '/Users/apple/Desktop/swin-wavelet/data/ideal/MASS_March/'

# 阈值范围
thresholds = np.arange(0.01, 0.98, 0.01)
#thresholds = [0.092

# 计算指标函
# 定义计算指标的函数
def calculate_metrics(threshold, preds, true_labels):
    binary_preds = (preds >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(true_labels, binary_preds).ravel()
    acc = accuracy_score(true_labels, binary_preds)
    #iou = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
    precision = precision_score(true_labels, binary_preds, zero_division=0)
    recall = recall_score(true_labels, binary_preds, zero_division=0)
    f1 = f1_score(true_labels, binary_preds, zero_division=0)
    #specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    kappa = cohen_kappa_score(true_labels, binary_preds)
    return {
        "Threshold": threshold, "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "ACC": acc, "Recall": recall, "Precision": precision, "Kappa": kappa,
        "F1": f1
    }


# 遍历文件夹与epoch，计算所有阈值下的F1分数
f1_results = []
metrics_results = []

for folder, epoch in folders.items():
    preds_path = f"{base_path}{folder}/val_epoch_{epoch}_true_label_preds.npy"
    labels_path = f"{base_path}{folder}/val_epoch_{epoch}_labels.npy"

    preds = np.load(preds_path)
    labels = np.load(labels_path)

    first_index = next((i for i, value in enumerate(labels) if value == 1), -1)
    if first_index != -1:
        preds[:first_index] = 1 - preds[:first_index]

    folder_f1 = []
    for threshold in thresholds:
        metrics = calculate_metrics(threshold, preds, labels)
        folder_f1.append(metrics["F1"])

    f1_results.append(folder_f1)

# 平均F1分数计算
average_f1 = np.mean(f1_results, axis=0)
best_threshold = thresholds[np.argmax(average_f1)]
#best_threshold = 0.0848

# 计算所有epoch在最佳阈值下的指标#
for folder, epoch in folders.items():
    preds_path = f"{base_path}{folder}/val_epoch_{epoch}_true_label_preds.npy"
    labels_path = f"{base_path}{folder}/val_epoch_{epoch}_labels.npy"

    preds = np.load(preds_path)
    labels = np.load(labels_path)

    first_index = next((i for i, value in enumerate(labels) if value == 1), -1)
    if first_index != -1:
        preds[:first_index] = 1 - preds[:first_index]

    metrics = calculate_metrics(best_threshold, preds, labels)
    metrics["Folder"] = folder
    metrics["Epoch"] = epoch
    metrics_results.append(metrics)

# 保存结果到Excel
metrics_df = pd.DataFrame(metrics_results)
output_path = '//Users/apple/Desktop/A/old/swin-wavelet/data/best F1/average_metrics_results_march.xlsx'
metrics_df.to_excel(output_path, index=False)

print(f"最佳阈值: {best_threshold:.3f}")
print(f"所有指标已保存至: {output_path}")
