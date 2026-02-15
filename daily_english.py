import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import google.generativeai as genai
from jinja2 import Template

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def load_prompt():
    """prompts 폴더의 텍스트 파일을 읽어서 날짜를 적용해 반환"""
    try:
        # 파일 읽기 (인코딩 utf-8 필수)
        with open("prompts/daily_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
            
        # 오늘 날짜 구하기
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 텍스트 파일 내의 {date} 부분을 오늘 날짜로 치환
        return template.replace("{date}", today_str), today_str
        
    except FileNotFoundError:
        print("Error: 프롬프트 파일을 찾을 수 없습니다.")
        return None, None

def generate_content(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        text_response = response.text
        
        # JSON 포맷팅 정리 (Markdown code block 제거)
        clean_text = text_response.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)
    except Exception as e:
        print(f"콘텐츠 생성/파싱 실패: {str(e)}")
        return None

def send_email(subject, data, today_str):
    try:
        # 1. Jinja2 템플릿 읽기
        with open("templates/email_template.html", "r", encoding="utf-8") as f:
            template_str = f.read()
        
        template = Template(template_str)
        
        # 2. 데이터 렌더링
        html_content = template.render(subject=subject, date=today_str, content=data)

        # 3. 이메일 구성
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        # HTML 형식으로 메일 본문 첨부
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # 4. 전송
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print("성공! 이메일을 확인하세요.")
        
    except Exception as e:
        print(f"이메일 전송 실패: {str(e)}")

if __name__ == "__main__":
    print("프롬프트 로딩 중...")
    prompt_text, today_str = load_prompt()
    
    if prompt_text:
        print("Gemini에게 영어 공부 콘텐츠 요청 중 (JSON)...")
        content_data = generate_content(prompt_text)
        
        if content_data:
            print("이메일 전송 중...")
            subject = f"[Gemini English] {today_str} 오늘의 영어 표현"
            send_email(subject, content_data, today_str)
        else:
            print("실패: 올바른 JSON 데이터를 생성하지 못했습니다.")
    else:
        print("실패: 프롬프트를 불러오지 못해 종료합니다.")