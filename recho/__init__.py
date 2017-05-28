from pbr.version import VersionInfo

__version__ = VersionInfo('recho').semantic_version().release_string()
