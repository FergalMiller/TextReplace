from abc import ABC, abstractmethod

from common.profile.abstract.Profile import Profile
from common.profile.abstract.FileRewriteProfile import FileRewriteProfile


class RunProfile(Profile, ABC):
    """
    RunProfile is an abstract class that accepts and invokes a FileRewriteProfile.
    """
    @abstractmethod
    def run(self, file_rewrite_profile: FileRewriteProfile): pass
