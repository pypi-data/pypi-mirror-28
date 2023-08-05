from lifter.backends.python import IterableStore
from schematics.models import Model as SchematicsModel
from schematics.models import ModelMeta
from schematics.types import *  # noqa: F401,F403


class DBOperationError(Exception):
    pass


class DataManager:
    def __init__(self, klass):
        self.klass = klass
        self._table = klass._table

    def get(self, eid):
        instance = self._table.get(eid=eid)
        if instance:
            return self.klass(eid=instance.eid, **instance)
        return None

    def all(self):
        # instances = self._table.all()
        # return [self.klass(eid=i.eid, **i) for i in instances]
        all_instances = [self.klass(eid=i.eid, **i) for i in self._table.all()]
        store = IterableStore(all_instances)
        manager = store.query(self)
        return manager.all()

    def filter(self, *args, **kwargs):
        all_objects = self.all()
        store = IterableStore(all_objects)
        manager = store.query(self)
        return manager.filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        all_objects = self.all()
        store = IterableStore(all_objects)
        manager = store.query(self)
        return manager.exclude(*args, **kwargs)

    def create(self, *args, **kwargs):
        eid = self._table.insert(kwargs)
        if not eid:
            raise DBOperationError('Failed to create record')
        return self.get(eid=eid)

    def save(self, data, eid=None):
        if not eid:
            eid = self._table.insert(data)
            if not eid:
                raise DBOperationError('Failed to save record')

        else:
            eid = self._table.update(data, eids=[eid, ])[0]
            if not eid:
                raise DBOperationError(
                    'Failed to update record {}'.format(eid))

        return eid

    def delete(self, eid):
        eid = self._table.remove(eids=[eid, ])
        if not eid:
            raise DBOperationError('Failed to remove record {}'.format(eid))

        return True


class ZeroMeta(type):
    def __getattr__(cls, key):
        if key == '_table':
            return cls.Meta.database.table(cls._schema.name.lower())

        elif key == 'objects':
            return DataManager(cls)

        return getattr(cls, key)


class FinalMeta(ModelMeta, ZeroMeta):
    pass


class Model(SchematicsModel, metaclass=FinalMeta):
    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            str(self),
        )

    def __str__(self):
        return '{} object'.format(self.__class__.__name__)

    def __init__(self, eid=None, *args, **kwargs):
        super().__init__()

        self.eid = eid
        self._table = self.Meta.database.table(self._schema.name.lower())
        self.manager = DataManager(self)

        for k, v in kwargs.items():
            if k in self._valid_input_keys:
                setattr(self, k, v)

    def __iter__(self):
        for k, v in self._data.items():
            yield k, v

    @property
    def pk(self):
        return self.eid

    def save(self):
        self.eid = self.manager.save(dict(self._data), self.eid)
        return self.eid

    def delete(self):
        if not self.eid:
            raise DBOperationError('Could not delete unsaved object')
        return self.manager.delete(self.eid)
