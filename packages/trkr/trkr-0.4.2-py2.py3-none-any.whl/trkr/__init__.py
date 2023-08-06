'''
Usage:
  trkr <command> <flags>

Commands:
  run             Runs the tracker
  setup           Launches the setup script
'''

import sys
import argparse

from trkr.run import main as run
from trkr.setup import main as setup

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("command")
  parser.add_argument("--gtm", help="use git-time-metric", action="store_true")
  args = parser.parse_args()

  method = globals().get(args.command)
  if not method:
    print(__doc__)
  else:
    method(gtm=args.gtm)
