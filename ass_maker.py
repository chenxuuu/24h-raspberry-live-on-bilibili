#coding:utf-8


def make_ass(filename, info, path):
    file_content = '''123123
dwadwadwad
'''+info+'''asdasd
saddsa'''

    file = open(path+'/downloads/'+str(filename)+'.ass','w')
    file.write(file_content)
    file.close()
