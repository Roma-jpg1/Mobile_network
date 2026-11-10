from math import ceil

import matplotlib.pyplot as plt
import numpy as np


f = 1800              # частота, МГц
p_bs = 46             # мощность передатчика БС, дБм
p_ue = 24             # мощность передатчика телефона, дБм
g_bs = 21             # усиление антенны БС, дБи
g_ue = 0              # усиление антенны телефона, дБи
g_mimo = 3            # выигрыш MIMO 2x2, дБ
l_feeder = 2          # потери в фидере, дБ
l_lna = 0.4           # потери в МШУ, дБ
l_jumper = 0.5        # потери в джампере, дБ
m_wall = 15           # запас на прохождение стен, дБ
m_interference = 1    # запас на интерференцию, дБ
b_ul = 10e6           # полоса UL, Гц
b_dl = 20e6           # полоса DL, Гц
nf_bs = 2.4           # коэффициент шума БС, дБ
nf_ue = 6             # коэффициент шума телефона, дБ
sinr_ul = 4           # требуемый SINR в UL, дБ
sinr_dl = 2           # требуемый SINR в DL, дБ
h_bs = 30             # высота антенны БС, м
h_ue = 1.5            # высота антенны телефона, м
l_clutter = 0         # поправка COST 231 для города, дБ
s_city = 100          # площадь территории, км²
s_indoor = 4          # площадь торговых и бизнес-центров, км²
n_sectors = 3         # число секторов одной БС
k_area = 1.95         # коэффициент площади для трёх секторов

# Бюджеты каналов: в UL принимает БС, в DL принимает телефон
loss = l_feeder + l_lna + l_jumper
gain = g_bs + g_ue + g_mimo
margin = m_wall + m_interference

noise_ul = -174 + 10 * np.log10(b_ul)
noise_dl = -174 + 10 * np.log10(b_dl)
rx_bs = noise_ul + nf_bs + sinr_ul
rx_ue = noise_dl + nf_ue + sinr_dl

mapl_ul = p_ue - loss + gain - margin - rx_bs
mapl_dl = p_bs - loss + gain - margin - rx_ue


# Расстояния для общего графика заданы в километрах
d = np.linspace(0.03, 6, 700)

# COST 231 Hata: частота в МГц, расстояние в км
a = 3.2 * np.log10(11.75 * h_ue) ** 2 - 4.97
cost_base = 46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(h_bs) - a + l_clutter
s_near = (47.88 + 13.9 * np.log10(f / h_bs)) / np.log10(50)
s_far = 44.9 - 6.55 * np.log10(h_bs)

pl_cost = []
for distance in d:
    if distance < 1:
        s = s_near
    else:
        s = s_far
    pl_cost.append(cost_base + s * np.log10(distance))

# При d = 1 км потери равны cost_base, по нему выбираем ветвь для радиуса
if mapl_ul < cost_base:
    r_cost_ul = 10 ** ((mapl_ul - cost_base) / s_near)
else:
    r_cost_ul = 10 ** ((mapl_ul - cost_base) / s_far)

if mapl_dl < cost_base:
    r_cost_dl = 10 ** ((mapl_dl - cost_base) / s_near)
else:
    r_cost_dl = 10 ** ((mapl_dl - cost_base) / s_far)

# UMi NLOS: частота в ГГц, расстояние в метрах
umi_base = 26 * np.log10(f / 1000) + 22.7
pl_umi = umi_base + 36.7 * np.log10(d * 1000)
r_umi_ul = 10 ** ((mapl_ul - umi_base) / 36.7) / 1000
r_umi_dl = 10 ** ((mapl_dl - umi_base) / 36.7) / 1000

# Walfisch-Ikegami для прямой видимости (LOS), расстояние в км
wi_base = 42.6 + 20 * np.log10(f)
pl_wi = wi_base + 26 * np.log10(d)
r_wi_ul = 10 ** ((mapl_ul - wi_base) / 26)
r_wi_dl = 10 ** ((mapl_dl - wi_base) / 26)

# Потери в свободном пространстве для сравнения
pl_fspl = 32.44 + 20 * np.log10(f) + 20 * np.log10(d)

# Берём меньший радиус, чтобы связь работала в обе стороны
models = [
    ("COST 231", r_cost_ul, r_cost_dl, s_city),
    ("UMi NLOS", r_umi_ul, r_umi_dl, s_indoor),
    ("WI LOS", r_wi_ul, r_wi_dl, s_city),
]

for name, r_ul, r_dl, area in models:
    radius = min(r_ul, r_dl)
    s_bs = k_area * radius ** 2
    n_bs = ceil(area / s_bs)

    print(f"\n{name}")
    print(f"Радиус UL = {r_ul} км, DL = {r_dl} км")
    print(f"Радиус соты = {radius} км")
    print(f"Площадь одной БС = {s_bs} км²")
    print(f"Количество БС = {n_bs}, секторов = {n_bs * n_sectors}")

# Общий график потерь и уровни MAPL
plt.figure()
plt.plot(d, pl_cost, label="COST 231")
plt.plot(d, pl_umi, label="UMi NLOS")
plt.plot(d, pl_wi, label="WI LOS")
plt.plot(d, pl_fspl, label="FSPL")
plt.axhline(mapl_ul, linestyle="--", color="black", label="MAPL UL")
plt.axhline(mapl_dl, linestyle=":", color="black", label="MAPL DL")
plt.xlim(0, 6)
plt.xlabel("Расстояние, км")
plt.ylabel("Потери, дБ")
plt.title("Потери сигнала по разным моделям")
plt.legend()
plt.grid()
plt.tight_layout()

freq = np.linspace(0.7, 3.5, 40)
bw = np.linspace(5, 100, 40)
freq, bw = np.meshgrid(freq, bw)

noise = -174 + 10 * np.log10(bw * 1e6)
rx = noise + nf_bs + sinr_ul
mapl = p_ue - loss + gain - margin - rx
r = 10 ** ((mapl - 26 * np.log10(freq) - 22.7) / 36.7) / 1000

ax = plt.figure().add_subplot(projection="3d")
ax.plot_surface(freq, bw, r)
ax.set_xlabel("Несущая частота, ГГц")
ax.set_ylabel("Ширина полосы UL, МГц")
ax.set_zlabel("Радиус соты, км")

plt.show()
