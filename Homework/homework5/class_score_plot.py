import matplotlib.pyplot as plt

# CSV 데이터 읽기
def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):  # 주석 행 제외
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # 점수 데이터 불러오기
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # 점수 준비
    midterm_kr, final_kr = zip(*class_kr)
    # 가중치 설정
    total_kr = [40 / 125 * midterm + 60 / 100 * final
                for midterm, final in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40 / 125 * midterm + 60 / 100 * final
                for midterm, final in class_en]

    # 산점도
    plt.figure()
    plt.plot(midterm_kr, final_kr, 'ro', label='Korean')
    plt.plot(midterm_en, final_en, 'b+', label='English')
    # 축과 범례 설정
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.grid(True)
    plt.legend()
    # 산점도 png로 저장
    plt.savefig('class_score_scatter.png')

    # 히스토그램
    # 5점 단위 구간 설정
    bins = range(0, 105, 5)
    plt.figure()
    # 두 반 분포 비교
    plt.hist(total_kr, bins=bins, range=(0, 100), alpha=0.5, label='Korean')
    plt.hist(total_en, bins=bins, range=(0, 100), alpha=0.5, label='English')
    plt.xlim(0, 100)
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.legend()
    # 히스토그램 png로 저장
    plt.savefig('class_score_hist.png')

    # 그래프 표시
    plt.show()
