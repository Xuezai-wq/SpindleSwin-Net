% This script processes EEG data stored in EDF files using the FieldTrip toolbox.
% It extracts specific channel data, resamples the data to a target sampling rate (256 Hz),
% and saves the resampled data along with metadata in a MATLAB .mat file for further analysis.
% The script also verifies the saved data by loading it back and checking its structure and sampling rate.

addpath('D:\Program Files\MATLAB\R2018a\toolbox\fieldtrip-20200605');
ft_defaults;

i = 1;
str1 = 'E:\MASS\matlab\DREAMS(ORI)\excerpt';
str2 = '.edf';
data1 = [str1, num2str(i), str2];

cfg = [];
cfg.dataset = data1;

hdr = ft_read_header(cfg.dataset);

disp(hdr.label);
disp(hdr.Fs);

channelName = 'CZ-A1';

channelIndex = find(strcmp(hdr.label, channelName));

if isempty(channelIndex)
    fprintf('Channel "%s" does not exist.\n', channelName);
else
    fprintf('Index of channel "%s" is %d.\n', channelName, channelIndex);
    
    data = ft_read_data(cfg.dataset);
    originalFs = hdr.Fs;
    fprintf('Original sampling rate: %.2f Hz.\n', originalFs);

    targetFs = 256;
    fprintf('Target sampling rate: %.2f Hz.\n', targetFs);

    if originalFs ~= targetFs
        [P, Q] = rat(targetFs / originalFs);
        dataResampled = resample(data', P, Q)';
    else
        dataResampled = data;
    end
    
    saveFileName = ['E:\MASS\matlab\DREAMS(MAT256)\', num2str(i), '.mat'];
    save(saveFileName, 'dataResampled', 'channelName', 'targetFs');
    fprintf('Channel "%s" data saved as "%s".\n', channelName, saveFileName);

    loadedData = load(saveFileName);
    fprintf('Verified target sampling rate in file: %.2f Hz.\n', loadedData.targetFs);
    if isfield(loadedData, 'dataResampled')
        fprintf('Resampled data dimensions: [%d channels ¡Á %d samples].\n', ...
                size(loadedData.dataResampled, 1), size(loadedData.dataResampled, 2));
    else
        error('Data field "dataResampled" not found in saved file.');
    end
end
