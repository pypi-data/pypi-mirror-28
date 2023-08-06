import os.path

from appdirs import user_cache_dir

from fac.files import JSONFile
from fac.api import DEFAULT_ORDER


class DB:
    # name -> (key, reversed)
    SORT_KEYS = dict(
        alpha=('name', False),
        updated=('updated_at', True),
        top=('downloads_count', True),
    )

    def __init__(self, api, use_only_api=False):
        self.api = api
        self.use_only_api = use_only_api
        self.db = JSONFile(os.path.join(
            user_cache_dir('fac', appauthor=False),
            'mods.json'
        ))
        if not self.db.get('mods'):
            self.db.mods = {}

        if not self.db.get('last_update'):
            self.db.last_update = None

    def update(self):
        if self.db.last_update is None:
            page_size = 'max'
        else:
            page_size = None

        updated = None
        for mod in self.api.search('', page_size=page_size, order='updated'):
            if updated is None:
                updated = mod.updated_at

            if self.db.last_update and mod.updated_at <= self.db.last_update:
                break

            self.db.mods[mod.name] = mod

        self.db.last_update = updated
        self.db.save()

    def search(self, *args, **kwargs):
        if self.use_only_api:
            return self.api.search(*args, **kwargs)
        else:
            return self.db_search(*args, **kwargs)

    def db_search(self,
                  query, tags=[],
                  order=None,
                  page_size=None,
                  page_count=None,
                  page=1,
                  limit=0):

        order = order or DEFAULT_ORDER
        sort_key, sort_reverse = self.SORT_KEYS[order]

        def sort(e):
            item = e[sort_key]

            if isinstance(item, str):
                return item.lower()
            else:
                return item

        matches = list(sorted(
            self.get_matches(query, tags),
            key=sort,
            reverse=sort_reverse
        ))

        matches = matches[(page - 1) * page_size:]
        if limit > 0:
            matches = matches[:limit]
        return matches

    def get_matches(self, query, tags):
        query = query.lower()
        for name in self.db.mods:
            mod = self.db.mods[name]
            if any(tag not in [mt.name for mt in mod.tags] for tag in tags):
                continue

            if (query in name.lower()
                    or query in mod.title.lower()
                    or query in mod.summary.lower()):
                yield mod

    def get_releases(game_version, mod):
