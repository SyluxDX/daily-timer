import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Daily standup Timer')
    # add arguments
    parser.add_argument('-c', '--config', help='Path to configuration json override')
    parser.add_argument('time', nargs='?', type=int, help='Time limit for each participant, if not provided will operate as stopwatch')
    parser.add_argument('-w', '--warning', type=int, help='Warning time, if not profided defaults to 1/3 of time limit')

    parser.add_argument('-p', '--participants', nargs='+', help='List of participants')
    parser.add_argument('-s', '', help='--sequencial', action='store_true', help='Use ')

    ARGS = parser.parse_args()
    print("asdasd")
    print(ARGS.limit)
    print(ARGS.time)
    print(ARGS.participants)