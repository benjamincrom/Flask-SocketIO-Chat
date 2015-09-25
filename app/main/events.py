import random
import copy

from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio

names = {}

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    global names
    room = session.get('name')
    if room == 'EndOfFile':
        contest_names = copy.deepcopy(names)
        winner = random.choice(contest_names.keys())
        contest_names[winner] = True
        for name in contest_names:
            if contest_names[name]:
                emit('message', {'msg': 'You are the winner!'}, room=name)
            else:
                emit('message', {'msg': 'Sorry!  Better luck next time!'}, room=name)
        fh = open('output.txt', 'a')
        fh.write("\n########   WINNER: {}!   ########\n".format(winner))
        fh.close()
    else:
        names[room] = False
        join_room(room)

        fh = open('output.txt', 'w')
        for name in sorted(names):
            fh.write("{}\n".format(name))
        fh.close()

@socketio.on('text', namespace='/chat')
def left(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('name')
    emit('message', {'msg': message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('name')
    leave_room(room)
