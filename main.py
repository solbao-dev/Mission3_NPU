import json
import time

# [1] 키보드 입력받는 함수
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

# [2] MAC 연산 함수
def calculate_mac(filter_matrix, pattern_matrix):
    score = 0
    size = len(filter_matrix) 
    for i in range(size):
        for j in range(size):
            score += filter_matrix[i][j] * pattern_matrix[i][j]
    return score

# (누락되었던 보조 함수들 추가)
def normalize_label(label):
    return label.strip().lower()

def get_decision(sc_cross, sc_x):
    if sc_cross > sc_x:
        return "cross"
    elif sc_x > sc_cross:
        return "x"
    else:
        return "unknown"

# ========= 프로그램 메인 함수 =========
# 모든 코드를 감싸는 main() 함수를 만들었어!
def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    choice = input("선택: ")
    
    # 💡 첫 번째 조건: choice가 1일 때
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
        
        print("\n#----------------------------------------")
        print("# [3] MAC 결과")
        print("#----------------------------------------")
        
        score_a = calculate_mac(filter_a, pattern)
        score_b = calculate_mac(filter_b, pattern)
        
        print(f"A 점수: {float(score_a)}") 
        print(f"B 점수: {float(score_b)}")
        
        if score_a > score_b:
            print("판정: A")
        elif score_b > score_a:
            print("판정: B")
        else:
            print("판정: 판정 불가 (동점)")
            
    # 💡 두 번째 조건: choice가 2일 때 (위의 if choice == '1': 과 완벽히 세로줄이 맞아야 해!)
    elif choice == '2':
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
            
            filters = data['filters']
            patterns = data['patterns'] 
            
            performance_stats = []
            fail_cases = []
            pass_count, total_count = 0, 0

            print("\n# [2] 패턴 분석 시작")
            
            for p_id, p_info in patterns.items():
                total_count += 1
                p_input = p_info['input']
                p_expected = normalize_label(p_info['expected'])
                
                try:
                    parts = p_id.split("_") 
                    n_val = int(parts[1])   
                    size_key = f"size_{n_val}"
                    
                    if size_key not in filters or len(p_input) != n_val:
                        raise ValueError(f"크기 불일치 또는 필터 없음 (N={n_val})")
                except Exception as e:
                    print(f"- [{p_id}] FAIL: {e}")
                    fail_cases.append(f"{p_id}: {e}")
                    continue

                f_set = filters[size_key]
                
                start = time.time()
                for _ in range(10):
                    sc_cross = calculate_mac(f_set['cross'], p_input)
                    sc_x = calculate_mac(f_set['x'], p_input)
                elapsed = (time.time() - start) / 10 * 1000 
                
                performance_stats.append((n_val, elapsed))
                
                decision = get_decision(sc_cross, sc_x)
                status = "PASS" if decision == p_expected else "FAIL"
                
                if status == "PASS": 
                    pass_count += 1
                else: 
                    fail_cases.append(f"{p_id}: 판정 불일치 (기대:{p_expected}, 실제:{decision})")
                
                print(f"- {p_id} | 판정: {decision} | 정답: {p_expected} | {status}")

            print("\n# [3] 성능 분석 (평균/10회)")
            print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
            unique_sizes = sorted(list(set([s[0] for s in performance_stats])))
            for sz in unique_sizes:
                times_for_size = [s[1] for s in performance_stats if s[0] == sz]
                avg = sum(times_for_size) / len(times_for_size)
                print(f"{sz}x{sz:<8} {avg:<15.4f} {sz*sz}")

            print(f"\n# [4] 결과 요약\n총 테스트: {total_count}개 | 통과: {pass_count}개 | 실패: {len(fail_cases)}개")
            if fail_cases:
                print("실패 케이스 목록:")
                for fc in fail_cases: 
                    print(f"  - {fc}")

        except FileNotFoundError:
            print("❌ data.json 파일이 없습니다.")

if __name__ == "__main__":
    main()