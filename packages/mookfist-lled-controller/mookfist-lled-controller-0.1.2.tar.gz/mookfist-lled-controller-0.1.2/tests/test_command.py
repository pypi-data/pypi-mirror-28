from mookfist_lled_controller.bridge import Command

def test_command_equals():
    cmd1 = Command(2)
    cmd1[0] = 0x00
    cmd1[1] = 0x01

    cmd2 = Command(2)
    cmd2[0] = 0x00
    cmd2[1] = 0x01

    assert cmd1 == cmd2

def test_command_notEquals():
    cmd1 = Command(2)
    cmd1[0] = 0x00
    cmd1[1] = 0x02

    cmd2 = Command(2)
    cmd2[0] = 0x00
    cmd2[1] = 0x01

    assert (cmd1 != cmd2) == True

    cmd3 = Command(3)
    cmd3[0] = 0x00
    cmd3[1] = 0x01
    cmd3[2] = 0x02

    assert cmd1 != cmd3

def test_command_getByteArray():

    cmd1 = Command(2)
    cmd1[0] = 0x00
    cmd1[1] = 0xff

    msg = cmd1.message()

    assert msg[0] == 0x00
    assert msg[1] == 0xff

    assert isinstance(msg, (bytes, bytearray))

def test_command_getString():

    cmd = Command(4)
    cmd[0] = 0x10
    cmd[1] = 0x20
    cmd[2] = 0x05

    msg = cmd.message_str()

    assert msg == '10 20 05 --'

def test_command_checksum():

    cmd = Command(2)
    cmd[0] = 0x00
    cmd[1] = 0xff

    checksum = cmd.checksum()

    assert checksum == 255
