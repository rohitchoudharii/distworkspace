import subprocess

ps = subprocess.run(args = 'start-ssh-agent.cmd', text=True,shell = True,input = "rohit")
print(ps)
