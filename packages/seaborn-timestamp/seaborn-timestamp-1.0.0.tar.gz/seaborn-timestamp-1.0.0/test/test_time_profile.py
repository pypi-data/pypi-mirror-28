from seaborn.time_profile import *
import time
import unittest

def basic():
    sleep(1)
    print("Hello World!")

class time_test(unittest.TestCase):
    def test_message(self,function=basic,line_number=1, message='test',
                     now=time.time(), thread_start=time.time()):
        msg = TimeMessage(function,line_number,message,now,thread_start)
        return msg

    def test_report(self):
        msg = self.test_message()
        self.assertEqual(msg.report(1),{})

    def test_update(self):
        msg = self.test_message()
        msg.update(time.time())
        self.assertEqual(1,1)   #TODO: Finish
        return msg

def smoke_test():
    """
    * Note this test is done 10 times to remove timing anomalies
    * Note Line number are only included so the test doesn't need to be updated on code change

    This will run a series of tests just to ensure the time profile works
    It should print out the following answer::
        | Function   | Line Number | Message                 | Start | End | Count | Min | Max | Avg | Sum |
        | func_frame | 209         | Starting 1 : 0          | 0.0   | 0.1 | 1     | 0.1 | 0.1 | 0.1 | 0.1 |
        | func_frame | 211         | Next 2 : 1              | 0.1   | 0.3 | 1     | 0.2 | 0.2 | 0.2 | 0.2 |
        | func_frame | 213         | Start and End 7 : 3     | 0.3   | 1.0 | 1     | 0.7 | 0.7 | 0.7 | 0.7 |
        | func_frame | 206         | Message Internal_0 : 10 | 1.0   | 1.0 | 1     | 0.0 | 0.0 | 0.0 | 0.0 |
        | func_frame | 219         | start loop test 1 : 12  | 1.2   | 5.4 | 5     | 0.1 | 0.1 | 0.1 | 0.5 |
        | func_frame | 221         | next loop test 2 : 13   | 1.3   | 5.6 | 5     | 0.2 | 0.2 | 0.2 | 1.0 |
        | func_frame | 207         |                         | 1.5   | 6.4 | 15    | 0.1 | 0.3 | 0.2 | 3.6 |
        | func_frame | 225         | Starting 1              | 6.4   | 6.4 | 0     |     |     |     |     |
    """
    globals()['SIGNIFICANT_DIGITS'] = 1
    TimeProfile.SIGNIFICANT_DIGITS = 1 # this is to make the test work
    tmi = TimeProfile.message

    def internal_loop_call_1_15():
        tmi()
        sleep(.1)

    @TimeProfile.decorator
    def decorator_test_4_6(a, b):
        assert a == 'a' and b == 'b'

        sleep(.4)
        tmi("Message Internal_0 : 10", line_number=206)

    def start():
        tmi("Starting 1 : 0", create=True, line_number=209)
        sleep(.1)
        tmi("Next 2 : 1", line_number=211)
        sleep(.2)
        tmi("Start and End 7 : 3", line_number=213)
        sleep(.3)
        decorator_test_4_6('a', b='b')

        tmi("Start and End 7 : 3", done=True, line_number=217)
        sleep(.2)
        for i in range(5):
            tmi("start loop test 1 : 12", line_number=219)
            sleep(.1)
            tmi("next loop test 2 : 13", line_number=221)
            for j in range(3):
                sleep(.2)
                internal_loop_call_1_15()
        tmi("Starting 1", done=True, line_number=225)
        return TimeProfile.report_table()

    calc_answer = start()
    calc_answer.tab = '    '
    right_answer = smoke_test.__doc__.split('::')[-1].replace('\n    ', '\n')[1:-1]
    print('Time Profile Report:\n%s'%calc_answer)
    for i in range(10):
        if str(calc_answer) == right_answer:
            return
        calc_answer = start()

if __name__ == "__main__":
    unittest.main()
