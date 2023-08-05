def smoke_test():
    """ This will test some basic uses of the timestamp """
    import re
    _now = now()
    print('\n\n            now = %s' % _now)
    assert re.search(TIMESTAMP_FORMAT, _now), '%s is not the correct format' % _now

    _str_to_datetime = str_to_datetime(_now)
    print('str_to_datetime = %s' % _str_to_datetime)

    _datetime_to_str = datetime_to_str(_str_to_datetime)
    print('datetime_to_str = %s' % _datetime_to_str)

    assert _now == _datetime_to_str, '%s != %s' % (_now, _datetime_to_str)
