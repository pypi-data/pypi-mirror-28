import sys

from textwrap import fill
from shutil import get_terminal_size

from fac.utils import parse_game_version
from fac.commands import Command, Arg
from fac.api import DEFAULT_PAGE_SIZE

class SearchCommand(Command):
    'Search the mods database.'

    name = 'search'

    arguments = [
        Arg('query', help='search string', nargs='?'),

        Arg('-t', help='filter by tag', nargs='*', dest='tag', default=[]),

        Arg('-d', help='sort results by most downloaded',
            action='store_const',
            dest='sort',
            const='top',
            default='top'),

        Arg('-a', help='sort results alphabetically',
            action='store_const',
            dest='sort',
            const='alpha'),

        Arg('-u', help='sort results by most recently updated',
            action='store_const',
            dest='sort',
            const='updated'),

        Arg('-l', '--limit', type=int,
            help='stop after returning that many results'),

        Arg('-p', '--page', type=int, default=1,
            help='starting page number for the API calls'),

        Arg('-s', '--page-size', type=str,  # allow 'max' to be used
            default=DEFAULT_PAGE_SIZE,
            help='maximum number of returned results per page'),

        Arg('-c', '--page-count', type=int,
            help='maximum number of pages to fetch'),

        Arg('-F', '--format',
            help='show results using the specified format string.'),
    ]

    epilog = """
    An optional format string can be specified with the -F flag.
    You can use this if you want to customize the default output format.

    The syntax of format strings is decribed here:
    https://docs.python.org/3/library/string.html#format-string-syntax

    There is only one argument passed to the format string which is the
    result object returned by the API.

    Using the default string ('s') specifier on a JSON list or object will
    output valid JSON.

    Some examples:
        {result.name}                   Name of the mod
        {result}                        JSON-repesentation of the result object
        {result.latest_release.version} Latest release version
    """

    def run(self, args):
        hidden = 0
        count = 0
        game_ver = self.config.game_version_major

        print("Note: search functionality is currently broken due to the "
              "switch to the new mod portal and all mods will always be shown "
              "regardless of the search criteria. This shall be adressed in a "
              "future release.")

        for result in self.api.search(
                query=args.query or '',
                page=args.page,
                page_size=args.page_size,
                page_count=args.page_count,
                tags=tuple(args.tag),
                order=args.sort):

            if 'tags' in result:
                tags = [tag.name for tag in result.tags]
            else:
                tags = []

            if game_ver != parse_game_version(result.latest_release):
                if args.ignore_game_ver:
                    tags.insert(0, 'incompatible')
                else:
                    hidden += 1
                    continue

            if args.format:
                print(args.format.format(result, result=result))
            else:
                print(result.title)
                print('    Name: %s' % result.name)

                if tags:
                    print('    Tags: %s' % (', '.join(tags)))

                print()
                print('\n'.join(
                    fill(
                        line,
                        width=get_terminal_size()[0] - 4,
                        tabsize=4,
                        subsequent_indent='    ',
                        initial_indent='    ',
                    )
                    for line in result.summary.splitlines()
                ))
                print()

            count += 1
            if args.limit and count >= args.limit:
                break

        if hidden:
            print('Note: %d mods were hidden because they have no '
                  'compatible game versions. Use -i to show them.' % hidden,
                  file=sys.stderr)
