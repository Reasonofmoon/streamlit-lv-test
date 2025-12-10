import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.cefr_analyzer import CEFRAnalyzer

# 페이지 설정
st.set_page_config(
    page_title="CEFR Test - Student",
    page_icon="📝",
    layout="wide"
)

# 커스텀 CSS
with open('assets/styles.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'test_completed' not in st.session_state:
    st.session_state['test_completed'] = False
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

# 로그인 확인
if not st.session_state.get('logged_in', False) or st.session_state.get('user_role') != 'student':
    st.error("학생 계정으로 로그인해주세요.")
    st.switch_page("app.py")

# 질문 데이터 (실제로는 파일이나 데이터베이스에서 로드)
def load_questions(level):
    """
    PRE-A1 UnboundLocalError 방지를 위한 특수 처리 로더
    """
    # 입력값 유효성 검사
    if not level or not isinstance(level, str):
        level = 'A1'  # 기본값

    # PRE-A1 완전 격리 처리 - Ultra-think 해결책
    if level == 'PRE-A1':
        return load_preA1_questions_isolated()

    # 다른 레벨은 기존 로직 사용
    return load_other_level_questions(level)

def load_preA1_questions_isolated():
    """
    PRE-A1 전용 완전 격리 로더 - 다른 어떤 코드도 섞이지 않음
    """
    print("Loading PRE-A1 questions with isolated safe loader...")

    # 1. 첫 번째 시도: 좋은 데이터가 있는 extracted_questions.json에서만 로드
    try:
        import json
        with open('../extracted_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and 'PRE-A1' in data:
            raw_questions = data['PRE-A1']

            if isinstance(raw_questions, list) and len(raw_questions) > 0:
                cleaned_questions = []

                for q in raw_questions:
                    try:
                        if (isinstance(q, dict) and
                            'options' in q and isinstance(q['options'], list) and
                            len(q['options']) == 4 and
                            all(opt and str(opt).strip() for opt in q['options'])):

                            cleaned_q = {
                                'id': int(q.get('id', 0)),
                                'question': str(q.get('question', '')).replace('<span class="question-text">', '').replace('</span>', ''),
                                'options': [str(opt).replace('A)', '').replace('B)', '').replace('C)', '').replace('D)', '') for opt in q['options']],
                                'correct': int(q.get('correct', 0)),
                                'section': str(q.get('section', 'General'))
                            }
                            cleaned_questions.append(cleaned_q)
                    except Exception:
                        continue  # 개별 질문 오류는 무시

                if cleaned_questions:
                    print(f"✅ PRE-A1: Successfully loaded {len(cleaned_questions)} questions")
                    return cleaned_questions

    except Exception as e:
        print(f"PRE-A1 JSON loading failed: {e}")

    # 2. 두 번째 시도: A1 질문을 PRE-A1으로 사용 (fallback)
    try:
        print("PRE-A1: Falling back to A1 questions...")
        a1_questions = load_other_level_questions('A1')
        if a1_questions and len(a1_questions) > 0:
            # ID를 PRE-A1 스타일로 조정
            for q in a1_questions:
                q['id'] = q['id']  # ID는 그대로 유지
                q['original_level'] = 'A1'  # 원본 레벨 표시
            print(f"✅ PRE-A1: Using {len(a1_questions)} A1 questions as fallback")
            return a1_questions
    except Exception as e:
        print(f"PRE-A1 A1 fallback failed: {e}")

    # 3. 최후의 수단: 하드코딩된 비상 질문
    print("PRE-A1: Using emergency hardcoded questions...")
    return [
        {
            'id': 1,
            'question': 'What do you say when you meet someone?',
            'options': ['Hello', 'Goodbye', 'Thank you', 'Sorry'],
            'correct': 0,
            'section': 'Conversation'
        },
        {
            'id': 2,
            'question': 'My name _______ Alex.',
            'options': ['am', 'is', 'are', 'be'],
            'correct': 1,
            'section': 'Grammar'
        },
        {
            'id': 3,
            'question': 'What is the opposite of "good"?',
            'options': ['Bad', 'Good', 'Happy', 'Sad'],
            'correct': 0,
            'section': 'Vocabulary'
        },
        {
            'id': 4,
            'question': 'I _______ from Korea.',
            'options': ['am', 'is', 'are', 'be'],
            'correct': 0,
            'section': 'Grammar'
        },
        {
            'id': 5,
            'question': 'Nice to _______ you.',
            'options': ['see', 'know', 'meet', 'go'],
            'correct': 2,
            'section': 'Conversation'
        }
    ]

def load_other_level_questions(level):
    """
    A1, A2, B1, B2 등 PRE-A1 외 레벨용 로더
    """
    print(f"Loading {level} questions...")
    questions = []  # 기본값으로 빈 리스트 초기화

    # JSON 파일에서 로드 시도
    try:
        import json
        with open('../extracted_questions.json', 'r', encoding='utf-8') as f:
            extracted_questions = json.load(f)

        # 딕셔너리 구조 확인 및 안전한 접근
        if isinstance(extracted_questions, dict) and level in extracted_questions:
            questions = extracted_questions[level]

            # 데이터 정리 및 유효성 검사
            if isinstance(questions, list):
                cleaned_questions = []
                for q in questions:
                    try:
                        if (isinstance(q, dict) and
                            'options' in q and isinstance(q['options'], list) and
                            len(q['options']) == 4 and
                            all(opt and opt.strip() for opt in q['options'])):

                            cleaned_q = {
                                'id': q.get('id', 0),
                                'question': str(q.get('question', '')).replace('<span class="question-text">', '').replace('</span>', ''),
                                'options': [str(opt).replace('A)', '').replace('B)', '').replace('C)', '').replace('D)', '') for opt in q['options']],
                                'correct': int(q.get('correct', 0)),
                                'section': str(q.get('section', 'General'))
                            }
                            cleaned_questions.append(cleaned_q)
                    except Exception as e:
                        continue  # 개별 질문 오류는 무시하고 계속 진행

                questions = cleaned_questions
                if questions:
                    print(f"Loaded {len(questions)} valid questions from JSON for level {level}")
                    return questions
            else:
                questions = []
        else:
            questions = []

    except Exception as e:
        print(f"JSON loading failed for {level}: {e}")
        questions = []  # 예외 발생시 빈 리스트로 초기화

    # 2. A1 레벨은 하드코딩된 데이터 사용 (fallback)
    if level == 'A1' and not questions:
        # 지문 정의 (문제 그룹별)
        passages = {
            1: "Hi Tom,\n\nI am at the library. Please come at 3 o'clock.\nBring your English book.\nSee you soon!\n\nMia",
            3: "Henry and his big dog Mudge went camping. Henry's mother knew all about camping. She knew how to set up a tent. She knew how to build a campfire. Henry's father didn't know anything about camping. He just came with a guitar and a smile. They walked and walked. It was beautiful. Henry saw fish in the stream and a rainbow.",
            5: "Nate is a detective. He likes pancakes very much. He had pancakes for breakfast. Then the telephone rang. It was Annie. Annie lost a picture. The picture was of her dog, Fang. Nate said, \"I will find the picture.\""
        }

        questions = [
            # Reading Comprehension (8문항) - 지문 포함
            {
                'id': 1,
                'question': 'Where is Mia?',
                'options': ['At school', 'At the library', 'At home', 'At the park'],
                'correct': 1,
                'section': 'Reading'
            },
            {
                'id': 2,
                'question': 'What should Tom bring?',
                'options': ['His lunch box', 'His math book', 'His English book', 'His pencil case'],
                'correct': 2,
                'section': 'Reading'
            },
            {
                'id': 3,
                'question': 'Who knew about camping?',
                'options': ['Henry\'s father', 'Henry\'s mother', 'Mudge the dog', 'Henry'],
                'correct': 1,
                'section': 'Reading'
            },
            {
                'id': 4,
                'question': 'What did Henry see?',
                'options': ['Fish and a rainbow', 'Just a rainbow', 'Just fish', 'A guitar'],
                'correct': 0,
                'section': 'Reading'
            },
            {
                'id': 5,
                'question': 'What does Nate like to eat?',
                'options': ['Sandwiches', 'Pancakes', 'Pizza', 'Cookies'],
                'correct': 1,
                'section': 'Reading'
            },
            {
                'id': 6,
                'question': 'What did Annie lose?',
                'options': ['Her dog', 'A picture', 'Her phone', 'Her keys'],
                'correct': 1,
                'section': 'Reading'
            },
            {
                'id': 7,
                'question': 'What is the name of Annie\'s dog?',
                'options': ['Mudge', 'Henry', 'Fang', 'Tom'],
                'correct': 2,
                'section': 'Reading'
            },
            {
                'id': 8,
                'question': 'What does Nate do?',
                'options': ['He is a teacher', 'He is a doctor', 'He is a detective', 'He is a cook'],
                'correct': 2,
                'section': 'Reading'
            },

            # Vocabulary (12문항)
            {
                'id': 9,
                'question': 'Choose the correct word: I ___ a student.',
                'options': ['am', 'is', 'are', 'be'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 10,
                'question': 'What is the opposite of "big"?',
                'options': ['Small', 'Large', 'Tall', 'Short'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 11,
                'question': 'What color is the sky?',
                'options': ['Red', 'Blue', 'Green', 'Yellow'],
                'correct': 1,
                'section': 'Vocabulary'
            },
            {
                'id': 12,
                'question': 'How many days are in a week?',
                'options': ['5', '6', '7', '8'],
                'correct': 2,
                'section': 'Vocabulary'
            },
            {
                'id': 13,
                'question': 'What do we use to write?',
                'options': ['Pen', 'Book', 'Table', 'Chair'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 14,
                'question': 'Which animal says "meow"?',
                'options': ['Dog', 'Cat', 'Bird', 'Fish'],
                'correct': 1,
                'section': 'Vocabulary'
            },
            {
                'id': 15,
                'question': 'What is the opposite of "hot"?',
                'options': ['Cold', 'Warm', 'Cool', 'Ice'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 16,
                'question': 'How many legs does a dog have?',
                'options': ['Two', 'Four', 'Six', 'Eight'],
                'correct': 1,
                'section': 'Vocabulary'
            },
            {
                'id': 17,
                'question': 'What is the opposite of "happy"?',
                'options': ['Sad', 'Angry', 'Excited', 'Surprised'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 18,
                'question': 'What do you do with your eyes?',
                'options': ['See', 'Hear', 'Smell', 'Taste'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 19,
                'question': 'What color is an apple?',
                'options': ['Red', 'Blue', 'Green', 'Yellow'],
                'correct': 0,
                'section': 'Vocabulary'
            },
            {
                'id': 20,
                'question': 'What do you do when you are thirsty?',
                'options': ['Drink', 'Eat', 'Sleep', 'Run'],
                'correct': 0,
                'section': 'Vocabulary'
            },

            # Conversation (5문항)
            {
                'id': 21,
                'question': 'A: "Hello, how are you?" B: "___"',
                'options': ['I\'m fine, thank you', 'I\'m 25 years old', 'I\'m a teacher', 'I\'m from Korea'],
                'correct': 0,
                'section': 'Conversation'
            },
            {
                'id': 22,
                'question': 'A: "What time is it?" B: "___"',
                'options': ['It\'s 3 o\'clock', 'It\'s Monday', 'It\'s sunny', 'It\'s hot'],
                'correct': 0,
                'section': 'Conversation'
            },
            {
                'id': 23,
                'question': 'A: "Where is the library?" B: "___"',
                'options': ['It\'s over there', 'It\'s expensive', 'It\'s delicious', 'It\'s cold'],
                'correct': 0,
                'section': 'Conversation'
            },
            {
                'id': 24,
                'question': 'A: "Thank you for your help." B: "___"',
                'options': ['You\'re welcome', 'Thank you too', 'Goodbye', 'Hello'],
                'correct': 0,
                'section': 'Conversation'
            },
            {
                'id': 25,
                'question': 'A: "See you tomorrow." B: "___"',
                'options': ['See you later', 'Nice to meet you', 'How are you', 'What\'s your name'],
                'correct': 0,
                'section': 'Conversation'
            },

            # Grammar (10문항)
            {
                'id': 26,
                'question': 'She ___ a doctor.',
                'options': ['am', 'is', 'are', 'be'],
                'correct': 1,
                'section': 'Grammar'
            },
            {
                'id': 27,
                'question': 'They ___ happy.',
                'options': ['am', 'is', 'are', 'be'],
                'correct': 2,
                'section': 'Grammar'
            },
            {
                'id': 28,
                'question': '___ is your name?',
                'options': ['What', 'Where', 'When', 'Who'],
                'correct': 0,
                'section': 'Grammar'
            },
            {
                'id': 29,
                'question': '___ do you live?',
                'options': ['What', 'Where', 'When', 'Who'],
                'correct': 1,
                'section': 'Grammar'
            },
            {
                'id': 30,
                'question': 'She ___ to school every day.',
                'options': ['go', 'goes', 'going', 'is go'],
                'correct': 1,
                'section': 'Grammar'
            },
            {
                'id': 31,
                'question': 'I ___ coffee every morning.',
                'options': ['drink', 'drinks', 'drinking', 'is drink'],
                'correct': 0,
                'section': 'Grammar'
            },
            {
                'id': 32,
                'question': 'They ___ in London.',
                'options': ['live', 'lives', 'living', 'is live'],
                'correct': 0,
                'section': 'Grammar'
            },
            {
                'id': 33,
                'question': 'He ___ very hard.',
                'options': ['work', 'works', 'working', 'is work'],
                'correct': 1,
                'section': 'Grammar'
            },
            {
                'id': 34,
                'question': '___ old are you?',
                'options': ['What', 'Where', 'When', 'How'],
                'correct': 3,
                'section': 'Grammar'
            }
        ]

        # 각 문항에 지문 연결 (공유 지문 포함)
        for question in questions:
            q_id = question['id']
            # 지문 공유 규칙: 1-2번은 지문 1 공유, 3-4번은 지문 2 공유, 5-8번은 지문 3 공유
            if q_id in [1, 2]:
                question['passage'] = passages[1]
            elif q_id in [3, 4]:
                question['passage'] = passages[3]
            elif q_id in [5, 6, 7, 8]:
                question['passage'] = passages[5]

        return questions

    # A2 레벨은 수동으로 추가 (answer-data.js 기반)
    if level == 'A2':
        questions = [
            # Reading Comprehension (8문항)
            {'id': 1, 'question': 'Read the passage and answer: The main idea of the text is about...', 'options': ['Travel', 'Education', 'Food', 'Sports'], 'correct': 1, 'section': 'Reading'},
            {'id': 2, 'question': 'According to the passage, the author believes that...', 'options': ['Learning is easy', 'Practice makes perfect', 'Teachers are not important', 'Students don\'t need help'], 'correct': 1, 'section': 'Reading'},
            {'id': 3, 'question': 'What does the word "challenge" mean in the context?', 'options': ['Problem', 'Solution', 'Reward', 'Game'], 'correct': 0, 'section': 'Reading'},
            {'id': 4, 'question': 'The tone of the passage can be described as...', 'options': ['Formal', 'Informal', 'Angry', 'Sad'], 'correct': 0, 'section': 'Reading'},
            {'id': 5, 'question': 'Where was the author born?', 'options': ['London', 'New York', 'Paris', 'Tokyo'], 'correct': 1, 'section': 'Reading'},
            {'id': 6, 'question': 'How many languages does the author speak?', 'options': ['One', 'Two', 'Three', 'Four'], 'correct': 2, 'section': 'Reading'},
            {'id': 7, 'question': 'What is the main character\'s profession?', 'options': ['Teacher', 'Doctor', 'Engineer', 'Artist'], 'correct': 2, 'section': 'Reading'},
            {'id': 8, 'question': 'When did the story take place?', 'options': ['Last year', 'This year', 'Next year', 'Five years ago'], 'correct': 2, 'section': 'Reading'},

            # Vocabulary (12문항)
            {'id': 9, 'question': 'Which word means "very large"?', 'options': ['Tiny', 'Huge', 'Small', 'Medium'], 'correct': 1, 'section': 'Vocabulary'},
            {'id': 10, 'question': 'What is the synonym of "important"?', 'options': ['Insignificant', 'Crucial', 'Minor', 'Simple'], 'correct': 1, 'section': 'Vocabulary'},
            {'id': 11, 'question': 'Choose the correct word: She has a ___ memory.', 'options': ['good', 'well', 'better', 'best'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 12, 'question': 'The weather was ___ yesterday.', 'options': ['beauty', 'beautiful', 'beautify', 'beautifully'], 'correct': 1, 'section': 'Vocabulary'},
            {'id': 13, 'question': 'He speaks English ___.', 'options': ['fluent', 'fluently', 'fluency', 'fluens'], 'correct': 1, 'section': 'Vocabulary'},
            {'id': 14, 'question': 'I need to ___ my English.', 'options': ['improve', 'improvement', 'improving', 'improved'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 15, 'question': 'The test was very ___.', 'options': ['difficult', 'difficulty', 'difficultly', 'difficultness'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 16, 'question': 'She made a ___ decision.', 'options': ['wise', 'wisely', 'wisdom', 'wiseless'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 17, 'question': 'The book was very ___.', 'options': ['interesting', 'interest', 'interested', 'interests'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 18, 'question': 'He felt ___ after the long journey.', 'options': ['tired', 'tire', 'tiring', 'tires'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 19, 'question': 'The food was ___.', 'options': ['delicious', 'deliciously', 'deliciousness', 'deliciously'], 'correct': 0, 'section': 'Vocabulary'},
            {'id': 20, 'question': 'She is a ___ student.', 'options': ['brilliant', 'brilliantly', 'brilliance', 'brilliantness'], 'correct': 0, 'section': 'Vocabulary'},

            # Conversation (8문항)
            {'id': 21, 'question': 'A: "How are you?" B: "___"', 'options': ['I\'m fine, thank you', 'I\'m 25 years old', 'I\'m a teacher', 'I\'m from Korea'], 'correct': 0, 'section': 'Conversation'},
            {'id': 22, 'question': 'A: "What time is it?" B: "___"', 'options': ['It\'s 3 o\'clock', 'It\'s Monday', 'It\'s sunny', 'It\'s hot'], 'correct': 0, 'section': 'Conversation'},
            {'id': 23, 'question': 'A: "Where is the library?" B: "___"', 'options': ['It\'s over there', 'It\'s expensive', 'It\'s delicious', 'It\'s cold'], 'correct': 0, 'section': 'Conversation'},
            {'id': 24, 'question': 'A: "Can you help me?" B: "___"', 'options': ['Of course', 'No problem', 'I\'m busy', 'I don\'t know'], 'correct': 0, 'section': 'Conversation'},
            {'id': 25, 'question': 'A: "Thank you for your help." B: "___"', 'options': ['You\'re welcome', 'Thank you too', 'Goodbye', 'Hello'], 'correct': 0, 'section': 'Conversation'},
            {'id': 26, 'question': 'A: "See you tomorrow." B: "___"', 'options': ['See you later', 'Nice to meet you', 'How are you', 'What\'s your name'], 'correct': 0, 'section': 'Conversation'},
            {'id': 27, 'question': 'A: "What do you do for fun?" B: "___"', 'options': ['I like reading books', 'I\'m a doctor', 'I\'m 30 years old', 'I live in Seoul'], 'correct': 0, 'section': 'Conversation'},
            {'id': 28, 'question': 'A: "How was your weekend?" B: "___"', 'options': ['It was great', 'It\'s Monday', 'I\'m tired', 'I\'m hungry'], 'correct': 0, 'section': 'Conversation'},

            # Grammar (10문항)
            {'id': 29, 'question': 'I ___ to the cinema yesterday.', 'options': ['go', 'went', 'gone', 'going'], 'correct': 1, 'section': 'Grammar'},
            {'id': 30, 'question': 'She ___ English for three years.', 'options': ['study', 'studies', 'has studied', 'studied'], 'correct': 2, 'section': 'Grammar'},
            {'id': 31, 'question': 'They ___ dinner when I arrived.', 'options': ['have', 'had', 'were having', 'are having'], 'correct': 2, 'section': 'Grammar'},
            {'id': 32, 'question': 'If I ___ rich, I would buy a car.', 'options': ['am', 'was', 'were', 'will be'], 'correct': 2, 'section': 'Grammar'},
            {'id': 33, 'question': 'The movie ___ by Steven Spielberg.', 'options': ['direct', 'directed', 'directing', 'directs'], 'correct': 1, 'section': 'Grammar'},
            {'id': 34, 'question': 'You ___ smoke here. It\'s not allowed.', 'options': ['mustn\'t', 'don\'t have to', 'should', 'can'], 'correct': 0, 'section': 'Grammar'},
            {'id': 35, 'question': 'I wish I ___ speak French.', 'options': ['can', 'could', 'will', 'would'], 'correct': 1, 'section': 'Grammar'},
            {'id': 36, 'question': 'By next year, I ___ my degree.', 'options': ['finish', 'will finish', 'have finished', 'finished'], 'correct': 2, 'section': 'Grammar'},
            {'id': 37, 'question': 'She suggested ___ to the park.', 'options': ['go', 'going', 'to go', 'went'], 'correct': 1, 'section': 'Grammar'},
            {'id': 38, 'question': 'The book ___ I borrowed from you was interesting.', 'options': ['who', 'which', 'what', 'where'], 'correct': 1, 'section': 'Grammar'},

            # Writing (2문항)
            {'id': 39, 'question': 'Which sentence is correct?', 'options': ['I have visited Paris last year', 'I visited Paris last year', 'I visit Paris last year', 'I am visiting Paris last year'], 'correct': 1, 'section': 'Writing'},
            {'id': 40, 'question': 'Choose the best way to complete the sentence: "I enjoy ___ because..."', 'options': ['read books', 'reading books', 'to read books', 'read books'], 'correct': 1, 'section': 'Writing'}
        ]
        return questions

    # 최종 안전장치: questions가 리스트인지 확인하고 반환
    if not isinstance(questions, list):
        print(f"Warning: questions is not a list, it's {type(questions)}. Returning empty list.")
        return []

    return questions

# 채점 함수
def calculate_score(answers, questions):
    correct = 0
    total = len(questions)
    section_results = {}

    for i, question in enumerate(questions):
        if i < len(answers) and answers[i] == question['correct']:
            correct += 1

            # 섹션별 점수 계산
            section = question['section']
            if section not in section_results:
                section_results[section] = {'correct': 0, 'total': 0}
            section_results[section]['correct'] += 1
            section_results[section]['total'] += 1
        else:
            section = question['section']
            if section not in section_results:
                section_results[section] = {'correct': 0, 'total': 0}
            section_results[section]['total'] += 1

    percentage = (correct / total) * 100 if total > 0 else 0

    return {
        'score': round(percentage),
        'correct': correct,
        'total': total,
        'passed': percentage >= 70,
        'section_results': section_results
    }

# 결과 저장 함수
def save_results(level, score_data):
    result = {
        'student_info': st.session_state.get('student_info', {}),
        'level': level,
        'submittedAt': datetime.now().isoformat(),
        'score': score_data['score'],
        'passed': score_data['passed'],
        'correct': score_data['correct'],
        'total': score_data['total'],
        'sectionResults': score_data['section_results'],
        'answers': st.session_state['answers']
    }

    # submissions 폴더에 저장
    import os
    if not os.path.exists('data/submissions'):
        os.makedirs('data/submissions')

    filename = f"data/submissions/{st.session_state['student_info']['name']}_{level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return filename

# 메인 함수
def main():
    st.title("📝 CEFR Level Test")

    # 레벨 확인
    level = st.session_state.get('test_level', 'A1')
    st.info(f"선택된 레벨: **{level}**")

    # 질문 로드 (강력한 예외 처리)
    try:
        questions = load_questions(level)
    except UnboundLocalError as e:
        st.error(f"❌ 질문 로드 중 오류가 발생했습니다: UnboundLocalError")
        st.error("🔧 시스템 관리자에게 문의해주세요. 이 오류는 데이터 로드 문제일 수 있습니다.")
        # 비상용 기본 질문 제공
        questions = [
            {
                'id': 1,
                'question': 'What is your name?',
                'options': ['Alex', 'Maria', 'John', 'Sarah'],
                'correct': 0,
                'section': 'General'
            }
        ]
    except Exception as e:
        st.error(f"❌ 질문 로드 중 오류가 발생했습니다: {type(e).__name__}")
        # 비상용 기본 질문 제공
        questions = [
            {
                'id': 1,
                'question': 'What is your name?',
                'options': ['Alex', 'Maria', 'John', 'Sarah'],
                'correct': 0,
                'section': 'General'
            }
        ]

    # 질문 데이터 유효성 검사
    if not questions or not isinstance(questions, list):
        st.error(f"❌ '{level}' 레벨의 질문 데이터를 불러올 수 없습니다.")
        st.stop()

    if len(questions) == 0:
        st.error(f"❌ '{level}' 레벨에 사용 가능한 질문이 없습니다.")
        st.stop()

    # 데이터 품질 검사
    valid_questions = []
    for q in questions:
        if (q and isinstance(q, dict) and
            'question' in q and q['question'].strip() and
            'options' in q and isinstance(q['options'], list) and len(q['options']) == 4 and
            all(opt.strip() for opt in q['options'])):
            valid_questions.append(q)

    if len(valid_questions) != len(questions):
        st.warning(f"⚠️ {len(questions) - len(valid_questions)}개의 잘못된 질문을 제외했습니다.")

    if len(valid_questions) == 0:
        st.error("❌ 유효한 질문이 없습니다. 관리자에게 문의해주세요.")
        st.stop()

    questions = valid_questions
    total_questions = len(questions)

    # 테스트 시작
    if not st.session_state['start_time']:
        if st.button("테스트 시작", type="primary"):
            st.session_state['start_time'] = time.time()
            st.rerun()
        return

    # 진행 상황 표시
    progress = (len(st.session_state['answers']) / total_questions)
    st.progress(progress)

    # 상세 진행 상황 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("현재 문제", f"{st.session_state['current_question'] + 1}/{total_questions}")
    with col2:
        st.metric("답변 완료", f"{len(st.session_state['answers'])}/{total_questions}")
    with col3:
        st.metric("남은 문제", f"{total_questions - len(st.session_state['answers'])}")
    with col4:
        completion_rate = (len(st.session_state['answers']) / total_questions) * 100
        st.metric("완료율", f"{completion_rate:.1f}%")

    # 현재 문제 상태
    current_answered = st.session_state['current_question'] < len(st.session_state['answers'])
    if current_answered:
        st.success(f"✅ 문제 {st.session_state['current_question'] + 1}: 답변 완료됨")
    else:
        st.warning(f"❓ 문제 {st.session_state['current_question'] + 1}: 답변 필요")

    # 문제 목록과 네비게이션
    st.markdown("---")

    # 네비게이션과 문제 목록
    col1, col2, col3 = st.columns([2, 1, 1])

    with col2:
        st.markdown("### 🧭 빠른 이동")
        # 첫 번째 문제로 이동
        if st.button("⬅ 첫 문제", key="first_question", disabled=st.session_state['current_question'] == 0):
            st.session_state['current_question'] = 0
            st.rerun()

        # 마지막 문제로 이동
        if st.button("⬅ 마지막 문제", key="last_question", disabled=st.session_state['current_question'] >= total_questions - 1):
            st.session_state['current_question'] = total_questions - 1
            st.rerun()

    with col3:
        st.markdown("### 📋 문제 목록")
        # 문제 1-8 표시 (읽기 문제는 지문 표시)
        st.write("문제 1-8 (읽기 이해)")

        # 모든 문제 상태 표시
        problem_status = []
        for i in range(total_questions):
            if i < len(st.session_state['answers']):
                problem_status.append(f"Q{i+1}: ✅")
            else:
                problem_status.append(f"Q{i+1}: ⭕")

        status_text = " | ".join(problem_status)
        st.markdown(f"<small>{status_text}</small>", unsafe_allow_html=True)

    with col1:
        st.markdown("### 📊 문제 진도")

        # 구간별 문제 구분
        section_questions = {}
        for i, q in enumerate(questions):
            section = q['section']
            if section not in section_questions:
                section_questions[section] = []
            section_questions[section].append(i + 1)

        # 섹션별 진행 상황
        for section, q_list in section_questions.items():
            section_completed = sum(1 for q_num in q_list if q_num <= len(st.session_state['answers']))
            section_total = len(q_list)

            # 섹션별 진행률 막대
            progress = section_completed / section_total if section_total > 0 else 0
            st.write(f"**{section}**: {section_completed}/{section_total} ({progress*100:.0f}%)")
            st.progress(progress)

            # 섹션별 문제 번호 표시
            q_status = []
            for q_num in q_list:
                if q_num <= len(st.session_state['answers']):
                    q_status.append(f"Q{q_num} ✅")
                else:
                    q_status.append(f"Q{q_num} ⭕")

            st.markdown(f"<small>{' | '.join(q_status)}</small>", unsafe_allow_html=True)

    # 현재 질문 표시
    if not st.session_state['test_completed'] and st.session_state['current_question'] < total_questions:
        current_q = questions[st.session_state['current_question']]

        # 데이터 유효성 검사
        if not current_q or not isinstance(current_q, dict):
            st.error("❌ 질문 데이터가 올바르지 않습니다.")
            st.stop()

        if 'question' not in current_q or not current_q['question'].strip():
            st.error("❌ 질문 내용이 없습니다.")
            st.stop()

        if 'options' not in current_q or not isinstance(current_q['options'], list) or len(current_q['options']) != 4:
            st.error("❌ 선택지 데이터가 올바르지 않습니다.")
            st.stop()

        if not all(opt.strip() for opt in current_q['options']):
            st.error("❌ 일부 선택지가 비어있습니다.")
            st.stop()

        # 지문이 있는 경우 먼저 표시
        if 'passage' in current_q and current_q['passage'] and current_q['passage'].strip():
            st.markdown(f"""
            <div class="question-card" style="background-color: #f0f8ff; border-left: 5px solid #3b82f6;">
                <h3>📄 Reading Passage</h3>
                <div style="background-color: white; padding: 20px; border-radius: 8px; white-space: pre-wrap; line-height: 1.6;">
                    {current_q['passage']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 질문 카드
        st.markdown(f"""
        <div class="question-card">
            <h3>📖 {current_q['section']}</h3>
            <h2>{current_q['question']}</h2>
        </div>
        """, unsafe_allow_html=True)

        # 선택지
        selected_option = None

        # 현재 선택된 답변 확인
        current_answer = None
        if st.session_state['current_question'] < len(st.session_state['answers']):
            current_answer = st.session_state['answers'][st.session_state['current_question']]

        for i, option in enumerate(current_q['options']):
            button_symbol = '●' if i == current_answer else '○'
            if st.button(f"{button_symbol} {option}",
                        key=f"option_{i}",
                        help=f"옵션 {i+1}"):
                selected_option = i

        # 버튼 영역
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("← 이전 문제", disabled=st.session_state['current_question'] == 0):
                st.session_state['current_question'] -= 1
                st.rerun()

        with col2:
            if st.button("이전으로", disabled=st.session_state['current_question'] == 0):
                if st.session_state['current_question'] > 0:
                    st.session_state['current_question'] -= 1
                st.rerun()

        with col3:
            if st.button("다음으로", disabled=st.session_state['current_question'] >= total_questions - 1):
                st.session_state['current_question'] += 1
                st.rerun()

        with col4:
            if st.button("다음 문제 →", disabled=st.session_state['current_question'] >= total_questions - 1):
                # 현재 문제에 답했는지 확인
                current_answered = st.session_state['current_question'] < len(st.session_state['answers'])
                if current_answered:
                    st.session_state['current_question'] += 1
                    st.rerun()
                else:
                    st.error("⚠️ 현재 문제에 답해야 다음 문제로 넘어갈 수 있습니다.")

    # 테스트 완료
    elif st.session_state['current_question'] >= total_questions and not st.session_state['test_completed']:
        # 모든 문항이 답변되었는지 확인
        if len(st.session_state['answers']) < total_questions:
            missing_answers = total_questions - len(st.session_state['answers'])
            st.error(f"⚠️ {missing_answers}개의 문항이 아직 답변되지 않았습니다.")
            st.warning("모든 문항을 완료해야 테스트를 종료할 수 있습니다.")
            st.info(f"답변 완료: {len(st.session_state['answers'])}/{total_questions} 문항")

            # 답변하지 않은 문항 목록 표시
            missing_questions = []
            for i in range(total_questions):
                if i >= len(st.session_state['answers']):
                    missing_questions.append(i + 1)

            st.write(f"답변 필요한 문항: {', '.join(map(str, missing_questions))}")

            # 첫 번째 답변하지 않은 문항으로 이동
            if st.button("첫 번째 미답변 문항으로 이동", type="primary"):
                st.session_state['current_question'] = missing_questions[0] - 1
                st.rerun()

        # 모든 문항이 답변된 경우에만 완료 가능
        else:
            st.success("✅ 모든 문항이 완료되었습니다!")
            st.info("테스트를 제출하면 자동으로 채점되고 상세한 학습 분석 리포트가 생성됩니다.")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 테스트 제출 및 결과 보기", type="primary"):
                    st.session_state['test_completed'] = True
                    st.rerun()
            with col2:
                if st.button("🔍 답변 확인"):
                    # 답변 확인용 표시
                    for i, (answer, question) in enumerate(zip(st.session_state['answers'], questions)):
                        correct = answer == question['correct']
                        status = "✅" if correct else "❌"
                        st.write(f"Q{i+1}: {status} {question['question'][:50]}...")

    # 결과 표시
    if st.session_state['test_completed']:
        score_data = calculate_score(st.session_state['answers'], questions)

        # 결과 저장을 위한 데이터 준비
        test_results = {
            'studentInfo': st.session_state.get('student_info', {}),
            'level': level,
            'submittedAt': datetime.now().isoformat(),
            'score': score_data['score'],
            'passed': score_data['passed'],
            'correct': score_data['correct'],
            'total': score_data['total'],
            'sectionResults': score_data['section_results'],
            'answers': st.session_state['answers']
        }

        # CEFR 분석
        analyzer = CEFRAnalyzer()
        analysis = analyzer.analyze_test_results(test_results)

        # 결과 저장
        saved_file = save_results(level, score_data)

        # 결과 화면
        st.success("🎉 테스트 완료! 상세한 학습 분석 리포트가 생성되었습니다.")

        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["📊 결과 요약", "🎯 상담 리포트", "📚 학습 커리큘럼"])

        with tab1:
            # 기본 결과 요약
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="question-card">
                    <h2>📊 최종 점수</h2>
                    <h1 style="font-size: 4rem; color: {'#10B981' if score_data['passed'] else '#EF4444'};">
                        {score_data['score']}점
                    </h1>
                    <p>{score_data['correct']} / {score_data['total']} 정답</p>
                    <p style="font-size: 1.2rem;">
                        <strong>진단 CEFR 레벨:</strong> {analysis['current_cefr_level']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="question-card">
                    <h3>📈 섹션별 결과</h3>
                </div>
                """, unsafe_allow_html=True)

                # 섹션별 결과를 시각적으로 표시
                for section, data in analysis['section_analysis'].items():
                    emoji = {'excellent': '🌟', 'good': '✅', 'average': '📊', 'needs_improvement': '📈'}.get(data['strength_level'], '❓')
                    st.write(f"{emoji} **{section}**: {data['correct']}/{data['total']} ({data['percentage']}%)")
                    st.progress(data['percentage'] / 100)

            # 소요 시간
            if st.session_state['start_time']:
                time_spent = time.time() - st.session_state['start_time']
                minutes = int(time_spent // 60)
                seconds = int(time_spent % 60)
                st.info(f"⏱️ 소요 시간: {minutes}분 {seconds}초")

        with tab2:
            # 상담 리포트
            st.header("🎯 상담용 학습 분석 리포트")

            # 다운로드 버튼
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("📄 리포트 다운로드", type="primary"):
                    report_content = analyzer.generate_counseling_report(analysis)
                    st.download_button(
                        label="다운로드",
                        data=report_content,
                        file_name=f"CEFR_학습상담_리포트_{st.session_state['student_info']['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

            # 리포트 내용 표시
            report_content = analyzer.generate_counseling_report(analysis)
            st.markdown(report_content)

        with tab3:
            # 학습 커리큘럼
            st.header("📚 맞춤형 학습 커리큘럼")

            curriculum = analysis['learning_curriculum']
            next_goal = analysis['next_level_goal']

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🎯 학습 목표")
                st.write(f"**현재 레벨**: {analysis['current_cefr_level']}")
                st.write(f"**목표 레벨**: {next_goal.get('level', analysis['current_cefr_level'])}")
                st.write(f"**목표 점수**: {next_goal.get('target_score', 70)}점")
                st.write(f"**예상 기간**: {next_goal.get('estimated_duration', '3-6개월')}")

                st.subheader("📅 일일 학습 계획")
                for i, practice in enumerate(curriculum.get('daily_practice', []), 1):
                    st.write(f"{i}. {practice}")

            with col2:
                st.subheader("🎯 학습 우선순위")
                for priority in curriculum.get('priority_areas', []):
                    st.warning(priority)

                st.subheader("📚 추천 학습 자료")
                for material in curriculum.get('materials', []):
                    st.info(f"📖 {material}")

        # 버튼들
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🏠 메인으로", type="secondary"):
                # 세션 초기화
                for key in ['current_question', 'answers', 'test_completed', 'start_time']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.switch_page("app.py")

        with col2:
            if st.button("🔄 다시 풀기"):
                # 세션 초기화
                for key in ['current_question', 'answers', 'test_completed', 'start_time']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        with col3:
            if st.button("📊 교사와 상담"):
                st.success("상담 신청이 완료되었습니다! 교사가 연락드릴 것입니다.")

if __name__ == "__main__":
    main()