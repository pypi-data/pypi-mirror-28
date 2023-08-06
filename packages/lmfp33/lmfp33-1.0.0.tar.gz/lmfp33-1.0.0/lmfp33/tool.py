import datetime 
import calendar



class tools:

    @staticmethod
    def add_months(dt,months):
        dt=datetime.datetime.strptime(dt,'%Y-%m-%d')
        month = dt.month - 1 + months
        if month>=0:
             year = dt.year + int(month / 12)
        else:
              year = dt.year + int(month / 12)-1
        month = int(month % 12 + 1)
        day = min(dt.day,calendar.monthrange(year,month)[1])
        x=dt.replace(year=year, month=month, day=day)
        x=datetime.datetime.strftime(x,'%Y-%m-%d')
        return x 

