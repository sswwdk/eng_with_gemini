import os
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def load_prompt():
    """prompts 폴더의 텍스트 파일을 읽어서 날짜를 적용해 반환"""
    try:
        # 파일 읽기 (인코딩 utf-8 필수)
        with open("prompts/daily_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
            
        # 오늘 날짜 구하기
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 텍스트 파일 내의 {date} 부분을 오늘 날짜로 치환
        return template.format(date=today_str), today_str
        
    except FileNotFoundError:
        print("Error: 프롬프트 파일을 찾을 수 없습니다.")
        return None, None

def generate_content(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"콘텐츠 생성 실패: {str(e)}"

def send_email(subject, markdown_content):
    # 1. 마크다운을 HTML로 변환
    html_content = markdown.markdown(markdown_content, extensions=['tables'])

    # 2. 이메일 꾸미기 (CSS 스타일 적용)
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', Arial, sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #2980b9; margin-top: 20px; }}
            h3 {{ color: #16a085; }}
            strong {{ color: #c0392b; background-color: #f9e79f; padding: 0 4px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; color: #333; }}
            blockquote {{ border-left: 4px solid #3498db; margin: 0; padding-left: 15px; color: #555; background-color: #f9f9f9; padding: 10px; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    # 3. HTML 형식으로 메일 본문 첨부
    msg.attach(MIMEText(styled_html, 'html', 'utf-8'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    print("프롬프트 로딩 중...")
    prompt_text, today_str = load_prompt()
    
    if prompt_text:
        print("Gemini에게 영어 공부 콘텐츠 요청 중...")
        content = generate_content(prompt_text)
        
        print("이메일 전송 중...")
        subject = f"[Gemini English] {today_str}영어 공부 도착!"
        send_email(subject, content)
        print("성공! 이메일을 확인하세요.")
    else:
        print("실패: 프롬프트를 불러오지 못해 종료합니다.")