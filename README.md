# SpindleSwin-Net

## Abstract

SpindleSwin-Net: End-to-end and flexible sleep spindles detection for EEG signals based on wavelet transform and Swin-Transformer.

Sleep spindle is an important physiological event which can be monitored by EEG that typically occurs in non-REM sleep. The detected spindle can be taken as a significant reference, which contributes to the neural mechanisms of cognition associated with sleep and pathophysiological underpinnings of sleep disorders. In this study, we proposed first transformer-based spindle detection approach on EEG signals combining wavelet transform and Swin-Transformer.

## Implementation

First, we extract data from raw EEG signals, focusing on regions of interest. The extracted signals are then subjected to a wavelet transform, which converts them into the frequency domain, enabling the generation of detailed time-frequency spectrograms. These spectrograms provide a visual representation of the signal's frequency dynamics over time, capturing key patterns and features. Here, we used two datasets, MASS and DREAMS, to train the model in order to achieve optimal performance. 

<img width="1050" height="2039" alt="图片 3" src="https://github.com/user-attachments/assets/e218b348-67f5-4632-ab03-25b1cf622a50" width="70%"/>

Finally, these spectrograms are input into a deep learning model, which leverages its advanced feature extraction and learning capabilities to perform classification and prediction tasks with high precision. This process facilitates further analysis such as specific sleep events or brain activity patterns.

<img width="1400" height="1938" alt="图片 2" src="https://github.com/user-attachments/assets/f94037eb-e0e1-44d5-bd76-5123b586918d" width="70%"/>


## Architecture

The model is based on the Swin Transformer architecture, designed to process time-frequency graph data for classification and prediction tasks. The diagrams below illustrate our model's overall architecture and substructure. Ultimately, the model determines whether the graph contains a spindle and recognizes its relative starting and ending coordinates.

<img width="1050" height="1695" alt="模型图" src="https://github.com/user-attachments/assets/cf729d45-108a-4303-9e00-55b6b0a2d7e2" width="70%"/>

