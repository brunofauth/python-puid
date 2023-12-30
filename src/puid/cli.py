import sys

try:
    import funparse.api as fa
except ImportError as error:
    error.add_note(
        "Did you forget to install this package with the 'cli' extra?")

from .chars import Charsets, Charset
from .puid import Puid


@fa.as_arg_parser
def cli(total: int, risk: float, charset: Charsets = Charsets.SAFE64) -> str:
    return Puid.from_risk(total=total, risk=risk, charset=charset).generate()


def main(argv=sys.argv) -> int:
    print(cli.run(sys.argv[1:]))
    return 0
