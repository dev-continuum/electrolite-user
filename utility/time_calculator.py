import datetime
import pytz


def get_current_date_time_format(timezone="UTC", time_format="isoformat"):
    data_to_return = {}
    if time_format == "isoformat":
        date_time_object = datetime.datetime.now(pytz.timezone(timezone))
        data_to_return["datetime_string"] = date_time_object.strftime('%Y-%m-%d %H:%M:%S')
        data_to_return["date"] = date_time_object.date().isoformat()
        data_to_return["time"] = date_time_object.time().isoformat(timespec='seconds')
        data_to_return["timezone"] = str(date_time_object.tzinfo)
        return data_to_return
    else:
        return data_to_return


def convert_time_stamp_to_time_delta(time_stamp: str):
    date_time_object = datetime.datetime.strptime(time_stamp, "%H:%M:%S")
    return datetime.timedelta(hours=date_time_object.hour, minutes=date_time_object.minute,
                              seconds=date_time_object.second)


def generate_all_slots():
    all_slots = set()
    init_datetime = datetime.datetime(1, 1, 1, 00, 00, 00)
    end_datetime = datetime.datetime(1, 1, 1, 23, 30, 00)
    delta = datetime.timedelta(minutes=30)
    all_slots.add(str(init_datetime.time()))
    while init_datetime < end_datetime:
        init_datetime += delta
        all_slots.add(str(init_datetime.time()))
    return all_slots


def calculate_30_min_slots(from_time, to_time):
    from_time = datetime.datetime.strptime(from_time, "%H:%M:%S").time()
    to_time = datetime.datetime.strptime(to_time, "%H:%M:%S").time()
    date = datetime.date(1, 1, 1)
    slots = []
    datetime1 = datetime.datetime.combine(date, from_time)
    datetime2 = datetime.datetime.combine(date, to_time)
    delta = datetime.timedelta(minutes=30)
    while datetime2 > datetime1:
        slots.append(str(datetime1.time()))
        datetime1 = datetime1 + delta
    return slots


def get_dat_time_combo(date):
    total_slots = {"00:00:00", "00:30:00", "01:00:00", "01:30:00", "02:00:00", "02:30:00", "03:00:00", "03:30:00", "04:00:00", "04:30:00",
                   "05:00:00", "05:30:00", "06:00:00", "06:30:00", "07:00:00", "07:30:00", "08:00:00", "08:30:00", "09:00:00", "09:30:00",
                   "10:00:00", "10:30:00", "11:00:00", "11:30:00", "12:00:00", "12:30:00", "13:00:00", "13:30:00", "14:00:00", "14:30:00",
                   "15:00:00", "15:30:00", "16:00:00", "16:30:00", "17:00:00", "17:30:00", "18:00:00", "18:30:00", "19:00:00", "19:30:00",
                   "20:00:00", "20:30:00", "21:00:00", "21:30:00", "22:00:00", "22:30:00", "23:00:00", "23:30:00"}

    return [f"{date}:{t}" for t in total_slots]


if __name__ == '__main__':
    # booked_datetime = calculate_30_min_slots(datetime.time(2, 00), datetime.time(2, 30))
    # all = generate_all_slots()
    # print(booked_datetime)
    # print(all)
    # print(sorted(all.difference(booked_datetime)))
    print(calculate_30_min_slots("00:30:00", "01:30:00"))