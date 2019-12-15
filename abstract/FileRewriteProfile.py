from abc import ABC, abstractmethod

from abstract.Profile import Profile


class FileRewriteProfile(Profile, ABC):
    @abstractmethod
    def run(self, target_file_path): pass
