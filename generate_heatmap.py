import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import subprocess
from datetime import datetime

# Git log에서 커밋 데이터를 직접 가져오기
def get_commit_data():
    result = subprocess.run(
        ["git", "log", "--date=short", "--pretty=format:%ad"],
        stdout=subprocess.PIPE,
        text=True
    )
    dates = result.stdout.splitlines()
    return pd.Series(dates).value_counts().sort_index()

# 데이터 준비
data = get_commit_data()
data.index = pd.to_datetime(data.index)
data = data.sort_index()

# 날짜 범위 설정
start_date = data.index.min()
end_date = data.index.max()
date_range = pd.date_range(start_date, end_date)

# 모든 날짜를 포함하는 DataFrame 생성 후 결합
heatmap_data = pd.DataFrame(0, index=date_range, columns=['Count'])
heatmap_data.update(data)
heatmap_data = heatmap_data['Count'].resample('D').sum()

# 데이터 배열로 변환하여 히트맵 준비
heatmap_matrix = np.zeros((7, len(heatmap_data) // 7 + 1))
for i, count in enumerate(heatmap_data):
    week = i // 7
    day = i % 7
    heatmap_matrix[day, week] = count

# 색상 설정 및 히트맵 출력
fig, ax = plt.subplots(figsize=(15, 5))
cmap = mcolors.ListedColormap(['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'])
bounds = [0, 1, 3, 6, 10, np.max(heatmap_matrix)]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

ax.imshow(heatmap_matrix, aspect='auto', cmap=cmap, norm=norm)
ax.set_yticks(range(7))
ax.set_yticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

# 월별 레이블 추가
months = pd.date_range(start_date, end_date, freq='MS').strftime('%b').tolist()
month_positions = [(i * 4.35) for i in range(len(months))]
ax.set_xticks(month_positions)
ax.set_xticklabels(months, ha='center')

# 이미지 파일로 저장
plt.savefig('commit_heatmap.png', dpi=300, bbox_inches='tight')
