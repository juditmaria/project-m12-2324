from . import db_manager as db

class BaseMixin():
    
    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        return r.save()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def db_query(cls, *args):
        return db.session.query(cls, *args)

    # @classmethod
    # def db_query_with(cls, join_cls):
    #     return cls.db_query(join_cls).join(join_cls)

    @classmethod
    def db_query_with(cls, join_cls, outerjoin_cls = []):
        joins = join_cls if type(join_cls) is list else [join_cls]
        ojoins = outerjoin_cls if type(outerjoin_cls) is list else [outerjoin_cls]
        args = tuple(joins + ojoins)
        query = cls.db_query(*args)
        for c in joins:
            query = query.join(c)
        for c in ojoins:
            query = query.outerjoin(c)
        return query
    
    @classmethod
    def get(cls, id):
        return cls.db_query().get(id)
    
    @classmethod
    def get_all(cls):
        return cls.db_query().all()

    @classmethod
    def get_filtered_by(cls, **kwargs):
        return cls.db_query().filter_by(**kwargs).one_or_none()

    @classmethod
    def get_all_filtered_by(cls, **kwargs):
        return cls.db_query().filter_by(**kwargs).order_by(cls.id.asc()).all()
    
    @classmethod
    def get_with(cls, id, join_cls, outerjoin_cls = []):
        return cls.db_query_with(join_cls, outerjoin_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_all_with(cls, join_cls, outerjoin_cls = []):
        return cls.db_query_with(join_cls, outerjoin_cls).order_by(cls.id.asc()).all()

    @staticmethod
    def db_enable_debug():
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from collections import OrderedDict
from sqlalchemy.engine.row import Row

class SerializableMixin():

    exclude_attr = []

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if key not in self.__class__.exclude_attr:
                result[key] = getattr(self, key)
        return result

    @staticmethod
    def to_dict_collection(collection):
        result = []
        for x in collection:  
            if (type(x) is Row):
                obj = {}
                first = True
                for y in x:
                    if first:
                        # model
                        obj = y.to_dict()
                        first = False
                    elif y:
                        # relationships
                        key = y.__class__.__name__.lower()
                        obj[key] = y.to_dict()
                        fk = key + '_id'
                        if fk in obj:
                            del obj[fk]
                result.append(obj)
            else:
                # only model
                result.append(x.to_dict())
        return result
