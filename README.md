# Swin-Wavelet

## Abstract

Swin-Wavelet: End-to-end and flexible sleep spindles detection for EEG signals based on wavelet transform and Swin-Transformer.

Sleep spindle is an important physiological event which can be monitored by EEG that typically occurs in non-REM sleep. The detected spindle can be taken as a significant reference, which contributes to the neural mechanisms of cognition associated with sleep and pathophysiological underpinnings of sleep disorders. In this study, we proposed first transformer-based spindle detection approach on EEG signals combining wavelet transform and Swin-Transformer.

## Implementation

First, we extract data from raw EEG signals, focusing on regions of interest. The extracted signals are then subjected to a wavelet transform, which converts them into the frequency domain, enabling the generation of detailed time-frequency spectrograms. These spectrograms provide a visual representation of the signal's frequency dynamics over time, capturing key patterns and features. Here, we used two datasets, MASS and DREAMS, to train the model in order to achieve optimal performance. 

![图片 3](https://github.com/user-attachments/assets/a6ff6975-2ceb-4582-be66-02dc11797b2a)


Finally, these spectrograms are input into a deep learning model, which leverages its advanced feature extraction and learning capabilities to perform classification and prediction tasks with high precision. This process facilitates further analysis such as specific sleep events or brain activity patterns.

![图片 4](https://github.com/user-attachments/assets/2febfaf1-a72b-4127-8230-36e698f7cde7)


## Architecture

The model is based on the Swin Transformer architecture, designed to process time-frequency graph data for classification and prediction tasks. The diagrams below illustrate our model's overall architecture and substructure. Ultimately, the model determines whether the graph contains a spindle and recognizes its relative starting and ending coordinates.

![图片 1](https://github.com/user-attachments/assets/5460a431-db5c-4f62-ad2a-04b3acddf212)



![图片 2](https://github.com/user-attachments/assets/c9f5c992-3cd1-4197-a20b-55d159fba9cf)

