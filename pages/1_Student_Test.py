import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import random

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
    # 예시 질문 데이터
    questions = {
        'A1': [
            {
                'id': 1,
                'question': 'What is your name?',
                'options': ['My name is...', 'I am from...', 'I live in...', 'I like...'],
                'correct': 0,
                'section': 'Personal Information'
            },
            {
                'id': 2,
                'question': 'Where are you from?',
                'options': ['I am 20 years old', 'I am from Korea', 'I am a student', 'I like English'],
                'correct': 1,
                'section': 'Personal Information'
            },
            {
                'id': 3,
                'question': 'Choose the correct form: I ___ a student.',
                'options': ['am', 'is', 'are', 'be'],
                'correct': 0,
                'section': 'Grammar'
            },
            {
                'id': 4,
                'question': 'What color is the sky?',
                'options': ['Red', 'Blue', 'Green', 'Yellow'],
                'correct': 1,
                'section': 'Vocabulary'
            },
            {
                'id': 5,
                'question': 'How many days are there in a week?',
                'options': ['5', '6', '7', '8'],
                'correct': 2,
                'section': 'General Knowledge'
            }
        ],
        'A2': [
            {
                'id': 1,
                'question': 'What did you do yesterday?',
                'options': ['I will go to school', 'I went to the park', 'I am studying', 'I have finished'],
                'correct': 1,
                'section': 'Past Tense'
            },
            {
                'id': 2,
                'question': 'Choose the correct sentence:',
                'options': [
                    'She go to school every day',
                    'She goes to school every day',
                    'She going to school every day',
                    'She is go to school every day'
                ],
                'correct': 1,
                'section': 'Grammar'
            }
        ],
        'Pre-A1': [
            {
                'id': 1,
                'question': 'Hello, how are you?',
                'options': ['Fine, thank you', 'Goodbye', 'My name is...', 'I don\'t know'],
                'correct': 0,
                'section': 'Greetings'
            },
            {
                'id': 2,
                'question': 'What is this? (pointing to a book)',
                'options': ['This is a pen', 'This is a book', 'This is a desk', 'This is a chair'],
                'correct': 1,
                'section': 'Objects'
            }
        ],
        'B1': [
            {
                'id': 1,
                'question': 'If you ___ harder, you would pass the exam.',
                'options': ['study', 'studied', 'had studied', 'were studying'],
                'correct': 2,
                'section': 'Conditional'
            },
            {
                'id': 2,
                'question': 'Choose the best response: "I haven\'t seen that movie yet."',
                'options': [
                    'Neither have I.',
                    'So have I.',
                    'I have too.',
                    'I did either.'
                ],
                'correct': 0,
                'section': 'Agreement'
            }
        ],
        'B2': [
            {
                'id': 1,
                'question': 'The company ___ its profits despite the economic downturn.',
                'options': ['managed increasing', 'managed to increase', 'managed increase', 'has managed increasing'],
                'correct': 1,
                'section': 'Business English'
            },
            {
                'id': 2,
                'question': '___ the heavy rain, they decided to continue the match.',
                'options': ['Despite', 'Although', 'Even though', 'In spite'],
                'correct': 0,
                'section': 'Conjunctions'
            }
        ]
    }

    return questions.get(level, [])

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

    # 질문 로드
    questions = load_questions(level)
    total_questions = len(questions)

    # 테스트 시작
    if not st.session_state['start_time']:
        if st.button("테스트 시작", type="primary"):
            st.session_state['start_time'] = time.time()
            st.rerun()
        return

    # 진행 상황 표시
    progress = (st.session_state['current_question'] / total_questions)
    st.progress(progress)
    st.write(f"문제 {st.session_state['current_question'] + 1} / {total_questions}")

    # 현재 질문 표시
    if not st.session_state['test_completed'] and st.session_state['current_question'] < total_questions:
        current_q = questions[st.session_state['current_question']]

        # 질문 카드
        st.markdown(f"""
        <div class="question-card">
            <h3>📖 {current_q['section']}</h3>
            <h2>{current_q['question']}</h2>
        </div>
        """, unsafe_allow_html=True)

        # 선택지
        selected_option = None
        for i, option in enumerate(current_q['options']):
            if st.button(f"{'●' if i == st.session_state['answers'][st.session_state['current_question']] if st.session_state['current_question'] < len(st.session_state['answers']) else '○'} {option}",
                        key=f"option_{i}",
                        help=f"옵션 {i+1}"):
                selected_option = i

        # 선택 저장
        if selected_option is not None:
            if st.session_state['current_question'] < len(st.session_state['answers']):
                st.session_state['answers'][st.session_state['current_question']] = selected_option
            else:
                st.session_state['answers'].append(selected_option)

            # 다음 질문으로
            st.session_state['current_question'] += 1
            time.sleep(0.3)
            st.rerun()

        # 이전 질문 버튼
        if st.session_state['current_question'] > 0:
            if st.button("← 이전 문제"):
                st.session_state['current_question'] -= 1
                st.rerun()

    # 테스트 완료
    elif st.session_state['current_question'] >= total_questions and not st.session_state['test_completed']:
        # 빈 답변 확인
        unanswered = total_questions - len(st.session_state['answers'])
        if unanswered > 0:
            st.warning(f"아직 답하지 않은 문제가 {unanswered}개 있습니다.")
            if st.button("테스트 완료", type="primary"):
                st.session_state['test_completed'] = True
                st.rerun()
        else:
            if st.button("테스트 완료", type="primary"):
                st.session_state['test_completed'] = True
                st.rerun()

    # 결과 표시
    if st.session_state['test_completed']:
        score_data = calculate_score(st.session_state['answers'], questions)

        # 결과 저장
        saved_file = save_results(level, score_data)

        # 결과 화면
        st.success("🎉 테스트 완료!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="question-card">
                <h2>📊 최종 점수</h2>
                <h1 style="font-size: 4rem; color: {'#10B981' if score_data['passed'] else '#EF4444'};">
                    {score_data['score']}점
                </h1>
                <p>{score_data['correct']} / {score_data['total']} 정답</p>
                <p style="font-size: 1.5rem;">
                    {'✅ 합격!' if score_data['passed'] else '❌ 불합격'}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="question-card">
                <h3>📈 섹션별 결과</h3>
            </div>
            """, unsafe_allow_html=True)

            for section, result in score_data['section_results'].items():
                percentage = (result['correct'] / result['total']) * 100
                st.write(f"**{section}**: {result['correct']}/{result['total']} ({percentage:.0f}%)")

        # 소요 시간
        if st.session_state['start_time']:
            time_spent = time.time() - st.session_state['start_time']
            minutes = int(time_spent // 60)
            seconds = int(time_spent % 60)
            st.info(f"소요 시간: {minutes}분 {seconds}초")

        # 피드백
        if score_data['passed']:
            st.markdown("""
            <div class="success-message">
                <h3>🎊 축하합니다!</h3>
                <p>테스트에 합격하셨습니다. 다음 레벨에 도전해보세요!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-message">
                <h3>💪 응원합니다!</h3>
                <p>아쉽게 불합격하셨지만, 포기하지 마세요! 더 많은 연습으로 발전할 수 있습니다.</p>
            </div>
            """, unsafe_allow_html=True)

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
            if st.button("📊 상세 결과"):
                st.info("상세 결과 페이지 준비 중...")

if __name__ == "__main__":
    main()