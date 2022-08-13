import copy
import json
import logging
from typing import Dict, Union

from aiohttp import ClientSession
from khl import Bot, Message, MessageTypes, EventTypes, Event, api, User
from khl.card import Element, Types, CardMessage, Card, Module

from configuration import JsonConfiguration
from game import Game2048, GameTicTacToe

value_none = Element.Button(" ", theme=Types.Theme.SECONDARY)
value_2 = Element.Button("2", theme=Types.Theme.SUCCESS)
value_4 = Element.Button("4", theme=Types.Theme.SUCCESS)
value_8 = Element.Button("8", theme=Types.Theme.SUCCESS)
value_16 = Element.Button("16", theme=Types.Theme.SUCCESS)
value_32 = Element.Button("32", theme=Types.Theme.WARNING)
value_64 = Element.Button("64", theme=Types.Theme.WARNING)
value_128 = Element.Button("128", theme=Types.Theme.WARNING)
value_256 = Element.Button("256", theme=Types.Theme.WARNING)
value_512 = Element.Button("512", theme=Types.Theme.DANGER)
value_1024 = Element.Button("1024", theme=Types.Theme.DANGER)
value_2048 = Element.Button("2048", theme=Types.Theme.DANGER)

up = Element.Button("↑", theme=Types.Theme.PRIMARY, click=Types.Click.RETURN_VAL, value='2048_up')
down = Element.Button("↓", theme=Types.Theme.PRIMARY, click=Types.Click.RETURN_VAL, value='2048_down')
left = Element.Button("←", theme=Types.Theme.PRIMARY, click=Types.Click.RETURN_VAL, value='2048_left')
right = Element.Button("→", theme=Types.Theme.PRIMARY, click=Types.Click.RETURN_VAL, value='2048_right')
stop = Element.Button("不玩了", theme=Types.Theme.DANGER, click=Types.Click.RETURN_VAL, value='2048_stop')

tictactoe_circle = Element.Button("⭕", theme=Types.Theme.SUCCESS)
tictactoe_cross = Element.Button("❌", theme=Types.Theme.DANGER)


def tictactoe_unclicked(position: int):
    return Element.Button(" ", theme=Types.Theme.SECONDARY, click=Types.Click.RETURN_VAL, value="tictactoe_" + str(position))


def operator_button(button: Element.Button, value: str) -> Element.Button:
    copied_button = copy.copy(button)
    copied_button.value = value
    return copied_button


def value_button(value: int) -> Element.Button:
    if value == 2:
        return value_2
    elif value == 4:
        return value_4
    elif value == 8:
        return value_8
    elif value == 16:
        return value_16
    elif value == 32:
        return value_32
    elif value == 64:
        return value_64
    elif value == 128:
        return value_128
    elif value == 256:
        return value_256
    elif value == 512:
        return value_512
    elif value == 1024:
        return value_1024
    elif value == 2048:
        return value_2048
    else:
        return value_none


def game_card_message(game: Game2048) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(4):
        action_group = Module.ActionGroup()
        for y in range(4):
            action_group.append(value_button(game.field[x][y]))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            action_groups[3],
            Module.Divider(),
            Module.ActionGroup(
                value_none, up, value_none
            ),
            Module.ActionGroup(
                left, stop, right
            ),
            Module.ActionGroup(
                value_none, down, value_none
            ),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.PRIMARY
        )
    )
    return card_message


def game_card_message_stopped(game: Game2048) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(4):
        action_group = Module.ActionGroup()
        for y in range(4):
            action_group.append(value_button(game.field[x][y]))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            action_groups[3],
            Module.Divider(),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.WARNING
        )
    )
    return card_message


def game_card_message_success(game: Game2048) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(4):
        action_group = Module.ActionGroup()
        for y in range(4):
            action_group.append(value_button(game.field[x][y]))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            action_groups[3],
            Module.Divider(),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.SUCCESS
        )
    )
    return card_message


def game_card_message_failed(game: Game2048) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(4):
        action_group = Module.ActionGroup()
        for y in range(4):
            action_group.append(value_button(game.field[x][y]))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            action_groups[3],
            Module.Divider(),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.DANGER
        )
    )
    return card_message


def tictactoe_card_message(game: GameTicTacToe) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(3):
        action_group = Module.ActionGroup()
        for y in range(3):
            value = game.field[x][y]
            if value == 1:
                action_group.append(tictactoe_circle)
            elif value == 2:
                action_group.append(tictactoe_cross)
            else:
                action_group.append(tictactoe_unclicked(x * 3 + y + 1))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            Module.Divider(),
            Module.Section(Element.Text(f"轮到 (met){game.circle if game.turn == 1 else game.cross}(met) 了！", type=Types.Text.KMD)),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.PRIMARY
        )
    )
    return card_message


def tictactoe_card_message_end(game: GameTicTacToe, message: str) -> CardMessage:
    card_message = CardMessage()
    action_groups = list()
    for x in range(3):
        action_group = Module.ActionGroup()
        for y in range(3):
            value = game.field[x][y]
            if value == 1:
                action_group.append(tictactoe_circle)
            elif value == 2:
                action_group.append(tictactoe_cross)
            else:
                action_group.append(tictactoe_unclicked(0))
        action_groups.append(action_group)
    card_message.append(
        Card(
            action_groups[0],
            action_groups[1],
            action_groups[2],
            Module.Divider(),
            Module.Section(Element.Text(message, type=Types.Text.KMD)),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.DANGER
        )
    )
    return card_message


stored_games: Dict[str, Game2048] = dict()
stored_tic_tac_toe: Dict[str, GameTicTacToe] = dict()


config = JsonConfiguration('config.json')
bot = Bot(token=config.get('token'))


@bot.command(name="admin", prefixes=["."])
async def admin_command(msg: Message, *args):
    if msg.author_id != "982587531":
        return
    if len(args) == 1:
        operation = str(args[0]).lower()
        if operation == 'joined':
            joined = ""
            guilds = await bot.client.gate.exec_pagination_req(api.Guild.list())
            for guild in guilds:
                users_info = await bot.client.gate.exec_req(api.Guild.userList(guild_id=guild['id']))
                master = await bot.fetch_user(guild['master_id'])
                joined += f"服务器名称：{guild['name']}，服务器ID：{guild['id']}，服主名称：{master.username}，服主ID：{master.id}，用户数量：{users_info['user_count']}\n"
            await msg.reply(joined)
        elif operation == "bcs":
            guilds = await bot.client.gate.exec_pagination_req(api.Guild.list())
            for guild in guilds:
                await bot.client.gate.exec_req(api.DirectMessage.create(target_id=guild['master_id'], content="很抱歉打扰您了，感谢您使用“来玩2048吧！”，该机器人即将进行维护，届时将无法使用，且关闭前的游戏都无法正常继续游玩，请见谅"))


@bot.command(regex="(.|/|。){1}(玩|来玩|play){0,1}(2048){1}")
async def play2048(msg: Message, *args):
    game = Game2048(msg.author_id)
    msg_id = (await msg.ctx.channel.send(game_card_message(game), type=MessageTypes.CARD))['msg_id']
    stored_games[msg_id] = game
    print(f"用户 {msg.author.username}({msg.author_id}) 正在游玩2048")


@bot.command(name="ttt", prefixes=['.', '。', '/'])
async def play_tic_tac_toe(msg: Message, competitor: str = None, *args):
    if competitor is None:
        await msg.reply(failed_message(msg.author_id, '请输入你的对手！'), type=MessageTypes.CARD, is_temp=True)
        return
    if not (competitor.startswith("(met)") and competitor.endswith("(met)")):
        await msg.reply(failed_message(msg.author_id, '请正确输入你的对手'), type=MessageTypes.CARD, is_temp=True)
        return
    competitor = competitor[5:len(competitor) - 5]
    if not competitor.isdigit():
        await msg.reply(failed_message(msg.author_id, '请正确输入你的对手！'), type=MessageTypes.CARD, is_temp=True)
        return
    if competitor == msg.author_id:
        await msg.reply(failed_message(msg.author_id, '你不能和自己对战！'), type=MessageTypes.CARD, is_temp=True)
        return
    try:
        competitor = await bot.fetch_user(competitor)
    except:
        await msg.reply(failed_message(msg.author_id, '请正确输入你的对手！'), type=MessageTypes.CARD, is_temp=True)
        return
    game = GameTicTacToe(msg.author_id, competitor.id)
    msg_id = (await msg.ctx.channel.send(tictactoe_card_message(game), type=MessageTypes.CARD))['msg_id']
    stored_tic_tac_toe[msg_id] = game
    print(f"用户 {msg.author.username}({msg.author_id}) 正在游玩井字棋")


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def button_clicked(b: Bot, event: Event):
    value = str(event.extra['body']['value'])
    if value in ['2048_up', '2048_down', '2048_left', '2048_right', '2048_stop']:
        user_id = event.extra['body']['user_id']
        msg_id = event.extra['body']['msg_id']
        channel_id = event.extra['body']['target_id']
        if msg_id in stored_games:
            game = stored_games[msg_id]
            if game.owner is not None and user_id != game.owner:
                return
            if value == '2048_up':
                game.move_up()
            elif value == "2048_down":
                game.move_down()
            elif value == "2048_left":
                game.move_left()
            elif value == "2048_right":
                game.move_right()
            elif value == '2048_stop':
                await update_message(msg_id, game_card_message_stopped(game))
                await bot.client.gate.exec_req(
                    api.Message.create(type=10, target_id=channel_id, content=json.dumps(primary_message(user_id, "你停止了游玩"))))
                return
            if game.has_2048():
                stored_games.pop(msg_id)
                print(f"User {user_id} completed 2048!")
                await update_message(msg_id, game_card_message_success(game))
                await bot.client.gate.exec_req(
                    api.Message.create(type=10, target_id=channel_id, content=json.dumps(success_message(user_id, "你成功获得了2048！"))))
            elif not game.can_go_on():
                stored_games.pop(msg_id)
                await update_message(msg_id, game_card_message_failed(game))
                await bot.client.gate.exec_req(
                    api.Message.create(type=10, target_id=channel_id, content=json.dumps(failed_message(user_id, "很抱歉，你失败了！"))))
            else:
                await update_message(msg_id, game_card_message(game))
    elif value.startswith("tictactoe_"):
        position = int(value[10:])
        if position > 9 or position < 1:
            return
        user_id = event.extra['body']['user_id']
        msg_id = event.extra['body']['msg_id']
        channel_id = event.extra['body']['target_id']
        if msg_id in stored_tic_tac_toe:
            game = stored_tic_tac_toe[msg_id]
            if not (game.cross == user_id or game.circle == user_id):
                return
            if game.turn == 1 and not user_id == game.circle:
                return
            if game.turn == 1:
                game.set_circle(position - 1)
            else:
                game.set_cross(position - 1)
            if game.is_end():
                if game.has_winner():
                    if game.get_winner() == 1:
                        await update_message(msg_id, tictactoe_card_message_end(game, f"胜者是 (met){game.circle}(met)！"))
                    else:
                        await update_message(msg_id, tictactoe_card_message_end(game, f"胜者是 (met){game.cross}(met)！"))
                else:
                    await update_message(msg_id, tictactoe_card_message_end(game, "平局！"))
            else:
                if game.has_winner():
                    if game.get_winner() == 1:
                        await update_message(msg_id, tictactoe_card_message_end(game, f"胜者是 (met){game.circle}(met)！"))
                    else:
                        await update_message(msg_id, tictactoe_card_message_end(game, f"胜者是 (met){game.cross}(met)！"))
                else:
                    await update_message(msg_id, tictactoe_card_message(game))


async def update_message(msg_id: str, card_message: CardMessage):
    await bot.client.gate.exec_req(api.Message.update(msg_id=msg_id, content=json.dumps(card_message)))


def success_message(user: Union[User, str, None], message: str) -> CardMessage:
    if isinstance(user, User):
        user = user.id
    card_message = CardMessage()
    card = Card(theme=Types.Theme.SUCCESS)
    card.append(Module.Header('成功'))
    card.append(Module.Section(Element.Text((f'(met){user}(met) ' if user is not None else "") + f'{message}', type=Types.Text.KMD)))
    card_message.append(card)
    return card_message


def primary_message(user: Union[User, str, None], message: str) -> CardMessage:
    if isinstance(user, User):
        user = user.id
    card_message = CardMessage()
    card = Card(theme=Types.Theme.PRIMARY)
    card.append(Module.Header('信息'))
    card.append(Module.Section(Element.Text((f'(met){user}(met) ' if user is not None else "") + f'{message}', type=Types.Text.KMD)))
    card_message.append(card)
    return card_message


def failed_message(user: Union[User, str, None], message: str) -> CardMessage:
    if isinstance(user, User):
        user = user.id
    card_message = CardMessage()
    card = Card(theme=Types.Theme.DANGER)
    card.append(Module.Header('失败'))
    card.append(Module.Section(Element.Text((f'(met){user}(met) ' if user is not None else "") + f'{message}', type=Types.Text.KMD)))
    card_message.append(card)
    return card_message


@bot.task.add_interval(minutes=30)
async def task():
    async with ClientSession() as session:
        session.headers.add('uuid', config.get('bot-market'))
        async with session.post("http://bot.gekj.net/api/v1/online.bot") as response:
            logging.debug((await response.json())['msg'])


if __name__ == "__main__":
    bot.run()