from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import or_
from one import db
from one.models import User, Video, Support, Review, SupportAnswer
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def admin_main():
    user_count = User.query.count()
    content_count = Video.query.count()
    inquiry_pending_count = Support.query.filter_by(status='pending').count()
    review_count = Review.query.count()

    return render_template(
        'admin/admin_main.html',
        user_count=user_count,
        content_count=content_count,
        inquiry_pending_count=inquiry_pending_count,
        review_count=review_count
    )


# ================= 회원 관리 =================
@bp.route('/members')
def member_list():
    keyword = request.args.get('keyword', '').strip()
    search_type = request.args.get('search_type', 'all').strip()
    page = request.args.get('page', 1, type=int)

    query = User.query

    if keyword:
        if search_type == 'user_unique_id':
            if keyword.isdigit():
                query = query.filter(User.user_unique_id == int(keyword))
            else:
                query = query.filter(User.user_unique_id == -1)

        elif search_type == 'user_email':
            query = query.filter(User.user_email.contains(keyword))

        elif search_type == 'user_phone':
            query = query.filter(User.user_phone.contains(keyword))

        elif search_type == 'user_gender':
            if keyword in ['남', '남자', 'M', 'm']:
                query = query.filter(User.user_gender.in_(['M', 'm', '남', '남자']))
            elif keyword in ['여', '여자', 'F', 'f']:
                query = query.filter(User.user_gender.in_(['F', 'f', '여', '여자']))
            else:
                query = query.filter(User.user_gender.contains(keyword))

        elif search_type == 'signup_method':
            if keyword in ['이메일', 'email']:
                query = query.filter(User.signup_method == 'email')
            elif keyword in ['카카오', 'kakao']:
                query = query.filter(User.signup_method == 'kakao')
            elif keyword in ['네이버', 'naver']:
                query = query.filter(User.signup_method == 'naver')
            else:
                query = query.filter(User.user_unique_id == -1)

        elif search_type == 'user_active':
            if keyword in ['활성', 'active', '1', 'true', 'True']:
                query = query.filter(User.user_active == True)
            elif keyword in ['비활성', 'inactive', '0', 'false', 'False']:
                query = query.filter(User.user_active == False)
            else:
                query = query.filter(User.user_unique_id == -1)

        else:
            query = query.filter(
                or_(
                    User.user_email.contains(keyword),
                    User.user_phone.contains(keyword),
                    User.user_gender.contains(keyword),
                    User.signup_method.contains(keyword)
                )
            )

    member_list = query.order_by(User.user_unique_id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'admin/member_list.html',
        member_list=member_list,
        keyword=keyword,
        search_type=search_type
    )


# ================= 활성 / 비활성 토글 =================
@bp.route('/members/toggle/<int:user_id>', methods=['POST'])
def member_toggle(user_id):
    member = User.query.get_or_404(user_id)
    member.user_active = not member.user_active
    db.session.commit()
    return redirect(url_for('admin.member_list', changed=1))


# ================= 콘텐츠 관리 =================
@bp.route('/contents')
def content_list():
    keyword = request.args.get('keyword', '').strip()
    search_type = request.args.get('search_type', 'all').strip()
    page = request.args.get('page', 1, type=int)

    query = Video.query

    if keyword:
        if search_type == 'video_unique_id':
            if keyword.isdigit():
                query = query.filter(Video.video_unique_id == int(keyword))
            else:
                query = query.filter(Video.video_unique_id == -1)

        elif search_type == 'video_title':
            query = query.filter(Video.video_title.contains(keyword))

        elif search_type == 'video_director':
            query = query.filter(Video.video_director.contains(keyword))

        elif search_type == 'video_actor':
            query = query.filter(Video.video_actor.contains(keyword))

        elif search_type == 'video_age_limit':
            query = query.filter(Video.video_age_limit.contains(keyword))

        elif search_type == 'video_date':
            query = query.filter(Video.video_date.contains(keyword))

        else:
            query = query.filter(
                or_(
                    Video.video_title.contains(keyword),
                    Video.video_director.contains(keyword),
                    Video.video_actor.contains(keyword),
                    Video.video_age_limit.contains(keyword)
                )
            )

    content_list = query.order_by(Video.video_unique_id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'admin/content_list.html',
        content_list=content_list,
        keyword=keyword,
        search_type=search_type
    )


# ================= 콘텐츠 등록 =================
@bp.route('/contents/create', methods=['GET', 'POST'])
def content_create():
    if request.method == 'POST':
        video_title = request.form.get('video_title', '').strip()
        video_director = request.form.get('video_director', '').strip()
        video_actor = request.form.get('video_actor', '').strip()
        video_age_limit = request.form.get('video_age_limit', '').strip()
        video_date_str = request.form.get('video_date', '').strip()
        video_url = request.form.get('video_url', '').strip()
        video_thumbnail = request.form.get('video_thumbnail', '').strip()
        video_synopsis = request.form.get('video_synopsis', '').strip()
        video_genres = request.form.get('video_genres', '').strip()
        video_is_movie = request.form.get('video_is_movie') == 'True'

        video_date = None
        if video_date_str:
            video_date = datetime.strptime(video_date_str, '%Y-%m-%d').date()

        new_video = Video(
            video_title=video_title,
            video_director=video_director,
            video_actor=video_actor,
            video_age_limit=video_age_limit,
            video_date=video_date,
            video_url=video_url,
            video_thumbnail=video_thumbnail,
            video_synopsis=video_synopsis,
            video_genres=video_genres,
            video_is_movie=video_is_movie,
            admin_unique_id=1
        )

        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('admin.content_list'))

    return render_template(
        'admin/content_form.html',
        mode='create',
        content=None
    )


# ================= 콘텐츠 수정 =================
@bp.route('/contents/edit/<int:video_id>', methods=['GET', 'POST'])
def content_edit(video_id):
    content = Video.query.get_or_404(video_id)

    if request.method == 'POST':
        content.video_title = request.form.get('video_title', '').strip()
        content.video_director = request.form.get('video_director', '').strip()
        content.video_actor = request.form.get('video_actor', '').strip()
        content.video_age_limit = request.form.get('video_age_limit', '').strip()

        video_date_str = request.form.get('video_date', '').strip()
        content.video_date = datetime.strptime(video_date_str, '%Y-%m-%d').date() if video_date_str else None

        content.video_url = request.form.get('video_url', '').strip()
        content.video_thumbnail = request.form.get('video_thumbnail', '').strip()
        content.video_synopsis = request.form.get('video_synopsis', '').strip()
        content.video_genres = request.form.get('video_genres', '').strip()
        content.video_is_movie = request.form.get('video_is_movie') == 'True'

        db.session.commit()
        return redirect(url_for('admin.content_list'))

    return render_template(
        'admin/content_form.html',
        mode='edit',
        content=content
    )


# ================= 콘텐츠 삭제 =================
@bp.route('/contents/delete/<int:video_id>', methods=['POST'])
def content_delete(video_id):
    content = Video.query.get_or_404(video_id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('admin.content_list'))


# ================= 문의 관리 =================
@bp.route('/inquiries')
def inquiry_list():
    keyword = request.args.get('keyword', '').strip()
    search_type = request.args.get('search_type', 'all').strip()
    page = request.args.get('page', 1, type=int)

    query = Support.query.join(User, Support.user_unique_id == User.user_unique_id)

    if keyword:
        if search_type == 'support_id':
            if keyword.isdigit():
                query = query.filter(Support.support_id == int(keyword))
            else:
                query = query.filter(Support.support_id == -1)

        elif search_type == 'user_email':
            query = query.filter(User.user_email.contains(keyword))

        elif search_type == 'category':
            query = query.filter(Support.category.contains(keyword))

        elif search_type == 'title':
            query = query.filter(Support.title.contains(keyword))

        elif search_type == 'content':
            query = query.filter(Support.content.contains(keyword))

        elif search_type == 'status':
            if keyword in ['답변 전', 'pending']:
                query = query.filter(Support.status == 'pending')
            elif keyword in ['답변 완료', 'completed']:
                query = query.filter(Support.status == 'completed')
            else:
                query = query.filter(Support.support_id == -1)

        else:
            query = query.filter(
                or_(
                    User.user_email.contains(keyword),
                    Support.category.contains(keyword),
                    Support.title.contains(keyword),
                    Support.content.contains(keyword)
                )
            )

    inquiry_list = query.order_by(Support.support_id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'admin/inquiry_list.html',
        inquiry_list=inquiry_list,
        keyword=keyword,
        search_type=search_type
    )


# ================= 문의 상세 / 답변 =================
@bp.route('/inquiries/<int:support_id>', methods=['GET', 'POST'])
def inquiry_detail(support_id):
    inquiry = Support.query.get_or_404(support_id)

    if request.method == 'POST':
        answer_content = request.form.get('answer_content', '').strip()

        if answer_content:
            answer = SupportAnswer(
                support_id=inquiry.support_id,
                admin_unique_id=1,
                content=answer_content
            )
            db.session.add(answer)
            inquiry.status = 'completed'
            db.session.commit()

        return redirect(url_for('admin.inquiry_detail', support_id=inquiry.support_id))

    return render_template(
        'admin/inquiry_detail.html',
        inquiry=inquiry
    )


# ================= 답변 수정 =================
@bp.route('/inquiries/answers/edit/<int:answer_id>', methods=['GET', 'POST'])
def inquiry_answer_edit(answer_id):
    answer = SupportAnswer.query.get_or_404(answer_id)

    if request.method == 'POST':
        answer.content = request.form.get('answer_content', '').strip()
        db.session.commit()
        return redirect(url_for('admin.inquiry_detail', support_id=answer.support_id))

    return render_template(
        'admin/inquiry_answer_form.html',
        mode='edit',
        answer=answer
    )


# ================= 답변 삭제 =================
@bp.route('/inquiries/answers/delete/<int:answer_id>', methods=['POST'])
def inquiry_answer_delete(answer_id):
    answer = SupportAnswer.query.get_or_404(answer_id)
    support_id = answer.support_id

    inquiry = Support.query.get_or_404(support_id)

    db.session.delete(answer)
    db.session.flush()

    remaining_answer = SupportAnswer.query.filter_by(support_id=support_id).first()
    if not remaining_answer:
        inquiry.status = 'pending'
    else:
        inquiry.status = 'completed'

    db.session.commit()

    return redirect(url_for('admin.inquiry_detail', support_id=support_id))


# ================= 리뷰 관리 =================
@bp.route('/reviews')
def review_list():
    keyword = request.args.get('keyword', '').strip()
    search_type = request.args.get('search_type', 'all').strip()
    page = request.args.get('page', 1, type=int)

    query = Review.query.join(User, Review.user_unique_id == User.user_unique_id) \
                        .join(Video, Review.video_unique_id == Video.video_unique_id)

    if keyword:
        if search_type == 'review_id':
            if keyword.isdigit():
                query = query.filter(Review.review_id == int(keyword))
            else:
                query = query.filter(Review.review_id == -1)

        elif search_type == 'user_email':
            query = query.filter(User.user_email.contains(keyword))

        elif search_type == 'video_title':
            query = query.filter(Video.video_title.contains(keyword))

        elif search_type == 'comment':
            query = query.filter(Review.comment.contains(keyword))

        else:
            query = query.filter(
                or_(
                    User.user_email.contains(keyword),
                    Video.video_title.contains(keyword),
                    Review.comment.contains(keyword)
                )
            )

    review_list = query.order_by(Review.review_id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'admin/review_list.html',
        review_list=review_list,
        keyword=keyword,
        search_type=search_type
    )


# ================= 리뷰 삭제 =================
@bp.route('/reviews/delete/<int:review_id>', methods=['POST'])
def review_delete(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('admin.review_list'))