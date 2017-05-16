from flask import render_template, request, url_for, redirect, flash, current_app
from ..models import Index, List
from .forms import IndexForm, ListForm
from .. import db
from . import main


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Index.query.order_by().paginate(
        page,
        per_page=current_app.config['FLASKY_INDEX_PER_PAGE'],
        error_out=False
    )
    index_list = pagination.items

    return render_template('index.html', index_list=index_list, pagination=pagination)


@main.route('/index_add', methods=['GET', 'POST'])
def index_add():
    form = IndexForm()
    if form.validate_on_submit():
        index = Index(name=form.name.data,
                      url=form.url.data,
                      html=form.html.data,
                      status=form.status.data)
        db.session.add(index)
        flash('Index add success.')
        return redirect(url_for('.index'))
    return render_template('index_add.html', form=form)


@main.route('/index_edit/<int:id>', methods=['GET', 'POST'])
def index_edit(id):
    index = Index.query.get_or_404(id)
    form = IndexForm(index)
    if form.validate_on_submit():
        index.name = form.name.data
        index.url = form.url.data
        index.html = form.html.data
        index.status = form.status.data
        db.session.add(index)
        flash('Index edit success.')
        return redirect(url_for('.index'))
    form.name.data = index.name
    form.url.data = index.url
    form.html.data = index.html
    form.status.data = index.status
    return render_template('index_edit.html', form=form)


@main.route('/index_delete/<int:id>')
def index_delete(id):
    index = Index.query.get_or_404(id)
    db.session.delete(index)
    flash('Index delete success.')
    return redirect(url_for('.index'))


@main.route('/index/<int:id>/list')
def index_list(id):
    index = Index.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = index.lists.order_by(List.id.asc()).paginate(
        page,
        per_page=current_app.config['FLASKY_LIST_PER_PAGE'],
        error_out=False
    )
    list_list = pagination.items
    return render_template('index_list.html', list_list=list_list, pagination=pagination)


@main.route('/list')
def list_list():
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (List.query.count() - 1) // \
               current_app.config['FLASKY_LIST_PER_PAGE'] + 1
    pagination = List.query.order_by(List.id.asc()).paginate(
        page,
        per_page=current_app.config['FLASKY_LIST_PER_PAGE'],
        error_out=False
    )
    list_list = pagination.items
    return render_template('list.html', list_list=list_list, pagination=pagination)


@main.route('/list_add', methods=['GET', 'POST'])
def list_add():
    form = ListForm()
    if form.validate_on_submit():
        item = List(index_id=form.index_id.data,
                    name=form.name.data,
                    url=form.url.data,
                    html=form.html.data,
                    status=form.status.data)
        db.session.add(item)
        flash('List add success.')
        return redirect(url_for('.list_list', page=-1))
    return render_template('list_add.html', form=form)


@main.route('/list_edit/<int:id>', methods=['GET', 'POST'])
def list_edit(id):
    item = List.query.get_or_404(id)
    form = ListForm(item)
    if form.validate_on_submit():
        item.index_id = form.index_id.data
        item.name = form.name.data
        item.url = form.url.data
        item.html = form.html.data
        item.status = form.status.data
        db.session.add(item)
        flash('List edit success.')
        return redirect(url_for('.list_list'))
    form.index_id.data = item.index_id
    form.name.data = item.name
    form.url.data = item.url
    form.html.data = item.html
    form.status.data = item.status
    return render_template('list_edit.html', form=form)


@main.route('/list_delete/<int:id>')
def list_delete(id):
    item = List.query.get_or_404(id)
    db.session.delete(item)
    flash('List delete success.')
    return redirect(url_for('.list_list'))


@main.route('/list_view/<int:id>')
def list_view(id):
    item = List.query.get_or_404(id)
    index = Index.query.get_or_404(item.index_id)
    lists = index.lists.filter_by(status=1).all()
    return render_template('list_view.html', item=item, index=index, lists=lists)
