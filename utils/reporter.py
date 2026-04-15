# utils/reporter.py
def print_performance(stats):
    print("\n# [3] 성능 분석 (평균/10회)")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    unique_sizes = sorted(list(set([s[0] for s in stats])))
    for sz in unique_sizes:
        times_for_size = [s[1] for s in stats if s[0] == sz]
        avg = sum(times_for_size) / len(times_for_size)
        print(f"{sz}x{sz:<8} {avg:<15.4f} {sz*sz}")

def print_summary(total, pass_cnt, fails):
    print(f"\n# [4] 결과 요약")
    print(f"총 테스트: {total}개 | 통과: {pass_cnt}개 | 실패: {len(fails)}개")
    if fails:
        print("실패 케이스 목록:")
        for fc in fails: print(f"  - {fc}")
        