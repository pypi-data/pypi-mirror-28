
import time
from architect import utils
from architect.manager.models import Resource, Manager, Relationship
from celery.utils.log import get_logger

logger = get_logger(__name__)


class BaseClient(object):

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.metadata = dict(kwargs.get('metadata', {}))
        self.kind = kwargs.get('engine')
        self.resources = {}
        self.resource_types = {}
        self.relations = {}
        self.timestamp = int(time.time())
        self._reverse_map = None
        self._schema = utils.get_resource_schema(self.kind)

    def get_resource_status(self, name, metadata):
        raise NotImplementedError

    def update_resources(self, resources=None):
        raise NotImplementedError

    def load_resources(self, resources=None):
        if resources is None:
            resources = self.resource_type_list()
        for resource in resources:
            self.load_resource_metadata(resource)
            count = len(self.resources.get(resource, {}))
            logger.info("Loaded {} {} resources".format(count,
                                                        resource))

    def load_resource_metadata(self, resource):
        if resource not in self.resources:
            self.resources[resource] = {}
        resources = Resource.objects.filter(manager=self.manager(),
                                            kind=resource)
        for item in resources:
            self.resources[resource]['id{}'.format(item.id)] = {
                'id': 'id{}'.format(item.id),
                'name': item.name,
                'kind': item.kind,
                'metadata': item.metadata,
            }

    def load_relations(self):
        relations = Relationship.objects.filter(manager=self.manager())
        for item in relations:
            if item.kind not in self.relations:
                self.relations[item.kind] = []
            self.relations[item.kind].append({
                'source': 'id{}'.format(item.source_id),
                'target': 'id{}'.format(item.target_id),
                'kind': item.kind,
            })

    def manager(self):
        return Manager.objects.get(name=self.name)

    def save(self):
        manager = Manager.objects.get(name=self.name)
        for resource_type, resources in self.resources.items():
            for resource_name, resource in resources.items():
                res, created = Resource.objects.get_or_create(uid=resource['uid'],
                                                              manager=manager)
                if created:
                    res.name = resource['name']
                    res.kind = resource_type
                    res.manager = manager
                    res.metadata = resource['metadata']
                    res.status = self.get_resource_status(resource_type,
                                                          resource['metadata'])
                    res.save()

        for relation_type, relations in self.relations.items():
            logger.info('Processed {} {} relations'.format(len(relations),
                                                           relation_type))
            for relation in relations:
                try:
                    source = Resource.objects.get(uid=relation['source'],
                                                  manager=manager)
                except Resource.DoesNotExist:
                    logger.error('No resource with'
                                 ' uid {} found'.format(relation['source']))
                    continue
                try:
                    target = Resource.objects.get(uid=relation['target'],
                                                  manager=manager)
                except Resource.DoesNotExist:
                    logger.error('No resource with'
                                 ' uid {} found'.format(relation['target']))
                    continue
                resource = {
                    'kind': relation['kind'],
                    'manager': manager,
                    'source': source,
                    'target': target
                }
                res, created = Relationship.objects.get_or_create(**resource)
                if created:
                    res.save()

    def to_dict(self):
        return {
            'name': self.name,
            'kind': self.kind,
            'timestamp': self.timestamp,
            'resource_types': self._get_resource_types(),
            'resources': self.resources,
            'relation_types': self._get_relation_types(),
            'relations': self.relations,
        }

    def _get_resource_types(self):
        res_map = {}
        for resource_name, resource in self.resources.items():
            res_map[resource_name] = self._schema['resource'][resource_name]
        return res_map

    def resource_type_list(self):
        res_list = []
        for resource in self._schema['resource']:
            res_list.append(resource)
        return res_list

    def _get_relation_types(self):
        rel_map = {}
        for relation_name, relation in self.relations.items():
            rel_map[relation_name] = self._schema['relation'][relation_name]
        return rel_map

    def _get_resource_mapping(self):
        if self._reverse_map is None:
            self._reverse_map = {}
            for resource_name, resource in self._schema['resource'].items():
                self._reverse_map[resource['resource']] = resource_name
        return self._reverse_map

    def _create_resource(self, uid, name, kind, metadata={}):
        if kind not in self.resources:
            self.resources[kind] = {}
        self.resources[kind][uid] = {
            'uid': uid,
            'name': name,
            'kind': kind,
            'metadata': metadata,
        }

    def _create_relation(self, kind, source, target):
        if kind not in self.relations:
            self.relations[kind] = []
        self.relations[kind].append({
            'source': source,
            'target': target,
            'kind': kind,
        })
