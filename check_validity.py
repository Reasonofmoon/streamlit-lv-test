import json
from collections import Counter

def analyze_level_validity(data):
    """레벨별 타당도 분석"""
    report = []
    
    for level, questions in data.items():
        report.append(f"\n{'='*60}")
        report.append(f"LEVEL: {level}")
        report.append(f"{'='*60}")
        report.append(f"Total Questions: {len(questions)}")
        
        # 섹션별 분포
        sections = [q.get('section', 'Unknown') for q in questions]
        section_counts = Counter(sections)
        report.append(f"\n📊 Section Distribution:")
        for section, count in sorted(section_counts.items()):
            report.append(f"   - {section}: {count}")
        
        # 지문 유무 확인
        with_passage = sum(1 for q in questions if q.get('passage'))
        without_passage = len(questions) - with_passage
        report.append(f"\n📄 Passage Status:")
        report.append(f"   - With passage: {with_passage}")
        report.append(f"   - Without passage: {without_passage}")
        
        # 정답 위치 분포 (0, 1, 2, 3)
        correct_answers = [q.get('correct', -1) for q in questions]
        answer_dist = Counter(correct_answers)
        report.append(f"\n🎯 Answer Position Distribution (0=A, 1=B, 2=C, 3=D):")
        for pos in [0, 1, 2, 3]:
            count = answer_dist.get(pos, 0)
            percentage = (count / len(questions)) * 100 if questions else 0
            report.append(f"   - Position {pos} ({['A', 'B', 'C', 'D'][pos]}): {count} ({percentage:.1f}%)")
        
        # 쏠림 현상 확인
        max_count = max(answer_dist.values()) if answer_dist else 0
        min_count = min(answer_dist.values()) if answer_dist else 0
        if max_count - min_count > len(questions) * 0.2:  # 20% 이상 차이
            report.append(f"   ⚠️ WARNING: Answer distribution is uneven (max: {max_count}, min: {min_count})")
        else:
            report.append(f"   ✅ Answer distribution is balanced")
        
        # Reading 섹션의 지문 체크
        reading_questions = [q for q in questions if q.get('section') == 'Reading']
        if reading_questions:
            reading_with_passage = sum(1 for q in reading_questions if q.get('passage'))
            report.append(f"\n📖 Reading Section:")
            report.append(f"   - Total reading questions: {len(reading_questions)}")
            report.append(f"   - Reading questions with passage: {reading_with_passage}")
            if reading_with_passage < len(reading_questions):
                report.append(f"   ⚠️ WARNING: Some reading questions lack passages!")
        
        # 지문 내용 샘플
        passages = [(q.get('id'), q.get('passage', '')) for q in questions if q.get('passage')]
        if passages:
            report.append(f"\n📝 Sample Passages:")
            for q_id, passage in passages[:3]:  # 처음 3개만 표시
                report.append(f"\n   Question ID {q_id}:")
                report.append(f"   \"{passage[:100]}{'...' if len(passage) > 100 else ''}\"")
    
    return '\n'.join(report)

if __name__ == "__main__":
    with open('extracted_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    report = analyze_level_validity(data)
    print(report)
    
    # 보고서 저장
    with open('VALIDITY_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n\n✅ Report saved to VALIDITY_REPORT.txt")
