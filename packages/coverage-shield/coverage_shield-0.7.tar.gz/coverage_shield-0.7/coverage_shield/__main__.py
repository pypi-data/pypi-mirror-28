import argparse
import os
import sys

import coverage

import coverage_shield.slug as slug
from coverage_shield.badges import upload


def total(cov: coverage.Coverage) -> float:
    with open(os.devnull, "w") as f:
        return cov.report(file=f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="Where to post badge data", default='https://badges-io.now.sh')
    parser.add_argument("--user", help="User part of slug. Defaults to autodetect")
    parser.add_argument("--repo", help="Repo part of slug. Defaults to autodetect")
    args = parser.parse_args()

    cov = coverage.Coverage()
    cov.load()
    c = total(cov)

    auto_user, auto_repo = slug.autodetect()
    user, repo = args.user or auto_user, args.repo or auto_repo
    if user and repo:
        svg = upload(args.url, user, repo, "coverage", "{0:.0f}%".format(c), "green")
        print(svg)
    else:
        print("Could not auto detect slug and --user and --repo not given", file=sys.stderr)
        sys.exit(-1)


if __name__ == "__main__":
    main()
