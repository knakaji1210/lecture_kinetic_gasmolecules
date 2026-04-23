import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 設定 ---
N = 50          # 分子の数（衝突計算のため少し減らしています）
L = 10.0        # 容器のサイズ
R = 0.2         # 分子の半径
sigma = 1.5     # 温度
dt = 0.03       # タイムステップ

# --- 初期状態 ---
pos = np.random.uniform(R, L-R, (N, 2))
vel = np.random.normal(0, sigma, (N, 2))

# --- 描画準備 ---
fig, (ax_sim, ax_hist) = plt.subplots(1, 2, figsize=(12, 5))
ax_sim.set_xlim(0, L)
ax_sim.set_ylim(0, L)
ax_sim.set_aspect('equal')
scat = ax_sim.scatter(pos[:, 0], pos[:, 1], s=150, edgecolors='black') # 大きめの粒子

n_bins = 15
max_v = sigma * 5
_, _, bar_container = ax_hist.hist(np.linalg.norm(vel, axis=1), bins=n_bins, range=(0, max_v), density=True, color='gray', alpha=0.7)
ax_hist.set_xlim(0, max_v)
ax_hist.set_ylim(0, 0.6)

def update(frame):
    global pos, vel
    
    # 1. 位置の更新
    pos += vel * dt
    
    # 2. 壁との衝突
    for i in range(N):
        for d in range(2):
            if pos[i, d] < R or pos[i, d] > L - R:
                vel[i, d] *= -1
                pos[i, d] = np.clip(pos[i, d], R, L - R)

    # 3. 分子同士の衝突判定と計算
    for i in range(N):
        for j in range(i + 1, N):
            diff = pos[i] - pos[j]
            dist = np.linalg.norm(diff)
            
            if dist < 2 * R:
                # 速度ベクトルを更新 (弾性衝突の公式)
                v_diff = vel[i] - vel[j]
                # 衝突軸方向の速度成分を計算して入れ替え
                collision_vec = diff / dist
                v_rel_dot = np.dot(v_diff, collision_vec)
                
                if v_rel_dot < 0: # 互いに近づいている場合のみ計算
                    impulse = v_rel_dot * collision_vec
                    vel[i] -= impulse
                    vel[j] += impulse
                    
                    # めり込み防止の補正
                    overlap = 2 * R - dist
                    pos[i] += (overlap / 2) * collision_vec
                    pos[j] -= (overlap / 2) * collision_vec

    # 4. 表示の更新
    speeds = np.linalg.norm(vel, axis=1)
    colors = plt.cm.jet(np.clip(speeds / (sigma * 2.5), 0, 1))
    scat.set_offsets(pos)
    scat.set_edgecolors(colors) # 縁の色を変える
    scat.set_facecolors(colors)

    n, _ = np.histogram(speeds, bins=n_bins, range=(0, max_v), density=True)
    for count, rect in zip(n, bar_container):
        rect.set_height(count)

    return scat, *bar_container

ani = FuncAnimation(fig, update, frames=200, interval=20, blit=True)
plt.tight_layout()

ani.save('./gif/gas_molecules_collision.gif', fps=30)

plt.show()

