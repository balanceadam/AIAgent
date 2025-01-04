from asgiref.sync import sync_to_async
import asyncio
from collections import defaultdict
from decimal import Decimal, getcontext
from hexbytes import HexBytes

from django.core.management.base import BaseCommand
from django.db import close_old_connections
from django.db.utils import OperationalError
from django.utils.timezone import now
from web3 import Web3
from web3.middleware import geth_poa_middleware

from account.models import Account
from assets import models, utils


@sync_to_async
def handle_sync(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except OperationalError:
        close_old_connections()
        return func(*args, **kwargs)


def get_token(protocol_id):
    token = models.AssetsToken.objects.filter(protocol__protocol_id=protocol_id).first()
    if not token:
        return None, None
    return token, token.protocol


def get_account(address):
    return Account.objects.filter(walletaddress__address=address).first()


# 提高 Decimal 的精度以处理大数
getcontext().prec = 50

# 配置
INFURA_PROJECT_ID = 'cd308e5454a04fa09d2f7451cf2bf1de'  # 替换为您的Infura项目ID

# Bonding Curve 参数
A = Decimal('1073000191')
B = Decimal('32190005730')
PROGRESS_THRESHOLD = Decimal('263300') * Decimal('1e18')  # 263300 * 10^18

# 平台费用（基点）
PLATFORM_FEE_BP = Decimal('50')  # 0.5%
DEX_FEE_BP = Decimal('50')       # 0.5%

# 事件ABI定义
EVENT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "tokenId", "type": "uint256"},
            {"indexed": False, "name": "tokenAddress", "type": "address"},
            {"indexed": False, "name": "name", "type": "string"},
            {"indexed": False, "name": "symbol", "type": "string"},
            {"indexed": False, "name": "launchTime", "type": "uint256"},
            {"indexed": False, "name": "tokenCreator", "type": "address"}
        ],
        "name": "TokenCreation",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "isTokenPurchase", "type": "bool"},
            {"indexed": False, "name": "tokenId", "type": "uint256"},
            {"indexed": True, "name": "tokenAddress", "type": "address"},
            {"indexed": True, "name": "trader", "type": "address"},
            {"indexed": False, "name": "tokenAmount", "type": "uint256"},
            {"indexed": False, "name": "currencyAmount", "type": "uint256"}
        ],
        "name": "TokenTrade",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "token", "type": "address"},
            {"indexed": False, "name": "amountETH", "type": "uint256"},
            {"indexed": False, "name": "amountToken", "type": "uint256"}
        ],
        "name": "DEXPoolCreation",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "message", "type": "string"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Debug",
        "type": "event"
    }
]

# 定义数据结构来保存token信息
tokens = {}
token_stats = defaultdict(lambda: {
    'trades': [],
    'volume': Decimal('0'),
    'last_price': Decimal('0'),
    'price_change': Decimal('0')
})


# Bonding Curve 计算函数
def calculate_price(currency_collected):
    denominator = Decimal('30') * Decimal('1e18') + (currency_collected) / Decimal('3000')
    if denominator == 0:
        return Decimal('0')
    current_price = (B * Decimal('1e36')) / (denominator ** 2)
    return current_price


def update_token_stats(token_id, currency_collected, token_sold):
    price = calculate_price(Decimal(currency_collected))
    stats = token_stats[token_id]
    if stats['last_price'] != 0:
        stats['price_change'] = ((price - stats['last_price']) / stats['last_price']) * Decimal('100')
    stats['last_price'] = price
    # 根据需要实现交易量的跟踪，例如累计currency_collected或token_sold
    # 例如: stats['volume'] += currency_collected
    stats['volume'] += Decimal('0')

# 异步事件监听器
async def listen_to_events(contracts):
    # 为所有合约创建事件过滤器
    event_filters = []
    for contract in contracts:
        # event_filters.append(contract.events.TokenCreation.create_filter(fromBlock='latest'))
        event_filters.append(contract.events.TokenTrade.create_filter(fromBlock='latest'))
        # event_filters.append(contract.events.DEXPoolCreation.create_filter(fromBlock='latest'))
        # event_filters.append(contract.events.Debug.create_filter(fromBlock='latest'))

    print("正在监听事件...")

    while True:
        try:
            for event_filter in event_filters:
                for event in event_filter.get_new_entries():
                    await handle_event(event)
        except Exception as e:
            print(e)
        # await asyncio.sleep(2)  # 每2秒轮询一次
        await asyncio.sleep(30)


# 事件处理函数
async def handle_event(event):
    event_name = event.event
    if event_name == 'TokenCreation':
        handle_token_creation(event)
    elif event_name == 'TokenTrade':
        try:
            await handle_token_trade(event)
        except Exception as e:
            print(e)
    elif event_name == 'DEXPoolCreation':
        handle_dex_pool_creation(event)
    elif event_name == 'Debug':
        handle_debug(event)


def handle_token_creation(event):
    token_id = event.args['tokenId']
    token_address = event.args['tokenAddress']
    name = event.args['name']
    symbol = event.args['symbol']
    launch_time = event.args['launchTime']
    token_creator = event.args['tokenCreator']

    tokens[token_id] = {
        'tokenAddress': token_address,
        'name': name,
        'symbol': symbol,
        'creator': token_creator,
        'tokenSold': Decimal('0'),
        'currencyCollected': Decimal('0')
    }

    print(f"\n[TokenCreation] Token ID: {token_id}")
    print(f"  地址: {token_address}")
    print(f"  名称: {name}")
    print(f"  符号: {symbol}")
    print(f"  启动时间: {launch_time}")
    print(f"  创建者: {token_creator}")


async def handle_token_trade(event):
    is_purchase = event.args['isTokenPurchase']
    token_id = event.args['tokenId']
    address = event.address
    trader = event.args['trader']
    token_amount = Decimal(event.args['tokenAmount'])
    currency_amount = Decimal(event.args['currencyAmount'])
    trade_type = "Buy" if is_purchase else "Sell"
    time_now = now()

    print(f"\n[TokenTrade] {trade_type}")
    print(f"  Token ID: {token_id}")
    print(f"  Token 地址: {address}")
    print(f"  交易者: {trader}")
    print(f"  Token 数量: {token_amount}")
    print(f"  货币数量: {currency_amount}")

    token, protocol = await handle_sync(get_token, protocol_id=token_id)
    if not token:
        print("  警告: Token ID 未在记录中找到。")
        return
    net_currency = currency_amount * (Decimal('100') - PLATFORM_FEE_BP / Decimal('100'))
    net_currency /= Decimal('100')
    if is_purchase:
        # protocol.market_value += utils.format_wei(net_currency)
        protocol.volume += utils.format_wei(token_amount)
    else:
        # protocol.market_value -= utils.format_wei(net_currency)
        protocol.volume -= utils.format_wei(token_amount)
    protocol.price = net_currency / token_amount
    await handle_sync(protocol.save)

    print(f"  当前价格: {protocol.price}")
    print(f"  市值: {protocol.market_value}")
    print(f"  交易量: {protocol.volume}")

    minute = time_now.replace(second=0, microsecond=0)
    minute_data, created = await handle_sync(models.MinuteMarketData.objects.get_or_create, protocol=protocol, time=minute, defaults={
        'open': protocol.price, 'close': protocol.price, 'high': protocol.price, 'low': protocol.price,
        'volume': utils.format_wei(token_amount)
    })
    if not created:
        minute_data.close = protocol.price
        if protocol.price > minute_data.high:
            minute_data.high = protocol.price
        if protocol.price < minute_data.low:
            minute_data.low = protocol.price
        minute_data.volume += utils.format_wei(token_amount)
        await handle_sync(minute_data.save)

    account = await handle_sync(get_account, address=trader)
    if not account:
        print("  警告: 交易者 未在记录中找到。")
        return
    await handle_sync(
        models.Transaction.objects.create,
        account=account,
        token=token,
        type=trade_type,
        quantity=utils.format_wei(token_amount),
        amount=utils.format_wei(net_currency),
        time=time_now,
        hash=event.transactionHash.to_0x_hex()
    )


def handle_dex_pool_creation(event):
    token = event.args['token']
    amount_eth = Decimal(event.args['amountETH'])
    amount_token = Decimal(event.args['amountToken'])

    print(f"\n[DEXPoolCreation]")
    print(f"  Token 地址: {token}")
    print(f"  ETH 数量: {amount_eth}")
    print(f"  Token 数量: {amount_token}")


def handle_debug(event):
    message = event.args['message']
    value = Decimal(event.args['value'])

    print(f"\n[Debug] {message}: {value}")


# 运行事件监听器
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 初始化Web3
        w3 = Web3(Web3.WebsocketProvider(f"wss://sepolia.infura.io/ws/v3/{INFURA_PROJECT_ID}"))

        # 如果连接的是使用PoA的测试网络（如Rinkeby），请取消以下行的注释
        # w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not w3.is_connected():
            raise ConnectionError("无法连接到Infura WebSocket。")
        CONTRACT_ADDRESSES = list(models.Protocol.objects.filter(is_enabled=True).values_list('address', flat=True))
        # 创建所有合约的实例
        contracts = []
        for addr in CONTRACT_ADDRESSES:
            checksum_address = w3.to_checksum_address(addr)
            contract = w3.eth.contract(address=checksum_address, abi=EVENT_ABI)
            contracts.append(contract)
        try:
            asyncio.run(listen_to_events(contracts))
        except KeyboardInterrupt:
            print("已停止监听事件。")
