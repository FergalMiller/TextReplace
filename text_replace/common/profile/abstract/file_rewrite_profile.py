from abc import ABC, abstractmethod

from text_replace.common.profile.abstract.profile import Profile


class FileRewriteProfile(Profile, ABC):
    """
    FileRewriteProfile is an abstract profile that carries out rewriting on a single target file path.
    """
    @abstractmethod
    def run(self, target_file_path): pass
