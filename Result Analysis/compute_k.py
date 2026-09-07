import os
import re
import warnings

import mne
import numpy as np
from sklearn.metrics import cohen_kappa_score

warnings.filterwarnings("ignore")


# ============================================================
# 1. Parse spindle annotation TXT files
# ============================================================

def parse_spindle_file(path):
    intervals = []

    # Try several possible text encodings
    for enc in ["utf-8", "gbk", "latin1"]:
        try:
            with open(path, "r", encoding=enc) as f:
                lines = f.readlines()
            break
        except Exception:
            continue
    else:
        raise RuntimeError(f"Unable to read annotation file: {path}")

    for line in lines:
        # Extract numerical values from each line
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)

        if len(numbers) < 2:
            continue

        try:
            start = float(numbers[0])
            duration = float(numbers[1])
            end = start + duration
            intervals.append([start, end])
        except Exception:
            continue

    return intervals


# ============================================================
# 2. Read EDF recording information
# ============================================================

def get_edf_info(edf_path):
    raw = mne.io.read_raw_edf(
        edf_path,
        preload=False,
        verbose=False
    )

    fs = int(raw.info["sfreq"])
    n_samples = raw.n_times
    duration = n_samples / fs

    return fs, n_samples, duration


# ============================================================
# 3. Build sample-level binary labels
# ============================================================

def build_time_labels(intervals, fs, length):
    label = np.zeros(length, dtype=np.uint8)

    for start_time, end_time in intervals:
        start = int(start_time * fs)
        end = int(end_time * fs)

        if start >= length:
            continue

        start = max(0, start)
        end = min(length, end)

        label[start:end] = 1

    return label


# ============================================================
# 4. Build epoch-level binary labels
# ============================================================

def build_epoch_labels(intervals, epoch_len, total_duration):
    n_epochs = int(total_duration // epoch_len)
    labels = np.zeros(n_epochs, dtype=np.uint8)

    for start_time, end_time in intervals:
        start_ep = int(start_time // epoch_len)
        end_ep = int(end_time // epoch_len)

        for ep in range(start_ep, end_ep + 1):
            if 0 <= ep < n_epochs:
                labels[ep] = 1

    return labels


# ============================================================
# 5. Compute Cohen's kappa
# ============================================================

def compute_sample_kappa(intervals1, intervals2, fs, length):
    label1 = build_time_labels(intervals1, fs, length)
    label2 = build_time_labels(intervals2, fs, length)

    # Cohen's kappa is not meaningful when both label arrays
    # contain only one class
    if len(np.unique(label1)) < 2 and len(np.unique(label2)) < 2:
        return None

    return cohen_kappa_score(label1, label2)


def compute_epoch_kappa(
    intervals1,
    intervals2,
    duration,
    epoch_len=25
):
    label1 = build_epoch_labels(
        intervals1,
        epoch_len,
        duration
    )
    label2 = build_epoch_labels(
        intervals2,
        epoch_len,
        duration
    )

    # Cohen's kappa is not meaningful when both label arrays
    # contain only one class
    if len(np.unique(label1)) < 2 and len(np.unique(label2)) < 2:
        return None

    return cohen_kappa_score(label1, label2)


# ============================================================
# 6. Main program
# ============================================================

def main():
    # Patient IDs used in the DREAMS dataset
    patient_id_list = [1, 2, 3, 4, 5, 6]

    # Example patient IDs used in the MASS dataset
    # patient_id_list = [
    #     1, 2, 3, 5, 6, 7, 9, 10,
    #     11, 12, 13, 14, 17, 18, 19
    # ]

    txt_dir = "/Users/apple/Desktop/A/spindle1/K/DatabaseSpindles"
    edf_dir = "/Users/apple/Desktop/A/new/spindle2/dataset/DREAMS"

    sample_kappa_list = []
    epoch_kappa_list = []

    print("===== Per Patient (Sample κ + Epoch κ) =====")

    for pid in patient_id_list:
        # File naming rules for the MASS dataset
        # pid_txt = f"{pid:04d}"
        # pid_edf = f"{pid:04d}"
        #
        # txt1 = os.path.join(
        #     txt_dir,
        #     f"01-02-{pid_txt} Spindles_E1.txt"
        # )
        # txt2 = os.path.join(
        #     txt_dir,
        #     f"01-02-{pid_txt} Spindles_E2.txt"
        # )
        # edf_path = os.path.join(
        #     edf_dir,
        #     f"01-02-{pid_edf} PSG.edf"
        # )

        # File naming rules for the DREAMS dataset
        txt1 = os.path.join(
            txt_dir,
            f"Visual_scoring1_excerpt{pid}.txt"
        )
        txt2 = os.path.join(
            txt_dir,
            f"Visual_scoring2_excerpt{pid}.txt"
        )
        edf_path = os.path.join(
            edf_dir,
            f"excerpt{pid}.edf"
        )

        # Skip the current subject if any required file is missing
        if not (
            os.path.exists(txt1)
            and os.path.exists(txt2)
            and os.path.exists(edf_path)
        ):
            print(f"❌ Missing patient {pid}")
            continue

        # Parse spindle intervals annotated by the two experts
        intervals1 = parse_spindle_file(txt1)
        intervals2 = parse_spindle_file(txt2)

        # Read sampling frequency, number of samples,
        # and total recording duration
        fs, length, duration = get_edf_info(edf_path)

        print(f"\nPatient {pid}")
        print(f"Duration: {duration:.1f}s")
        print(f"Sampling frequency: {fs} Hz")

        # Compute sample-level Cohen's kappa
        sample_kappa = compute_sample_kappa(
            intervals1,
            intervals2,
            fs,
            length
        )

        # Compute epoch-level Cohen's kappa using 25-second epochs
        epoch_kappa = compute_epoch_kappa(
            intervals1,
            intervals2,
            duration,
            epoch_len=25
        )

        print(f"Sample κ = {sample_kappa}")
        print(f"Epoch  κ = {epoch_kappa}")

        if sample_kappa is not None:
            sample_kappa_list.append(sample_kappa)

        if epoch_kappa is not None:
            epoch_kappa_list.append(epoch_kappa)

    # ========================================================
    # Report overall statistics
    # ========================================================

    print("\n===== Overall =====")

    if len(sample_kappa_list) > 0:
        arr = np.array(sample_kappa_list)

        print("\n--- Sample κ ---")
        print(f"Mean: {np.mean(arr):.4f}")
        print(f"Std:  {np.std(arr):.4f}")
        print(f"Min:  {np.min(arr):.4f}")
        print(f"Max:  {np.max(arr):.4f}")

    if len(epoch_kappa_list) > 0:
        arr = np.array(epoch_kappa_list)

        print("\n--- Epoch κ (25 s) ---")
        print(f"Mean: {np.mean(arr):.4f}")
        print(f"Std:  {np.std(arr):.4f}")
        print(f"Min:  {np.min(arr):.4f}")
        print(f"Max:  {np.max(arr):.4f}")


if __name__ == "__main__":
    main()

