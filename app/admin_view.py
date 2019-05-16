from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_login import current_user

from flask import redirect, url_for, request

from flask_admin import Admin


class AdminMixin:
    def is_accessible(self):
        #return current_user.has_role('admin')
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class RecordAdminView(AdminMixin, BaseModelView):
    form_columns = ['body']
    pass


class UserAdminView(AdminMixin, BaseModelView):
    pass

class ChatAdminView(AdminMixin, BaseModelView):
    pass
