import os, filecmp ,sys

codes = {200:'success',404:'file not found',400:'error',408:'timeout'}

def compile(file,lang):

    if(lang =='python3'):
        return 200

    if (os.path.isfile(file)):
        if lang=='c':
            os.system('gcc ' + file)
        elif lang=='cpp':
            os.system('g++ ' + file)
        elif lang=='java':
            os.system('javac ' + file)
        if (os.path.isfile('a.out')) or (os.path.isfile('main.class')):
            return 200
        else:
            return 400
    else:
        return 404

def run(file,input,lang):
    cmd='sudo -u judge '
    if lang == 'java':
        cmd += 'java main'
    elif lang=='c' or lang=='cpp':
        cmd += './a.out'
    elif lang=='python3':
        cmd += 'python3 '+ file

    r = os.system(('timeout '+ '1'+' '+cmd+' < '+input + ' > '+testout))

    # r = os.system("python "+file +' < '+input + ' > '+testout)

    if r==0:
        return 200
    elif r==31744:
        return 408
    else:
        return 400

def match(output):
    if os.path.isfile('out.txt') and os.path.isfile(output):
        b = filecmp.cmp('out.txt',output)
        os.remove('out.txt')
        return b
    else:
        return 404

params=sys.argv
path = params[1]
folder = path.split('/')[-2]
file = path.split('/')[-1]

path = os.getcwd()
os.chdir(f"{path}/temp/{folder}")
lang = params[2]


testin =  "input.txt"
testout =  "output.txt"

status=compile(file,lang)
if status == 200:
    status=run(file,testin,lang)
print(codes[status])

print(params)

os.system()