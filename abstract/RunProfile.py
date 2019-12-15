from abc import ABC, abstractmethod

from abstract.Profile import Profile
from abstract.FileRewriteProfile import FileRewriteProfile


class RunProfile(Profile, ABC):

    @abstractmethod
    def run(self, file_rewrite_profile: FileRewriteProfile): pass
