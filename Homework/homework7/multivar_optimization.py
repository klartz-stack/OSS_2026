import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

if __name__ == '__main__':
    # 비용 함수와 그 기울기 정의
    f   = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    fd  = lambda x: np.array([
        2 * (x[0] - 1) - 400 * x[0] * (x[1] - x[0]**2),
        200 * (x[1] - x[0]**2),
    ])

    # 최적화 설정
    x_init = [-1, 1]   # Please try other initial points
    learn_rate = 0.001 # Please try 0.01, 0.005, and 0.0001
    max_iter = 10000   # Please try 100, 1000, and 100000
    min_tol = 1e-6

    # 직접 구현한 경사하강법으로 비용 함수 최적화
    x = np.array(x_init)
    gd_xs = [x]
    for i in range(max_iter):
        # 경사하강법 한 단계 수행
        xp = x
        x = x - learn_rate * fd(x)
        gd_xs.append(x)

        # 종료 조건 확인
        if np.linalg.norm(x - xp) < min_tol:
            break
    gd_xs = np.array(gd_xs)

    # SciPy를 사용해 비용 함수 최적화
    result = minimize(f, x_init, tol=min_tol, options={'maxiter': max_iter, 'return_all': True})
    sp_xs = np.array(result.allvecs)

    # 최적화 결과 시각화
    x_range = np.linspace(-2, 2, 100)
    y_range = np.linspace(-1, 3, 100)
    xx, yy = np.meshgrid(x_range, y_range)
    zz = f((xx, yy))
    plt.contourf(xx, yy, zz)
    plt.plot(gd_xs[:,0], gd_xs[:,1], 'r.', label=f'GD (iter={len(gd_xs)})')
    plt.plot(sp_xs[:,0], sp_xs[:,1], 'b.', label=f'SciPy (iter={result.nit})')
    plt.xlabel('$x_0$')
    plt.ylabel('$x_1$')
    plt.legend()
    plt.savefig('multivar_optimization.png', bbox_inches='tight')
    plt.show()
