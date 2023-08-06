import psycopg2 
import pymssql

class db:
    pools={
            'mssql':[
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','basedb','dbo'],
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','regdb','dbo'],
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','msa_intinfo','dbo'],
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','sbsj','resmg'],
                        
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','providentfund','resmg'],
                    
                        ['DmyyReader','Sjbd*0708','10.204.168.114\MSSQLSERVER2','test_dmyy','dbo']
                        ,['sa','since2015','10.204.169.70','sist','dbo']
                    ]
            ,
            'postgresql':[
                            ['postgres','since2015','10.204.169.71','test','t1']
                            ,['postgres','since2015','10.204.169.17','sist','public']
                            ,['postgres','since2015','10.204.22.58','sist','public']
                         ]
        
            }
    @staticmethod
    def db_query(sql,dbtype='postgresql',pool=0,conp=None):
        if dbtype=='postgresql':
            result=db.db_query_postgresql(sql,pool,conp)
            return result
        if dbtype=='mssql':
        
            result=db.db_query_mssql(sql,pool,conp)
            return result 
        result='不在指定数据库类型内'
        return result
    @staticmethod
    def db_query_postgresql(sql,pool=0,conp=None):
        if conp is None:conp=db.pools['postgresql'][pool]
        #con=create_engine("postgresql://%s:%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]),encoding='utf-8')
        con=psycopg2.connect(user=conp[0],password=conp[1],host=conp[2],port='5432',database=conp[3])
        cur=con.cursor()

        #sql="set search_path to %s;"%conp[4]+sql 
        cur.execute(sql)
        b=[w[0] for w in  cur.description]
        #a=[list(w) for w in cur.fetchall()]
        a=cur.fetchall()
        data=[tuple(b)]
        data.extend(a)
        cur.close()
        con.close()
        return data

    @staticmethod
    def db_query_mssql(sql,pool=0,conp=None):
        if conp is None:conp=db.pools['mssql'][pool]
        #con=create_engine("postgresql://%s:%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]),encoding='utf-8')
        con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
        cur=con.cursor()

        #sql="set search_path to %s;"%conp[4]+sql 
        cur.execute(sql)
        b=[w[0] for w in  cur.description]
        #a=[list(w) for w in cur.fetchall()]
        a=cur.fetchall()
        data=[tuple(b)]
        data.extend(a)
        cur.close()
        con.close()
        return data

