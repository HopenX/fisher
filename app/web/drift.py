from flask import flash, redirect, url_for, render_template, request, current_app
from sqlalchemy import desc, or_

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web
from flask_login import login_required, current_user


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    点击「向他们请求此书」跳转到此函数，发起一个索要书的申请
    """
    current_gift = Gift.query.get_or_404(gid)
    gifter = current_gift.user

    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        sava_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user, gift=current_gift)  # 后面这些是 **kwargs
        return redirect(url_for('web.pending'))

    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did, Gift.uid == current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject.value
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += current_app.config['BEANS_EVERY_DRIFT']
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw.value
        current_user.beans += current_app.config['BEANS_EVERY_DRIFT']
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    """
        确认邮寄，只有书籍赠送者才可以确认邮寄
        注意需要验证超权
    """
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success.value
        current_user.beans += current_app.config['BEANS_EVERY_DRIFT']
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        # 不查询直接更新;这一步可以异步来操作.和上面的 gift 一样的
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def sava_drift(drift_form, current_gift):
    """
    把某一次表单填写的交易保存为 Drift 类，写入数据库中
    :param drift_form:
    :param current_gift:
    :return:
    """
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)  # 确保名称相同，表单信息可以进行复制

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= current_app.config['BEANS_EVERY_DRIFT']

        db.session.add(drift)
