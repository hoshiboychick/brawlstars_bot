import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from tok import main_token
from db import name_to_nick, admins

# Connect to vk api
vk_session = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(vk_session, group_id=213213914)


# Bot sends message
def write(chat_id, text):
    vk_session.method('messages.send', {'chat_id': chat_id, 'message': text, 'random_id': 0})


# Bot deletes message
def delete(msg_id):
    vk_session.method('messages.delete',
                      {'message_ids': msg_id, 'delete_for_all': 1, 'peer_id': peer_id, 'group_id': 213213914})


# Get firstname and lastname by user id
def get_user_info(user_id):
    return vk_session.method('users.get', {'user_ids': user_id})


# Template for bot's message
def msg_template():
    return '[@id' + str(user_id) + '(' + str(name) + ')] (' + str(name_to_nick[name]) + '): '


# Listen to events
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            # Properties of each message
            attach = event.message['attachments']
            msg = event.message['text']
            chat_id = event.chat_id
            user_id = event.message['from_id']
            msg_id = event.message['conversation_message_id']
            peer_id = event.message['peer_id']
            print(event.message)

            # Name in VK
            first_name = get_user_info(user_id)[0]['first_name']
            last_name = get_user_info(user_id)[0]['last_name']
            name = str(first_name) + ' ' + str(last_name)

            if name not in admins and not attach:
                # delete(data_msg)
                write(chat_id, str(msg_template()) + msg)
            elif attach and name not in admins:
                write(chat_id, '⬆' + str(name_to_nick[name]) + '⬆')
