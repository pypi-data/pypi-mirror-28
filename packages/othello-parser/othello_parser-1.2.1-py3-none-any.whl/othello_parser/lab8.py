from argparse import ArgumentParser


class Lab8Parser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        self.default_puzzle = '...........................OX......XO...........................'
        super(Lab8Parser, self).__init__(*args, **kwargs)
        self.add_argument("puzzle", nargs='?', default=self.default_puzzle)
        self.add_argument("next_player", nargs='?', default='_')
        self.add_argument("extra", nargs='*')

    def valid_puzzle(self, puzzle):
        return isinstance(puzzle, str) and len(puzzle) == 64

    def valid_player(self, player):
        return player.lower() in {'x', 'o'}

    def calc_player(self, puzzle):
        return ["X", "O"][puzzle.count('.') % 2 == 1]

    def parse_args(self, args=None, namespace=None):
        args = super(Lab8Parser, self).parse_args(args, namespace)
        set_player = (args.next_player == "_")
        if not self.valid_player(args.next_player) and not set_player:
            args.extra = [args.next_player] + args.extra
            set_player = True
        if not self.valid_puzzle(args.puzzle):
            if not self.valid_player(args.puzzle):
                args.extra = [args.puzzle] + args.extra
            else:
                args.next_player = args.puzzle.upper()
                set_player = False
            args.puzzle = self.default_puzzle
        if set_player:
            args.next_player = self.calc_player(args.puzzle)
        return args
