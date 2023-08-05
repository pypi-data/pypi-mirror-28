import json
import certifi
from elasticsearch import Elasticsearch as ES
from elasticsearch.exceptions import ConflictError

class ElasticSearchDocumentModel(object):
    def __init__(self, index, doc_type, doc_id, body):
        self._index = index
        self._doc_type = doc_type
        self._doc_id = doc_id
        self._body = body

    @property
    def index(self):
        return self._index

    @property
    def doc_type(self):
        return self._doc_type
    
    @property
    def doc_id(self):
        return self._doc_id

    @property
    def body(self):
        return self._body

    def to_json(self):
        self.__dict__

    def to_str(self):
        json.dumps(self.__dict__)

class Search(object):
    def __init__(self):
        pass

    def upsert_document(self, doc):
        raise NotImplementedError

    def delete_document(self, id):
        raise NotImplementedError

class ElasticSearch(Search):
    def __init__(self, host):
        self._client = ES(hosts=[host], ca_certs=certifi.where())

    def upsert_document(self, doc):
        try:
            return self._client.create(index=doc.index,
                                       doc_type=doc.doc_type,
                                       id=doc.doc_id,
                                       body=doc.body)
        except ConflictError:
            return self._client.update(index=doc.index,
                                       doc_type=doc.doc_type,
                                       id=doc.doc_id,
                                       body={"doc":doc.body})
        except Exception:
            return False

    def delete_document(self, id):
        #TODO: add delete document function
        return False