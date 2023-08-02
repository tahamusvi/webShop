from . import jalali
import datetime

def jalali_converter(time):

    jmonth = ["فرودین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
    time_to_str = "{},{},{}".format(time.year,time.month,time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index,month in enumerate(jmonth):
        if time_to_list[1] == index+1:
            time_to_list[1] = month
            break

    hour = time.hour
    minute = time.minute
    min = ""

    if(int(time.minute)+30):
        hour += 5
    else:
        hour += 4

    minute += 30
    minute %= 60
    if(minute<10):
        min = '0' + str(minute)
    else:
        min = str(minute)

    output = "{} {} {} ساعت {}:{}".format(
    time_to_list[2],
    time_to_list[1],
    time_to_list[0],
    int(hour),
    min,
    )
    return persion_converter_number(output)




def persion_converter_number(en_number):
    numbers = {
        "1" : "۱",
        "2" : "۲",
        "3" : "۳",
        "4" : "۴",
        "5" : "۵",
        "6" : "۶",
        "7" : "۷",
        "8" : "۸",
        "9" : "۹",
        "0" : "۰",
    }
    for k , v in numbers.items():
        en_number = en_number.replace(k,v)
    return en_number




# def jalali_month_show():
#     jmonth = ["فرودین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
#     now = datetime.datetime.now.month()
#     month = now.month
#     for index , mongth in enumerate(jmonth):
#         if month == index + 1:
#             month =  mongth
#             break
#
#
#
#     return month
