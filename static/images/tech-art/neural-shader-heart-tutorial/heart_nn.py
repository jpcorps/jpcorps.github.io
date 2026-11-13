# heart_nn.py : 하트를 그리는 아주 작은 신경망 (numpy 만 씁니다)
import numpy as np

# 1) 정답 그림 만들기: 64x64 칸마다 "하트 안이면 1, 밖이면 0"
N = 64
g = (np.arange(N) + 0.5) / N                 # 0~1 사이 좌표
U, V = np.meshgrid(g, g)
x, y = (U - 0.5) * 3.0, (V - 0.45) * 3.0     # 하트 공식에 맞게 좌표를 옮기고 키움
answer = (((x*x + y*y - 1)**3 - x*x * y**3) <= 0).astype(float).reshape(-1, 1)
inputs = np.stack([U.ravel(), V.ravel()], 1) * 2 - 1   # (u, v)를 -1~1 로

# 2) 신경망 준비: 입력 2개 → 뉴런 16개 → 뉴런 16개 → 출력 1개
rng = np.random.default_rng(11)
W1 = rng.normal(0, 3.0, (2, 16));  b1 = rng.uniform(-2, 2, 16)
W2 = rng.normal(0, 0.35, (16, 16)); b2 = np.zeros(16)
W3 = rng.normal(0, 0.35, (16, 1));  b3 = np.zeros(1)
params = [W1, b1, W2, b2, W3, b3]

def relu(z):                     # 0보다 작으면 0으로 자르기
    return np.maximum(z, 0)

def forward(p):                  # 곱하고, 더하고, 자르기를 층마다 반복
    z1 = p @ W1 + b1; h1 = relu(z1)
    z2 = h1 @ W2 + b2; h2 = relu(z2)
    out = h2 @ W3 + b3
    return z1, h1, z2, h2, out

def picture():                   # 지금 신경망이 그리는 그림 (0~1로 자름)
    return np.clip(forward(inputs)[-1], 0, 1).reshape(N, N)

# 3) 학습: 틀린 만큼 가중치를 조금씩 고치기를 수천 번
m = [np.zeros_like(q) for q in params]; s = [np.zeros_like(q) for q in params]
for step in range(1, 8001):
    z1, h1, z2, h2, out = forward(inputs)
    err = out - answer                       # 얼마나 틀렸나
    d3 = 2 * err / len(inputs)               # 여기서부터는 "어느 가중치를 얼마나
    d2 = (d3 @ W3.T) * (z2 > 0)              #  고치면 틀림이 줄어드나"를 거꾸로
    d1 = (d2 @ W2.T) * (z1 > 0)              #  거슬러 올라가며 계산 (역전파)
    grads = [inputs.T @ d1, d1.sum(0), h1.T @ d2, d2.sum(0), h2.T @ d3, d3.sum(0)]
    lr = 0.01 * (1 - step / 8001) + 0.0005   # 고치는 폭: 처음엔 크게, 갈수록 작게
    for i, (q, gq) in enumerate(zip(params, grads)):   # Adam 이라는 고치는 요령
        m[i] = 0.9 * m[i] + 0.1 * gq
        s[i] = 0.999 * s[i] + 0.001 * gq * gq
        q -= lr * (m[i] / (1 - 0.9**step)) / (np.sqrt(s[i] / (1 - 0.999**step)) + 1e-8)
    if step % 1000 == 0:
        print(f"step {step:5d}  틀린 정도 {np.mean(err**2):.4f}")

# 다 배운 그림을 글자로 찍어 보기 (두 칸에 한 번씩)
for row in picture()[::-2, ::2]:
    print("".join("#" if v > 0.5 else "." for v in row))

# 4) 셰이더에 붙여 넣을 숫자 출력
def arr(a):
    return ", ".join(f"{v:.4f}" for v in np.ravel(a))
with open("weights.hlsl", "w") as f:
    f.write(f"static const float2 W1[16] = {{ {', '.join(f'float2({a:.4f}, {b:.4f})' for a, b in W1.T)} }};\n")
    f.write(f"static const float  B1[16] = {{ {arr(b1)} }};\n")
    f.write("static const float  W2[16][16] = {\n" + ",\n".join("    { " + arr(W2[:, j]) + " }" for j in range(16)) + "\n};\n")
    f.write(f"static const float  B2[16] = {{ {arr(b2)} }};\n")
    f.write(f"static const float  W3[16] = {{ {arr(W3)} }};\n")
    f.write(f"static const float  B3 = {b3[0]:.4f};\n")
print("weights.hlsl 저장 완료")
