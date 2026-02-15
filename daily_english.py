import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import google.generativeai as genai

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 프롬프트 구성
today_str = datetime.now().strftime("%Y-%m-%d")
prompt = f"""
너는 멜버른에 거주하는 개발자를 위한 영어 튜터야.
오늘은 {today_str}이다.
'멜버른 생존 & OPIc 대비 영어 공부' 콘텐츠를 작성해줘.
형식은 마크다운으로 깔끔하게 정리해줘.

[포함할 내용]
1. 멜버른/호주 슬랭 또는 필수 단어 5개 (뜻, 예문 포함)
2. 실생활 생존 문장 2개 (주문, 길묻기 등 상황 부여)
3. OPIc 시험 대비 문장 2개 (자기소개, 묘사 등 고급 표현)
4. 문법적으로 복잡한 긴 문장 1개 (구문 분석 포함)
5. 영어 단어와 문장은 한글 뜻과 해석 팁을 꼭 포함할 것.

이전과 겹치지 않는 새로운 내용으로 부탁해.
"""

def generate_content():
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"콘텐츠 생성 실패: {str(e)}"

def send_email(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    print("Gemini에게 영어 공부 콘텐츠 요청 중...")
    content = generate_content()
    print("이메일 전송 중...")
    subject = f"[Gemini English] {today_str} 멜버른 영어 공부 도착!"
    send_email(subject, content)
    print("성공! 이메일을 확인하세요.")