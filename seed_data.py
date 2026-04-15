from datetime import datetime, date, timezone, timedelta
import random

from one import db, create_app
from one.models import (
    User, Video, Genre, Plan, Admin, Subscription,
    Support, SupportAnswer, WatchHistory, Payment, Notice,
    VideoLike, VideoWish, Review
)

# 1. Flask 앱 인스턴스 생성
app = create_app()


def seed_data():
    with app.app_context():
        # 0. 기존 데이터 초기화 (선택 사항)
        db.drop_all()
        db.create_all()

        # 1. 관리자 및 요금제 생성
        admin = Admin(
            admin_id="admin_01",
            admin_password="hashed_password_123",
            admin_name="운영팀장",
            admin_role="superadmin"
        )
        db.session.add(admin)

        premium_plan = Plan(plan_name="premium", price=14500)
        db.session.add(premium_plan)
        db.session.flush()  # ID 생성을 위해 flush

        # 2. 유저 생성 (signup_method default, kakao_id null)
        test_user = User(
            user_email="testuser@example.com",
            user_password="user_password_456",
            user_name="홍길동",
            user_phone="010-1234-5678",
            user_gender="M",
            signup_method="email",  # default 값 명시
            kakao_id=None  # null 설정
        )
        db.session.add(test_user)
        db.session.flush()

        # 3. 구독 정보 생성 (현재 활성화 상태)
        sub = Subscription(
            user_unique_id=test_user.user_unique_id,
            plan_id=premium_plan.plan_id,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=30),
            status='active'
        )
        db.session.add(sub)

        # 4. 영상 데이터 12개 생성
        videos = []
        for i in range(1, 13):
            video = Video(
                video_title=f"대작 영화 시리즈 {i}",
                video_director=f"감독 {i}",
                video_url=f"https://stream.example.com/v{i}",
                video_thumbnail=f"https://img.example.com/t{i}.jpg",
                admin_unique_id=admin.admin_unique_id
            )
            videos.append(video)
            db.session.add(video)

        db.session.flush()

        # 5. 유저 활동 데이터 (시청기록, 찜하기, 문의)
        for i, video in enumerate(videos):
            # (1) 시청 기록 (12개)
            history = WatchHistory(
                user_unique_id=test_user.user_unique_id,
                video_unique_id=video.video_unique_id,
                last_played_time=i * 100,  # 조금씩 다르게 설정
                is_finished=(i % 2 == 0)  # 짝수 영상은 다 본 걸로 처리
            )
            db.session.add(history)

            # (2) 찜하기 (12개)
            wish = VideoWish(
                user_unique_id=test_user.user_unique_id,
                video_unique_id=video.video_unique_id
            )
            db.session.add(wish)

            # (3) 문의 남기기 (12개)
            support = Support(
                user_unique_id=test_user.user_unique_id,
                category="영상오류",
                title=f"영상 {i}번이 안 나와요.",
                content=f"이 영상({video.video_title})의 버퍼링이 너무 심합니다. 확인 부탁드려요.",
                status="pending"
            )
            db.session.add(support)

        # 6. 최종 커밋
        try:
            db.session.commit()
            print("✅ 1명의 유저와 12개의 활동 데이터가 성공적으로 생성되었습니다.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    seed_data()