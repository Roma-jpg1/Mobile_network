filename = 'my_voice.wav';

[y, Fs] = audioread(filename);
info = audioinfo(filename);

y1=downsample(y, 3)
zv=audioplayer(y1, Fs/1)
play(zv)
plot(y1)

N = size(y, 1);       
T = info.Duration;    
Fsc = N / T; 

yfft = fft(y1)
disp(size(y))
fprintf('Отсч: %d\n', N);
fprintf('Длит: %.6f с\n', T);
fprintf('Рез Fs: %.2f Гц\n', Fsc);
fprintf('Fs в MATLAB: %.2f Гц\n', Fs);