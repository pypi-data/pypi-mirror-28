import json
import os
import base64
import getpass

def set_net_id():
    net_id = input_user_creds(True)
    creds["me"] = net_id
    write_creds(creds)

def set_user():
    # If they didn't have any users, add a new object
    if "users" not in creds:
        creds["users"] = {}

    users = creds["users"]

    net_id, password = input_user_creds()

    users[net_id] = {"password": password}
    write_creds(creds)

def delete_user():
    net_id = input_user_creds(True)

    if "users" not in creds:
        raise Exception("You have no users saved in your creds file. To add a user, use the `set_user` function.")

    if net_id not in creds["users"]:
        raise Exception("{} does not exist in your user list.".format(net_id))

    del creds["users"][net_id]
    write_creds(creds)

def set_client():
    # If they didn't have any clients, add a new object
    if "clients" not in creds:
        creds["clients"] = {}

    clients = creds["clients"]

    client_id, id, secret, sandbox_id, sandbox_secret = input_client_creds()

    clients[client_id] = {"id":id, "secret": secret, "sandbox_id": sandbox_id, "sandbox_secret": sandbox_secret}
    write_creds(creds)

def delete_client():
    client_id = input_client_creds(True)

    if "clients" not in creds:
        raise Exception("You have no clients saved in your creds file. To add a client, use the `set_client` function.")

    if client_id not in creds["clients"]:
        raise Exception("{} does not exist in your client list.".format(client_id))

    del creds["clients"][client_id]
    write_creds(creds)

### PRIVATE FUNCTIONS ###

def read_creds():
    try:
        with open(CRED_LOCATION) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def read_creds():
    try:
        with open(CRED_LOCATION) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_creds(creds):
    with open(CRED_LOCATION, "w") as f:
        json.dump(creds, f, indent = "\t")

def input_user_creds(net_id_only = False):
    net_id = input("Net ID: ")
    if net_id_only:
        return net_id

    password = getpass.getpass("Password: ")
    password = str(base64.b64encode(password.encode("utf-8")))
    return net_id, password

def input_client_creds(client_id_only = False):
    client_id = input("client_id: ")
    if client_id_only:
        return client_id

    id = input("id:" )
    secret = input("secret: ")
    sandbox_id = input("sandbox_id: ")
    sandbox_secret = input("sandbox_secret: ")
    return client_id, id, secret, sandbox_id, sandbox_secret


CRED_LOCATION = "{}/Documents/Credentials/creds.json".format(os.environ["HOME"])
creds = read_creds()