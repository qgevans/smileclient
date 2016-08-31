__module_name__ = "smileclient-responder"
__module_version__ = "0.1"
__module_description__ = "Replies to all events in a channel with \":D\""

import hexchat

responding_channels = { "##:D" }
triggering_commands = { "PRIVMSG", "NOTICE", "JOIN", "PART", "QUIT", "TOPIC", "MODE" }
overly_happy_users = { "heddwch" }
rejoin_delay = 5000

rejoin_hooks = dict()

def responder_hook(word, word_eol, userdata):
    triggering_command = word[1]
    triggering_channel = hexchat.get_info("channel")
    responding_channel = False
    for channel in responding_channels:
        if(hexchat.nickcmp(triggering_channel, channel) == 0):
            responding_channel = True
    if responding_channel:
        triggering_user = word[0][1:].split('!', 1)[0]
        print(triggering_command)
        if(hexchat.nickcmp(triggering_command, "PRIVMSG") == 0 or hexchat.nickcmp(triggering_command, "NOTICE") == 0):
            overly_happy = False
            if(word[3] == ":D" or word[3] == "::D" or word[3] == ":+:D"):
                for user in overly_happy_users:
                    if(hexchat.nickcmp(triggering_user, user) == 0):
                        overly_happy = True
                        break
                if(overly_happy):
                    print("Ignoring message from overly happy user: {}".format(triggering_user))
                    return hexchat.EAT_NONE
        command = "MSG"
        if(hexchat.nickcmp(triggering_command, "NOTICE") == 0):
            command = "NOTICE"
        hexchat.command(command + " " + channel + " :D")
    return hexchat.EAT_NONE

def rejoin(userdata):
    hook = rejoin_hooks[userdata]
    del rejoin_hooks[userdata]
    hexchat.unhook(hook)
    print("Rejoining {}…".format(userdata))
    hexchat.command("join " + userdata)
    return hexchat.EAT_NONE

def handle_kick(word, word_eol, userdata):
    channel = hexchat.get_info("channel")
    if(hexchat.nickcmp(channel, userdata) == 0):
        print("There was a kick")
        if(hexchat.nickcmp(word[3], hexchat.get_info("nick")) == 0):
            print("Rejoining {} in {}ms…".format(channel, rejoin_delay))
            rejoin_hooks[channel] = hexchat.hook_timer(rejoin_delay, rejoin, channel)
    return hexchat.EAT_NONE

for channel in responding_channels:
    hexchat.command("join " + channel)
    hexchat.hook_server("KICK", handle_kick, channel)
    for command in triggering_commands:
        hexchat.hook_server(command, responder_hook, channel)
