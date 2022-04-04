import argparse
import api

def parse_args():

  parser = argparse.ArgumentParser(description="Regular Disclosure Crawler", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--year", default=2021, type=int, dest="year") 
  parser.add_argument("--month", default=12, type=int, dest="month")
  parser.add_argument("--start_page", default=1, type=int, dest="start_page")

  return parser.parse_args()


def main():
  args = parse_args()
  api.saveBranchTables(args)

if __name__ == '__main__':
  main()