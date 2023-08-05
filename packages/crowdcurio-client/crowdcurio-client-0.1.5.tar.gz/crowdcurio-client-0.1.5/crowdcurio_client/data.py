import datetime
import requests
import time

from crowdcurio_client.crowdcurio import CrowdCurioObject

class Data(CrowdCurioObject):
    _api_slug = 'data'
    _link_slug = 'data'
    _edit_attributes = (
        'slug',
        'name',
        'type',
        'url',
        'content',
        'order',
        {}
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def add(self, task, experiment = None, condition = None):
        if experiment == None and condition == None:
            self.put(
                '{}'.format(self.id),
                json={"data": {"type": "Data", "id": self.id, "attributes": {"content": self.content},"relationships": {"task":{"data":{"type":"Task","id":task.id}} }}}
            )
        else:
            if condition == None:
                self.put(
                    '{}'.format(self.id),
                    json={"data": {"type": "Data", "id": self.id, "attributes": {"content": self.content},"relationships": {"task":{"data":{"type":"Task","id":task.id}}, "experiment":{"data":{"type":"Experiment","id":experiment.id}} }}}
                )
            else:
                self.put(
                    '{}'.format(self.id),
                    json={"data": {"type": "Data", "id": self.id, "attributes": {"content": self.content},"relationships": {"task":{"data":{"type":"Task","id":task.id}}, "experiment":{"data":{"type":"Experiment","id":experiment.id}}, "condition":{"data":{"type":"Condition","id":condition.id}} }}}
                )

    def remove(self, task, experiment):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Data", "id": self.id, "attributes": {"content": self.content}, "relationships": {"task":{}, "experiment": {}}}}
        )

    def destroy(self):
        self.delete('{}'.format(self.id), json={'data': {'type':'Data', 'id': self.id}})

class DataSet(CrowdCurioObject):
    _api_slug = 'dataset'
    _link_slug = 'dataset'
    _edit_attributes = (
        'name',
        'order',
        'is_active',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def add(self, task):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Dataset", "id": self.id, "relationships": {"task":{"data":{"type":"Task","id":task.id}}}}}
        )

    def remove(self, task):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Dataset", "id": self.id, "relationships": {"task":{}}}}
        )

    def destroy(self):
        self.delete('{}'.format(self.id), json={'data': {'type':'Dataset', 'id': self.id}})


class DataRecord(CrowdCurioObject):
    _api_slug = 'datarecord'
    _link_slug = 'datarecord'
    _edit_attributes = (
        'seen',
        'order',
        'assigned',
        'retirement_limit',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def add(self, task, data, experiment=None, condition=None):
        if experiment is None and condition is None:
            self.put(
                '{}'.format(self.id),
                json={"data": {"type": "Datarecord", "id": self.id, "relationships": {"task":{"data":{"type":"Task","id":task.id}},"data":{"data":{"type":"Data","id":data.id}}}}}
            )
        else:
            self.put(
                '{}'.format(self.id),
                json={"data": {"type": "Datarecord", "id": self.id, "relationships": {"task":{"data":{"type":"Task","id":task.id}},"data":{"data":{"type":"Data","id":data.id}},"experiment":{"data":{"type":"Experiment","id":experiment.id}},"condition":{"data":{"type":"Condition","id":condition.id}}}}}
            )

    def remove(self, task, data, experiment, condition):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Datarecord", "id": self.id, "relationships": {"task":{}, "data":{}, "experiment":{}, "condition":{}}}}
        )

    def destroy(self):
        self.delete('{}'.format(self.id), json={'data': {'type':'Datarecord', 'id': self.id}})
