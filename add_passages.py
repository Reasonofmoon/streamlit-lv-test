import json

def add_passages_to_json():
    """extracted_questions.json에 지문 추가"""
    
    with open('extracted_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 지문 정의 (레벨별)
    passages = {
        "PRE-A1": {
            1: """Hi Tom,

I am at the library. Please come at 3 o'clock.
Bring your English book.
See you soon!

Mia""",
            2: """This is my room. I have a blue bed and a brown desk. 
My favorite color is blue. I like my room.""",
            3: """My Family

Hello! I am Tom. I have a big family.
I have one brother and one sister.
We live in Seoul."""
        },
        "A1": {
            1: """Dear Alice,

How are you? I am fine. I am writing this letter to tell you about my school.

My school is big and beautiful. It has many classrooms, a library, and a playground. I like reading books in the library.

What about your school? Please write soon.

Best,
Emma""",
            2: """The Weather

Today is Sunday. The weather is very nice. The sun is shining and the sky is blue. 

Tom and his friends are playing in the park. They are happy and having fun.

Tomorrow will be rainy. They should bring umbrellas."""
        },
        "A2": {
            1: """The Park Experience

Last Sunday, Tom went to the park with his friends. The park was beautiful with green trees and colorful flowers. They played soccer and ate sandwiches on the grass.

In the afternoon, they went to the small lake and saw many ducks. Tom's friend Sarah took some photos. It was a wonderful day, and everyone went home feeling happy and tired.""",
            2: """School Life

My school starts at 8:30 AM every morning. I have six classes each day. My favorite subject is English because I like learning new words and speaking with foreigners.

After school, I usually go to the library to study. Sometimes I play basketball with my classmates in the gym. I think school is important for my future."""
        },
        "B1": {
            1: """The Impact of Technology on Education

Technology has changed education significantly in recent years. Students can now access information instantly through the internet and use various educational apps to enhance their learning experience.

However, some experts argue that excessive technology use may reduce face-to-face interaction skills. Finding the right balance between traditional teaching methods and digital tools is crucial for modern education.""",
            2: """Environmental Protection

Climate change is one of the most serious problems facing our planet today. Rising temperatures, melting ice caps, and extreme weather events are becoming more common worldwide.

Individuals can help by reducing waste, recycling, and using public transportation. Small changes in daily habits can make a significant difference in protecting our environment for future generations."""
        },
        "B2": {
            1: """The Evolution of Artificial Intelligence

Artificial Intelligence (AI) has evolved dramatically since its inception in the 1950s. From simple rule-based systems to complex neural networks, AI now powers countless applications in healthcare, finance, and transportation.

While AI offers numerous benefits, including increased efficiency and data analysis capabilities, it also raises important ethical questions about privacy, job displacement, and decision-making transparency. Society must carefully navigate these challenges as AI continues to advance.""",
            2: """Global Economic Challenges

The global economy faces unprecedented challenges in the post-pandemic era. Supply chain disruptions, inflation concerns, and geopolitical tensions have created a complex economic landscape.

Policymakers must balance short-term recovery measures with long-term structural reforms. Central banks are adjusting monetary policies to stabilize markets while governments implement fiscal strategies to support sustainable growth and address inequality."""
        }
    }
    
    # 각 레벨별로 Reading 섹션 문항에 지문 추가
    for level, questions in data.items():
        if level in passages:
            passage_pool = passages[level]
            reading_questions = [q for q in questions if q.get('section') == 'Reading']
            
            # 지문 번호 할당 (순서대로)
            passage_idx = 1
            for q in questions:
                if q.get('section') == 'Reading':
                    # 지문 번호를 순환 할당
                    passage_num = (q.get('id', 1) - 1) % len(passage_pool) + 1
                    if passage_num in passage_pool:
                        q['passage'] = passage_pool[passage_num]
                        print(f"✓ Added passage {passage_num} to {level} Q{q.get('id')}")
    
    # 수정된 데이터 저장
    with open('extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Passages added to extracted_questions.json")

if __name__ == "__main__":
    add_passages_to_json()
