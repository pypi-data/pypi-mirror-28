import datetime
import click
import requests
import sys
from tinydb import TinyDB, Query
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from terminaltables import SingleTable


@click.group()
def cli():
    """Welcome to cryptoprice!
        For further information about commands, use the --help
        flag along with the command.
        Ex: cryptoprice price --help
    """
    pass

# Price command
@click.command()
@click.option('--nocolor', is_flag=True, default=False, help="Disable colorized output.")
@click.option('--table', is_flag=True, default=False, help="Show output in a neat table.")
@click.option('--nousd', is_flag=True, default=False, help="Hide price in USD.")
@click.option('--btc', is_flag=True, default=False, help="Show price in BTC.")
@click.option('--rank', is_flag=True, default=False, help="Show coin rank.")
@click.option('--all', 'allcoins', is_flag=True, default=False, help="Show top 100 coins according to market capital.")
@click.option('--volume', is_flag=True, default=False, help="Show volume traded in 24 hours.")
@click.option('--marketcap', is_flag=True, default=False, help="Show coin market capital.")
@click.option('--change1h', is_flag=True, default=False, help="Show change in the past 1 hour.")
@click.option('--change24h', is_flag=True, default=False, help="Show change in the past 24 hours.")
@click.option('--change7d', is_flag=True, default=False, help="Show change in the past 7 days")
@click.argument('coins', nargs=-1)
def price(nocolor, table, coins, nousd, btc, rank, allcoins, volume, marketcap, change1h, change24h, change7d):
    """Command to view information about cryptocurrencies"""

    response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    crypto_data = response.json()
    crypto_data_map = {}  # Dictionary for faster access
    all_coins = []  # List of all coin names

    for crypto in crypto_data:
        all_coins.append(crypto['symbol'])
        crypto_data_map[crypto['symbol']] = crypto

    # Print table if specified
    table_data = []
    table_headers = ['Name']
    if(not nousd):
        table_headers.append('USD')
    if(btc):
        table_headers.append('BTC')
    if(rank):
        table_headers.append('Rank')
    if(volume):
        table_headers.append('Volume')
    if(marketcap):
        table_headers.append('Market Cap')
    if(change1h):
        table_headers.append('% Change 1H')
    if(change24h):
        table_headers.append('% Change 24H')
    if(change7d):
        table_headers.append('% Change 7D')
    table_data.append(table_headers)

    # if --all or no coin is specified, list all
    if allcoins or not coins:
        coins = all_coins

    for coin in coins:
        if not coin.upper() in crypto_data_map:
            continue

        coin_data = crypto_data_map[coin.upper()]

        table_row = []

        coin_info = coin_data['name'] + " (" + coin_data['symbol'] + ")"
        table_row.append(coin_info)

        if(not nousd):
            coin_info += " | USD: " + coin_data['price_usd']
            table_row.append(coin_data['price_usd'])

        if(btc):
            coin_info += " | BTC: " + coin_data['price_btc']
            table_row.append(coin_data['price_btc'])

        if(rank):
            coin_info += " | Rank: " + coin_data['rank']
            table_row.append(coin_data['rank'])

        if(volume):
            coin_info += " | Volume: " + coin_data['24h_volume_usd']
            table_row.append(coin_data['24h_volume_usd'])

        if(marketcap):
            coin_info += " | Market Cap: " + coin_data['market_cap_usd']
            table_row.append(coin_data['market_cap_usd'])

        if(change1h):
            perc_change = coin_data['percent_change_1h']
            if not nocolor:
                if float(perc_change) > 0:
                    perc_change = click.style(perc_change, fg='green')
                else:
                    perc_change = click.style(perc_change, fg='red')

            coin_info += " | % Change 1H: " + perc_change
            table_row.append(perc_change)

        if(change24h):
            perc_change = coin_data['percent_change_24h']
            if not nocolor:
                if float(perc_change) > 0:
                    perc_change = click.style(perc_change, fg='green')
                else:
                    perc_change = click.style(perc_change, fg='red')

            coin_info += " | % Change 24H: " + perc_change
            table_row.append(perc_change)

        if(change7d):
            perc_change = coin_data['percent_change_7d']
            if not nocolor:
                if float(perc_change) > 0:
                    perc_change = click.style(perc_change, fg='green')
                else:
                    perc_change = click.style(perc_change, fg='red')

            coin_info += " | % Change 7D: " + perc_change
            table_row.append(perc_change)

        table_data.append(table_row)

        if(not table):
            click.echo(coin_info)

    if(table):
        term_table = SingleTable(table_data)
        click.echo(term_table.table)


# Portfolio tools
@click.command()
@click.option('--nocolor', is_flag=True, default=False, help="Disable colorized output.")
@click.option('--value', is_flag=True, default=False, help="Show portfolio value in USD.")
@click.option('--profit', is_flag=True, default=False, help="Show total profit in USD.")
@click.argument('cmd', type=click.Choice(['add', 'remove', 'history', 'clear']), nargs=1, required=False)
def portfolio(cmd, nocolor, value, profit):
    """Command to manage your local portfolio"""

    # Database
    db = TinyDB('db.json')

    # Add transaction
    if cmd == 'add':
        click.echo('Add new transaction')

        response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
        crypto_data = response.json()
        crypto_data_map = {}  # Dictionary for faster access
        all_coins = []  # List of all coin names

        for crypto in crypto_data:
            all_coins.append(crypto['symbol'])
            crypto_data_map[crypto['symbol']] = crypto

        # buy/sell transaction
        tx_type_completer = WordCompleter(['buy', 'sell'], ignore_case=True)
        tx_type = prompt('type (buy/sell) > ', completer=tx_type_completer)

        while not (tx_type.lower() == 'buy' or tx_type.lower() == 'sell'):
            click.secho('ERROR: invalid transaction type', fg='red')
            tx_type = prompt('type (buy/sell) > ', completer=tx_type_completer)

        # coin type
        tx_coin_completer = WordCompleter(all_coins, ignore_case=True)
        tx_coin = prompt('coin > ', completer=tx_coin_completer)

        while tx_coin not in all_coins:
            click.secho('ERROR: coin does not exist in list', fg='red')
            tx_coin = prompt('coin > ', completer=tx_coin_completer)

        # buy/sell price
        tx_coin_price = prompt(
            tx_type + ' price per coin (leave blank to use market price) > ')
        if not tx_coin_price and tx_coin_price != 0:
            tx_coin_price = crypto_data_map[tx_coin]['price_usd']

        # amount
        tx_amount = prompt('amount > ')

        while not tx_amount:
            click.secho('ERROR: invalid amount')
            tx_amount = prompt('amount > ')

        # date
        tx_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # coin market value
        coin_market_price = crypto_data_map[tx_coin]['price_usd']

        # calculate tx ID
        db_transactions = db.all()
        if not db_transactions:
            tx_id = 0x1
        else:
            db_transactions = sorted(
                db_transactions, key=lambda k: k['id'], reverse=True)
            tx_id = db_transactions[0]['id'] + 0x1

        tx_info = {
            'type': tx_type.upper(),
            'coin': tx_coin,
            'price': float(tx_coin_price),
            'amount': float(tx_amount),
            'date': tx_date,
            'id': tx_id
        }

        db.insert(tx_info)

        hodl_change = float(tx_amount) * float(coin_market_price)
        if(tx_type.lower() == 'buy'):
            hodl_change = click.style('+' + str(hodl_change), fg='green')
        if(tx_type.lower() == 'sell'):
            hodl_change = click.style('-' + str(hodl_change), fg='red')

        tx_info_table = [
            ['ADDED TRANSACTION'],
            ['Type', tx_type.upper()],
            ['Coin', tx_coin],
            ['Price ($)', tx_coin_price],
            ['Amount', tx_amount],
            ['Timestamp', tx_date],
            ['ID', tx_id],
            ['Δ holdings', hodl_change]
        ]

        click.echo(SingleTable(tx_info_table).table)

    # Remove transaction
    if cmd == 'remove':
        if not sys.stdin.isatty():
            remove_tx_tuple = sys.stdin.readline()
        else:
            remove_tx_tuple = prompt('remove transactions > ')

        if not remove_tx_tuple:
            return

        remove_tx_tuple = tuple(int(x.strip())
                                for x in remove_tx_tuple.split(','))

        transaction = Query()
        removed_ids = []
        for tx_id in remove_tx_tuple:
            if db.search(transaction.id == tx_id):
                removed_ids.append(tx_id)
                db.remove(transaction.id == tx_id)

        if removed_ids:
            click.echo('Removed transaction(s): ' + str(tuple(removed_ids)))
        else:
            click.echo('No transactions were removed')

    # Clear transaction database
    if cmd == 'clear':
        if not db.all():
            click.echo('There are no transactions to delete')
            return

        decision = prompt(
            'are you sure you want to clear all transactions? (y/n) > ')

        if decision.lower() == 'y':
            db.purge()
            click.echo('DELETED ALL TRANSACTIONS')

    # Print all transactions
    if cmd == 'history':
        db_transactions = db.all()

        if not db_transactions:
            click.echo('There are no transactions to display')
            return

        for tx in db_transactions:
            if(tx['type'] == 'BUY'):
                tx_type = click.style(tx['type'], fg='green')
            if(tx['type'] == 'SELL'):
                tx_type = click.style(tx['type'], fg='red')

            tx_info_table = [
                ['Type', tx_type],
                ['Coin', tx['coin']],
                ['Price ($)', tx['price']],
                ['Amount', tx['amount']],
                ['Timestamp', tx['date']],
                ['ID', tx['id']]
            ]

            table = SingleTable(tx_info_table)
            table.inner_heading_row_border = False
            click.echo(table.table)

    # Display portfolio data
    if not cmd:

        if not db.all():
            click.echo('Your portfolio is empty.')
            return

        response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
        crypto_data = response.json()
        crypto_data_map = {}  # Dictionary for faster access
        all_coins = []  # List of all coin names

        for crypto in crypto_data:
            all_coins.append(crypto['symbol'])
            crypto_data_map[crypto['symbol']] = crypto

        total_hodlings_usd = 0
        investment_usd = 0
        all_coin_info = {}

        for tx in db.all():

            if tx['coin'] in all_coin_info:
                coin_info = all_coin_info[tx['coin']]
            else:
                all_coin_info[tx['coin']] = coin_info = {
                    'amount': 0,
                    'investment': 0,
                    'profit': 0
                }

            if tx['type'] == 'BUY':
                modifier = 1
            elif tx['type'] == 'SELL':
                modifier = -1

            total_hodlings_usd += modifier * \
                tx['amount'] * float(crypto_data_map[tx['coin']]['price_usd'])
            investment_usd += modifier * tx['amount'] * tx['price']
            coin_info['amount'] += modifier * tx['amount']
            coin_info['investment'] += modifier * tx['amount'] * tx['price']

            all_coin_info[tx['coin']] = coin_info

        # Calculate profit for each coin
        for key in all_coin_info:
            coin_info = all_coin_info[key]
            coin_info['coin'] = key
            coin_info['profit'] = coin_info['amount'] * float(
                crypto_data_map[key]['price_usd']) - coin_info['investment']

        all_coin_info = all_coin_info.values()
        all_coin_info = sorted(
            all_coin_info, key=lambda k: k['profit'], reverse=True)

        # Calculate profits
        port_profit = round(total_hodlings_usd - investment_usd, 5)
        if not nocolor:
            if port_profit > 0: port_profit = click.style(str(port_profit), fg='green')
            elif port_profit < 0: port_profit = click.style(str(port_profit), fg='red')

        min_info = ''
        if value:
            min_info += 'Value: ' + str(round(total_hodlings_usd, 5)) + ' '

        if profit:
            min_info += 'Profit: ' + str(port_profit)

        if value or profit:
            click.echo(min_info + '\n')
            return

        # Individual coin value and profit table
        coin_table = [
            ['Coin', 'Amount', 'Investment ($)', 'Profit ($)'],
        ] + [
            [
                coin_info['coin'],
                round(coin_info['amount'], 5),
                round(coin_info['investment'], 5),
                click.style(str(round(coin_info['profit'], 5)), fg='green') if coin_info['profit'] > 0 else click.style(str(round(coin_info['profit'], 5)), fg='red') if not nocolor or (coin_info['profit'] == 0) else round(coin_info['profit'], 5)
            ] for coin_info in all_coin_info
        ]

        table = SingleTable(coin_table)
        table.inner_row_border = True
        table.inner_heading_row_border = False
        click.echo(table.table)

        # Portfolio value and profit table
        total_table = [
            ['Portfolio Value ($)', round(total_hodlings_usd, 5)],
            ['Investment ($)', round(investment_usd, 5)],
            ['Profit ($)', str(port_profit)],
        ]

        table = SingleTable(total_table)
        table.inner_row_border = True
        table.inner_heading_row_border = False
        click.echo(table.table)

cli.add_command(price)
cli.add_command(portfolio)