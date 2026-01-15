import json

def fix_question_sections():
    """
    extracted_questions.json의 잘못된 섹션 분류를 수정합니다.
    문제 내용을 분석하여 적절한 섹션으로 재분류합니다.
    """
    
    # JSON 파일 로드
    with open('extracted_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 섹션 분류 키워드
    vocabulary_keywords = ['color', 'opposite', 'number', 'word', 'meaning']
    grammar_keywords = ['_______', 'verb', 'tense', ' is ', ' am ', ' are ', ' have ', ' has ']
    conversation_keywords = ['say when', 'best response', 'A:', 'B:', 'Choose the best']
    reading_indicators = ['Read', 'passage', 'according to', 'author', 'main idea']
    
    stats = {'changed': 0, 'total': 0}
    
    for level, questions in data.items():
        print(f"\n처리 중: {level}")
        for q in questions:
            stats['total'] += 1
            original_section = q.get('section', 'General')
            question_text = q.get('question', '').lower()
            
            # 섹션 판단 로직
            new_section = original_section
            
            # Reading: 지문이 필요한 질문 (현재는 하드코딩된 ID 기반)
            # PRE-A1과 A1: 1-2번, 3-4번, 5-8번이 각각 지문 공유
            # 다른 레벨은 별도 분석 필요
            
            # Conversation: 대화 관련
            if any(keyword in question_text for keyword in conversation_keywords):
                new_section = 'Conversation'
            
            # Grammar: 빈칸 채우기 (특히 동사 관련)
            elif '_______' in question_text:
                # 추가 분석: 색깔, 반대말 등은 Vocabulary
                if any(keyword in question_text for keyword in vocabulary_keywords):
                    new_section = 'Vocabulary'
                else:
                    new_section = 'Grammar'
            
            # Vocabulary: 색깔, 반대말, 단어 의미
            elif any(keyword in question_text for keyword in vocabulary_keywords):
                new_section = 'Vocabulary'
            
            # Reading: 나머지는 General로
            elif not any(keyword in question_text for keyword in reading_indicators):
                # Reading이었던 것 중 위 카테고리에 해당 안 되면 General로
                if original_section == 'Reading':
                    # PRE-A1, A1의 특정 ID만 Reading 유지 (지문 연결용)
                    if level in ['PRE-A1', 'A1']:
                        # ID 기반 Reading 문제 판단 (실제 지문이 있는 문제들)
                        # 이것은 추후 실제 HTML 파일에서 추출된 데이터로 교체되어야 함
                        q_id = q.get('id', 0)
                        if q_id in [1, 2, 3, 4, 5, 6, 7, 8]:
                            # 이 중에서도 실제로 지문 기반 질문인지 확인
                            if any(indicator in question_text for indicator in ['where', 'what', 'who', 'when', 'how']):
                                new_section = 'Reading'
                            else:
                                new_section = 'General'
                        else:
                            new_section = 'General'
                    else:
                        new_section = 'General'
            
            if new_section != original_section:
                q['section'] = new_section
                stats['changed'] += 1
                print(f"  Q{q['id']}: {original_section} → {new_section}")
                print(f"    질문: {question_text[:60]}...")
    
    # 수정된 데이터 저장
    with open('extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n완료! 총 {stats['total']}개 문제 중 {stats['changed']}개 수정됨")
    
    # 레벨별 섹션 분포 출력
    print("\n=== 레벨별 섹션 분포 ===")
    for level, questions in data.items():
        section_counts = {}
        for q in questions:
            section = q.get('section', 'General')
            section_counts[section] = section_counts.get(section, 0) + 1
        
        print(f"\n{level}: 총 {len(questions)}문제")
        for section, count in sorted(section_counts.items()):
            print(f"  {section}: {count}문제")

if __name__ == "__main__":
    fix_question_sections()
