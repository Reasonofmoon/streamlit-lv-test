
import json
import os

# Define the A2 questions that were hardcoded in pages/1_Student_Test.py
a2_questions = [
    {'id': 1, 'question': 'Read the passage and answer: The main idea of the text is about...', 'options': ['Travel', 'Education', 'Food', 'Sports'], 'correct': 1, 'section': 'Reading'},
    {'id': 2, 'question': 'According to the passage, the author believes that...', 'options': ['Learning is easy', 'Practice makes perfect', 'Teachers are not important', 'Students don\'t need help'], 'correct': 1, 'section': 'Reading'},
    {'id': 3, 'question': 'What does the word "challenge" mean in the context?', 'options': ['Problem', 'Solution', 'Reward', 'Game'], 'correct': 0, 'section': 'Reading'},
    {'id': 4, 'question': 'The tone of the passage can be described as...', 'options': ['Formal', 'Informal', 'Angry', 'Sad'], 'correct': 0, 'section': 'Reading'},
    {'id': 5, 'question': 'Where was the author born?', 'options': ['London', 'New York', 'Paris', 'Tokyo'], 'correct': 1, 'section': 'Reading'},
    {'id': 6, 'question': 'How many languages does the author speak?', 'options': ['One', 'Two', 'Three', 'Four'], 'correct': 2, 'section': 'Reading'},
    {'id': 7, 'question': 'What is the main character\'s profession?', 'options': ['Teacher', 'Doctor', 'Engineer', 'Artist'], 'correct': 2, 'section': 'Reading'},
    {'id': 8, 'question': 'When did the story take place?', 'options': ['Last year', 'This year', 'Next year', 'Five years ago'], 'correct': 2, 'section': 'Reading'},
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
    {'id': 21, 'question': 'A: "How are you?" B: "___"', 'options': ['I\'m fine, thank you', 'I\'m 25 years old', 'I\'m a teacher', 'I\'m from Korea'], 'correct': 0, 'section': 'Conversation'},
    {'id': 22, 'question': 'A: "What time is it?" B: "___"', 'options': ['It\'s 3 o\'clock', 'It\'s Monday', 'It\'s sunny', 'It\'s hot'], 'correct': 0, 'section': 'Conversation'},
    {'id': 23, 'question': 'A: "Where is the library?" B: "___"', 'options': ['It\'s over there', 'It\'s expensive', 'It\'s delicious', 'It\'s cold'], 'correct': 0, 'section': 'Conversation'},
    {'id': 24, 'question': 'A: "Can you help me?" B: "___"', 'options': ['Of course', 'No problem', 'I\'m busy', 'I don\'t know'], 'correct': 0, 'section': 'Conversation'},
    {'id': 25, 'question': 'A: "Thank you for your help." B: "___"', 'options': ['You\'re welcome', 'Thank you too', 'Goodbye', 'Hello'], 'correct': 0, 'section': 'Conversation'},
    {'id': 26, 'question': 'A: "See you tomorrow." B: "___"', 'options': ['See you later', 'Nice to meet you', 'How are you', 'What\'s your name'], 'correct': 0, 'section': 'Conversation'},
    {'id': 27, 'question': 'A: "What do you do for fun?" B: "___"', 'options': ['I like reading books', 'I\'m a doctor', 'I\'m 30 years old', 'I live in Seoul'], 'correct': 0, 'section': 'Conversation'},
    {'id': 28, 'question': 'A: "How was your weekend?" B: "___"', 'options': ['It was great', 'It\'s Monday', 'I\'m tired', 'I\'m hungry'], 'correct': 0, 'section': 'Conversation'},
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
    {'id': 39, 'question': 'Which sentence is correct?', 'options': ['I have visited Paris last year', 'I visited Paris last year', 'I visit Paris last year', 'I am visiting Paris last year'], 'correct': 1, 'section': 'Writing'},
    {'id': 40, 'question': 'Choose the best way to complete the sentence: "I enjoy ___ because..."', 'options': ['read books', 'reading books', 'to read books', 'read books'], 'correct': 1, 'section': 'Writing'}
]

# Format fields to match the rest of the JSON (HTML span, A) B) C) D) prefixes)
prefixes = ['A)', 'B)', 'C)', 'D)']
formatted_questions = []

for q in a2_questions:
    new_q = q.copy()
    # Wrap question text in span
    new_q['question'] = f'<span class="question-text">{q["question"]}</span>'
    
    # Add prefixes to options
    new_options = []
    for i, opt in enumerate(q['options']):
        new_options.append(f'{prefixes[i]}{opt}')
    new_q['options'] = new_options
    
    formatted_questions.append(new_q)

# Safe path handling
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'extracted_questions.json')

print(f"Reading from: {json_path}")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Original A2 count: {len(data.get('A2', []))}")
    
    data['A2'] = formatted_questions
    
    print(f"New A2 count: {len(data['A2'])}")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Migration successful.")
    
except Exception as e:
    print(f"Error during migration: {e}")
