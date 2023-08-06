# -*- coding: utf-8 -*-
import mimetypes
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import InvalidXMLError, InvalidEndpointError,  NoSuchKey, NoSuchBucket
from urllib3.exceptions import MaxRetryError


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


@deconstructible
class MinioStorage(Storage):
    # TODO: Log errors caused by exceptions
    server = setting('MINIO_SERVER')
    access_key = setting('MINIO_ACCESSKEY')
    secret_key = setting('MINIO_SECRET')
    bucket = setting('MINIO_BUCKET')
    secure = setting('MINIO_SECURE')

    def __init__(self, *args, **kwargs):
        super(MinioStorage, self).__init__(*args, **kwargs)
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            try:
                self._connection = Minio(
                    self.server, self.access_key, self.secret_key, self.secure)
            except InvalidEndpointError:
                self._connection = None
        return self._connection

    def _save(self, name, content):
        pathname, ext = os.path.splitext(str(name.encode('utf-8')))
        dir_path, file_name = os.path.split(pathname)
        hashed_name = "{0}/{1}{2}".format(dir_path, hash(content), ext)
        if hasattr(content.file, 'content_type'):
            content_type = content.file.content_type
        else:
            content_type = mimetypes.guess_type(name.encode('utf-8'))[0]
        if self.connection:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            try:
                self.connection.put_object(
                    self.bucket, hashed_name, content, content.file.size, content_type=content_type
                )
            except InvalidXMLError:
                pass
            except MaxRetryError:
                pass
        return hashed_name  # TODO: Do not return name if saving was unsuccessful

    def url(self, name):
        if self.connection:
            try:
                if self.connection.bucket_exists(self.bucket):
                    return self.connection.presigned_get_object(self.bucket, name.encode('utf-8'))
                else:
                    return "image_not_found"  # TODO: Find a better way of returning errors
            except MaxRetryError:
                return "image_not_found"
        return "could_not_establish_connection"

    def exists(self, name):
        try:
            self.connection.stat_object(self.bucket, name.encode('utf-8'))
            return True
        except (NoSuchKey, NoSuchBucket):
            return False
        except Exception as err:
            raise IOError("Could not stat file {0} {1}".format(name, err))

    def size(self, name):
        info = self.connection.stat_object(self.bucket, name.encode('utf-8'))
        return info.size
