from abc import ABC, abstractmethod

from text_replace.common.profile.abstract.profile import Profile
from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile


class RunProfile(Profile, ABC):
    """
    RunProfile is an abstract class that accepts and invokes a FileRewriteProfile.
    """
    @abstractmethod
    def run(self, file_rewrite_profile: FileRewriteProfile): pass
