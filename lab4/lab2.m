
clc
clear
close all

N = 31

x1 = [1 0 0 0 1]
y1 = [1 1 0 0 0]

x2 = [1 0 0 1 0]
y2 = [1 0 0 1 1]

gold1 = zeros(1, N)
gold2 = zeros(1, N)



for i = 1:N

    gold1(i) = xor(x1(5), y1(5))
    gold2(i) = xor(x2(5), y2(5))

    nx1 = xor(x1(4), x1(5))
    ny1 = xor(y1(2), y1(5))

    nx2 = xor(x2(4), x2(5))
    ny2 = xor(y2(2), y2(5))

    x1 = [nx1 x1(1:4)]
    y1 = [ny1 y1(1:4)]

    x2 = [nx2 x2(1:4)]
    y2 = [ny2 y2(1:4)]
end

disp('Первая последовательность')
disp(gold1)

disp('Вторая последовательность')
disp(gold2)
lag = 0:N-1

prav = [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
prav = 2*prav -1

a = 2 * gold1 -1
b = 2 * gold2 -1




noise  = prav + 0.3 * randn(size(prav))
noise2 = prav + 0.9 * randn(size(prav))
noise3 = a + 0.3 * randn(size(a))
noise4 = a + 0.9 * randn(size(a))

[cor21, lag21] = xcorr(prav,noise, 'normalized')
[cor22, lag22] = xcorr(prav,noise2, 'normalized')
[cor23, lag23] = xcorr(a,noise3, 'normalized')
[cor24, lag24] = xcorr(a,noise4, 'normalized')



fprintf('prav, шум 0.2: %.4f\n', cor21(lag21 == 0));
fprintf('prav, шум 0.9: %.4f\n', cor22(lag22 == 0));
fprintf('gold1, шум 0.2: %.4f\n', cor23(lag23 == 0));
fprintf('gold1, шум 0.9: %.4f\n', cor24(lag24 == 0));

figure;

plot(lag21, cor21)
hold on
plot(lag22, cor22)
plot(lag23, cor23)
plot(lag24, cor24)
hold off

xlabel('Лаг')
xlim([0,32])
ylabel('Автокорреляция')
title('Автокорреляция последовательностей с шумом')
legend('prav, шум 0.2', 'prav, шум 0.9','gold1, шум 0.2', 'gold1, шум 0.9')
grid on



figure
stem(lag, noise)
hold on
stem(lag, noise2)
stem(lag, prav)
hold off
xlim([0,32])
legend('prav, шум 0.2', 'prav, шум 0.9', 'изначальная')
grid on


figure
stem(lag, noise3)
hold on
stem(lag, noise4)
stem(lag, a)
hold off
xlim([0,32])
legend('gold1, шум 0.2', 'gold1, шум 0.9', 'изначальная')
grid on









% Автокорреляция через autocorr

[R1, lag3]=autocorr(a, 'NumLags', 30)

figure
stem(lag3, R1)
title('Автокорреляция autocorr')

% График автокорреляции
[cor, lag1] = xcorr(a)
R = cor(lag1 >= 0 & lag1 < N) / N

figure
stem(lag, R)
title('Автокорреляция последовательности Голда')
xlabel('Сдвиг')
ylabel('Корреляция')
grid on

% График взаимной корреляции
[vz_cor, lag2] = xcorr(a,b)
C = vz_cor(lag2 >= 0 & lag2 < N) / N


figure
stem(lag, C)
title('Взаимная корреляция')
xlabel('Сдвиг')
ylabel('Корреляция')
grid on


T = table(lag', R', C')
disp(T)

% Автокорреляция второй последовательности
[cor2, lag4] = xcorr(b)
R2 = cor2(lag4 >= 0 & lag4 < N) / N

figure
stem(lag, R2)
title('Автокорреляция второй последовательности Голда')
xlabel('Сдвиг')
ylabel('Корреляция')
grid on


