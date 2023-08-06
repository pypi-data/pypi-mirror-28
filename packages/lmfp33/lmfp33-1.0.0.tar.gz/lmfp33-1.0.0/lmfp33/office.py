import os 
import xlsxwriter as xl
import re
import datetime  

class office:
    xlformat={'font_size':10}
    xlpath="E:\\workdata\\task"

    @staticmethod 
    def checkpath(name,dir1=None):
        nw=datetime.datetime.strftime(datetime.datetime.now(),'data%Y%m%d')
        dirx=office.xlpath+'\\%s'%nw
        if not os.path.exists(dirx):os.mkdir(dirx)
        if dir1 is None:
            path=dirx+'\\%s.xlsx'%(name)
            i=1
            while os.path.exists(path):
                i+=1
                path=dirx+'\\%s(%d).xlsx'%(name,i)

            return path
        else:
            dirn=dirx+'\\%s'%dir1
            i=0
            dirx=dirn
            while os.path.exists(dirx):
              i+=1
              dirx="%s(%d)"%(dirn,i)
            os.mkdir(dirx)
            paths=[dirx+'\\%s.xlsx'%w for w in name]
            return paths
    @staticmethod
    def outdf(data,ws_name='Sheet 1',wb_name="dmyy"):
        
        wb_name=office.checkpath(wb_name)
        
        office._outdf(data,ws_name,wb_name)
        print("worksheet-%s完成"%ws_name)
        print("workbook-%s完成"%wb_name)

    @staticmethod
    def _outdf(data,ws_name,wb_name):
        wb=xl.Workbook(wb_name)
        fm=wb.add_format(office.xlformat)
        ws1=wb.add_worksheet(ws_name)
        i=0
        for w in data:
            ws1.write_row(i,0,w)
            i+=1
        ws1.set_column('A:AA',8.43,fm)
        wb.close()

    @staticmethod
    def outdfs(dts,ws_name='Sheet 1',wb_name="dmyy"):
        wb_name=office.checkpath(wb_name)
        office._outdfs(dts,ws_name,wb_name)
        print("worksheet-%s完成"%ws_name)
        print("workbook-%s完成"%wb_name)

    @staticmethod
    def _outdfs(dts,ws_name,wb_name):
        wb=xl.Workbook(wb_name)
        fm=wb.add_format(office.xlformat)
        ws1=wb.add_worksheet(ws_name)
        i=0
        for dt in dts:
            
            for w in dt:
                ws1.write_row(i,0,w)
                i+=1
            i+=5
        ws1.set_column('A:AA',8.43,fm)
        wb.close()

    @staticmethod 
    def outdfss(dtss,ws_names=None,wb_name="dmyy"):
        if ws_names is None:
            ws_names=["Sheet %d"%(i+1) for i in range(len(dtss))]
        wb_name=office.checkpath(wb_name)
        office._outdfss(dtss,ws_names,wb_name)

    @staticmethod
    def _outdfss(dtss,ws_names,wb_name):
        wb=xl.Workbook(wb_name)
        fm=wb.add_format(office.xlformat)
        wsi=0
        for dts in dtss:
            i=0
            ws1=wb.add_worksheet(ws_names[wsi])
            for dt in dts:
               
                for w in dt:
                    ws1.write_row(i,0,w)
                    i+=1
                i+=5
            ws1.set_column('A:AA',8.43,fm)
            print('worksheet-%s完成'%ws_names[wsi])
            wsi+=1
        wb.close()
        print('workbook-%s完成'%wb_name)

    @staticmethod
    def outdfsss(dtsss,ws_namess=None,wb_names=None,dir_name='集合'):
        n=len(dtsss)
        m=len(dtsss[0])
        if ws_namess is None:
            ws_namess=[["Sheet %d"%(j+1) for j in range(m)]  for i in range(n)]

        wb_names=office.checkpath(["dmyy_%d"%(i+1) for i in range(n)],dir_name)
        office._outdfsss(dtsss,ws_namess,wb_names)



    @staticmethod
    def _outdfsss(dtsss,ws_namess,wb_names):
        for i in range(len(wb_names)):
            office._outdfss(dtsss[i],ws_namess[i],wb_names[i])