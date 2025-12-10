"""
CEFR 레벨 분석 및 학습 상담 리포트 생성 유틸리티
"""

from typing import Dict, List, Any
import json
from datetime import datetime

class CEFRAnalyzer:
    def __init__(self):
        self.cefr_descriptions = {
            'Pre-A1': {
                'name': 'Beginner (Pre-A1)',
                'description': '영어를 처음 배우는 단계로, 기본적인 인사와 자기소개가 가능합니다.',
                'abilities': [
                    '간단한 인사와 소개 (Hello, Goodbye, My name is...)',
                    '기본 색깔, 숫자, 물건 이름 인지',
                    '간단한 질문 이해 (What is your name?)',
                    '기본 명령어 이해 (Sit down, Stand up)'
                ],
                'weaknesses': [
                    '문장 구조에 대한 이해 부족',
                    '어휘력이 매우 제한적',
                    '발음에 어려움',
                    '문법 규칙 인지 부족'
                ],
                'curriculum': {
                    'duration': '3-6개월',
                    'focus': [
                        '기본 발음 (phonics)',
                        '핵심 어휘 500개 학습',
                        '기본 문장 구조 (S-V-O)',
                        '일상생활 표현 (일기예보, 날씨 등)',
                        '간단한 질문과 답변 연습'
                    ],
                    'materials': [
                        '파닉스 교재',
                        '그림 카드',
                        '간단한 동화책',
                        '영어 노래와 챈트'
                    ],
                    'daily_practice': [
                        '15분 영어 노래 듣기',
                        '10분 단어 암기',
                        '5분 영어로 자기소개 연습'
                    ]
                }
            },
            'A1': {
                'name': 'Elementary (A1)',
                'description': '일상생활에서 친숙한 상황에 대한 기본적인 소통이 가능합니다.',
                'abilities': [
                    '개인정보, 가족, 쇼핑, 지역 등에 대한 질문과 답변',
                    '간단한 지시문 이해',
                    '익숙한 상황에서의 간단한 대화',
                    '간단한 글자 읽기와 쓰기'
                ],
                'weaknesses': [
                    '복잡한 문장 구조 어려움',
                    '추상적인 개념 표현 어려움',
                    '자연스러운 대화 유지 부족',
                    '시제 변화에 혼동'
                ],
                'curriculum': {
                    'duration': '6-12개월',
                    'focus': [
                        '현재시제, 과거시제, 미래시제 완전히 마스터',
                        '어휘력 확장 (1000-1500개)',
                        '질문문과 부정문 완전히 이해',
                        '간단한 일상 대화 연습',
                        '기본적인 이메일 쓰기'
                    ],
                    'materials': [
                        'A1 레벨 교과서 (Headway, Interchange 등)',
                        '영어 동영상 (TED-Ed, BBC Learning)',
                        '간단한 영어 뉴스',
                        '영어 학습 앱 (Duolingo, Memrise)'
                    ],
                    'daily_practice': [
                        '20분 영어 뉴스 듣기',
                        '15분 어휘 학습',
                        '10분 영어 일기 쓰기',
                        '주 2회 영어 회화 스터디'
                    ]
                }
            },
            'A2': {
                'name': 'Pre-Intermediate (A2)',
                'description': '자주 마주치는 상황에 대해 직접적인 정보 교환이 가능하며, 익숙한 주제에 대한 간단한 설명이 가능합니다.',
                'abilities': [
                    '개인 경험, 환경, 직업 등에 대한 소통',
                    '간단한 현재, 과거, 미래 사건 설명',
                    '일상적인 용건 처리',
                    '필요한 정보 교환'
                ],
                'weaknesses': [
                    '복잡한 주제에 대한 깊은 토론 어려움',
                    '추상적인 표현 제한적',
                    '자연스러운 어휘 선택 부족',
                    '정확한 발음과 억양 필요'
                ],
                'curriculum': {
                    'duration': '9-15개월',
                    'focus': [
                        '완료시제 완전히 마스터',
                        '관계대명사와 조건문 학습',
                        '어휘력 2000개 이상 확장',
                        '전화 통화 연습',
                        '의견 표현과 이유 설명 연습'
                    ],
                    'materials': [
                        'A2 레벨 교재',
                        'TED 영상 (초급)',
                        '영어 드라마 (자막 포함)',
                        '영어 라디오 프로그램',
                        '영어 신문 기사 (간단한)'
                    ],
                    'daily_practice': [
                        '30분 영어 콘텐츠 시청',
                        '20분 영어 글 읽기',
                        '15분 영어로 생각하기',
                        '주 3회 영어 회화'
                    ]
                }
            },
            'B1': {
                'name': 'Intermediate (B1)',
                'description': '영어권 지역에서 여행이 가능하며, 경험, 사건, 꿈, 희망 등에 대한 설명과 의견, 계획에 대한 이유를 제시할 수 있습니다.',
                'abilities': [
                    '익숙하지 않은 상황에서의 대화',
                    '관심 있는 주제에 대한 토론',
                    '다양한 상황에서의 의사소통',
                    '경험과 생각의 주장 및 설명'
                ],
                'weaknesses': [
                    '전문 분야 용어 부족',
                    '미묘한 뉘앙스 표현 어려움',
                    '완벽한 문법准确性',
                    '문화적 배경 이해 부족'
                ],
                'curriculum': {
                    'duration': '12-18개월',
                    'focus': [
                        '가정법과 고급 문법 구문',
                        '어휘력 3000개 이상 확장',
                        '발표와 토론 기술',
                        '학술적 글쓰기 기초',
                        '문화적 이해와 관용 표현'
                    ],
                    'materials': [
                        'B1 레벨 전문 교재',
                        'TED 강연 (중급)',
                        '영문 소설 (초급)',
                        '전문 분야 기사',
                        '영어 토론 그룹'
                    ],
                    'daily_practice': [
                        '45분 영어 콘텐츠 소비',
                        '30분 영어 글쓰기',
                        '20분 영어로 일기 쓰기',
                        '일 1회 영어만 사용 시간'
                    ]
                }
            },
            'B2': {
                'name': 'Upper-Intermediate (B2)',
                'description': '원어민과 자연스럽고 상호적인 대화가 가능하며, 복잡한 주제에 대한 명확한 의견 제시와 장단점 분석이 가능합니다.',
                'abilities': [
                    '다양한 주제에 대한 유창한 의사소통',
                    '자신의 전문 분야에서의 설명과 논증',
                    '문학, 학술 등 복잡한 텍스트 이해',
                    '자연스럽고 효과적인 소통'
                ],
                'weaknesses': [
                    '전문 분야에서의 완벽한 유창성',
                    '가장 미묘한 문화적 뉘앙스',
                    '학술적 글쓰기의 완벽함',
                    '발음의 완벽한 원어민 수준'
                ],
                'curriculum': {
                    'duration': '18-24개월',
                    'focus': [
                        '고급 어휘와 관용 표현',
                        '학술적 글쓰기 완성',
                        '전문 분역 통역 기술',
                        '문화적 깊이 이해',
                        '원어민 수준의 발음'
                    ],
                    'materials': [
                        '고급 영어 교재',
                        '학술 논문과 저널',
                        '원서 소설',
                        'CNN, BBC 등 전문 뉴스',
                        '전문 컨퍼런스 참여'
                    ],
                    'daily_practice': [
                        '60분 이상 영어 콘텐츠',
                        '30분 학술적 글쓰기',
                        '영어로 생각하는 시간 늘리기',
                        '원어민과 정기적인 대화'
                    ]
                }
            }
        }

        self.section_descriptions = {
            'Vocabulary': {
                'description': '어휘력은 영어 학습의 기초입니다.',
                'importance': '어휘가 많을수록 더 정확하고 풍부한 표현이 가능합니다.',
                'improvement_tips': [
                    '문맥 속에서 단어 학습',
                    '동의어와 반의어 함께 암기',
                    '어원을 통한 단어 이해',
                    '일상에서 새로운 단어 사용하기'
                ]
            },
            'Grammar': {
                'description': '문법은 정확한 의사소통의 규칙입니다.',
                'importance': '올바른 문법은 오해를 줄이고 전문성을 보여줍니다.',
                'improvement_tips': [
                    '문장 구조 분석 연습',
                    '다양한 문장 패턴 학습',
                    '오답노트 작성',
                    '원어민의 문장 모방하기'
                ]
            },
            'Reading': {
                'description': '읽기는 이해력을 측정하는 중요한 기준입니다.',
                'importance': '다양한 주제의 글을 읽으며 배경지식을 넓힐 수 있습니다.',
                'improvement_tips': [
                    '다양한 장르의 글 읽기',
                    '속독 훈련',
                    '키워드 찾기 연습',
                    '요약하기 연습'
                ]
            },
            'Listening': {
                'description': '듣기는 실제 소통 능력을 나타냅니다.',
                'importance': '다양한 억양과 속도에 적응해야 실제 대화가 가능합니다.',
                'improvement_tips': [
                    '다양한 영어 콘텐츠 시청',
                    '딕테이션 연습',
                    '백그라운드 노이즈 환경 연습',
                    '메모하며 듣기 연습'
                ]
            },
            'Writing': {
                'description': '쓰기는 생각을 논리적으로 표현하는 능력입니다.',
                'importance': '글쓰기를 통해 생각을 정리하고 정확한 표현을 배울 수 있습니다.',
                'improvement_tips': [
                    '매일 영어 일기 쓰기',
                    '다양한 문장 길이 연습',
                    '논리적 구조 따르기',
                    '수정과 피드백 받기'
                ]
            }
        }

    def analyze_test_results(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        테스트 결과를 분석하여 상담용 데이터 생성
        """
        level = test_results.get('level', 'A1')
        score = test_results.get('score', 0)
        section_results = test_results.get('sectionResults', {})

        # 기본 분석
        analysis = {
            'student_info': test_results.get('studentInfo', {}),
            'test_level': level,
            'score': score,
            'test_date': test_results.get('submittedAt', ''),
            'section_analysis': {},
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'current_cefr_level': self._determine_cefr_level(level, score),
            'next_level_goal': self._get_next_level_goal(level, score),
            'learning_curriculum': None
        }

        # 섹션별 분석
        for section, result in section_results.items():
            percentage = (result.get('correct', 0) / result.get('total', 1)) * 100
            analysis['section_analysis'][section] = {
                'percentage': round(percentage),
                'correct': result.get('correct', 0),
                'total': result.get('total', 1),
                'strength_level': self._evaluate_strength_level(percentage)
            }

        # 강점과 약점 분석
        analysis['strengths'] = self._identify_strengths(analysis['section_analysis'])
        analysis['weaknesses'] = self._identify_weaknesses(analysis['section_analysis'])

        # 학습 커리큘럼 추천
        analysis['learning_curriculum'] = self._generate_learning_curriculum(
            analysis['current_cefr_level'],
            analysis['section_analysis']
        )

        return analysis

    def _determine_cefr_level(self, test_level: str, score: int) -> str:
        """
        실제 CEFR 레벨 결정
        """
        if score >= 85:
            # 테스트 레벨보다 한 단계 높은 실력
            level_order = ['Pre-A1', 'A1', 'A2', 'B1', 'B2']
            current_index = level_order.index(test_level)
            if current_index < len(level_order) - 1:
                return level_order[current_index + 1]
        elif score >= 60:
            return test_level
        else:
            # 테스트 레벨보다 한 단계 낮은 실력
            level_order = ['Pre-A1', 'A1', 'A2', 'B1', 'B2']
            current_index = level_order.index(test_level)
            if current_index > 0:
                return level_order[current_index - 1]

        return test_level

    def _get_next_level_goal(self, current_level: str, score: int) -> Dict[str, Any]:
        """
        다음 레벨 목표 설정
        """
        level_order = ['Pre-A1', 'A1', 'A2', 'B1', 'B2']
        current_index = level_order.index(current_level)

        if score >= 85 and current_index < len(level_order) - 1:
            # 현재 레벨 마스터, 다음 레벨 목표
            next_level = level_order[current_index + 1]
            target_score = 70  # 다음 레벨 합격 점수
        elif score >= 70:
            # 현재 레벨 유지 및 완벽함 목표
            next_level = current_level
            target_score = 90
        else:
            # 현재 레벨 합격 목표
            next_level = current_level
            target_score = 70

        return {
            'level': next_level,
            'target_score': target_score,
            'estimated_duration': self._estimate_duration(current_level, score, target_score)
        }

    def _evaluate_strength_level(self, percentage: float) -> str:
        """
        실력 수준 평가
        """
        if percentage >= 85:
            return "excellent"
        elif percentage >= 70:
            return "good"
        elif percentage >= 50:
            return "average"
        else:
            return "needs_improvement"

    def _identify_strengths(self, section_analysis: Dict) -> List[str]:
        """
        강점 식별
        """
        strengths = []
        for section, data in section_analysis.items():
            if data['strength_level'] in ['excellent', 'good']:
                section_desc = self.section_descriptions.get(section, {})
                strengths.append(f"{section}: {section_desc.get('description', '')}")

        return strengths

    def _identify_weaknesses(self, section_analysis: Dict) -> List[str]:
        """
        약점 식별
        """
        weaknesses = []
        for section, data in section_analysis.items():
            if data['strength_level'] in ['average', 'needs_improvement']:
                weaknesses.append(f"{section}: 개선이 필요합니다. ({data['percentage']}%)")

        return weaknesses

    def _generate_learning_curriculum(self, cefr_level: str, section_analysis: Dict) -> Dict[str, Any]:
        """
        학습 커리큘럼 생성
        """
        base_curriculum = self.cefr_descriptions.get(cefr_level, {}).get('curriculum', {})

        # 섹션별 맞춤 학습 계획 추가
        section_focus = []
        for section, data in section_analysis.items():
            if data['strength_level'] in ['average', 'needs_improvement']:
                section_focus.append(f"{section} 집중 훈련 ({data['percentage']}% → 80%+ 목표)")

        return {
            **base_curriculum,
            'section_focus': section_focus,
            'priority_areas': self._get_priority_areas(section_analysis)
        }

    def _estimate_duration(self, current_level: str, current_score: int, target_score: int) -> str:
        """
        목표 달성 예상 기간
        """
        score_gap = target_score - current_score
        if score_gap <= 10:
            return "1-2개월"
        elif score_gap <= 20:
            return "3-4개월"
        elif score_gap <= 30:
            return "5-6개월"
        else:
            return "6개월 이상"

    def _get_priority_areas(self, section_analysis: Dict) -> List[str]:
        """
        우선 학습 영역
        """
        priorities = []
        for section, data in section_analysis.items():
            if data['strength_level'] == 'needs_improvement':
                priorities.append(f"🔥 {section}: 가장 먼저 개선 필요")
            elif data['strength_level'] == 'average':
                priorities.append(f"⚡ {section}: 집중 강화 필요")

        return priorities

    def generate_counseling_report(self, analysis: Dict[str, Any]) -> str:
        """
        상담용 리포트 생성
        """
        student_name = analysis.get('student_info', {}).get('name', '학생')
        current_level = analysis['current_cefr_level']
        level_info = self.cefr_descriptions.get(current_level, {})

        report = f"""
# 🎓 CEFR 영어 능력 진단 및 학습 상담 리포트

## 👤 학생 정보
- **이름**: {student_name}
- **테스트 일자**: {analysis.get('test_date', '')[:10]}
- **응시 레벨**: {analysis.get('test_level', '')}
- **점수**: {analysis.get('score', 0)}점
- **진단 CEFR 레벨**: {level_info.get('name', current_level)}

## 📊 섹션별 상세 분석

"""

        # 섹션별 분석 추가
        for section, data in analysis.get('section_analysis', {}).items():
            report += f"""
### {section}
- **정답률**: {data['correct']}/{data['total']} ({data['percentage']}%)
- **실력 수준**: {self._get_strength_text(data['strength_level'])}
- **상태**: {self._get_status_emoji(data['strength_level'])}
"""

        report += f"""

## 💪 강점 분석

학생의 주요 강점은 다음과 같습니다:

"""

        for strength in analysis.get('strengths', []):
            report += f"- ✅ {strength}\n"

        report += f"""

## 🎯 개선 영역

집중적으로 개선이 필요한 영역입니다:

"""

        for weakness in analysis.get('weaknesses', []):
            report += f"- ⚠️ {weakness}\n"

        report += f"""

## 📚 CEFR 레벨 {current_level} 상세 설명

**레벨 정의**: {level_info.get('description', '')}

**현재 레벨에서 가능한 능력**:
"""

        for ability in level_info.get('abilities', []):
            report += f"- {ability}\n"

        report += f"""

**개선이 필요한 부분**:
"""

        for weakness in level_info.get('weaknesses', []):
            report += f"- {weakness}\n"

        curriculum = analysis.get('learning_curriculum', {})

        report += f"""

## 🎯 맞춤형 학습 커리큘럼

**예상 학습 기간**: {curriculum.get('duration', '3-6개월')}

### 학습 우선 순위
"""

        for priority in curriculum.get('priority_areas', []):
            report += f"- {priority}\n"

        report += f"""

### 집중 학습 영역
"""

        for focus in curriculum.get('section_focus', []):
            report += f"- {focus}\n"

        report += f"""

### 주요 학습 목표
"""

        for focus in curriculum.get('focus', []):
            report += f"- {focus}\n"

        report += f"""

### 추천 학습 자료
"""

        for material in curriculum.get('materials', []):
            report += f"- {material}\n"

        report += f"""

### 일일 학습 계획
"""

        for practice in curriculum.get('daily_practice', []):
            report += f"- {practice}\n"

        next_goal = analysis.get('next_level_goal', {})

        report += f"""

## 🚀 다음 단계 목표

**목표 레벨**: {next_goal.get('level', current_level)}
**목표 점수**: {next_goal.get('target_score', 70)}점
**예상 기간**: {next_goal.get('estimated_duration', '3-6개월')}

## 📋 상담사를 위한 노트

- 학생은 현재 {current_level} 레벨에 있습니다.
- 전체적인 학습 동기 부여가 중요합니다.
- 정기적인 진단 테스트로 진전 상황을 확인하세요.
- 약점 영역에 대한 집중적인 보완 학습이 필요합니다.
- 성공 경험을 통해 자신감을 높여주세요.

---
*리포트 생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}*
*CEFR Teacher Dashboard 상담 시스템*
        """

        return report.strip()

    def _get_strength_text(self, level: str) -> str:
        """실력 수준 텍스트"""
        texts = {
            'excellent': '매우 우수',
            'good': '우수',
            'average': '보통',
            'needs_improvement': '개선 필요'
        }
        return texts.get(level, '알 수 없음')

    def _get_status_emoji(self, level: str) -> str:
        """상태 이모지"""
        emojis = {
            'excellent': '🌟',
            'good': '✅',
            'average': '📊',
            'needs_improvement': '📈'
        }
        return emojis.get(level, '❓')