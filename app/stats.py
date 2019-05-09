from app import db
from app.models import User, Chat, Message

HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7

def time_stat():
    messages_data = Message.query.all()

    messages_quantity = len(messages_data)

    stat_by_hours = []
    for i in range(HOURS_IN_DAY):
        stat_by_hours.append(0)

    stat_by_days = []
    for i in range(DAYS_IN_WEEK):
        stat_by_days.append(0)

    for msg in messages_data:
        weekday = msg.timestamp.weekday()
        hour = msg.timestamp.hour - 1
        stat_by_days[weekday] += 1
        stat_by_hours[hour] += 1

    return stat_by_hours, stat_by_days

def average_words_in_message():
    messages_data = Message.query.all()
    messages_quantity = len(messages_data)
    words_quantity = 0

    for msg in messages_data:
        msg_splited = msg.body.split()
        words_quantity += len(msg_splited)
        words_quantity_average = words_quantity // messages_quantity

    return words_quantity_average

def user_activity():
    users_data = User.query.all()

    most_active_users = []

    for u in users_data:
        most_active_users.append([u.id, u.username])
        messages_quantity_by_id = len(Message.query.filter(Message.user_id==u.id).all())
        most_active_users[u.id - 1].append(messages_quantity_by_id)

    most_active_users.sort(key=lambda row: row[2], reverse=True)

    return most_active_users
