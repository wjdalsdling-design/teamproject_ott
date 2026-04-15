from datetime import datetime, date, timezone, timedelta
import random

from one import db, create_app
from one.models import (
    User, Video, Plan, Admin, Subscription,
    Support, SupportAnswer, WatchHistory, Payment, Notice,
    VideoLike, VideoWish, Review
)

# 1. Flask 앱 인스턴스 생성
app = create_app()


def seed_data():
    with app.app_context():
        # 0. 기존 데이터 초기화 (주의: 실제 운영 환경에서는 사용 금지)
        db.drop_all()
        db.create_all()
        print("Database tables created.")

        # 1. 관리자 생성
        admin = Admin(
            admin_id="admin01",
            admin_password="password123",  # 실제로는 해싱 권장
            admin_name="운영자",
            admin_role="superadmin"
        )
        db.session.add(admin)
        db.session.commit()  # ID 생성을 위해 커밋

        # 2. 요금제 생성
        plans = [
            Plan(plan_name="Basic", price=9900.00),
            Plan(plan_name="Standard", price=13500.00),
            Plan(plan_name="Premium", price=17000.00)
        ]
        db.session.add_all(plans)
        db.session.commit()

        # 3. 사용자 생성
        user = User(
            user_email="test@example.com",
            user_password="password123",
            user_name="홍길동",
            signup_method="email",
            user_active=True
        )
        db.session.add(user)
        db.session.commit()

        # 4. 비디오 생성
        video = Video(
            video_title="파이썬 마스터 클래스",
            video_director="스네이크",
            video_actor="구이도 반 로섬",
            video_url="https://example.com",
            video_thumbnail="https://example.com",
            video_age_limit="All",
            video_synopsis="파이썬을 정복해봅시다.",
            video_genres="Education",
            admin_unique_id=admin.admin_unique_id
        )
        db.session.add(video)
        db.session.commit()

        # 5. 구독 정보 생성
        sub = Subscription(
            user_unique_id=user.user_unique_id,
            plan_id=plans[0].plan_id,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=30),
            status="active"
        )
        db.session.add(sub)
        db.session.commit()

        # 6. 결제 내역 생성
        pay = Payment(
            user_unique_id=user.user_unique_id,
            subscription_id=sub.subscription_id,
            price=9900.00,
            status="success"
        )
        db.session.add(pay)

        # 7. 리뷰 및 시청 기록
        review = Review(
            user_unique_id=user.user_unique_id,
            video_unique_id=video.video_unique_id,
            comment="정말 유익한 강의입니다!",
            rating=5
        )
        history = WatchHistory(
            user_unique_id=user.user_unique_id,
            video_unique_id=video.video_unique_id,
            last_played_time=120,
            is_finished=False
        )

        # 8. 좋아요 및 찜하기
        like = VideoLike(user_unique_id=user.user_unique_id, video_unique_id=video.video_unique_id)
        wish = VideoWish(user_unique_id=user.user_unique_id, video_unique_id=video.video_unique_id)

        db.session.add_all([review, history, like, wish])
        db.session.commit()

        print("Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()