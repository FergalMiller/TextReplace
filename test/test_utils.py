import os


class TestUtils:
    @staticmethod
    def create_resource_file(resource_file_path: str):
        open(resource_file_path, 'w').close()

    @staticmethod
    def destroy_resource_file(resource_file_path: str):
        os.remove(resource_file_path)

    @staticmethod
    def overwrite_resource_file_content(resource_file_path: str, content: str):
        with open(resource_file_path, 'w') as resource:
            return resource.write(content)

    @staticmethod
    def append_resource_file_content(resource_file_path:str, content: str):
        with open(resource_file_path, 'a') as resource:
            return resource.write(content)

    @staticmethod
    def fetch_resource_file_content(resource_file_path: str) -> str:
        with open(resource_file_path, 'r') as resource:
            return resource.read()
