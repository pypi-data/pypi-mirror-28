import random,time


def time_sleep(total_time_sleep):
    delay_schedule = list()
    while sum(delay_schedule) < total_time_sleep:
        delay_schedule.append(random.randint(1, 10))
    print("total time sleep", total_time_sleep)
    print(delay_schedule)
    for delay in delay_schedule:
        time.sleep(delay)
