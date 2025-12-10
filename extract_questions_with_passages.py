import re
import json
from bs4 import BeautifulSoup
import glob

def extract_section_from_context(q_div, content, q_num):
    """문제 위치를 기반으로 섹션 추출"""
    # 문제 앞의 섹션 헤더 찾기
    q_pos = content.find(f'<span class="question-number">{q_num}</span>')
    if q_pos == -1:
        return "General"

    # 문제 앞에서 가장 가까운 섹션 헤더 찾기
    section_pattern = r'<section[^>]*>.*?<div class="section-header">.*?<h2[^>]*>(.*?)</h2>'
    sections = re.findall(section_pattern, content[:q_pos])

    if sections:
        section_text = sections[-1].strip()
        if "Reading" in section_text:
            return "Reading"
        elif "Vocabulary" in section_text:
            return "Vocabulary"
        elif "Conversation" in section_text:
            return "Conversation"
        elif "Grammar" in section_text:
            return "Grammar"
        elif "Writing" in section_text:
            return "Writing"

    # 문제 내용으로 섹션 판단
    q_search = content[q_pos:q_pos+500]
    if "Read the" in q_search or "passage" in q_search.lower():
        return "Reading"
    elif "mean" in q_search or "word" in q_search.lower():
        return "Vocabulary"
    elif "对话" in q_search or "conversation" in q_search.lower():
        return "Conversation"
    elif "verb" in q_search.lower() or "tense" in q_search.lower():
        return "Grammar"
    elif "write" in q_search.lower():
        return "Writing"

    return "General"

def extract_passages_for_question(content, q_num):
    """특정 문제에 대한 관련 지문 추출"""
    # 문제 위치 찾기
    q_pattern = f'<span class="question-number">{q_num}</span>'
    q_pos = content.find(q_pattern)

    if q_pos == -1:
        return None

    # 문제 앞의 모든 지문 찾기
    passage_pattern = r'<div class="passage">.*?<span class="passage-label">([^<]+)</span>(.*?)</div>'
    passages = re.findall(passage_pattern, content[:q_pos])

    if passages:
        # 가장 마지막 지문을 해당 문제의 지문으로 사용
        last_passage = passages[-1]
        passage_text = re.sub(r'<[^>]+>', ' ', last_passage[1]).strip()
        return passage_text

    return None

def extract_questions_from_html(html_file):
    """HTML 파일에서 문항과 지문 추출"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # 모든 question div 찾기
    questions = []

    # 문제 번호 패턴으로 모든 문제 찾기
    q_pattern = r'<div class="question">[^<]*<span class="question-number">(\d+)</span>(.*?)</div>\s*(?=</div>|<div class="question">|</section>)'
    q_matches = re.findall(q_pattern, content, re.DOTALL)

    for q_match in q_matches:
        q_num = int(q_match[0])
        q_content = q_match[1]

        # 문제 텍스트 추출
        question_text_pattern = r'<span class="question-text">(.*?)</span>'
        q_text_match = re.search(question_text_pattern, q_content)
        if q_text_match:
            question_text = re.sub(r'<[^>]+>', '', q_text_match.group(1)).strip()
        else:
            question_text = f"Question {q_num}"

        # 선택지 추출
        options = []
        option_pattern = r'<input[^>]*name="[^"]*" value="([A-D])"[^>]*>.*?<span[^>]*>([^<]+)</span>'
        option_matches = re.findall(option_pattern, q_content)

        for opt_match in option_matches:
            if len(opt_match) == 2:
                option_text = re.sub(r'^[A-D]\)\s*', '', opt_match[1]).strip()
                options.append(option_text)

        # 섹션 결정
        section = extract_section_from_context(None, content, str(q_num))

        # 관련 지문 추출
        passage = extract_passages_for_question(content, str(q_num))

        if len(options) == 4:
            question_data = {
                'id': q_num,
                'question': question_text,
                'options': options,
                'correct': 0,  # 나중에 answer-data.js에서 설정
                'section': section
            }

            # 지문이 있으면 추가
            if passage:
                question_data['passage'] = passage

            questions.append(question_data)

    return questions

def load_answer_key(level):
    """answer-data.js에서 정답 로드"""
    try:
        with open('js/answer-data.js', 'r', encoding='utf-8') as f:
            content = f.read()

        # 해당 레벨의 정답 추출
        pattern = rf"'{level}':.*?answers:\s*\{{([^}}]*)\}}"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            answers_str = match.group(1)
            # 정답 파싱
            answers = {}
            for answer_match in re.finditer(r"'Q(\d+)':\s*'(A|B|C|D)'", answers_str):
                q_num = int(answer_match.group(1))
                answer = answer_match.group(2)
                answers[q_num] = answer
            return answers
    except:
        pass

    return {}

def main():
    levels = ['PRE-A1', 'A1', 'A2', 'B1', 'B2']
    all_questions = {}

    for level in levels:
        print(f"Processing {level}...")

        # HTML 파일 찾기
        html_files = glob.glob(f"CEFR_{level}_English_Level_Test_Student.html")

        if html_files:
            html_file = html_files[0]
            questions = extract_questions_from_html(html_file)

            # 정답 설정
            answers = load_answer_key(level)
            for question in questions:
                q_id = question['id']
                if q_id in answers:
                    # 정답 문자(A, B, C, D)를 인덱스로 변환
                    answer_char = answers[q_id]
                    question['correct'] = ord(answer_char) - ord('A')

            all_questions[level] = questions
            print(f"  Found {len(questions)} questions for {level}")
            # 지문이 있는 문항 수 출력
            with_passage = sum(1 for q in questions if 'passage' in q)
            print(f"  {with_passage} questions have passages")
        else:
            print(f"  No HTML file found for {level}")

    # 결과 저장
    with open('../extracted_questions_with_passages.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print("Questions with passages extracted and saved to extracted_questions_with_passages.json")

if __name__ == "__main__":
    main()