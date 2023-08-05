# .. License
#
#   Copyright 2017 Bryan A. Jones
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# ***************************************************
# |docname| - Provide extensions for Flask-SQLAlchemy
# ***************************************************
# See `../tests/test_flask.py` for usage and examples.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
# None.

# Third-party imports
# -------------------
from sqlalchemy.ext.declarative import declarative_base
from flask import _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model, DefaultMeta

# Local imports
# -------------
from . import QueryMakerScopedSession, QueryMaker


# Flask-SQLAlchemy customization
# ==============================
# Create a SQLAlchemy class that includes the pythonic_sqlalchemy_query extension. In particular, it supports the following improvements over Flask-SQLAlchemy's `queries <http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records>`_:
#
# - ``User['peter'].q.first()`` as a shortcut for ``User.query.filter_by(username='peter').first()``.
# - ``db.session(User)['peter'].q.first()`` as a shortcut to ``db.session.query(User).filter_by(username='peter').first()``.
#
# To use: ``db = SQLAlchemyPythonicQuery(app)`` instead of ``db = SQLAlchemy(app)``, as shown in `../tests/test_flask.py`.
#
# Enable syntax such as ``Model[id]`` for queries.
class QueryMakerFlaskDeclarativeMeta(DefaultMeta):
    def __getitem__(cls, key):
        # Extract the session from the Flask-SQLAlchemy `query <http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records>`_ attribute.
        session = cls.query.session
        # Build a new query from here, since ``cls.query`` has already invoked ``add_entity`` on ``cls``.
        return QueryMaker(cls, session.query())[key]


# Then, use this in the `Flask-SQLAlchemy session <http://flask-sqlalchemy.pocoo.org/2.3/api/#sessions>`_.
class SQLAlchemyPythonicQuery(SQLAlchemy):
    # Unlike the standard `SQLAlchemy parameters <http://flask-sqlalchemy.pocoo.org/2.3/api/#flask_sqlalchemy.SQLAlchemy>`_, this **does not** allow the ``model_class`` keyword argument.
    def __init__(self, *args, **kwargs):
        # Provide a declarative_base model for Flask-SQLAlchemy. This is almost identical to code in  ``flask_sqlalchemy.SQLAlchemy.make_declarartive_base``, but using our custom metaclass.
        assert 'model_class' not in kwargs
        kwargs['model_class'] = declarative_base(
            cls=Model,
            name='Model',
            metadata=kwargs.get('metadata', None),
            # Use our custom metaclass.
            metaclass=QueryMakerFlaskDeclarativeMeta
        )

        super(SQLAlchemyPythonicQuery, self).__init__(*args, **kwargs)

    # Enable syntax such as ``db.session(User)['peter']``. The only change from the Flask-SQLAlchemy v2.3.2 source: ``QueryMakerScopedSession`` instead of ``orm.scoped_session``.
    def create_scoped_session(self, options=None):
        if options is None:
            options = {}

        scopefunc = options.pop('scopefunc', _app_ctx_stack.__ident_func__)
        options.setdefault('query_cls', self.Query)
        return QueryMakerScopedSession(
            self.create_session(options), scopefunc=scopefunc
        )
