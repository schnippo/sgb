import subprocess

#cmd = "ls /dev | grep ttyACM"
cmd = "ls /dev "
sp = subprocess.Popen(cmd,
                            shell=True,
                      stdout = subprocess.PIPE,
                      stderr = subprocess.PIPE,
                      universal_newlines=True)
#rc = sp.wait()
out = sp.communicate()[0].split()
#values = out.split()
#print("output : ", values)
print("output : ", out)
