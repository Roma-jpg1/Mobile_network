filename = 'my_voice.wav'
[y,Fs] = audioread(filename)


function X = mDFT(x)
    N = length(x);
    X = zeros(1, N);
    for k = 0:N-1
        sum_val = 0;
        for n = 0:N-1
            sum_val = sum_val + x(n+1) * exp(-1i * 2 * pi * k * n / N);
        end
        X(k+1) = sum_val;
    end
end




   


M=3
y1=downsample(y,M)
Fs1=Fs/M


N=length(y)
Y = abs(fft(y)) / N
Y = Y(1:floor(N/2)+1);

f = (0:floor(N/2)) * Fs / N;




N1=length(y1)
Y1=abs(fft(y1))/N
Y1 = Y1(1:floor(N1/2)+1);

f1 = (0:floor(N1/2)) * Fs1 / N1;


figure;

subplot(2,1,1);
plot(f, Y);
grid on;
xlabel('Частота, Гц');
ylabel('Амплитуда');
title('Исходный сигнал');

subplot(2,1,2);
plot(f1, Y1);
grid on;
xlabel('Частота, Гц');
ylabel('Амплитуда');
title('Прореженный сигнал');
