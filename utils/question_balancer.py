import random
import math
from typing import List, Dict, Any, Union

def balance_and_shuffle_quiz(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    퀴즈 데이터의 정답 분포를 균등하게 섞어 반환합니다.
    
    Args:
        questions: 질문 리스트 (각 질문은 'options'와 'correct'(정답인덱스)를 포함해야 함)
        
    Returns:
        Dict: {
            "questions": 섞인 질문 리스트,
            "stats": 정답 분포 통계,
            "is_balanced": True
        }
    """
    if not questions:
        return {"questions": [], "stats": {}, "is_balanced": False}

    total_q = len(questions)
    
    # 문항 당 선택지 개수 파악 (첫 번째 문항 기준)
    # 선택지가 없는 경우 등을 대비해 안전하게 처리
    first_valid_q = next((q for q in questions if 'options' in q and q['options']), None)
    if not first_valid_q:
        return {"questions": questions, "stats": {}, "is_balanced": False}
        
    num_options = len(first_valid_q['options'])
    
    # [STEP 1] 전체 문항에 대해 균등한 정답 위치(인덱스) 리스트 생성
    target_indices = []
    repeat_count = math.ceil(total_q / num_options)
    for _ in range(repeat_count):
        target_indices.extend(list(range(num_options)))
    
    # 필요한 만큼 자르고 랜덤 셔플
    target_indices = target_indices[:total_q]
    random.shuffle(target_indices)

    shuffled_questions = []

    # [STEP 2] 각 문항별로 재조립
    for idx, q in enumerate(questions):
        # 필수 필드 확인
        if 'options' not in q or 'correct' not in q:
            shuffled_questions.append(q)
            continue
            
        original_options = q['options']
        # 기존 정답 인덱스
        correct_idx_original = q['correct']
        
        # 인덱스 유효성 검사
        if not (0 <= correct_idx_original < len(original_options)):
            shuffled_questions.append(q)
            continue
            
        # 정답 내용과 오답 내용 분리
        correct_content = original_options[correct_idx_original]
        distractors = [opt for i, opt in enumerate(original_options) if i != correct_idx_original]
        
        # 오답들도 순서를 섞어줌
        random.shuffle(distractors)
        
        # 이번 문항이 가질 새로운 정답 위치
        new_answer_idx = target_indices[idx]
        
        # 선택지 수가 다를 경우 (예: 어떤 문제는 4지, 어떤건 5지)
        # 현재 로직은 첫 번째 문제 기준으로 num_options를 잡았으므로, 
        # 만약 현재 문제의 옵션 수가 다르면 target_indices의 값이 범위를 벗어날 수 있음.
        # 안전하게 현재 문제의 옵션 수로 모듈러 연산
        current_num_options = len(original_options)
        if new_answer_idx >= current_num_options:
            new_answer_idx = new_answer_idx % current_num_options
            
        # 새로운 선택지 배열 생성
        new_options = [None] * current_num_options
        
        # 1. 정답 배치
        new_options[new_answer_idx] = correct_content
        
        # 2. 나머지 자리에 오답 채우기
        distractor_ptr = 0
        for i in range(current_num_options):
            if i != new_answer_idx:
                if distractor_ptr < len(distractors):
                    new_options[i] = distractors[distractor_ptr]
                    distractor_ptr += 1
                else:
                    new_options[i] = "Error: Missing Option"

        # 문항 정보 업데이트
        q_copy = q.copy()
        q_copy['options'] = new_options
        q_copy['correct'] = new_answer_idx # 0-based index
        
        # 디버그용 정보 추가 (선택사항)
        q_copy['_original_correct'] = correct_idx_original
        q_copy['_shuffled_index'] = new_answer_idx
        
        shuffled_questions.append(q_copy)

    # [STEP 3] 검증용 통계 생성
    stats = {i+1: 0 for i in range(num_options)}
    for q in shuffled_questions:
        if 'correct' in q:
            # 1-based index for label
            label = q['correct'] + 1
            if label not in stats:
                stats[label] = 0
            stats[label] += 1
            
    return {
        "questions": shuffled_questions,
        "stats": stats,
        "is_balanced": True
    }
