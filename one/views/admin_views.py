from flask import Blueprint, render_template, redirect, url_for
from one import db
from one.models import User, Video, Support, Review

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def admin_main():
    return render_template('admin/admin_main.html')


# ================= 회원 관리 =================
@bp.route('/members')
def member_list():
    member_list = User.query.order_by(User.user_unique_id.desc()).all()
    return render_template('admin/member_list.html', member_list=member_list)


#  활성 / 비활성 토글
@bp.route('/members/toggle/<int:user_id>', methods=['POST'])
def member_toggle(user_id):
    member = User.query.get_or_404(user_id)

    # 상태 반전
    member.user_active = not member.user_active

    db.session.commit()
    return redirect(url_for('admin.member_list', changed=1))


# ================= 콘텐츠 관리 =================
@bp.route('/contents')
def content_list():
    content_list = Video.query.order_by(Video.video_unique_id.desc()).all()
    return render_template('admin/content_list.html', content_list=content_list)


# ================= 문의 관리 =================
@bp.route('/inquiries')
def inquiry_list():
    inquiry_list = Support.query.order_by(Support.support_id.desc()).all()
    return render_template('admin/inquiry_list.html', inquiry_list=inquiry_list)


# ================= 리뷰 관리 =================
@bp.route('/reviews')
def review_list():
    review_list = Review.query.order_by(Review.review_id.desc()).all()
    return render_template('admin/review_list.html', review_list=review_list)