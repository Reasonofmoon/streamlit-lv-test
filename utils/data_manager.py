import json
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.submissions_dir = os.path.join(data_dir, "submissions")
        self.questions_dir = os.path.join(data_dir, "questions")

        # 디렉토리 생성
        os.makedirs(self.submissions_dir, exist_ok=True)
        os.makedirs(self.questions_dir, exist_ok=True)

    def save_submission(self, submission_data: Dict[str, Any]) -> str:
        """
        테스트 제출 데이터 저장
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        student_name = submission_data.get('studentInfo', {}).get('name', 'unknown')
        level = submission_data.get('level', 'unknown')

        filename = f"{student_name}_{level}_{timestamp}.json"
        filepath = os.path.join(self.submissions_dir, filename)

        # 메타데이터 추가
        submission_data['savedAt'] = datetime.now().isoformat()
        submission_data['filename'] = filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(submission_data, f, ensure_ascii=False, indent=2)

        return filepath

    def load_submissions(self) -> List[Dict[str, Any]]:
        """
        모든 제출 데이터 로드
        """
        submissions = []

        for file in os.listdir(self.submissions_dir):
            if file.endswith('.json'):
                try:
                    filepath = os.path.join(self.submissions_dir, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        submissions.append(data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")

        return submissions

    def filter_submissions(self,
                          submissions: List[Dict[str, Any]],
                          level: Optional[str] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          student_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        제출 데이터 필터링
        """
        filtered = submissions.copy()

        if level:
            filtered = [s for s in filtered if s.get('level') == level]

        if start_date:
            filtered = [
                s for s in filtered
                if datetime.fromisoformat(s.get('submittedAt', '')) >= start_date
            ]

        if end_date:
            filtered = [
                s for s in filtered
                if datetime.fromisoformat(s.get('submittedAt', '')) <= end_date
            ]

        if student_name:
            filtered = [
                s for s in filtered
                if s.get('studentInfo', {}).get('name') == student_name
            ]

        return filtered

    def get_student_submissions(self, student_name: str) -> List[Dict[str, Any]]:
        """
        특정 학생의 모든 제출 데이터 가져오기
        """
        all_submissions = self.load_submissions()
        return self.filter_submissions(all_submissions, student_name=student_name)

    def get_submissions_by_level(self, level: str) -> List[Dict[str, Any]]:
        """
        특정 레벨의 모든 제출 데이터 가져오기
        """
        all_submissions = self.load_submissions()
        return self.filter_submissions(all_submissions, level=level)

    def export_to_csv(self, submissions: List[Dict[str, Any]], filename: str) -> str:
        """
        제출 데이터를 CSV로 내보내기
        """
        data = []
        for s in submissions:
            student_info = s.get('studentInfo', {})
            row = {
                '이름': student_info.get('name', ''),
                '학교': student_info.get('school', ''),
                '학년': student_info.get('grade', ''),
                '반': student_info.get('class', ''),
                '레벨': s.get('level', ''),
                '점수': s.get('score', 0),
                '합격여부': '합격' if s.get('passed', False) else '불합격',
                '제출시간': s.get('submittedAt', ''),
                '정답수': s.get('correct', 0),
                '전체문제수': s.get('total', 0)
            }

            # 섹션별 결과 추가
            section_results = s.get('sectionResults', {})
            for section, result in section_results.items():
                row[f'{section}_점수'] = round((result.get('correct', 0) / result.get('total', 1)) * 100)

            data.append(row)

        df = pd.DataFrame(data)
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')

        return filepath

    def export_to_excel(self, submissions: List[Dict[str, Any]], filename: str) -> str:
        """
        제출 데이터를 Excel로 내보내기
        """
        # CSV 데이터 생성
        csv_data = self.export_to_csv(submissions, 'temp_export.csv')
        df = pd.read_csv(csv_data)

        # Excel 파일 생성
        filepath = os.path.join(self.data_dir, filename)

        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            # 메인 데이터 시트
            df.to_excel(writer, sheet_name='전체 결과', index=False)

            # 레벨별 시트
            levels = set(s.get('level', '') for s in submissions)
            for level in levels:
                if level:
                    level_data = [s for s in submissions if s.get('level') == level]
                    level_df = pd.DataFrame(self._prepare_excel_data(level_data))
                    level_df.to_excel(writer, sheet_name=f'{level} 레벨', index=False)

            # 통계 요약 시트
            stats_df = self._create_stats_dataframe(submissions)
            stats_df.to_excel(writer, sheet_name='통계 요약', index=False)

        # 임시 파일 삭제
        if os.path.exists('temp_export.csv'):
            os.remove('temp_export.csv')

        return filepath

    def _prepare_excel_data(self, submissions: List[Dict[str, Any]]) -> List[Dict]:
        """
        Excel 내보내기를 위한 데이터 준비
        """
        data = []
        for s in submissions:
            student_info = s.get('studentInfo', {})
            row = {
                'Name': student_info.get('name', ''),
                'School': student_info.get('school', ''),
                'Grade': student_info.get('grade', ''),
                'Class': student_info.get('class', ''),
                'Level': s.get('level', ''),
                'Score': s.get('score', 0),
                'Passed': 'Yes' if s.get('passed', False) else 'No',
                'Submission Date': s.get('submittedAt', ''),
                'Correct': s.get('correct', 0),
                'Total': s.get('total', 0)
            }
            data.append(row)
        return data

    def _create_stats_dataframe(self, submissions: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        통계 요약 데이터프레임 생성
        """
        if not submissions:
            return pd.DataFrame()

        # 기본 통계
        total_count = len(submissions)
        avg_score = round(sum(s.get('score', 0) for s in submissions) / total_count)
        pass_count = sum(1 for s in submissions if s.get('passed', False))
        pass_rate = round((pass_count / total_count) * 100)

        # 레벨별 통계
        level_stats = {}
        for s in submissions:
            level = s.get('level', 'Unknown')
            if level not in level_stats:
                level_stats[level] = {'count': 0, 'total_score': 0, 'passed': 0}
            level_stats[level]['count'] += 1
            level_stats[level]['total_score'] += s.get('score', 0)
            if s.get('passed', False):
                level_stats[level]['passed'] += 1

        # 데이터프레임 생성
        stats_data = []

        # 전체 통계
        stats_data.append({
            'Category': '전체',
            'Count': total_count,
            'Average Score': avg_score,
            'Pass Rate': f"{pass_rate}%",
            'Passed': pass_count,
            'Failed': total_count - pass_count
        })

        # 레벨별 통계
        for level, stats in level_stats.items():
            avg_level_score = round(stats['total_score'] / stats['count'])
            level_pass_rate = round((stats['passed'] / stats['count']) * 100)

            stats_data.append({
                'Category': f"{level} Level",
                'Count': stats['count'],
                'Average Score': avg_level_score,
                'Pass Rate': f"{level_pass_rate}%",
                'Passed': stats['passed'],
                'Failed': stats['count'] - stats['passed']
            })

        return pd.DataFrame(stats_data)

    def get_statistics(self, submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        제출 데이터에 대한 통계 정보 계산
        """
        if not submissions:
            return {}

        total = len(submissions)
        scores = [s.get('score', 0) for s in submissions]

        stats = {
            'total_students': total,
            'average_score': round(sum(scores) / total),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'pass_count': sum(1 for s in submissions if s.get('passed', False)),
            'fail_count': sum(1 for s in submissions if not s.get('passed', False)),
            'pass_rate': round((sum(1 for s in submissions if s.get('passed', False)) / total) * 100),
            'level_distribution': {},
            'score_ranges': {
                '90-100': 0, '80-89': 0, '70-79': 0,
                '60-69': 0, '50-59': 0, '0-49': 0
            }
        }

        # 레벨별 분포
        for s in submissions:
            level = s.get('level', 'Unknown')
            stats['level_distribution'][level] = stats['level_distribution'].get(level, 0) + 1

        # 점수 구간별 분포
        for score in scores:
            if score >= 90: stats['score_ranges']['90-100'] += 1
            elif score >= 80: stats['score_ranges']['80-89'] += 1
            elif score >= 70: stats['score_ranges']['70-79'] += 1
            elif score >= 60: stats['score_ranges']['60-69'] += 1
            elif score >= 50: stats['score_ranges']['50-59'] += 1
            else: stats['score_ranges']['0-49'] += 1

        return stats

    def cleanup_old_files(self, days: int = 30):
        """
        오래된 파일 정리
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for file in os.listdir(self.submissions_dir):
            if file.endswith('.json'):
                filepath = os.path.join(self.submissions_dir, file)
                if os.path.getctime(filepath) < cutoff_date:
                    os.remove(filepath)
                    print(f"Removed old file: {file}")