'''
Usage:
  trkr <command>

Commands:
  run             Runs the tracker
  setup           Launches the setup script
  help            Displays this message
'''

import sys
from parse import parse

from trkr.run import main as run
from trkr.setup import main as setup

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--gtm", help="use git-time-metric", action="store_true")
  args = parser.parse_args()

  if len(sys.argv) > 1:
    method = globals().get(sys.argv[1])
    if not method:
      print(__doc__)
    else:
      method(gtm=args.gtm)
  else:
    run(gtm=args.gtm)
