import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove, ForceReply
import PikInterActor
import UserStory
def messageSender(chatId, type, msg, *KBList):
    print(chatId,type,msg,*KBList)
    #todo: if have error
    #todo: if kbList is empty
    #todo: change false with return bot.sendMessage()
    if KBList:
        for items in KBList:
            keyboardList = items
    if type == 'text':
        bot.sendMessage(chatId, msg)
    if type == 'keyboard':
        keyboard = ReplyKeyboardMarkup(keyboard=keyboardList)
        bot.sendMessage(chatId, msg, reply_markup=keyboard)
    if type == 'hide':
        keyboard = ReplyKeyboardRemove()
        bot.sendMessage(chatId, msg, reply_markup=keyboard)
    if type == 'reply':
        markup = ForceReply()
        bot.sendMessage(chatId, msg, reply_markup=markup)
    if type == 'button':
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboardList)
        bot.sendMessage(chatId, msg, reply_markup=keyboard)
    if type == 'forward':
        for k in KBList:
            bot.forwardMessage(chatId, k, msg)
#todo: get func messages from another func
def welcome(chatId,msg):
    #todo: update user if start byself
    PikInterActor.getUser(msg['chat'])
    UserStory.freshUserSteps(chatId)
    UserStory.storeNewStep(chatId, 'welcome')
    messageSender(chatId, 'text', 'your welcome')
    KBList = [['Add Expense'], ['My Account']]
    messageSender(chatId, 'keyboard', 'share your owe', KBList)


def addExpense(chatId):
    UserStory.storeNewStep(chatId, 'AddExpense')
    messageSender(chatId, 'hide', 'create group')
    messageSender(chatId, 'reply', 'what is your group name?')

def howMuch(chatId,text):
    UserStory.storeData(chatId,{'group_name' : str(text)})
    UserStory.storeNewStep(chatId, 'HowMuch')
    messageSender(chatId, 'reply', 'how much?')


def forWhat(chatId,text):
    alpha = False
    for char in str(text):
        if char.isalpha() == True:
            alpha = True
    if alpha == True:
        messageSender(chatId,'reply', 'please number, how much?')
        return False
    else:
        UserStory.storeData(chatId, {'cost': str(text)})
        UserStory.storeNewStep(chatId, 'ForWhat')
        messageSender(chatId, 'reply', 'for what?')
        return False

#todo: separate new step to new func with message and last one
#todo: change store step to goto Step

def forWho(chatId,text):
    if UserStory.isStoreData(chatId,'description') == False:
        UserStory.storeData(chatId, {'description': str(text)})
    if UserStory.isStoreData(chatId,'group_id'):
        messageSender(chatId, 'keyboard', 'you must select',[['NEW'],['ALL']])
    else:
        UserStory.storeNewStep(chatId, 'ForWho')
        messageSender(chatId, 'reply', 'for who?')

def MyAcc(chatId):
    UserStory.storeNewStep(chatId, 'MyAcc')
    messageSender(chatId, 'keyboard', 'my profile:', [['My Groups'], ['My Ledger']])

def MyLedger(chatId):
    UserStory.storeNewStep(chatId, 'MyLedger')
    state = PikInterActor.makeTotalAccStatement(chatId)
    KBList = [['OWE'], ['CREDITOR']]
    messageSender(chatId, 'keyboard', str(state), KBList)

def MyCreditor(chatId):
    BKList = PikInterActor.getUserCreditorButton(chatId)
    if BKList is None:
        messageSender(chatId, 'text', 'you dont have')
    else:
        messageSender(chatId, 'button', 'your creditor', BKList)

def MyOwe(chatId):
    BKList = PikInterActor.getUserOweButton(chatId)
    if BKList is None:
        messageSender(chatId, 'text', 'you dont have')
    else:
        messageSender(chatId, 'button', 'your owe', BKList)


def MyGroups(chatId):
    UserStory.storeNewStep(chatId, 'MyGroups')

    KBList = PikInterActor.getMyGroups(chatId)
    if len(KBList) == 0:
        messageSender(chatId, 'text', 'doesnt exist')
    else:
        messageSender(chatId, 'button', 'this is your groups', KBList)


def createBillandFlush(chatId):
    dataStory = UserStory.getUserStroy(chatId)
    PikInterActor.createBillAndShare(chatId,dataStory['data'])
    # shareMems = UserStory.getUserShareToMembers(chatId)
    # messageSender(chatId,'you have new bill', shareMems)
    UserStory.freshUserSteps(chatId)
    messageSender(chatId, 'hide', 'created')
    #todo:same to MyAcc
    UserStory.storeNewStep(chatId, 'MyAcc')
    messageSender(chatId, 'keyboard', 'my profile:', [['My Groups'], ['My Ledger']])

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    stage = UserStory.getLastStage(chat_id)
    #todo: set priority to remove this if else
    if (content_type == 'text'):
        if str(msg['text']) == '/start' or str(msg['text']) == 'Menu':
            welcome(chat_id,msg)
            return False
        if str(msg['text']) == 'My Account' and stage == 'welcome':
            MyAcc(chat_id)
            return False
        if (str(msg['text']) == 'Add Expense' and stage == 'welcome'):
            addExpense(chat_id)
            return False
        if stage == 'MyLedger' and str(msg['text']) == 'CREDITOR':
            MyCreditor(chat_id)
            return False
        if stage == 'MyLedger' and str(msg['text']) == 'OWE':
            MyOwe(chat_id)
            return False
        if stage == 'MyAcc' and str(msg['text']) == 'My Groups':
            MyGroups(chat_id)
            return False
        if stage == 'settle' and str(msg['text']) == 'YES':
            uStory = UserStory.getUserStroy(chat_id)
            settle = uStory['data']['settle']
            PikInterActor.settle(settle)
            MyLedger(chat_id)
            return False
        if stage == 'settle' and str(msg['text']) == 'NO':
            MyLedger(chat_id)
            return False
        if stage == 'MyAcc' and str(msg['text']) == 'My Ledger':
            MyLedger(chat_id)
            return False
        if stage == 'AddExpense':
            howMuch(chat_id,msg['text'])
            return False
        if stage == 'HowMuch':
            forWhat(chat_id,msg['text'])
            return False
        if stage == 'ForWhat' and msg['text'] == 'NEW':
            UserStory.storeNewStep(chat_id, 'ForWho')
            messageSender(chat_id, 'reply', 'for who?')
            return False
        if stage == 'ForWhat' and msg['text'] == 'ALL' and UserStory.isStoreData(chat_id,'group_id'):
            UserStory.storeData(chat_id,{'shareToAll' : True})
            createBillandFlush(chat_id)
            return False
        if stage == 'ForWhat':
            forWho(chat_id, msg['text'])
            return False
        if stage == 'ForWho' and str(msg['text']) == 'anymore?':
            createBillandFlush(chat_id)
            return False
    if stage == 'ForWho':
        if content_type == 'contact':
            if 'user_id' in msg['contact']:
                if msg['contact']['user_id'] != msg['chat']['id']:
                    UserStory.storeData(chat_id, {'shareTo': {msg['contact']['user_id'] : msg['contact']}})
                messageSender(chat_id, 'keyboard', 'from your contact', [['anymore?']])
                return False
        messageSender(chat_id, 'keyboard', 'should contact', [['anymore?'], ['Menu']])
        return False




def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    bot.answerCallbackQuery(query_id, text='Got it')
    cT = str(query_data[0])
    cTId = int(query_data[1:])
    if cT == 'G':
        UserStory.storeData(from_id,{'group_id': cTId})
        UserStory.storeNewStep(from_id, 'HowMuch')
        messageSender(from_id, 'reply', 'how much?')
    if cT == 'O' or cT == 'C':
        UserStory.storeData(from_id, {'settle': cTId})
        UserStory.storeNewStep(from_id, 'settle')
        state = PikInterActor.getTotalAccBetween(from_id,cTId)
        state = state + 'are you sure??'
        KBList = [['YES'],['NO']]
        messageSender(from_id, 'keyboard', state, KBList)


TOKEN = '235238648:AAEu9NQ9OROtBpQ1wwxJ0wbEcWKspkrKAmU'  # get token from command-line

bot = telepot.Bot(TOKEN)
# MessageLoop(bot, handle).run_as_thread() #simple loop
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

    # KBList=[['Add', 'List'], ['Settings', 'a']]
    # KBList=[[dict(text = 'Add', request_contact=True), 'List'], ['Settings', 'a']]
    # KBList=[
    #     [dict(text='Line 1, BTN 1', callback_data='11')],
    #     [dict(text='Line 1, BTN 2', callback_data='12'), dict(text='Line2, button 2', callback_data='22')]
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=KBList)
    # keyboard = InlineKeyboardMarkup(inline_keyboard=KBList)
    # bot.sendMessage(chat_id, msg,reply_markup=keyboard)



#
# {'message_id': 1436, 'from': {'id': 103218048, 'is_bot': False, 'first_name': 'Mahsa', 'username': 'Mahsame', 'language_code': 'en-AU'},
#  'chat': {'id': 103218048, 'first_name': 'Mahsa', 'username': 'Mahsame', 'type': 'private'}, 'date': 1541244605,
#  'reply_to_message': {'message_id': 1435, 'from': {'id': 235238648, 'is_bot': True, 'first_name': 'ScoreGuest', 'username': 'ScoreGuessBot'},
#                       'chat': {'id': 103218048, 'first_name': 'Mahsa', 'username': 'Mahsame', 'type': 'private'}, 'date': 1541244562, 'text': 'for who?'},
#  'contact': {'phone_number': '989112718982', 'first_name': 'Shayan', 'last_name': 'Hoseini', 'user_id': 22222222}}
#
# {'message_id': 1457,
#  'from': {'id': 103218048, 'is_bot': False, 'first_name': 'Mahsa', 'username': 'Mahsame', 'language_code': 'en-AU'},
#  'chat': {'id': 103218048, 'first_name': 'Mahsa', 'username': 'Mahsame', 'type': 'private'}, 'date': 1541244829,
#  'contact': {'phone_number': '09112703615', 'first_name': 'man'}}