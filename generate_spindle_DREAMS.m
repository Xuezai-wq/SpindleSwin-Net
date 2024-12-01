% This script is designed for the DREAMS dataset to generate spindle wave segments.
% It identifies spindle-related events from annotation files, filters valid events based on duration,
% generates random sampling points for spindle wave segments, and computes their Continuous Wavelet Transform (CWT).
% The results are saved as scalogram images for further analysis.

addpath('C:\Program Files\MATLAB\R2023b\toolbox\fieldtrip-20200605');

for i = [1, 2, 3, 4, 5, 6]
    write_txt = ['D:\DREAMS\coordinate3\coordinate', num2str(i), '.txt'];
    fileID = fopen(write_txt, 'w');
    if fileID == -1
        error('%s', write_txt);
    end
    
    folder = ['D:DREAMS\spindle3\', num2str(i)];
    mkdir(folder);
    
    str1 = 'E:\MASS\matlab\DREAMS(MAT256)\';
    str2 = '.mat';
    data1 = [str1, num2str(i), str2];
    a = load(data1);
    b = a.dataResampled;
    if (i == 1 || i == 3)
        C3 = b(7, :);
    else
        C3 = b(3, :);
    end
    C3 = double(C3);
    
    str3 = 'E:\MASS\Dream\Visual_scoring1_excerpt';
    str4 = '.txt';
    data2 = [str3, num2str(i), str4];
    datatxt = importdata(data2);
    datatxt = datatxt.data;
    record_start = datatxt(:, 1);
    record_Duration = datatxt(:, 2);
    record_onset = record_start;
    record_offset = record_start + record_Duration;
    
    z = length(record_onset);
    onset_coordinate = [];
    re_onset_list = [];
    Duration = [];
    offset_coordinate = [];
    re_offset_list = [];
    record_onset2 = [];
    record_offset2 = [];
    namecount = 1;
    
    for l = 1:z
        if record_Duration(l) > 1.5
            continue;
        end
        record_onset2(end + 1) = record_onset(l);
        record_offset2(end + 1) = record_offset(l);
        random = (1.5 - record_Duration(l)) * rand();
        re_onset = record_onset(l) - random;
        re_offset = re_onset + 1.5;
        re_onset_list(end + 1) = re_onset;
        Duration(end + 1) = record_Duration(l);
        re_offset_list(end + 1) = re_offset;
        onset_coordinate(end + 1) = random;
        offset_coordinate(end + 1) = random + record_Duration(l);
    end
    
    for j = 1:length(re_onset_list)
        head = round(re_onset_list(j) * 256);
        tail = head + 1.5 * 256;
        A1 = C3(head:tail);
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
        local = ['D:DREAMS\spindle3\', num2str(i), '\', num2str(i), '-', num2str(namecount), '.png'];
        print(gcf, '-dpng', local);
        namecount = namecount + 1;
    end
    
    for k = 1:length(re_onset_list)
        fprintf(fileID, '%d %d %d %d %d %d %d\n', record_onset2(k), record_offset2(k), re_onset_list(k), re_offset_list(k), offset_coordinate(k), onset_coordinate(k), Duration(k));
    end
end
