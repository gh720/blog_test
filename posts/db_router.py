class main_db_router:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'posts':
            return 'oracle'
        return False

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'posts':
            return 'oracle'
        return False

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'posts' and \
                obj2._meta.app_label == 'posts':
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'posts':
            return db == 'posts'
        return False
