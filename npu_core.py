def normalize_label(label):
    """라벨을 Cross 또는 X로 표준화합니다."""
    clean_label = str(label).strip().lower()
    if clean_label in ['+', 'cross']:
        return 'Cross'
    elif clean_label == 'x':
        return 'X'
    else:
        return 'Unknown'

def calculate_mac(filter_matrix, pattern_matrix):
    """필터와 패턴의 MAC 연산을 수행합니다."""
    score = 0
    size = len(filter_matrix) 
    for i in range(size):
        for j in range(size):
            score += filter_matrix[i][j] * pattern_matrix[i][j]
    return score

def get_decision(sc_cross, sc_x):
    """Epsilon을 적용하여 최종 판정을 내립니다."""
    epsilon = 1e-9
    if abs(sc_cross - sc_x) < epsilon:
        return "Unknown"
    
    return "Cross" if sc_cross > sc_x else "X"