# Part 1
def read_pgn(file_name: str) -> list[dict]:
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


# Part 2
def win_loss_by_opening(games: list[dict]) -> dict:
    opening_statistics = {}

    for game in games:
        opening = game['opening']
        result = game['result']

        if opening not in opening_statistics:
            opening_statistics[opening] = [0, 0]

        white_win, black_win, draw = '1-0', '0-1', '1/2-1/2'

        if result == white_win:
            opening_statistics[opening][0] += 1
        elif result == black_win:
            opening_statistics[opening][1] += 1

    return {opening: (counts[0], counts[1]) for opening, counts in opening_statistics.items()}


# Part 3
def win_loss_by_elo(games: list[dict], lower: int, upper: int) -> tuple[int, int]:
    lower_elo_wins, higher_elo_wins = 0, 0

    for game in games:

        try:
            white_elo = int(game['whiteelo'])
            black_elo = int(game['blackelo'])
        except KeyError:
            continue
        except ValueError:
            continue

        difference = abs(white_elo - black_elo)

        if not (lower < difference < upper):
            continue

        white_is_lower = white_elo < black_elo

        game_result = game['result']
        if game_result == '1-0':

            if white_is_lower:
                lower_elo_wins += 1
            else:
                higher_elo_wins += 1

        elif game_result == '0-1':

            if white_is_lower:
                higher_elo_wins += 1
            else:
                lower_elo_wins += 1

    return lower_elo_wins, higher_elo_wins


# Part 4
def win_loss_by_moves(games: list[dict], moves: list[str]) -> tuple[int, int]:
    white_win_count = 0
    black_win_count = 0

    length_of_prefix = len(moves)

    for game in games:

        game_moves = []
        for i in range(1, 21):
            white_key = f"w{i}"
            black_key = f"b{i}"

            white_move = game.get(white_key, '-')
            if white_move != '-':
                game_moves.append(white_move)

            black_move = game.get(black_key, '-')
            if black_move != '-':
                game_moves.append(black_move)

        if len(game_moves) < length_of_prefix:
            continue

        if game_moves[0:length_of_prefix] != moves:
            continue

        result = game.get('result', '')
        if result == '1-0':
            white_win_count += 1
        elif result == '0-1':
            black_win_count += 1

    return white_win_count, black_win_count


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    pass
