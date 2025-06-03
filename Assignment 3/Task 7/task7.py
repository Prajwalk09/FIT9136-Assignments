# This function should be taken from task 6
import binh_chess


def read_pgn(file_name: str) -> list[dict]:
    """
    This function is used to read the contents of the PGN file, whose name is given to this function as an input.

    Parameters:
        file_name(str): A string value denoting the name of the PGN file to be read

    Returns:
        This function returns a list of dictionaries.
    """
    all_games = []

    game_tags = {
        'Event': 'event',
        'White': 'white',
        'Black': 'black',
        'Result': 'result',
        'WhiteElo': 'whiteelo',
        'BlackElo': 'blackelo',
        'Opening': 'opening'
    }

    with open(file_name, 'r') as input_file:
        lines = [line.strip('\n') for line in input_file]

        i = 0
        total_lines = len(lines)

        while i < total_lines:
            if lines[i].strip() == '':
                i += 1
                continue

            headers = {}
            while i < total_lines and lines[i].strip() != '':
                line = lines[i].strip()

                if line.startswith('[') and line.endswith(']'):

                    space_index = line.find(' ')

                    if 0 < space_index < len(line):

                        tag_name = line[1:space_index]

                        first_quote_index = line.find('"')
                        last_quote_index = line.rfind('"')

                        if 0 <= first_quote_index < last_quote_index:

                            tag_value = line[first_quote_index + 1: last_quote_index]

                            if tag_name in game_tags:
                                headers[game_tags[tag_name]] = tag_value
                i += 1

            i += 1
            if i >= total_lines:
                break

            moves_line = lines[i].strip()
            i += 1

            tokens = moves_line.split()

            move_tokens = []
            for token in tokens:
                if not token.endswith('.'):
                    move_tokens.append(token)

            if move_tokens and move_tokens[-1] in ('1-0', '0-1', '1/2-1/2'):
                move_tokens = move_tokens[:-1]

            moves_dictionary = {}
            for round_number in range(1, 21, 1):
                moves_dictionary[f'w{round_number}'] = '-'
                moves_dictionary[f'b{round_number}'] = '-'

            for index, move in enumerate(move_tokens):

                round_number = (index // 2) + 1
                if round_number > 20:
                    break
                if index % 2 == 0:
                    moves_dictionary[f"w{round_number}"] = move
                else:
                    moves_dictionary[f"b{round_number}"] = move

            for key in game_tags.values():
                if key not in headers:
                    headers[key] = '-'

            game_entries = {
                'event': headers['event'],
                'white': headers['white'],
                'black': headers['black'],
                'result': headers['result'],
                'whiteelo': headers['whiteelo'],
                'blackelo': headers['blackelo'],
                'opening': headers['opening']
            }
            game_entries.update(moves_dictionary)
            all_games.append(game_entries)

        return all_games


# Part 1
def count_positions(moves: list[str], depth: int) -> int:
    """
    This function returns the total number of legal positions which are reachable at exactly
    depth from the position defined by moves.
    :param moves: a list of legal moves from the starting position
    :param depth: number of additional half moves to explore
    :return: an integer value which represents all legal continuations
    """
    def recursive_function(current_moves, d):

        if d == 0:
            # Base case, if d == 0 return 1
            return 1
        else:
            total = 0
            next_moves = binh_chess.possible_moves(current_moves)

            for move in next_moves:
                current_moves.append(move)
                total += recursive_function(current_moves, d - 1)
                current_moves.pop()

            return total

    return recursive_function(moves.copy(), depth)


# Part 2
def winning_statistics(file_name: str, depth: int, tolerance: int) -> tuple[int, list[str]]:
    """
    Out of all the games in the PGN file, finds a sequence of depth half moves from the starting position
    that:
        1. Appears in the least tolerance games
        2. Maximises white's win probability

    :param file_name: String value denoting the name of the file
    :param depth: an integer value denoting depth
    :param tolerance:an integer value denoting tolerance
    :return: a tuple containing best_win_probability, best_sequence and total_games for best sequence
    """
    game_dictionary = read_pgn(file_name)

    games = []
    for game in game_dictionary:
        game_list = []
        for i in range(1, 21):
            white_key = f"w{i}"
            black_key = f"b{i}"

            white_move = game.get(white_key)
            black_move = game.get(black_key)

            if white_move != '-':
                game_list.append(white_move)

            if black_move != '-':
                game_list.append(black_move)
        game_result = game.get('result')
        games.append((game_list, game_result))

    best_overall = (0.0, [], 0)

    def recursive_function(prefix, remaining_depth):
        nonlocal best_overall
        matching_games = []

        for g_list, g_result in games:
            if len(g_list) < len(prefix):
                continue
            if g_list[:len(prefix)] == prefix:
                matching_games.append((g_list, g_result))

        total_matches = len(matching_games)

        if total_matches < tolerance:
            return

        if remaining_depth == 0:
            white_wins = 0
            for index, result in matching_games:
                if result == '1-0':
                    white_wins += 1
            win_probability = white_wins / total_matches
            if win_probability > best_overall[0]:
                best_overall = (win_probability, prefix.copy(), total_matches)
            return

        next_moves = {}
        for g_list, i in matching_games:
            if len(g_list) > len(prefix):
                move = g_list[len(prefix)]
                next_moves[move] = next_moves.get(move, 0) + 1

        for move in next_moves:
            prefix.append(move)
            recursive_function(prefix, remaining_depth - 1)
            prefix.pop()

    recursive_function([], depth)

    return best_overall


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    pass
