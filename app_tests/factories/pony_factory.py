from factory import base
from pony.orm import db_session, flush


class PonyFactory(base.Factory):
    class Meta:
        abstract = True

    @classmethod
    @db_session
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        flush()
        return obj
