def get_3x3_input(name):
    # 무한 반복! 사용자가 제대로 입력할 때까지 계속 물어볼 거예요.
    while True:
        print(f"\n{name} (3줄 입력, 공백 구분)")
        matrix = []       # 숫자들을 담을 큰 빈 상자
        is_valid = True   # 입력이 정상적인지 확인하는 깃발 (일단 정상이라고 가정!)
        
        for i in range(3):
            try:
                # 1. input()으로 키보드 입력을 받음
                # 2. split()으로 공백 기준 자름
                # 3. map(int, ...)로 각각을 숫자로 변환
                # 4. list()로 묶어서 한 줄(row)을 만듦
                row = list(map(int, input().split()))
                
                # 만약 한 줄에 숫자가 3개가 아니라면? 에러!
                if len(row) != 3:
                    is_valid = False
            except ValueError:
                # 숫자가 아닌 이상한 글자(a, b, ! 등)를 입력했다면? 에러!
                is_valid = False
            
            matrix.append(row) # 한 줄을 큰 상자에 넣기
            
        # 3줄을 다 받았는데 에러가 없었다면(is_valid가 여전히 True라면) 성공!
        if is_valid:
            return matrix 
        else:
            print("❌ 입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요. 다시 입력해주세요.")

# ========= 여기서부터 프로그램이 진짜 시작되는 부분 =========
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
        
        # 짠! 우리가 입력한 데이터가 어떻게 저장되었는지 확인해 볼까요?
        print("\n[확인용] 잘 저장되었나 볼까요?")
        print("필터 A:", filter_a)
        print("패턴:", pattern)
        
    elif choice == '2':
        print("\n[안내] 2번 모드는 3단계에서 만들 예정입니다! 조금만 기다려주세요.")
    else:
        print("\n[오류] 1 또는 2를 입력해주세요.")