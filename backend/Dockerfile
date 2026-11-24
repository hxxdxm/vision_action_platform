# Django(웹)와 Celery Worker가 같이 쓰는 이미지. compose.yaml에서 command만 다르게 실행합니다.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# opencv-python-headless는 libGL 등 시스템 패키지가 필요 없어 apt 설치 단계를 두지 않음

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN DJANGO_SECRET_KEY=build python manage.py collectstatic --noinput \
    && chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
# 작업자 2개 × 스레드 4개: IP Webcam 미리보기가 카메라 응답을 기다리는 동안에도 다른 요청(상태 조회·화면)을 처리
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "120"]
