import json
from collections import Counter

def shuffle_options_to_balance():
    """
    옵션을 섞어서 정답 분포를 균형 있게 만듭니다.
    실제 정답의 내용도 함께 변경됩니다.
    """
    
    with open('extracted_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for level, questions in data.items():
        if level not in ['A2', 'B1']:
            continue  # 쏠림 현상이 있는 레벨만 처리
        
        print(f"\n{'='*60}")
        print(f"LEVEL: {level}")
        print(f"{'='*60}")
        
        # 현재 정답 분포
        correct_answers = [q.get('correct', -1) for q in questions]
        answer_dist = Counter(correct_answers)
        
        print("Before:")
        for pos in [0, 1, 2, 3]:
            count = answer_dist.get(pos, 0)
            percentage = (count / len(questions)) * 100 if questions else 0
            print(f"   Position {pos} ({['A', 'B', 'C', 'D'][pos]}): {count} ({percentage:.1f}%)")
        
        # 목표 분포: 각 위치에 거의 동일한 개수
        target_per_pos = len(questions) // 4
        remainder = len(questions) % 4
        
        # 각 위치별 목표 개수
        target_counts = {}
        for i, pos in enumerate([0, 1, 2, 3]):
            target_counts[pos] = target_per_pos + (1 if i < remainder else 0)
        
        # 각 위치별로 현재 개수와 목표 개수 비교
        surplus = {}
        deficit = {}
        
        for pos in [0, 1, 2, 3]:
            current = answer_dist.get(pos, 0)
            target = target_counts[pos]
            diff = target - current
            if diff > 0:
                deficit[pos] = diff
            elif diff < 0:
                surplus[pos] = -diff
        
        print(f"\nTarget counts: {target_counts}")
        print(f"Surplus: {surplus}")
        print(f"Deficit: {deficit}")
        
        # 초과분을 부족분으로 이동
        for surplus_pos in surplus.keys():
            if surplus[surplus_pos] <= 0:
                continue
            
            for deficit_pos in deficit.keys():
                if deficit[deficit_pos] <= 0:
                    continue
                if surplus[surplus_pos] <= 0:
                    break
                
                # 이동할 개수
                move_count = min(surplus[surplus_pos], deficit[deficit_pos])
                
                # 해당 위치의 문항들을 찾아서 옵션 섞기
                changed = 0
                for q in questions:
                    if changed >= move_count:
                        break
                    if q.get('correct') == surplus_pos:
                        # 옵션 내용을 저장
                        options = q.get('options', []).copy()
                        current_correct_idx = q.get('correct', 0)
                        
                        # 현재 정답 옵션
                        correct_option = options[current_correct_idx]
                        
                        # 새로운 정답 위치 선택
                        q['correct'] = deficit_pos
                        
                        # 옵션을 섞어서 새로운 정답이 원하는 위치에 오도록 함
                        # 간단한 방법: 정답을 원하는 위치에 놓고 나머지를 섞기
                        
                        # 정답 위치에 정답 옵션 배치
                        new_options = ['', '', '', '']
                        new_options[deficit_pos] = correct_option
                        
                        # 나머지 옵션 채우기
                        other_options = [opt for i, opt in enumerate(options) if i != current_correct_idx]
                        other_idx = 0
                        for i in range(4):
                            if i != deficit_pos:
                                new_options[i] = other_options[other_idx]
                                other_idx += 1
                        
                        # 섞기 (나머지 옵션들의 순서를 랜덤하게)
                        import random
                        random.seed(42)  # 재현 가능하도록 시드 고정
                        
                        # 나머지 옵션들의 위치
                        other_positions = [i for i in range(4) if i != deficit_pos]
                        other_options_shuffled = other_options.copy()
                        random.shuffle(other_options_shuffled)
                        
                        # 채우기
                        final_options = [''] * 4
                        final_options[deficit_pos] = correct_option
                        for pos_idx, opt in zip(other_positions, other_options_shuffled):
                            final_options[pos_idx] = opt
                        
                        q['options'] = final_options
                        changed += 1
                
                surplus[surplus_pos] -= move_count
                deficit[deficit_pos] -= move_count
                
                print(f"   Moved {changed} answers from {surplus_pos} to {deficit_pos}")
        
        # 최종 분포 확인
        final_correct_answers = [q.get('correct', -1) for q in questions]
        final_answer_dist = Counter(final_correct_answers)
        
        print("\nAfter:")
        for pos in [0, 1, 2, 3]:
            count = final_answer_dist.get(pos, 0)
            percentage = (count / len(questions)) * 100 if questions else 0
            print(f"   Position {pos} ({['A', 'B', 'C', 'D'][pos]}): {count} ({percentage:.1f}%)")
    
    # 수정된 데이터 저장
    with open('extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n\n✅ Balanced questions saved to extracted_questions.json")

if __name__ == "__main__":
    shuffle_options_to_balance()
