"""
Назначения функций:
user_get - принимает id пользователя или короткий адрес. Возвращает id пользователя.
information_groups - принимает тип объекта, который нужно вернуть, id пользователя, токен.
                     Возвращает список групп и краткую нформацию о ней, если type_object=list.
                     Возвращает множество названий груп, если type_object=set
friend_list - Принимает id пользователя. Возвращает id его друзей
delete_joint_groups - принимает множество названий групп и список id друзей. Выводит список названий групп, которые есть только у пользователя
list_information_individual_group - список названий групп. Возвращает Более расширенную информацию о них. Информацию берет из функции information_groups
exit_file - создает json файл и кладет туда информациюю о группах

"""


import requests
import json
import time


token = "5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128"
user_id_or_screen_name = input()


def user_get(user_id_or_screen_name):
    params = {
        "user_ids": user_id_or_screen_name,
        "v": 5.70
    }

    user_information = requests.get("https://api.vk.com/method/users.get", params=params)
    return user_information.json()["response"][0]["id"]


def information_groups(type_object, user_id, token):
    params_my_groups = {
        "access_token": token,
        "user_id": user_id,
        "extended": 1,
        "fields": "members_count",
        "v": 5.70
    }
    group_list = requests.get("https://api.vk.com/method/groups.get", params=params_my_groups)
    name_group_type_object = type_object()

    if type_object == list:
        for group_information in group_list.json()["response"]["items"]:
            name_group_type_object.append([group_information['name'], group_information['id'], group_information['members_count']])
    else:
        for group_information in group_list.json()["response"]["items"]:
            name_group_type_object.add(group_information['name'])
    return name_group_type_object,

def friend_list(user_id):
    params_my_friends = {
        "access_token": token,
        "user_id": user_id,
        "v": 5.70
    }

    friend_list = requests.get("https://api.vk.com/method/friends.get", params=params_my_friends)
    return friend_list


information_groups_set = set(information_groups(set, user_get(user_id_or_screen_name), token)[0])

friend_list = friend_list(user_get(user_id_or_screen_name)).json()["response"]["items"]


def delete_joint_groups(information_groups_set, friend_list):
    inquiry = 0

    for friend_id in friend_list:
        params_groups_my_friend = {
            "access_token": token,
            "user_id": friend_id,
            "extended": 1,
            "v": 5.70
        }
        print("Осталось обработать друзей: {}, Времени примерно осталось: {} секунд".format(len(friend_list) - inquiry, round((len(friend_list) - inquiry) / 2.7, 0 )))

        start_time = time.time()
        groups_my_friends = requests.get("https://api.vk.com/method/groups.get", params=params_groups_my_friend)
        inquiry += 1
        if "error" in groups_my_friends.json():
            pass
        else:
            for groups_friend in groups_my_friends.json()["response"]["items"]:
                information_groups_set.discard(groups_friend["name"])
        if inquiry % 3 == 0:
            if time.time() - start_time > 1:
                pass
            else:
                time.sleep(1 - (time.time() - start_time))
    name_group_list_ = list(information_groups_set)
    return name_group_list_


name_grop_list_ = delete_joint_groups(information_groups_set, friend_list)
print("Подождите еще немного...")


def list_information_individual_group(name_grop_list_):
    list_information_individual_group = list()

    for group_information in list(information_groups(list, user_get(user_id_or_screen_name), token)[0]):
        if group_information[0] in name_grop_list_:
            list_information_individual_group.append(group_information)
    return list_information_individual_group


def exit_file():
    json_list = []
    for group_infotmation in list_information_individual_group(name_grop_list_):
        json_list.append({
            "name": group_infotmation[0],
            "gid": str(group_infotmation[1]),
            "members_count": str(group_infotmation[2])
        })
    with open("groups.json", "w", encoding="UTF-8") as f:
        json.dump(json_list, f)


exit_file()
print("json файл сформирован")


