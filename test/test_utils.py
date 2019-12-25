import os


class TestUtils:
    @staticmethod
    def create_resource_file():
        open(TestUtils.get_resource_path(), 'w').close()

    @staticmethod
    def destroy_resource_file():
        os.remove(TestUtils.get_resource_path())

    @staticmethod
    def overwrite_resource_file_content(content: str):
        with open(TestUtils.get_resource_path(), 'w') as resource:
            return resource.write(content)

    @staticmethod
    def append_resource_file_content(content: str):
        with open(TestUtils.get_resource_path(), 'a') as resource:
            return resource.write(content)

    @staticmethod
    def fetch_resource_file_content() -> str:
        with open(TestUtils.get_resource_path(), 'r') as resource:
            return resource.read()

    @staticmethod
    def get_resource_path(): return "TEST__RESOURCE__FILE.txt"
