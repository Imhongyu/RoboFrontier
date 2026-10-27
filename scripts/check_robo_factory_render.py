"""Retired Classic image diagnostic; factory images now use Cycles."""
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.error('The Classic factory image diagnostic has been retired; render inspection views with Cycles')


if __name__ == '__main__':
    main()
