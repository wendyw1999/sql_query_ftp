from ftplib import FTP 
import cx_Oracle as oracle
import pandas as pd


def query_to_csv(query):
    
    query = "select * from most_viewed_sample m inner join user_profile u on m.userid = u.userid"
    try:
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        SqlDomain = cursor.description
        DomainNum = len(SqlDomain)
        SqlDomainName = [None]*DomainNum
        for i in range(DomainNum):
            SqlDomainName[i] = SqlDomain[i][0]
    #获取表头
    
        df = pd.DataFrame(data)
        df.columns = SqlDomainName
    
    
    
        display(df)
        file_name = input("保存csv为（不用csv后缀,如果不保存不填写）：   ")
        if file_name !="":
            df.to_csv(file_name+".csv")
            print("Successfully Saved to CSV in path: "+file_name+".csv")
        cursor.close()
        print("Finished")
        return file_name+".csv"
    
    except:
        print("Query failed")
def upload_ftp(ip,port,username,password,filename):
    ftp = FTP()
# 打开调试级别2, 显示详细信息 
    ftp.set_debuglevel(2) # 
    try:
        ftp.connect(ip,int(port))
        ftp.login(username,password)
    except:
        ftp.connect("127.0.0.1",2121)
        ftp.login("alex", "123")
          
     
    ftp.cwd("drop_files") #ftp location下的目录，里面用于存放文件
    # 切换目录, 相对于ftp目录, 比如设置的ftp根目录为/vat/ftp, 那么pub就是/var/ftp下面的目录 
    
    f = open(filename, 'rb') # 打开csv文件夹
    ftp.storbinary("STOR {}".format(filename), f,1024) 
    f.close() # 关闭调试模式 
    ftp.set_debuglevel(0) # 退出FTP连接 
    ftp.quit()
    print("Successfully upload")
    print("Quitting FTP upload")
    
if __name__ == '__main__':
    username = input("Database Username(必须大写）:   ")
    password = input("Database Password:   ")
    database_ip = input("数据库IP(默认127.0.0.1):   ")
    port = input("Port(默认1521):    ")
    database = input("服务名/数据库(默认orcl):    ")
    string = username+"/"+password+"@"+database_ip+":"+"port"+"/"+database
    try:
        db = oracle.connet(string)
    except:
        db = oracle.connect('tenant01/123456@127.0.0.1:1521/orcl')
    print("successfully_connected")
    query = input("Enter SQL Query:    ")
    filename  = query_to_csv(query)
    ipconfig = input("FTP IP address(default 127.0.0.1):   ")
    port = input("Port number(default 2121):   ")
    username = input("FTP Username: (default alex):   ")
    password = input("FTP Password: (default 123):   ")
    upload_ftp(ipconfig,port,username,password,filename)
    

    
    

