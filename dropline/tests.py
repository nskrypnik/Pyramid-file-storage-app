import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'dropline')

    def test_filestorage(self):
        import os
        from paste.deploy.loadwsgi import appconfig
        from filestorage import FileStorage
        config = appconfig('config:test.ini', 'main', relative_to='.')
        aws_access_key_id     = config['aws.access_key_id']
        aws_secret_access_key = config['aws.secret_access_key']
        bucket                = config['s3.test_bucket']
        fs = FileStorage(aws_access_key_id, aws_secret_access_key, bucket)
        key_name = 'testfile.txt'
        string_length = 2000
        data = os.urandom(string_length)
        self.assertTrue(fs.set_file(key_name, data, rewrite=True))
        self.failUnlessEqual(fs.get_file(key_name), data)
        new_data = os.urandom(string_length)
        self.failIfEqual(data, new_data)
        self.assertTrue(fs.set_file(key_name, new_data, rewrite=True))
        self.failUnlessEqual(fs.get_file(key_name), new_data)
        data = os.urandom(string_length)
        self.failIfEqual(new_data, data)
        self.assertFalse(fs.set_file(key_name, data))
