import os

from hypothesis import settings
from hypothesis.database import (
    DirectoryBasedExampleDatabase,
    GitHubArtifactDatabase,
    MultiplexedDatabase,
    ReadOnlyDatabase,
)

local = DirectoryBasedExampleDatabase(".hypothesis/examples")
shared = ReadOnlyDatabase(GitHubArtifactDatabase("agucova", "spidermatch"))

settings.register_profile("ci", database=local)
settings.register_profile("dev", database=MultiplexedDatabase(local, shared))
settings.load_profile("ci" if os.environ.get("CI") else "dev")
