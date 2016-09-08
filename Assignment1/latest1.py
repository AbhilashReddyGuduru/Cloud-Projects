import swiftclient
import os
import datetime

user = 'Admin_66f6118215840cb6a3037874dc242f416e9aaac0'
key = 'ow}jjvGj/C((o39g'
project_id = 'c4e2d8fe4ff74fc9b527d992b78da901'
region_name = 'dallas'
user_id="b98b0277d50c41d9ac442cd99b994fc9"
project="object_storage_45a35408_f718_4d62_9a5b_1268b9ff9f9d"

conn = swiftclient.Connection(
        user=user,
        key=key,
        authurl='https://identity.open.softlayer.com/v3',
		auth_version='3',
		os_options={"project_id": project_id,
                    "user_id": user_id,
                    "region_name": region_name
							 }
						
	
)

container_name = 'assignment1_container'
conn.put_container(container_name);
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
cur = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT pass FROM users WHERE name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
def upload():
    
    file_name=raw_input("Enter the file name: ")
    
    with open(file_name,'rb') as f :
        b = os.path.getsize(file_name)
        if(b>1024):
            print "File size exceeds the specified limit\n"
            return 
        conn.put_object(container_name,file_name,f.read(),content_type='text/plain')
def download():
    a=[]
    print "List of files present in bluemix\n"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print '{0}'.format(data['name'])
            a.append(str(data['name']))
            
            
    file_name=raw_input("Enter the file name to be downloaded: ")
    
    if(file_name in a):
        downloaded_file_name = 'downloadexample.txt'
        obj = conn.get_object(container_name, file_name)
        with open(downloaded_file_name, 'w') as my_example:
            my_example.write(obj[1])
            print "\nObject %s downloaded successfully." % downloaded_file_name
    else:
        print "file not found in cloud service"

def listf():
    print "List of files present in bluemix\n"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print '{0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

def delete():
    a=[]
    print "List of files present in bluemix\n"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print '{0}'.format(data['name'])
            a.append(str(data['name']))
            
            
    file_name=raw_input("Enter the file name to be deleted: ")
    
    if(file_name in a):
        conn.delete_object(container_name, file_name)
        print "File deleted successfully"
    else:
        print "File not found in cloud service"

def deletetime():
    a=[]
    print "List of files present in bluemix\n"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print '{0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
            a.append(str(data['name']))

     
    time=raw_input("Enter the time to delete files: ")

    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            date1=str(data['last_modified'])
            print date1
            if( date1 == time):
               file_name=data['name']
               print file_name
               if(file_name in a):
                 conn.delete_object(container_name, file_name)
                 print "File deleted successfully"
            else:
                 print "File not deleted"
            
def readfile():

    a=[]
    print "List of files present in bluemix\n"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print '{0}'.format(data['name'])
            a.append(str(data['name']))
            
    file_name=raw_input("Enter the file name")
    if(file_name in a):
      with open(file_name,'rb') as f :
          lines=f.readlines()
          print lines[1]
    else:
        print "File not found in cloud service" 

    
    
    
choice=1
while(choice != 0):
    print "\nIbm BlueMix Cloud Storage Assignment\n"
    print "1:Upload File"
    print "2:Download File"
    print "3:List Files"
    print "4:Delete File"
    print "5:Delete with time"
    print "6:readfile"
    print "0:Exit"
    choice=raw_input("Enter a selection: ")
    choice=int(choice)
    if(choice==1):
        upload()
    elif(choice==2):
        download()
    elif(choice==3):
        listf()
    elif(choice==4):
        delete()
    elif(choice==5):
        deletetime()
    elif(choice==6):
        readfile()
    
