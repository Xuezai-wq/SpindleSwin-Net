[output1.tif](https://github.com/user-attachments/files/31891477/output1.tif)
# SpindleSwin-Net

## Description

SpindleSwin-Net: End-to-end and flexible sleep spindle detection for EEG signals based on wavelet and advanced vision transformer

Sleep spindle is an important physiological event which can be monitored by EEG that typically occurs in non-REM sleep. The detected spindle can be taken as a significant reference, which contributes to the neural mechanisms of cognition associated with sleep and pathophysiological underpinnings of sleep disorders. In this study, we proposed first transformer-based spindle detection approach on EEG signals combining wavelet transform and Swin-Transformer.

## Implementation

We extract data from raw EEG signals, focusing on regions of interest. The extracted signals are then subjected to a wavelet transform, which converts them into the frequency domain, enabling the generation of detailed time-frequency spectrograms. These spectrograms provide a visual representation of the signal's frequency dynamics over time, capturing key patterns and features. Here, we used two datasets, MASS and DREAMS, to train the model in order to achieve optimal performance. 



<img width="4665" height="2625" alt="figure1a_1b_1c_1d" src="https://github.com/user-attachments/assets/631429fb-a119-442d-95a7-b45eda901803" />


These spectrograms are input into a deep learning model, which leverages its advanced feature extraction and learning capabilities to perform classification and prediction tasks with high precision. This process facilitates further analysis such as specific sleep events or brain activity patterns.

<img width="4665" height="2625" alt="figure5" src="https://github.com/user-attachments/assets/d6705d70-b4ef-4691-afd2-184a35bdc46e" />

<img width="3300" height="2197" alt="figure2a_2b_2c" src="https://github.com/user-attachments/assets/c61c6cb9-3de3-448f-b614-1b7b10b89c13" />







## Architecture

The model is based on the Swin Transformer architecture, designed to process time-frequency graph data for classification and prediction tasks. The diagrams below illustrate our model's overall architecture and substructure. Ultimately, the model determines whether the graph contains a spindle and recognizes its relative starting and ending coordinates.

<img width="5072" height="2205" alt="figure4" src="https://github.com/user-attachments/assets/3975fa47-ec60-402e-aa78-7aa02b9c0106" />



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


