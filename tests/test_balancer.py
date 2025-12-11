
import sys
import os
import unittest
from collections import Counter

# Add parent directory to path to allow importing from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.question_balancer import balance_and_shuffle_quiz

class TestQuestionBalancer(unittest.TestCase):
    def test_balancing_logic(self):
        # Create a mock list of questions with all correct answers at index 0 (highly biased)
        questions = []
        for i in range(20):
            questions.append({
                'id': i,
                'question': f'Question {i}',
                'options': ['Correct', 'Wrong A', 'Wrong B', 'Wrong C'],
                'correct': 0, 
                'section': 'General'
            })
            
        # Run the balancer
        result = balance_and_shuffle_quiz(questions)
        balanced_questions = result['questions']
        stats = result['stats']
        
        # Check if the result is balanced
        # With 20 questions and 4 options, each option should be correct exactly 5 times
        expected_count = 20 // 4
        for i in range(4):
            # implementation returns 1-based stats keys
            self.assertEqual(stats[i+1], expected_count, f"Option {i+1} count should be {expected_count}")
            
        # Verify the content is correct (options are shuffled but logic holds)
        for q in balanced_questions:
            original_correct_text = 'Correct'
            new_correct_index = q['correct']
            self.assertEqual(q['options'][new_correct_index], original_correct_text, 
                             f"Question {q['id']}: Correct answer should be '{original_correct_text}' at index {new_correct_index}")

    def test_smaller_dataset(self):
        # Test with a number of questions not divisible by 4 (e.g., 5 questions)
        questions = []
        for i in range(5):
            questions.append({
                'id': i,
                'question': f'Question {i}',
                'options': ['Correct', 'Wrong A', 'Wrong B', 'Wrong C'],
                'correct': 0,
                'section': 'General'
            })
            
        result = balance_and_shuffle_quiz(questions)
        stats = result['stats']
        
        # With 5 questions: 1, 1, 1, 1 plus one extra. 
        # So counts should be either 1 or 2, and the difference between max and min count should be at most 1.
        counts = list(stats.values())
        self.assertTrue(max(counts) - min(counts) <= 1, "Distribution should be as balanced as possible")

if __name__ == '__main__':
    unittest.main()
