% This script is designed for the DREAMS dataset to generate non-spindle segments.
% It identifies spindle-related events from annotation files, filters valid events based on duration,
% generates random sampling points for non-spindle segments, and computes their Continuous Wavelet Transform (CWT).
% The results are saved as scalogram images for further analysis.

addpath('C:\Program Files\MATLAB\R2023b\toolbox\fieldtrip-20200605');

for i = [1, 2, 3, 4, 5, 6]
    folder = ['D:DREAMS\non-spindle2\', num2str(i)];  
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
    str5 = 'E:\MASS\Dream\Visual_scoring2_excerpt';
    str6 = '.txt';
    
    data3 = [str5, num2str(i), str6];
    datatxt = importdata(data3);
    datatxt = datatxt.data;
    start = datatxt(:, 1);
    Duration = datatxt(:, 2);
    validIdx = Duration <= 1.5;
    start = start(validIdx);
    Duration = Duration(validIdx);
    
    onset = start;
    offset = start + Duration;
    namecount = 1;

    L = length(C3);
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
        local = ['D:DREAMS\non-spindle2\', num2str(i), '\', 'non_', num2str(i), '-', num2str(namecount), '.png'];
        print(gcf, '-dpng', local);  
        namecount = namecount + 1;
    end
end
