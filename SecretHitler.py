# -*- coding: utf-8 -*-

import pygame
import random
from enum import Enum
from time import sleep
import threading
import logging
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, ParseMode, ChatAction


class Role(Enum):
    Liberal = 0
    Fascist = 1
    Hitler = 2


class Player:
    name = ""
    phone = ""
    secretRole = Role.Liberal
    chancellor = False
    president = False
    nameText = []
    nameRect = []
    highlights = ()

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return self.name + " " + self.phone + " " + str(self.secretRole) + " c:" + str(self.chancellor) + " p:" + str(self.president)


class GameState:
    players = []
    deck = [Role.Liberal] * 9 + [Role.Fascist] * 11
    drawable = 17
    discarded = 0
    fascistPosition = 0
    liberalPosition = 0

    liberalLocations = [(363, 436), (494, 435), (622, 433), (750, 437), (883, 435)]
    fascistLocations = [(303, 108), (432, 105), (561, 107), (689, 106), (819, 107), (948, 105)]

    def __init__(self):
        file = open("players.txt", "r")
        for line in file:
            foo = line.strip().split("\t")
            bar = Player(foo[0], foo[1])
            self.players.append(bar)
        file.close()
        foo2 = []
        if len(self.players) == 5:
            foo2 = [Role.Liberal] * 3 + [Role.Fascist] * 1 + [Role.Hitler]
        if len(self.players) == 6:
            foo2 = [Role.Liberal] * 4 + [Role.Fascist] * 1 + [Role.Hitler]
        if len(self.players) == 7:
            foo2 = [Role.Liberal] * 4 + [Role.Fascist] * 2 + [Role.Hitler]
        if len(self.players) == 8:
            foo2 = [Role.Liberal] * 5 + [Role.Fascist] * 2 + [Role.Hitler]
        if len(self.players) == 9:
            foo2 = [Role.Liberal] * 5 + [Role.Fascist] * 3 + [Role.Hitler]
        if len(self.players) == 10:
            foo2 = [Role.Liberal] * 6 + [Role.Fascist] * 3 + [Role.Hitler]
        random.shuffle(foo2)
        fascists = []
        fascists_names = []
        the_hitler = ""
        for pl, role in zip(self.players, foo2):
            pl.secretRole = role
            bot.send_message(chat_id=pl.phone, text=pl.name + ' your role is <b>' + pl.secretRole.name + "</b>", parse_mode=ParseMode.HTML)
            if role == Role.Fascist:
                fascists.append(pl)
                fascists_names.append(pl.name)
            if role == Role.Hitler:
                the_hitler = pl.name

        for f in fascists:
            bot.send_message(chat_id=f.phone, text="Hitler is <b>" + the_hitler + "</b>\nFascists are:\n\t<b>" + "</b>\n\t<b>".join(fascists_names) + "</b>", parse_mode=ParseMode.HTML)
        random.shuffle(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
        self.drawable = 17
        self.discarded = 0

    def draw_three(self):
        ans = [self.deck[self.drawable - 1], self.deck[self.drawable - 2], self.deck[self.drawable - 3]]
        self.drawable -= 3
        return ans

    def discard(self):
        self.discarded += 1

    def paint_cards(self):
        if self.drawable == 2:
            screen.blit(cardIMG, (74, 424))
            screen.blit(cardIMG, (74 + 5, 424 + 5))
        elif self.drawable == 1:
            screen.blit(cardIMG, (74, 424))
        elif self.drawable >= 3:
            screen.blit(cardIMG, (74, 424))
            screen.blit(cardIMG, (74 + 3, 424 + 3))
            screen.blit(cardIMG, (74 + 6, 424 + 6))
        if self.discarded == 2:
            screen.blit(cardIMG, (1169, 424))
            screen.blit(cardIMG, (1169 + 5, 424 + 5))
        elif self.discarded == 1:
            screen.blit(cardIMG, (1169, 424))
        elif self.discarded >= 3:
            screen.blit(cardIMG, (1169, 424))
            screen.blit(cardIMG, (1169 + 3, 424 + 3))
            screen.blit(cardIMG, (1169 + 6, 424 + 6))
        for j in range(self.fascistPosition):
            screen.blit(fascistPolicyIMG, self.fascistLocations[j])
        for j in range(self.liberalPosition):
            screen.blit(liberalPolicyIMG, self.liberalLocations[j])

    def set_policy(self, is_fascist):
        if is_fascist.value:
            self.fascistPosition += 1
        else:
            self.liberalPosition += 1


def sqr_distance(v1, v2):
    return (v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2


def inside_boundary(mouse, rect):
    return rect.topleft[0] < mouse[0] < rect.bottomright[0] and rect.topleft[1] < mouse[1] < rect.bottomright[1]


def inside_rectangle(mouse, A, B, C):
    def vector(p1, p2):
        return p2[0]-p1[0], p2[1]-p1[1]

    def dot(v1, v2):
        return v1[0]*v2[0]+v1[1]*v2[1]
    AB = vector(A, B)
    AM = vector(A, mouse)
    BC = vector(B, C)
    BM = vector(B, mouse)
    return 0 <= dot(AB, AM) <= dot(AB, AB) and 0 <= dot(BC, BM) <= dot(BC, BC)


def draw_cards():
    global response_msg_list
    if game.drawable >= 3:
        pres = None
        chan = None
        for pl in game.players:
            if pl.president:
                pres = pl
            if pl.chancellor:
                chan = pl
        if pres and chan:
            three_cards = game.draw_three()
            if game.fascistPosition == 5:
                response_msg_list = [three_cards[0].name, three_cards[1].name, three_cards[2].name, "Veto"]
                bot.send_message(chat_id=pres.phone, text=pres.name + " you are the president.\nSelect one to discard:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=three_cards[0].name, callback_data="1")], [InlineKeyboardButton(text=three_cards[1].name, callback_data="2")], [InlineKeyboardButton(text=three_cards[2].name, callback_data="3")], [InlineKeyboardButton(text="Veto", callback_data="4")]]))
            else:
                response_msg_list = [three_cards[0].name, three_cards[1].name, three_cards[2].name]
                bot.send_message(chat_id=pres.phone, text=pres.name + " you are the president.\nSelect one to discard:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=three_cards[0].name, callback_data="1")], [InlineKeyboardButton(text=three_cards[1].name, callback_data="2")], [InlineKeyboardButton(text=three_cards[2].name, callback_data="3")]]))

            reply = int(get_reply())
            if reply != 4:
                reply -= 1
                del three_cards[reply]
                game.discard()
                response_msg_list = [three_cards[0].name, three_cards[1].name]
                bot.send_message(chat_id=chan.phone, text=chan.name + " you are the chancellor.\nSelect one to <b>discard</b>:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=three_cards[0].name, callback_data="1")], [InlineKeyboardButton(text=three_cards[1].name, callback_data="2")]]), parse_mode=ParseMode.HTML)

                reply = int(get_reply())
                reply -= 1
                del three_cards[reply]
                game.discard()
                game.set_policy(three_cards[0])
            else:
                response_msg_list = ["Agree", "Disagree"]
                bot.send_message(chat_id=chan.phone, text=chan.name + " you are the chancellor.\nPresident wants to veto.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Agree", callback_data="1")], [InlineKeyboardButton(text="Disagree", callback_data="2")]]))
                reply = int(get_reply())
                if reply == 1:
                    game.discard()
                    game.discard()
                    game.discard()
                else:
                    game.drawable += 3


def ja_nein():
    pres = None
    chan = None
    for pl in game.players:
        if pl.president:
            pres = pl
        if pl.chancellor:
            chan = pl
    if pres and chan:
        global ja_nein_list
        ja_nein_list = []
        for pl in game.players:
            bot.send_message(chat_id=pl.phone, text="Vote for\nPresident: " + pres.name + "\n"+ "Chancellor: " + chan.name, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Ja!", callback_data="Ja!")], [InlineKeyboardButton(text="Nein!", callback_data="Nein!")]]))
        while len(ja_nein_list) != player_count:
            sleep(0.1)
        for pl in game.players:
            bot.send_message(chat_id=pl.phone, text="Results for\nPresident: " + pres.name + "\n"+ "Chancellor: " + chan.name + "\n" + "\n".join(ja_nein_list))


def callback_query_handler(update, context):
    query = update.callback_query
    if(query.data == "Ja!" or query.data == "Nein!"):
        pres = None
        chan = None
        for pl in game.players:
            if pl.president:
                pres = pl
            if pl.chancellor:
                chan = pl
        new_msg = "President: " + pres.name + "\n"+ "Chancellor: " + chan.name + "\n" + query.data
        query.edit_message_text(text=new_msg, parse_mode=ParseMode.HTML)
        the_name = update.effective_user.first_name
        if update.effective_user.last_name:
            the_name = update.effective_user.first_name + " " + update.effective_user.last_name
        the_name += ": "+ query.data
        ja_nein_list.append(the_name)
        
    else:
        new_msg = ""
        foobar = False
        for j in range(len(response_msg_list)):
            el = response_msg_list[j]
            if j == int(query.data) - 1:
                if el != "Veto" and el != "Agree" and el != "Disagree":
                    new_msg += "\n<s>" + el + "</s>"
                else:
                    new_msg += "\n<b>" + el + "</b>"
                    foobar = True
            else:
                new_msg += "\n" + el
        if foobar:
            new_msg = "Selected option: " + new_msg
        else:
            new_msg = "Discarded card: " + new_msg
    
        query.edit_message_text(text=new_msg, parse_mode=ParseMode.HTML)
        global message_id_data
        global got_reply
        message_id_data = query.data
        got_reply = True


def get_reply():
    global got_reply
    global message_id_data
    while not got_reply:
        sleep(0.1)
    got_reply = False
    return message_id_data


def command_handler_start(update, context):
    if lobby:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Secret Hitler COVID-19 Edition")
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id, text="ONLINE Edition. ONLINE. Damn autocorrect.")
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(2)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Whatever, lets get to business.\nPlease type /join in order to enter as a player.")


def command_handler_join(update, context):
    if lobby:
        for el in lobby_info:
            if el[1] == str(update.effective_chat.id):
                context.bot.send_message(chat_id=update.effective_chat.id, text="You have already joined.")
                return
        the_name = update.effective_user.first_name
        if update.effective_user.last_name:
            the_name = update.effective_user.first_name + " " + update.effective_user.last_name
        context.bot.send_message(chat_id=update.effective_chat.id, text="Your name is " + the_name + "\nYour chat id is " + str(update.effective_chat.id))
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Is this your name?")
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(2)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Don't bother answering. I am too lazy to change it anyways.")
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(2)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Just relax and get comfy until the host starts the game.")
        with the_lock:
            lobby_info.append((the_name, str(update.effective_chat.id)))
            print("\n" + the_name + " has joined the game.")


ja_nein_list = []
response_msg_list = []
message_id_data = ""
got_reply = False
the_lock = threading.Lock()
lobby_info = []
lobby = False

ask = input("Do you want to change players? [Y/n]:")
while not (ask == "" or ask.lower() == "y" or ask.lower() == "yes" or ask.lower() == "n" or ask.lower() == "no"):
    ask = input("Do you want to change players? [Y/n]:")
lobby = ask == "" or ask.lower() == "y" or ask.lower() == "yes"

token_file = open("token.txt", "r")
token = token_file.readline().strip()
bot_name = token_file.readline().strip()
token_file.close()
bot = Bot(token=token)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
start_handler = CommandHandler('start', command_handler_start)
join_handler = CommandHandler('join', command_handler_join)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(join_handler)
updater.start_polling()

if lobby:
    print("Please install Telegram and go to https://t.me/" + bot_name)
    input("Press Enter once everybody joins.")
    lobby = False
    players_file = open("players.txt", "w")
    for p_name, p_id in lobby_info:
        players_file.write(p_name+"\t"+p_id+"\n")
    players_file.close()
    print("Starting the game")


scale = 0.33
scale2 = 0.33
scale3 = 0.285
scale4 = 0.33
scale5 = 0.2
totalWidth = int(2816 * scale) + 2 * int(496 * scale2)
totalHeight = 2 * int(1000 * scale)

game = GameState()
player_count = len(game.players)

liberalIMG = pygame.image.load('res/liberal.png')
liberalIMG = pygame.transform.smoothscale(liberalIMG, (int(2816 * scale), int(1000 * scale)))

fascistIMG = None
if player_count <= 6:
    fascistIMG = pygame.image.load('res/fascist56.png')
elif player_count <= 8:
    fascistIMG = pygame.image.load('res/fascist78.png')
else:
    fascistIMG = pygame.image.load('res/fascist910.png')
fascistIMG = pygame.transform.smoothscale(fascistIMG, (int(2816 * scale), int(1000 * scale)))

drawPileIMG = pygame.image.load('res/drawpile.png')
drawPileIMG = pygame.transform.smoothscale(drawPileIMG, (int(496 * scale2), int(696 * scale2)))

discardPileIMG = pygame.image.load('res/discardpile.png')
discardPileIMG = pygame.transform.smoothscale(discardPileIMG, (int(496 * scale2), int(696 * scale2)))

cardIMG = pygame.image.load('res/cards.png')
cardIMG = pygame.transform.smoothscale(cardIMG, (int(394 * scale3), int(549 * scale3)))
drawCardRect = cardIMG.get_rect()
discardCardRect = cardIMG.get_rect()
drawCardRect.x = 74
drawCardRect.y = 424
discardCardRect.x = 1169
discardCardRect.y = 424

fascistPolicyIMG = pygame.image.load('res/fascistPolicy.jpg')
fascistPolicyIMG = pygame.transform.smoothscale(fascistPolicyIMG, (int(340 * scale4), int(489 * scale4)))

liberalPolicyIMG = pygame.image.load('res/liberalPolicy.jpg')
liberalPolicyIMG = pygame.transform.smoothscale(liberalPolicyIMG, (int(340 * scale4), int(489 * scale4)))

jaNeinIMG = pygame.image.load('res/ja-nein.png')
jaNeinIMG = pygame.transform.smoothscale(jaNeinIMG, (int(989 * scale5), int(848 * scale5)))

jaNeinRect = jaNeinIMG.get_rect()
jaNeinRect.x = 1152
jaNeinRect.y = 95

highlight_yellow = pygame.image.load('res/highlight-yellow.png')
highlight_blue = pygame.image.load('res/highlight-blue.png')

paraIMG = pygame.image.load('res/25-Kurus.png')
paraIMG = pygame.transform.smoothscale(paraIMG, (35, 35))
paraStates = [(525, 610), (612, 610), (699, 611), (785, 612)]
paraState = 0

pygame.font.init()
font = pygame.font.Font('res/FreeSansBold.ttf', 20)

nameText = []
for p in game.players:
    nameText.append(font.render(p.name, True, (0, 0, 0)))

nameRect = []
highlights_yellow = []
highlights_blue = []
counter_foo = 0
for e in nameText:
    r = e.get_rect()
    highlights_yellow.append(pygame.transform.smoothscale(highlight_yellow, (r.bottomright[0] * 2, r.bottomright[1])))
    highlights_blue.append(pygame.transform.smoothscale(highlight_blue, (r.bottomright[0] * 2, r.bottomright[1])))
    r.x = 76
    r.y = 45 + 27 * counter_foo
    counter_foo += 1
    nameRect.append(r)

for p, e in zip(game.players, zip(nameText, nameRect, tuple(zip(highlights_yellow, highlights_blue)))):
    p.nameText = e[0]
    p.nameRect = e[1]
    p.highlights = e[2]

pygame.init()
screen = pygame.display.set_mode((100 + totalWidth, totalHeight + 40))

theThread = None
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 511 < mouse_pos[0] < 828 and 606 < mouse_pos[1] < 647:
                min_dist = 1000
                for i in range(4):
                    old_paraState = paraState
                    center = (paraStates[i][0] + 17, paraStates[i][1] + 17)
                    if min_dist > sqr_distance(center, mouse_pos):
                        min_dist = sqr_distance(center, mouse_pos)
                        paraState = i
                    if old_paraState == 3 and paraState == 0:
                        game.set_policy(game.deck[game.drawable - 1])
                        game.drawable -= 1
            if 555 < mouse_pos[0] < 676 and 107 < mouse_pos[1] < 272 and game.fascistPosition == 3 and player_count <= 6:
                pres3 = None
                for p in game.players:
                    if p.president:
                        pres3 = p
                if pres3:
                    bot.send_message(chat_id=pres3.phone, text="Here are the top 3 cards:\n" + game.deck[game.drawable - 1].name + "\n" + game.deck[game.drawable - 2].name + "\n" + game.deck[game.drawable - 3].name)
            if (305 < mouse_pos[0] < 415 and 107 < mouse_pos[1] < 272 and game.fascistPosition == 1 and player_count >= 9) or (426 < mouse_pos[0] < 548 and 107 < mouse_pos[1] < 272 and game.fascistPosition == 2 and player_count >= 7):
                pres2 = None
                chan2 = None
                for p in game.players:
                    if p.president:
                        pres2 = p
                    if p.chancellor:
                        chan2 = p
                if pres2 and chan2:
                    role_foo = chan2.secretRole.name
                    if role_foo == "Hitler":
                        role_foo = "Fascist"
                    bot.send_message(chat_id=pres2.phone, text="The role of " + chan2.name + " is " + role_foo)
            for p in game.players:
                if inside_boundary(mouse_pos, p.nameRect):
                    if p.chancellor:
                        p.chancellor = False
                    else:
                        if p.president:
                            p.chancellor = True
                            p.president = False
                        else:
                            p.president = True
            if inside_boundary(mouse_pos, drawCardRect):
                if theThread:
                    if not theThread.is_alive():
                        theThread = threading.Thread(target=draw_cards)
                        theThread.start()
                else:
                    theThread = threading.Thread(target=draw_cards)
                    theThread.start()

            elif inside_boundary(mouse_pos, discardCardRect):
                if game.drawable < 3:
                    game.shuffle()
            
            elif inside_rectangle(mouse_pos, (1243, 96), (1154, 136), (1209, 263)) or inside_rectangle(mouse_pos, (1257, 97), (1348, 132), (1298, 262)):
                pres2 = None
                chan2 = None
                for p in game.players:
                    if p.president:
                        pres2 = p
                    if p.chancellor:
                        chan2 = p
                if pres2 and chan2:
                    theThread2 = threading.Thread(target=ja_nein)
                    theThread2.start()

            # print(mouse_pos)

    drawText = font.render(str(game.drawable), True, (0, 0, 0))
    discardText = font.render(str(game.discarded), True, (0, 0, 0))
    drawText_rect = drawText.get_rect(center=(63, 616))
    discardText_rect = discardText.get_rect(center=(1159, 616))

    screen.fill((180, 180, 180))

    for p in game.players:
        screen.blit(p.nameText, p.nameRect)
        if p.president:
            screen.blit(p.highlights[0], p.highlights[0].get_rect(center=p.nameRect.center))
        if p.chancellor:
            screen.blit(p.highlights[1], p.highlights[1].get_rect(center=p.nameRect.center))

    screen.blit(fascistIMG, (52 + int(496 * scale2), 20))
    screen.blit(liberalIMG, (52 + int(496 * scale2), int(1000 * scale) + 22))
    screen.blit(drawPileIMG, (50, 1.5 * int(1000 * scale) - 0.5 * int(696 * scale2) + 22))
    screen.blit(discardPileIMG, (54 + int(496 * scale2) + int(2816 * scale), 1.5 * int(1000 * scale) - 0.5 * int(696 * scale2) + 22))
    screen.blit(drawText, drawText_rect)
    screen.blit(discardText, discardText_rect)
    screen.blit(jaNeinIMG, (1152, 95))
    game.paint_cards()
    screen.blit(paraIMG, paraStates[paraState])
    pygame.display.update()

pygame.quit()
updater.stop()