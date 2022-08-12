import copy
import json
from typing import Dict, Union

from khl import Bot, Message, MessageTypes, EventTypes, Event, api, User
from khl.card import Element, Types, CardMessage, Card, Module

from configuration import JsonConfiguration
from game import Game2048

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
                left, up, right, down
            ),
            Module.Context(Element.Text("由 DeeChael 开发,  在 [Github](https://github.com/DeeChael/LetsPlay2048) 查看源码", type=Types.Text.KMD)),
            theme=Types.Theme.PRIMARY
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


stored_games: Dict[str, Game2048] = dict()


config = JsonConfiguration('config.json')
bot = Bot(token=config.get('token'))


@bot.command(regex="(.|/|。){1}(玩|来玩|play){0,1}(2048){1}")
async def play2048(msg: Message, *args):
    game = Game2048(msg.author_id)
    msg_id = (await msg.ctx.channel.send(game_card_message(game), type=MessageTypes.CARD))['msg_id']
    stored_games[msg_id] = game


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def button_clicked(b: Bot, event: Event):
    value = str(event.extra['body']['value'])
    if value in ['2048_up', '2048_down', '2048_left', '2048_right']:
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
            if game.has_2048():
                await update_message(msg_id, game_card_message_success(game))
                await bot.client.gate.exec_req(
                    api.Message.create(type=10, target_id=channel_id, content=json.dumps(success_message(user_id, "你成功获得了2048！"))))
            elif not game.can_go_on():
                await update_message(msg_id, game_card_message_failed(game))
                await bot.client.gate.exec_req(
                    api.Message.create(type=10, target_id=channel_id, content=json.dumps(success_message(user_id, "很抱歉，你失败了！"))))
            else:
                await update_message(msg_id, game_card_message(game))


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


if __name__ == "__main__":
    bot.run()