# This file is part of filestore-gs. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import uuid

from google.cloud import storage
from trytond.config import config
from trytond.filestore import FileStore


class FileStoreGS(FileStore):

    def __init__(self):
        client = storage.Client()
        self.bucket = client.get_bucket(config.get('database', 'bucket'))

    def get(self, id, prefix=''):
        blob = self.bucket.blob(name(id, prefix))
        return blob.download_as_string()

    def getmany(self, ids, prefix=''):
        with self.bucket.client.batch():
            return super(FileStoreGS, self).getmany(ids, prefix=prefix)

    def size(self, id, prefix=''):
        blob = self.bucket.blob(name(id, prefix))
        blob.reload()
        return blob.size

    def sizemany(self, ids, prefix=''):
        with self.bucket.client.batch():
            return super(FileStoreGS, self).sizemany(ids, prefix=prefix)

    def set(self, data, prefix=''):
        id = uuid.uuid4().hex
        blob = self.bucket.blob(name(id, prefix))
        blob.upload_from_string(
            bytes(data), content_type='application/octet-stream')
        return id

    def setmany(self, data, prefix=''):
        with self.bucket.client.batch():
            return super(FileStoreGS, self).setmany(data, prefix=prefix)


def name(id, prefix=''):
    return '/'.join(filter(None, [prefix, id]))
