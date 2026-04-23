import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 設定 ---
N = 100         # 分子の数（分布を見やすくするため少し多めに）
L = 10.0        # 容器のサイズ
sigma = 1.5     # 温度（速度の標準偏差）
dt = 0.05       # タイムステップ

# --- 初期状態 ---
pos = np.random.uniform(0, L, (N, 2))
vel = np.random.normal(0, sigma, (N, 2))

# --- 描画準備 (2つのグラフを並べる) ---
fig, (ax_sim, ax_hist) = plt.subplots(1, 2, figsize=(12, 5))

# 左：シミュレーション画面
ax_sim.set_xlim(0, L)
ax_sim.set_ylim(0, L)
ax_sim.set_aspect('equal')
scat = ax_sim.scatter(pos[:, 0], pos[:, 1], c='blue', s=30, edgecolors='black')

# 右：ヒストグラム画面
speeds = np.linalg.norm(vel, axis=1)
n_bins = 15
max_speed = sigma * 4
_, _, bar_container = ax_hist.hist(speeds, bins=n_bins, range=(0, max_speed), 
                                   density=True, color='gray', alpha=0.7)
ax_hist.set_xlim(0, max_speed)
ax_hist.set_ylim(0, 0.6)
ax_hist.set_title("Speed Distribution")

def update(frame):
    global pos, vel
    
    # 1. 位置の更新と壁との衝突
    pos += vel * dt
    out_of_bounds = (pos <= 0) | (pos >= L)
    vel[out_of_bounds] *= -1
    pos = np.clip(pos, 0, L)
    
    # 2. 速さと色の計算
    speeds = np.linalg.norm(vel, axis=1)
    # 速さに応じて 0(青)〜1(赤) に正規化
    colors = plt.cm.jet(np.clip(speeds / (sigma * 2.5), 0, 1))
    
    # 3. 散布図の更新
    scat.set_offsets(pos)
    scat.set_color(colors)
    
    # 4. ヒストグラムの更新
    n, _ = np.histogram(speeds, bins=n_bins, range=(0, max_speed), density=True)
    for count, rect in zip(n, bar_container):
        rect.set_height(count)
        
    return scat, *bar_container

ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.tight_layout()
plt.show()
