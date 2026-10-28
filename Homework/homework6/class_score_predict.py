import numpy as np
import matplotlib.pyplot as plt

midterm_range = np.array([0, 125])
final_range = np.array([0, 100])

# 한국어반과 영어반 점수 데이터를 읽어 하나로 합침
class_kr = np.loadtxt('data/class_score_kr.csv', delimiter=',')
class_en = np.loadtxt('data/class_score_en.csv', delimiter=',')
data = np.vstack((class_kr, class_en))

# 중간고사 점수와 기말고사 점수 분리
xn = data[:, 0]  # 중간고사 점수
yn = data[:, 1]  # 기말고사 점수
A = np.vstack((xn, np.ones(xn.shape))).T  # 기울기와 절편을 구할 행렬
b = yn
line = np.linalg.pinv(A) @ b  # 최소제곱법으로 [기울기, 절편] 계산

# 입력한 중간고사 점수로 기말고사 점수 예측
final = lambda midterm: line[0] * midterm + line[1]
while True:
    try:
        given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
        # 입력하지 않거나 음수를 입력하면 종료
        if given == '' or float(given) < 0:
            break
        print(f'A) Your final score is expected to be {final(float(given)):.3f}.')
    except Exception as ex:
        print(f'Cannot answer the question. (message: {ex})')
        break

# 점수 데이터와 예측선을 그래프로 표시
plt.figure()
plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
plt.xlabel('Midterm scores')
plt.ylabel('Final scores')
plt.xlim(midterm_range)
plt.ylim(final_range)
plt.grid()
plt.legend()
# 그래프를 PNG 파일로 저장
plt.savefig('class_score_predict.png', dpi=300, bbox_inches='tight')
plt.show()
