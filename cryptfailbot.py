#!/usr/bin/python3


import zpipe
import time


rooms = ["cryptfailbot-test"]


def info(zp, cls, instance, message):
    nn = zpipe.Zephyrgram('cryptfailbot', cls, instance, None, 'auto', False,
                          ['ryp in pyp', message])
    zp.zwrite(nn)


def handle_zgram(zp, zgram):
    if zgram.cls not in rooms:
        return
    opcode = zgram.opcode.lower()
    if 'auto' in opcode:
        return
    try:
        message = zgram.fields[1]
    except IndexError:
        return
    if not message:
        return
    if 'crypt' in opcode and '-----BEGIN PGP MESSAGE' in message:
        return
    if not check_rate(zgram.cls):
        return
    info(zp, zgram.cls, zgram.instance, 'cryptfail!')


last_time = {}
def check_rate(cls):
    l = last_time.get(cls, float('-inf'))
    if time.time() >= l + 5:
        last_time[cls] = time.time()
        return True
    else:
        return False


def main():
    zp = zpipe.ZPipe(["zpipe"], handle_zgram)
    for room in rooms:
        zp.subscribe(room)

if __name__ == '__main__':
    main()
