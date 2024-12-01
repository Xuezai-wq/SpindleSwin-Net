% This script is designed for the MASS dataset to generate non-spindle segments.
% It identifies spindle-related events from annotation files, filters valid events based on duration,
% generates random sampling points for non-spindle segments, and computes their Continuous Wavelet Transform (CWT).
% The results are saved as scalogram images for further analysis.

addpath('C:\Program Files\MATLAB\R2023b\toolbox\fieldtrip-20200605');

for i = [1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 17, 18, 19]
    folderName = ['E:\EEGMASS\', num2str(i)];
    mkdir(folderName);
    
    if (i <= 9)
        edf_prefix = 'E:\EEGMASS\01-02-000';
        annotation_prefix = 'E:\EEGMASS\txt\01-02-000';
    else
        edf_prefix = 'E:\EEGMASS\01-02-00';
        annotation_prefix = 'E:\EEGMASS\txt\01-02-00';
    end
    
    edf_suffix = ' PSG.edf';
    annotation_suffix = ' Spindles_E2.txt';
    
    filename = [edf_prefix, num2str(i), edf_suffix];
    txtname = [annotation_prefix, num2str(i), annotation_suffix];
    datatxt = importdata(txtname);
    z = length(datatxt);
    
    cfg = [];
    cfg.dataset = filename;
    data = ft_preprocessing(cfg);
    
    channel_label = 'EEG C3-CLE';
    channel_index = find(strcmp(data.label, channel_label));
    if isempty(channel_index)
        error('C3 channel not found in the EDF file.');
    end
    c3_signal = data.trial{1}(channel_index, :);
    
    onset_coordinate = [];
    onset = [];
    re_onset_list = [];
    Duration = [];
    offset_coordinate = [];
    offset = [];
    re_offset_list = [];
    namecount = 1;
    
    for l = 2:z
        m = datatxt(l);
        m1 = cell2mat(m);
        k = find(m1 == ',');
        onset1 = m1(k(2) + 1:k(3) - 1);
        Duration1 = m1(k(3) + 1:k(4) - 1);
        if str2num(Duration1) > 1.5
            continue;
        end
        
        onset(end + 1) = str2num(onset1);
        offset(end + 1) = str2num(onset1) + str2num(Duration1);
        random = (1.5 - str2num(Duration1)) * rand();
        re_onset = str2num(onset1) - random;
        re_offset = re_onset + 1.5;
        re_onset_list(end + 1) = re_onset;
        Duration(end + 1) = str2num(Duration1);
        re_offset_list(end + 1) = re_offset;
        onset_coordinate(end + 1) = random;
        offset_coordinate(end + 1) = random + str2num(Duration1);
    end
    
    L = length(c3_signal);
    sampoint = randperm(L);
    sampoint_list = [];
    sample_number = length(onset) * 10;
    onset_point = onset * 256;
    offset_point = offset * 256;
    y = 1;
    f = 1;
    
    for flag = 1:L
        for flag2 = 1:length(onset)
            if ((sampoint(flag) >= onset_point(flag2)) && (sampoint(flag) <= offset_point(flag2))) || ...
               ((sampoint(flag) + 256 * 1.5 >= onset_point(flag2)) && (sampoint(flag) + 256 * 1.5 <= offset_point(flag2))) || ...
               (sampoint(flag) + 256 * 1.5 > L)
                f = 0;
                break;
            end
        end
        if f == 1
            sampoint_list(end + 1) = sampoint(flag);
            y = y + 1;
        else
            f = 1;
        end
        if y > sample_number
            break;
        end
    end
    
    for j = 1:length(sampoint_list)
        head = round(sampoint_list(j));
        tail = head + 1.5 * 256;
        A1 = c3_signal(head:tail);
        c = round(tail - head + 1);
        Fs = 256;
        fb = cwtfilterbank('SignalLength', c, 'SamplingFrequency', Fs, 'VoicesPerOctave', 10);
        sig = A1;
        [cfs, frq] = wt(fb, sig);
        t = (0:tail - head) / Fs;
        pcolor(t, frq, abs(cfs));
        set(gca, 'yscale', 'log');
        shading interp;
        axis tight;
        set(gca, 'XColor', 'none', 'YColor', 'none');
        local = ['E:\EEGMASS\', num2str(i), '\', 'non_', num2str(i), '-', num2str(namecount), '.png'];
        print(gcf, '-dpng', local);
        namecount = namecount + 1;
    end
end
