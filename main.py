import json
import time
from core.npu_core import normalize_label, calculate_mac, get_decision
from utils.reporter import print_performance, print_summary

# [1] 키보드 입력받는 함수 (UX 개선 버전)
def get_3x3_input(name):
    print(f"\n# {name} 입력을 시작합니다 (0 또는 1만 입력 가능, 공백 구분)")
    matrix = []
    i = 0
    
    while i < 3:  # 3행을 다 채울 때까지 반복
        try:
            user_input = input(f"  [{i+1}행 입력]: ").split()
            
            # [검증 1] 숫자 파싱 실패 확인 (정수가 아니면 ValueError 발생)
            row = [int(val) for val in user_input]
            
            # [검증 2] 열 개수 불일치 확인 (정확히 3개여야 함)
            if len(row) != 3:
                print(f"    ❌ [입력 오류] 정확히 3개의 숫자가 필요합니다. (현재 {len(row)}개 입력됨)")
                continue  # i를 증가시키지 않고 해당 행 다시 시작
            
            # [검증 3] 값 범위 확인 (0 또는 1만 허용)
            if any(val not in [0, 1] for val in row):
                print(f"    ❌ [값 범위 오류] 0 또는 1만 입력 가능합니다. (잘못된 숫자 포함)")
                continue
            
            # 모든 검증 통과! 행 추가 후 다음 단계로
            matrix.append(row)
            i += 1
            
        except ValueError:
            print(f"    ❌ [데이터 오류] 숫자가 아닌 값이 포함되어 있습니다. 다시 입력해주세요.")
            
    return matrix


# ========= 프로그램 메인 함수 =========
def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    choice = input("선택: ")
    
    if choice == '1':
        print("\n# [1] 필터 입력")
        filter_a = get_3x3_input("필터 A")
        filter_b = get_3x3_input("필터 B")
        
        print("\n# [2] 패턴 입력")
        pattern = get_3x3_input("패턴")
        
        score_a = calculate_mac(filter_a, pattern)
        score_b = calculate_mac(filter_b, pattern)
        
        print(f"\nA 점수: {float(score_a)}") 
        print(f"B 점수: {float(score_b)}")
        
        decision = get_decision(score_a, score_b)
        
        if decision == "Cross":
            print("판정: A")
        elif decision == "X":
            print("판정: B")
        else:
            print("판정: 판정 불가 (동점)")
            
    elif choice == '2':
        try:
            with open('data/data.json', 'r') as f:
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
                sc_cross = calculate_mac(f_set['cross'], p_input)
                sc_x = calculate_mac(f_set['x'], p_input)

                # 성능 측정을 위한 10회 반복
                start = time.time()
                for _ in range(10):
                    calculate_mac(f_set['cross'], p_input)
                    calculate_mac(f_set['x'], p_input)
                elapsed = (time.time() - start) / 10 * 1000 
                
                performance_stats.append((n_val, elapsed))
                
                decision = get_decision(sc_cross, sc_x)
                status = "PASS" if decision == p_expected else "FAIL"
                
                if status == "PASS": 
                    pass_count += 1
                else: 
                    fail_cases.append(f"{p_id}: 판정 불일치 (기대:{p_expected}, 실제:{decision})")
                
                print(f"- {p_id} | 판정: {decision} | 정답: {p_expected} | {status}")

            print_performance(performance_stats)
            print_summary(total_count, pass_count, fail_cases)

        except FileNotFoundError:
            print("❌ data.json 파일이 없습니다.")

if __name__ == "__main__":
    main()