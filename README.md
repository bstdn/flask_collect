# 学习《Flask Web开发：基于Python的Web应用开发实战》分享

- 一直在说学习Python，对同事，对朋友，都说我正在学习Python，这无形给自己一定的压力，促使自己要去学习，进步。
- Python的语法看了忘，忘了再看。每天学习时长不固定，会造成这样的效果。
- 然后看到这本书《Flask Web开发：基于Python的Web应用开发实战》，时间不长不短，也学习了一段时间，前后看了两三遍，学会了一些知识，在这里做一个整理、分享。
- 坚持学习很重要，活到老学到老，让我们一起学习Python吧。

- 下面从一个小项目中，分享一下。
- 小项目：采集[`廖雪峰的官方网站`](http://www.liaoxuefeng.com/)部分教程，并在Web中展示。
- 小项目在`Mac OS X`，`python3`中运行。(`python2`调试中)

## 1. 使用虚拟环境

- 与系统的Python解释器分开，在项目中的私有副本

### 安装

- 检查virtualenv

```
$ virtualenv -- version
```

- 安装virtualenv

```
$ sudo pip install virtualenv
```

- 新建一个文件夹作为项目目录
- 按照惯例，一般虚拟环境会被命名为 venv

```
virtualenv venv
New python executable in venv/bin/python
Installing distribute......done.
Installing pip.............done.
```

- 可指定python版本

```
virtualenv venv --python=python2.7
virtualenv venv --python=python3.5
```

- 激活这个虚拟环境

```
source venv/bin/activate
```

- 为了提醒你已经激活了虚拟环境，激活虚拟环境的 命令会修改命令行提示符，加入环境名

```
(venv) $
```

- 回到全局 Python 解释器

```
deactivate
```

### 使用pip安装Python包

- pip 的 安装请参见 [https://pip.pypa.io/en/latest/installing.html](https://pip.pypa.io/en/latest/installing.html)
- 在虚拟环境中安装 Flask

```
(venv) $ pip install flask
```

- 尝试导入 Flask

```
(venv) $ python
>>> import flask
>>>
```

### 第一个程序

```
from flask import Flask

app = Flask(__name__)#Flask 类的对象

'''
修饰器是 Python 语言的标准特性，可以使用不同的方式修改函数的行为。
惯常用法是使用修饰器把函数注册为事件的处理程序
'''
#app.route 修饰器，把修饰的函数注册为路由
@app.route('/')
def hello():
    return '<h1>Hello World</h1>'

#程序会显示一个使用 name 动态参数生成的欢迎消息
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

if __name__ == '__main__':#__name__=='__main__' 是 Python 的惯常用法
    app.run(debug=True)#要想启用调试模式，我们可以把 debug 参数设为 True

```

### 运行

```
#保存以上程序至上述项目根目录 hello.py
(venv) $ python hellp.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 277-775-896
#访问 http://127.0.0.1:5000/ 与 http://127.0.0.1:5000/user/Python 即可
```

## 2. 初始项目结构

```
|-flasky
    |-app/
        |-templates/
        |-static/
        |-main/
            |-__init__.py
            |-errors.py
            |-forms.py
            |-views.py
        |-collect/
            |-__init__.py
        |-__init__.py
        |-models.py
    |-migrations/
    |-venv/
    |-requirements.txt
    |-config.py
    |-manage.py
```

- Flask 程序一般都保存在名为 app 的包中;
- migrations文件夹包含数据库迁移脚本;
- venv文件夹包含Python虚拟环境。

- pip 可以使用如下命令自动生成requirements.txt文件
- 该文件便是项目中所需要的所有Python包

```
(venv) $ pip freeze > requirements.txt
```

- 创建一个新的虚拟环境，并在其上运行以下命令
- 即可安装该项目中所需要的所有Python包

```
(venv) $ pip install -r requirements.txt
```

- 创建迁移仓库

```
(venv) $ python manage.py db init
```

- 创建迁移脚本

```
(venv) $ python manage.py db migrate -m "initial migration"
```

- 更新数据库

```
(venv) $ python manage.py db upgrade <revision>
```

- 启动脚本

```
(venv) $ python manage.py runserver
```


## 3. 定义模型

```
from datetime import datetime
from . import db
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from .collect import create_collect


class Index(db.Model):
    __tablename__ = 'indexs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(255))
    html = db.Column(LONGTEXT)
    status = db.Column(TINYINT(3), default=0)
    dateline = db.Column(db.DateTime(), default=datetime.utcnow)
    lists = db.relationship('List', backref='list', lazy='dynamic')

    def __repr__(self):
        return '<Index %r>' % self.name


class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    index_id = db.Column(db.Integer, db.ForeignKey('indexs.id'))
    name = db.Column(db.String(64))
    url = db.Column(db.String(255))
    html = db.Column(LONGTEXT)
    status = db.Column(TINYINT(3), default=0)
    dateline = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<List %r>' % self.name

```

## 4. 采集数据

```
#采集页面列表
@manager.command
def collect_index(name='liaoxuefeng'):
    Index.index_add(name)
    Index.index_edit(name)

#采集列表页面
@manager.command
def collect_list_add(name='liaoxuefeng'):
    List.list_add(name)

#采集列表内容
@manager.command
def collect_list_edit(name='liaoxuefeng'):
    List.list_edit(name)

#在终端执行

(venv) $ python manage.py collect_index <name>
```

## 5. 定义路由

```
#首页 采集页面列表
@main.route('/')
def index():
    pass

#添加采集页面
@main.route('/index_add', methods=['GET', 'POST'])
def index_add():
    pass

#编辑采集页面
@main.route('/index_edit/<int:id>', methods=['GET', 'POST'])
def index_edit(id):
    pass

#删除添加采集页面
@main.route('/index_delete/<int:id>')
def index_delete(id):
    pass

#采集页面下的列表页面
@main.route('/index/<int:id>/list')
def index_list(id):
    pass

#列表页面
@main.route('/list')
def list_list():
    pass

#添加列表页面
@main.route('/list_add', methods=['GET', 'POST'])
def list_add():
    pass

#编辑列表页面
@main.route('/list_edit/<int:id>', methods=['GET', 'POST'])
def list_edit(id):
    pass

#删除列表页面
@main.route('/list_delete/<int:id>')
def list_delete(id):
    pass

#详细页面
@main.route('/list_view/<int:id>')
def list_view(id):
    pass

```

## 6. CRUD

```
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, URL
from wtforms import ValidationError
from ..models import Index, List


class IndexForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)])
    url = StringField('Url', validators=[Required(), Length(1, 255), URL()])
    html = TextAreaField('Html')
    status = RadioField('Status', coerce=int, default='0')
    submit = SubmitField('Submit')

    def __init__(self, index=None, *args, **kwargs):
        super(IndexForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, 'Initial'), (1, 'Downloaded'), (2, 'Deprecated')]
        self.index = index

    def validate_url(self, field):
        if self.index is None:
            if Index.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')
        else:
            if self.index.url != field.data and \
                    Index.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')


class ListForm(FlaskForm):
    index_id = SelectField('Index id', coerce=int)
    name = StringField('Name', validators=[Length(0, 64)])
    url = StringField('Url', validators=[Required(), Length(1, 255), URL()])
    html = TextAreaField('Html')
    status = RadioField('Status', coerce=int, default=0)
    submit = SubmitField('Submit')

    def __init__(self, item=None, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.index_id.choices = [(index.id, index.name) for index in Index.query.filter_by(status=1).all()]
        self.status.choices = [(0, 'Initial'), (1, 'Downloaded'), (2, 'Deprecated')]
        self.item = item

    def validate_url(self, field):
        if self.item is None:
            if List.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')
        else:
            if self.item.url != field.data and \
                    List.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')


```

## 7.运行

- 本项目代码存放在github中 [https://github.com/bstdn/flask_collect](https://github.com/bstdn/flask_collect)

```
#运行项目
git clone https://github.com/bstdn/flask_collect.git
cd flask_collect
virtualenv venv
source venv/bin/activate
(venv) $ pip install -r requirements.txt

#定义环境变量 或 修改config.py中配置指定数据库
(venv) $ export SECRET_KEY=<SECRET_KEY>
(venv) $ export DEV_DATABASE_URL=<DEV_DATABASE_URL>

(venv) $ python manage.py db upgrade
(venv) $ python manage.py collect_index
(venv) $ python manage.py collect_list_add
(venv) $ python manage.py collect_list_edit
(venv) $ python manage.py runserver

#访问 http://127.0.0.1:5000/
```

## 效果展示

![输入图片说明](https://images.gitee.com/uploads/images/2020/0427/105726_885ec995_1185106.png "list.png")

![输入图片说明](https://images.gitee.com/uploads/images/2020/0427/105739_21af8747_1185106.png "list_edit.png")

![输入图片说明](https://images.gitee.com/uploads/images/2020/0427/105748_b04e2154_1185106.png "list_view.png")
