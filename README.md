[figure2a_2b_2c.tif](https://github.com/user-attachments/files/23353202/figure2a_2b_2c.tif)# SpindleSwin-Net

## Description

SpindleSwin-Net: End-to-end and flexible sleep spindles detection for EEG signals based on wavelet transform and Swin-Transformer.

Sleep spindle is an important physiological event which can be monitored by EEG that typically occurs in non-REM sleep. The detected spindle can be taken as a significant reference, which contributes to the neural mechanisms of cognition associated with sleep and pathophysiological underpinnings of sleep disorders. In this study, we proposed first transformer-based spindle detection approach on EEG signals combining wavelet transform and Swin-Transformer.

## Implementation

We extract data from raw EEG signals, focusing on regions of interest. The extracted signals are then subjected to a wavelet transform, which converts them into the frequency domain, enabling the generation of detailed time-frequency spectrograms. These spectrograms provide a visual representation of the signal's frequency dynamics over time, capturing key patterns and features. Here, we used two datasets, MASS and DREAMS, to train the model in order to achieve optimal performance. 
<img width="1400" height="1938" alt="图片 2" src="https://github.com/user-attachments/assets/f94037eb-e0e1-44d5-bd76-5123b586918d" width="70%"/>



These spectrograms are input into a deep learning model, which leverages its advanced feature extraction and learning capabilities to perform classification and prediction tasks with high precision. This process facilitates further analysis such as specific sleep events or brain activity patterns.

<img width="1050" height="2039" alt="图片 3" src="https://github.com/user-attachments/assets/e218b348-67f5-4632-ab03-25b1cf622a50" width="70%"/>

<img width="3006" height="2145" alt="图片 1" src="https://github.com/user-attachments/assets/e757060c-5d71-4448-8264-beec20d846d3" />

## Architecture

The model is based on the Swin Transformer architecture, designed to process time-frequency graph data for classification and prediction tasks. The diagrams below illustrate our model's overall architecture and substructure. Ultimately, the model determines whether the graph contains a spindle and recognizes its relative starting and ending coordinates.

<img width="1050" height="1695" alt="模型图" src="https://github.com/user-attachments/assets/cf729d45-108a-4303-9e00-55b6b0a2d7e2" width="70%"/>


## Citations

```tex
@article{oreilly2014mass,
  title={Montreal Archive of Sleep Studies: an open-access resource for instrument benchmarking and exploratory research},
  author={O'Reilly, Christian and Gosselin, Nadia and Carrier, Julie and Nielsen, Tore},
  journal={Journal of Sleep Research},
  volume={23},
  number={6},
  pages={628--635},
  year={2014},
  doi={10.1111/jsr.12169}
}
@article{wong2025dreams,
  title={A dream EEG and mentation database},
  author={Wong, William and Valli, Katja and Tsuchiya, Naotsugu and others},
  journal={Nature Communications},
  volume={16},
  number={1},
  pages={7495},
  year={2025},
  doi={10.1038/s41467-025-61945-1}
}
@inproceedings{liu2021swin,
  title={Swin Transformer: Hierarchical Vision Transformer using Shifted Windows},
  author={Liu, Ze and Lin, Yutong and Cao, Yue and Hu, Han and Wei, Yixuan and Zhang, Zheng and Lin, Stephen and Guo, Baining},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  pages={10012--10022},
  year={2021}
}
``` 


