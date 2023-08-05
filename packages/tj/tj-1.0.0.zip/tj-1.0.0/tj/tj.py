import os,sys,time,shutil
__doc__='''

 _______ ________
|__   __|___   __| PRODUCTIONS 2018
   | |      | |
   | |    __| |
   |_|    \___/ 

A module that can be used to to multiple common tasks that otherwise you
would do by writing long lines of code
Last modified: %s
File Size: %s %s
Last Accessed: %s
Date Created: %s''' % (time.asctime(time.localtime(os.stat(__file__)[-2])),
os.stat(__file__)[6],"Bytes",
time.asctime(time.localtime(os.stat(__file__)[-3])),
time.asctime(time.localtime(os.stat(__file__)[-1])))


#    DATA
__all__=['factorial','combination','permutation','factors','get_data','get_file_name',
        'get_full_path','all_files','get_folder_Size','get_Size','is_file','remove_dir','passed_time',
        'extract_filename','extract_foldername','get_last_modified']


__data__={'pi':3.141592653490860,'cwd':os.getcwd(),'full_path':sys.argv[0],'file_name':os.path.basename(sys.argv[0]),'functions':__all__}


#   FUNCTIONS
def factorial(x):
    '''Returns the factorial of a number x and x should be
    an integer'''
    product=1
    try:
        x=int(x)
    except:
        raise TypeError ,'Argument should be an integer'
    for i in range(1,x+1):
        product=product*i
    return product


def combination(n,r):
    '''Returns the combination C(n,r)'''
    try:
        n=int(n)
    except:
        raise TypeError,'First argument should be an integer.'
    try:
        r=int(r)
    except:
        raise TypeError,'Second argument should be an integer.'
    if n<r:
        raise Exception,'First argument should be greater than the second.'
    res=factorial(n)/(factorial(r)*factorial(n-r))
    return res


def permutation(n,r):
    '''Returns the permutation P(n,r)'''
    try:
        n=int(n)
    except:
        raise TypeError,'First argument should be an integer.'
    try:
        r=int(r)
    except:
        raise TypeError,'Second argument should be an integer.'
    if n<r:
        raise Exception,'First argument should be greater than the second.'
    res=factorial(n)/factorial(n-r)
    return res



def factors(num):
    '''Takes a number as argument and returns all its factors in a list
eg- if 24 is entered, result would be [1,2,3,4,6,8,12,24]'''
    l=[]
    num=int(num)
    i=0
    while i<(num/2+1):
        i+=1
        if i==0:
            continue
        if num%i==0:
            l+=[i]
    l+=[num]
    return l


def current_directory():
    '''Returs the current directory of the running script, takes no argument'''
    return os.getcwd()


def data():
    '''Return all the data of this module in a dictionary format'''
    return __data__


def get_file_name():
    '''Returns the name of the current running script'''
    return os.path.basename(sys.argv[0])


def get_full_path():
    '''Returns the full path of the current running script'''
    return sys.argv[0]



def all_files(directory,word=[''],):
    root=directory
    '''Returns a list of all the files in the directory
    word-> if the file name has either of the word in the list
    , then only it will be added in the list'''
    l=[]
    for folder, subfolders, files in os.walk(root):
        for file1 in files:
            add=False
            for i in word:
                if i in file1:
                    add=True
            if add:
                try:
                    filePath = os.path.join(folder, file1)
                except:
                    filePath=folder+'\\'+file1
                l+=[filePath]
    return l


def get_folder_Size(root):
    '''Returns size of a directory'''
    for a,b,c in os.walk(root):
        total=0
    for folder, subfolders, files in os.walk(root):
        for file1 in files:
            try:
                filePath = os.path.join(folder, file1)
            except:
                filePath=folder+'\\'+file1
            try:total+=os.path.getsize(filePath)
            except:pass
    return total


def is_file(path):
    '''Returns in bool if the path given is of a file or not'''
    try:
        os.path.isfile(path)
    except:
        return True


def get_Size(path,flag=False):
    '''Returns the size of the file/folder in a desired manner (automatically sees if its a folder or a file)
takes 2 arguments in which one if optional (filePath,flag=False)
filePath is the full path of the file and flag does the following-
    1) if flag=False, the size will be returned in bytes and in integer
    2) if flag is True, then the size will be returned in string
        in appropriate manner eg- 1024 bytes will be returnes as 1 KB
        etc..'''
    if flag!=False:
        try:
            size=get_folder_Size(path)
        except:
            size=os.path.getsize(path)

        if 1<=(size/(1024**3))<1024:
            size=str(size/(1024.0**3))[0:6]+' GB'

        elif 1<=(size/(1024**2))<1024:
            size=str(size/(1024.0**2))[0:6]+' MB'

        elif 1<=(size/1024)<1024:
            size=str(size/1024.0)[0:6]+' KB'

        else:
            size=str(size)+' Bytes'
        return size
    else:
        try:
            size=get_folder_Size(path)

        except:

            size=os.path.getsize(path)

        return size


def remove_dir(path):
    '''Deletes a directory which is either empty or non-empty'''
    shutil.rmtree(path)


def passed_time(flag=True):
    '''if flag=False, then returns the time after the function is called
        from the time the function was called first time in the program

    if flag=True, then returns the time in seconds b/w two successive calls
    Use it as a generator function
    You can create different instances to use it as per your convinience
    eg-
    import tj
    a=tj.passed_time()
    print a.next(); time.sleep(5)
    print a.next() #This is used after waiting 5 sec.
    b=tj.passed_time()
    print b.next(); time.sleep(5)
    print a.next(); time.sleep(5)
    print b.next()
>>>0.0
>>>5.0
>>>0.0
>>>5.0
>>>10.0
    '''
    t=time.time()
    while True:

        if flag:
            m=time.time()-t
            t=time.time()
            yield m
        if not flag:
            yield time.time()-t

def extract_filename(string):
    """Takes a path as a string as argument and returns the name of the file"""
    s=string[::-1]
    s2=''
    for i in s:
        if (i=="//") or (i=="\\"):
            break
        s2+=i
    s3=s2[::-1]
    return s3

def extract_foldername(string):
    """Takes a path as a string as argument and returns the name of the folder of the file"""
    s=string[::-1]
    a=0
    s2=''
    for i in s:
        if (i=="//") or (i=="\\"):
            a+=1
        if a>0:
            s2+=i
    s3=s2[::-1]
    return s3
            

def get_last_modified(path,flag=False):
    '''Get the date the the file was last modified of the.
    Arguments:\n path -> the path of the file
    flag-> Its a bool value, when False, the time is returned in
    Epoch seconds, if flag is True, time is returned in proper format.'''
    try:a=os.stat(path)[-2]
    except:raise "Path not found"
    if flag==False:
        return a
    if flag==True:
        return time.asctime(time.localtime(a))





