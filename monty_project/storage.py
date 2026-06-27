from whitenoise.storage import CompressedManifestStaticFilesStorage


class SelectiveHashStorage(CompressedManifestStaticFilesStorage):
    # Don't hash flag files, breaks with django-countries + WHITENOISE_KEEP_ONLY_HASHED_FILES
    def hashed_name(self, name, content=None, filename=None):
        if name.startswith("flags/"):
            return name
        return super().hashed_name(name, content, filename)
