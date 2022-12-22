from backend.main import db


class RepositoryMixin(object):
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def delete(cls, id: int):
        obj = cls.get_by_id(id)
        db.session.delete(obj)
        db.session.commit()
