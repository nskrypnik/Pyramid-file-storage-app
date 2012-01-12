from boto.s3.connection import S3Connection

DEFAULT_BUCKET = 'dropline_test'


class FileStorage(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 bucket=DEFAULT_BUCKET):
        connection = S3Connection(aws_access_key_id, aws_secret_access_key)
        self.bucket = connection.get_bucket(bucket)

    def set_file(self, key_name, contents):
        if self.bucket.get_key(key_name):
            return False
        key = self.bucket.new_key(key_name)
        key.set_contents_from_string(contents)
        return True

    def get_file(self, key_name):
        key = self.bucket.get_key(key_name)
        if key:
            return key.get_contents_as_string()
        else:
            return None
