# [1] 키보드 입력받는 함수 (아까와 동일해요!)
def get_3x3_input(name):
    while True:
        print(f"\n{name} (3줄 입력, 공백 구분)")
        matrix = []
        is_valid = True
        
        for i in range(3):
            try:
                row = list(map(int, input().split()))
                if len(row) != 3:
                    is_valid = False
            except ValueError:
                is_valid = False
            
            matrix.append(row)
            
        if is_valid:
            return matrix 
        else:
            print("❌ 입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요. 다시 입력해주세요.")

# [2] MAC 연산을 수행하는 새로운 함수 추가! ⭐
def calculate_mac(filter_matrix, pattern_matrix):
    score = 0
    size = len(filter_matrix) # 3x3이면 3, 5x5면 5가 됩니다.
    
    # 가로(i) 세로(j)를 돌면서 같은 위치의 숫자끼리 곱하고 더합니다.
    for i in range(size):
        for j in range(size):
            score += filter_matrix[i][j] * pattern_matrix[i][j]
            
    return score

# ========= 여기서부터 프로그램 시작 =========
if __name__ == "__main__":
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    choice = input("선택: ")
    
    if choice == '1':
        print("\n#----------------------------------------")
        print("# [1] 필터 입력")
        print("#----------------------------------------")
        filter_a = get_3x3_input("필터 A")
        filter_b = get_3x3_input("필터 B")
        
        print("\n#----------------------------------------")
        print("# [2] 패턴 입력")
        print("#----------------------------------------")
        pattern = get_3x3_input("패턴")
        
        # [3] 추가된 부분: 저장된 데이터를 계산 함수에 넣고 결과를 출력합니다! ⭐
        print("\n#----------------------------------------")
        print("# [3] MAC 결과")
        print("#----------------------------------------")
        
        score_a = calculate_mac(filter_a, pattern)
        score_b = calculate_mac(filter_b, pattern)
        
        print(f"A 점수: {float(score_a)}") # 미션 예시처럼 소수점 형태로 출력
        print(f"B 점수: {float(score_b)}")
        
        # 누가 점수가 더 높은지 판정하기
        if score_a > score_b:
            print("판정: A")
        elif score_b > score_a:
            print("판정: B")
        else:
            print("판정: 판정 불가 (동점)")
            
    elif choice == '2':
        print("\n[안내] 2번 모드는 3단계에서 만들 예정입니다!")
    else:
        print("\n[오류] 1 또는 2를 입력해주세요.")