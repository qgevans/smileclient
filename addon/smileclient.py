__module_name__ = "smileclient"
__module_version__ = "0.1"
__module_description__ = "A corrollary client to smilebot"

import hexchat
smileclient_path = hexchat.get_info("configdir") + "/addons/smileclient/"

def load_module(module):
    hexchat.command("py load " + smileclient_path + module + ".py")
    hexchat.hook_unload(lambda current_module: hexchat.command("py unload smileclient-" + module))

load_module("hello")
load_module("responder")
