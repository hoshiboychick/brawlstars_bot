import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tok import main_token

vk_session = vk_api.VkApi(token=main_token)
longpoll = VkLongPoll(vk_session)

name_to_nick = {'Владислав Лазебный': 'Vladig', 'Захар Беброчкин': 'MAT6_E6AL'}


def write(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def delete(msg_id):
    vk_session.method('messages.delete', {'message_ids': msg_id, 'delete_for_all': 1})


def get_user_info(user_id):
    return vk_session.method('users.get', {'user_ids': user_id})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:
                msg = event.text
                chat_id = event.chat_id
                user_id = event.user_id
                msg_id = event.message_id

                first_name = get_user_info(user_id)[0]['first_name']
                last_name = get_user_info(user_id)[0]['last_name']
                name = str(first_name) + ' ' + str(last_name)

                if user_id != 236517980:
                    delete(msg_id)
                    write(chat_id,
                          '[@id' + str(user_id) + '(' + str(name) + ')] (' + str(name_to_nick[name]) + '): ' + msg)
