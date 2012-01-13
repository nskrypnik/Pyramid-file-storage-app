from boto.s3.connection import S3Connection

DEFAULT_BUCKET = 'dropline_test'


class FileStorage(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 bucket=DEFAULT_BUCKET):
        connection = S3Connection(aws_access_key_id, aws_secret_access_key)
        self.bucket = connection.get_bucket(bucket)

    def send_file(self, key_name, contents, content_type=None, rewrite=False):
        if not rewrite and self.bucket.get_key(key_name):
            return False
        key = self.bucket.new_key(key_name)
        headers = None
        if content_type:
            headers = {}
            headers['Content-Type'] = content_type
        key.set_contents_from_string(contents, headers=headers)
        return True

    def get_file(self, key_name):
        key = self.bucket.get_key(key_name)
        if key:
            return key.get_contents_as_string()
        else:
            return None

    def generate_url(self, key_name, expires_in):
        return self.bucket.connection.generate_url(expires_in,
                                                   method='GET',
                                                   bucket=self.bucket.name,
                                                   key=key_name,
                                                   headers=None,
                                                   query_auth=True,
                                                   force_http=False,
                                                   response_headers=None)
