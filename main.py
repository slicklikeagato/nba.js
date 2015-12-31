import requests
import sys
import html
from datetime import date as d

URL = 'http://data.nba.com/data/json/cms/noseason/scoreboard/{0}/games.json'

date = d.today().strftime('%Y%m%d') if len(sys.argv) == 1 else sys.argv[1]


def serve(date):
    games = parse(fetch(date))
    if len(games) == 0:  # no games
        return 'No games for provided date'

    prompt = ''
    for i in range(len(games)):
        game_str = '{0}: {1} @ {2}'
        prompt += game_str.format(i + 1, games[i]['visitor']['abbr'], games[i]['home']['abbr'])
        prompt += '\n'
    prompt += str(len(games) + 1) + ': All\n'
    choice = int(input(prompt))

    if choice == len(games) + 1:
        return '\nAll scores for ' + date + '\n' + html.unescape(prep_all(games))
    else:
        return '\n' + html.unescape(prep_single(games[choice - 1]))


def fetch(date):
    return requests.get(URL.format(date)).json()


def parse(response):
    games = []

    for game in response['sports_content']['games']['game']:

        g = {}
        g['loc'] = '{0} - {1}, {2}'.format(game['arena'], game['city'], game['state'])
        g['period_status'] = game['period_time']['period_status']
        g['game_clock'] = game['period_time']['game_clock']
        g['visitor'] = {
            'abbr': game['visitor']['abbreviation'],
            'city': game['visitor']['city'],
            'name': game['visitor']['nickname'],
            'score': game['visitor']['score']
        }
        g['home'] = {
            'abbr': game['home']['abbreviation'],
            'city': game['home']['city'],
            'name': game['home']['nickname'],
            'score': game['home']['score']
        }
        games.append(g)
    return games


def prep_all(games):
    output = ''
    for game in games:
        output += '\n' + prep_single(game) + '\n' + ('-' * 25)
    return output


def prep_single(game):
    line = '{0} {1} @ {2} {3}\n{4}\n\n{5} {6} - {7} {8} {9} {10}'
    return line.format(
        game['visitor']['city'], game['visitor']['name'],
        game['home']['city'], game['home']['name'],
        game['loc'],
        game['visitor']['abbr'], game['visitor']['score'],
        game['home']['abbr'], game['home']['score'],
        game['period_status'], game['game_clock']
    )

if __name__ == '__main__':
    print(serve(date))
