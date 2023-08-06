import pexpect

child = pexpect.spawn('python -m cmenu.py')
child.expect('>>> ')
child.sendline('execute')
print(child.before)
child.interact()
