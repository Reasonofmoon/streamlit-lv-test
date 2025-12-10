import re
import json
from bs4 import BeautifulSoup
import glob

def extract_questions_from_html(html_file):
    """HTML 파일에서 문항 추출"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # 모든 question div 찾기
    questions = []
    question_elements = soup.find_all('div', class_='question')

    for i, q_div in enumerate(question_elements):
        # 문제 번호 추출
        question_number_elem = q_div.find('span', class_='question-number')
        if question_number_elem:
            question_number = question_number_elem.get_text().strip()
        else:
            question_number = str(i + 1)

        # 문제 내용 추출
        question_text_elem = q_div.find('div', class_='question-text')
        if question_text_elem:
            question_text = question_text_elem.get_text().strip()
        else:
            # 다른 방식으로 문제 찾기
            text_pattern = r'<span class="question-number">' + re.escape(question_number) + r'</span>(.*?)<div'
            match = re.search(text_pattern, content, re.DOTALL)
            if match:
                question_text = match.group(1).strip()
            else:
                question_text = f"Question {question_number}"

        # 선택지 추출
        options = []
        option_elements = q_div.find_all('label')  # radio button labels

        if option_elements:
            for opt in option_elements:
                option_text = opt.get_text().strip()
                # 앞의 문자(A, B, C, D) 제거
                option_text = re.sub(r'^[A-D]\.\s*', '', option_text)
                options.append(option_text)
        else:
            # 다른 방식으로 선택지 찾기
            input_pattern = rf'<input[^>]*name="Q{question_number}"[^>]*value="([A-D])"[^>]*>.*?([^<]*(?:<[^>]*>[^<]*)*)'
            matches = re.findall(input_pattern, content, re.DOTALL)
            for match in matches:
                if len(match) >= 2:
                    option_value = match[0]
                    option_text = re.sub(r'<[^>]*>', '', match[1]).strip()
                    options.append(option_text)

        # 정답은 answer-data.js에서 찾아야 함
        if len(options) == 4:
            questions.append({
                'id': int(question_number),
                'question': question_text,
                'options': options,
                'correct': 0,  # 나중에 answer-data.js에서 설정
                'section': extract_section_from_question(question_text)
            })

    return questions

def extract_section_from_question(question_text):
    """문제 내용으로 섹션 추출"""
    question_lower = question_text.lower()

    if any(word in question_lower for word in ['read', 'passage', 'text', 'story']):
        return 'Reading'
    elif any(word in question_lower for word in ['vocabulary', 'word', 'meaning', 'synonym']):
        return 'Vocabulary'
    elif any(word in question_lower for word in ['conversation', 'dialogue', 'talk']):
        return 'Conversation'
    elif any(word in question_lower for word in ['grammar', 'verb', 'tense', 'sentence']):
        return 'Grammar'
    elif any(word in question_lower for word in ['write', 'writing']):
        return 'Writing'
    else:
        return 'General'

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
        else:
            print(f"  No HTML file found for {level}")

    # 결과 저장
    with open('../extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print("Questions extracted and saved to extracted_questions.json")

if __name__ == "__main__":
    main()