import json
from jinja2 import Template
from datetime import datetime

# 1. Mock Data matching the new schema
mock_data = {
    "words": [
        {
            "word": "Tram",
            "pronunciation": "트램",
            "meaning": "노면 전차",
            "example_en": "I'll take the tram to the city.",
            "example_ko": "나는 시내로 트램을 타고 갈 거야.",
            "tip": "멜버른의 상징적인 대중교통입니다."
        },
        {
            "word": "Queue",
            "pronunciation": "큐",
            "meaning": "줄, 대기열",
            "example_en": "There's a long queue for coffee.",
            "example_ko": "커피 줄이 기네요.",
            "tip": "영국/호주식 표현으로 'line' 대신 씁니다."
        }
    ],
    "survival_sentences": [
        {
            "situation": "카페 주문",
            "en": "Could I get a flat white, please?",
            "ko": "플랫 화이트 한 잔 주세요.",
            "tip": "정중한 요청 표현입니다."
        }
    ],
    "opic_sentences": [
        {
            "situation": "자기소개",
            "en": "I'm particularly drawn to Melbourne's vibrant arts scene.",
            "ko": "저는 멜버른의 활기찬 예술 씬에 매력을 느낍니다.",
            "key_points": [
                {"phrase": "be drawn to", "desc": "~에 끌리다"},
                {"phrase": "vibrant", "desc": "활기찬"}
            ]
        }
    ],
    "complex_sentence": {
        "en": "If you're planning to explore Melbourne thoroughly...",
        "ko": "멜버른을 철저히 탐험할 계획이라면...",
        "analysis": [
            {
                "part": "If you're planning",
                "grammar": "조건절",
                "meaning": "계획이라면",
                "tip": "가정법 현재"
            }
        ]
    }
}

# 2. Render Template
def verify_template():
    try:
        with open("templates/email_template.html", "r", encoding="utf-8") as f:
            template_str = f.read()
        
        template = Template(template_str)
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        html_content = template.render(subject="[TEST] Design Verification", date=today_str, content=mock_data)
        
        output_file = "test_output.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Success! Generated {output_file}")
        
    except Exception as e:
        print(f"Error rendering template: {e}")

if __name__ == "__main__":
    verify_template()
