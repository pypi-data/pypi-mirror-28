import timeboard as tb
from timeboard.interval import Interval
from timeboard.workshift import Workshift
from timeboard.exceptions import (OutOfBoundsError,
                                  PartialOutOfBoundsError,
                                  UnacceptablePeriodError)

import datetime
import pandas as pd
import pytest

@pytest.fixture(scope='module')
def tb_12_days():
    return tb.Timeboard(base_unit_freq='D',
                        start='31 Dec 2016', end='12 Jan 2017',
                        layout=[0, 1, 0, 0, 2, 0])
    # 31  01  02  03  04  05  06  07  08  09  10  11  12
    #  0   1   0   0   2   0   0   1   0   0   2   0   0
    #
    # _on_duty_idx == [0:1, 1:4, 2:7, 3:10]
    # _off_duty_idx == [0:0, 1:2, 2:3, 3:5, 4:6, 5:8, 6:9, 7:11, 8:12]


class TestIntervalFindMyBounds(object):

    def test_interval_find_my_bounds_on(self):
        clnd = tb_12_days()
        for locs in ((2,11), (4, 11), (2,10), (4,10)):
            ivl = Interval(clnd, locs, clnd.default_schedule)
            _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
            assert duty_loc == (1, 3)

    def test_interval_find_my_bounds_off(self):
        clnd = tb_12_days()
        for locs in ((1,10), (2, 10), (1,9), (2,9)):
            ivl = Interval(clnd, locs, clnd.default_schedule)
            _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
            assert duty_loc == (1, 6)

    def test_interval_find_my_bounds_no_such_duty_in_interval(self):
        clnd = tb_12_days()
        
        ivl = Interval(clnd, (11, 12), clnd.default_schedule)
        _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
        assert duty_loc == (None, None)
        _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
        assert duty_loc == (7, 8)
        
        ivl = Interval(clnd, (0, 0), clnd.default_schedule)
        _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
        assert duty_loc == (None, None)
        _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
        assert duty_loc == (0, 0)
        
        ivl = Interval(clnd, (10, 10), clnd.default_schedule)
        _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
        assert duty_loc == (3, 3)
        _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
        assert duty_loc == (None, None)

    def test_interval_find_my_bounds_no_on_duty_in_tb(self):
        clnd = tb.Timeboard(base_unit_freq='D',
                            start='31 Dec 2016', end='12 Jan 2017',
                            layout=[0])
        ivl = Interval(clnd, (1,2), clnd.default_schedule)
        _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
        assert duty_loc == (None, None)
        _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
        assert duty_loc == (1, 2)

    def test_interval_find_my_bounds_no_off_duty_in_tb(self):
        clnd = tb.Timeboard(base_unit_freq='D',
                            start='31 Dec 2016', end='12 Jan 2017',
                            layout=[1])
        ivl = Interval(clnd, (1,2), clnd.default_schedule)
        _, duty_loc = ivl._get_duty_idx('on', ivl.schedule)
        assert duty_loc == (1, 2)
        _, duty_loc = ivl._get_duty_idx('off', ivl.schedule)
        assert duty_loc == (None, None)


class TestIntervalFirstLastNth(object):

    def test_interval_nth_on(self):
        clnd = tb_12_days()
        for locs in ((2,11), (4, 11), (2,10), (4,10)):
            ivl = Interval(clnd, locs, clnd.default_schedule)
            wsf = ivl.first()
            wsl = ivl.last()
            ws2 = ivl.nth(1)
            wsneg = ivl.nth(-2)
            assert isinstance(wsf, Workshift)
            assert isinstance(wsl, Workshift)
            assert isinstance(ws2, Workshift)
            assert isinstance(wsneg, Workshift)
            assert wsf._loc == 4
            assert wsl._loc == 10
            assert ws2._loc == 7
            assert wsneg._loc == 7

    def test_interval_nth_off(self):
        clnd = tb_12_days()
        for locs in ((1,10), (2, 10), (1,9), (2,9)):
            ivl = Interval(clnd, locs, clnd.default_schedule)
            wsf = ivl.first(duty='off')
            wsl = ivl.last(duty='off')
            ws2 = ivl.nth(1, duty='off')
            wsneg = ivl.nth(-2, duty='off')
            assert isinstance(wsf, Workshift)
            assert isinstance(wsl, Workshift)
            assert isinstance(ws2, Workshift)
            assert isinstance(wsneg, Workshift)
            assert wsf._loc == 2
            assert wsl._loc == 9
            assert ws2._loc == 3
            assert wsneg._loc == 8

    def test_interval_nth_any(self):
        clnd = tb_12_days()
        ivl = Interval(clnd, (2, 10), clnd.default_schedule)
        wsf = ivl.first(duty='any')
        wsl = ivl.last(duty='any')
        ws2 = ivl.nth(1, duty='any')
        wsneg = ivl.nth(-2, duty='any')
        assert isinstance(wsf, Workshift)
        assert isinstance(wsl, Workshift)
        assert isinstance(ws2, Workshift)
        assert isinstance(wsneg, Workshift)
        assert wsf._loc == 2
        assert wsl._loc == 10
        assert ws2._loc == 3
        assert wsneg._loc == 9

    def test_interval_nth_single(self):
        clnd = tb_12_days()
        for loc, duty in ((0, 'off'), (3, 'any'), (4,'on'),
                          (7, 'any'), (12, 'off')):
            ivl = Interval(clnd, (loc, loc), clnd.default_schedule)
            wsf = ivl.first(duty=duty)
            wsl = ivl.last(duty=duty)
            ws2 = ivl.nth(0, duty=duty)
            assert isinstance(wsf, Workshift)
            assert isinstance(wsl, Workshift)
            assert isinstance(ws2, Workshift)
            assert wsf._loc == loc
            assert wsl._loc == loc
            assert ws2._loc == loc

    # def test_interval_nth_zero(self):
    #     clnd = tb_12_days()
    #     ivl = Interval(clnd, (1, 10), clnd.default_schedule)
    #     with pytest.raises(ValueError):
    #         ivl.nth(0)

    def test_interval_nth_no_on_duty(self):
        clnd = tb_12_days()
        ivl = Interval(clnd, (2, 3), clnd.default_schedule)
        with pytest.raises(OutOfBoundsError):
            ivl.first()
        with pytest.raises(OutOfBoundsError):
            ivl.last()
        with pytest.raises(OutOfBoundsError):
            ivl.nth(0)

    def test_interval_nth_no_off_duty(self):
        clnd = tb_12_days()
        ivl = Interval(clnd, (4, 4), clnd.default_schedule)
        with pytest.raises(OutOfBoundsError):
            ivl.first(duty='off')
        with pytest.raises(OutOfBoundsError):
            ivl.last(duty='off')
        with pytest.raises(OutOfBoundsError):
            ivl.nth(0, duty='off')

    def test_interval_nth_OOB(self):
        clnd = tb_12_days()
        ivl = Interval(clnd, (2, 8), clnd.default_schedule)
        with pytest.raises(OutOfBoundsError):
            ivl.nth(2)
        with pytest.raises(OutOfBoundsError):
            ivl.nth(5, duty='off')
        with pytest.raises(OutOfBoundsError):
            ivl.nth(7, duty='any')

    def test_interval_default_nth(self):
        clnd = tb_12_days()
        ivl = clnd.get_interval()
        for duty, first, third, last in ( ('on', 1, 7, 10),
                                          ('off', 0, 3, 12),
                                          ('any', 0, 2, 12)):
            assert ivl.first(duty=duty)._loc == first
            assert ivl.nth(2, duty=duty)._loc == third
            assert ivl.last(duty=duty)._loc == last

    def test_interval_default_nth_OOB(self):
        clnd = tb_12_days()
        ivl = clnd.get_interval()
        with pytest.raises(OutOfBoundsError):
            ivl.nth(4)
        with pytest.raises(OutOfBoundsError):
            ivl.nth(9, duty='off')
        with pytest.raises(OutOfBoundsError):
            ivl.nth(13, duty='any')


class TestIntervalCount(object):

    def test_interval_count_on(self):
        clnd = tb_12_days()
        for locs in ((2,11), (4, 11), (2,10), (4,10)):
            assert Interval(clnd, locs, clnd.default_schedule).count() == 3

    def test_interval_count_off(self):
        clnd = tb_12_days()
        for locs in ((1, 10), (2, 10), (1, 9), (2, 9)):
            assert Interval(clnd, locs,
                            clnd.default_schedule).count(duty='off') == 6

    def test_interval_count_any(self):
        clnd = tb_12_days()
        assert Interval(clnd, (1,9),
                        clnd.default_schedule).count(duty='any') == 9

    def test_interval_count_single(self):
        clnd = tb_12_days()
        for loc, duty in ((2, 'off'), (3, 'any'), (4,'on'), (7, 'any')):
            assert Interval(clnd, (loc, loc),
                            clnd.default_schedule).count(duty=duty) == 1

    def test_interval_count_no_such_duty(self):
        clnd = tb_12_days()
        assert Interval(clnd, (2, 3),
                        clnd.default_schedule).count() == 0
        assert Interval(clnd, (4, 4),
                        clnd.default_schedule).count(duty='off') == 0

    def test_interval_count_default(self):
        clnd = tb_12_days()
        ivl = clnd.get_interval()
        assert ivl.count() == 4
        assert ivl.count(duty='off') == 9
        assert ivl.count(duty='any') == 13


@pytest.fixture(scope='module')
def tb_281116_020517_8x5():
    week5x8 = tb.Organizer(marker='W', structure=[[1, 1, 1, 1, 1, 0, 0]])
    amendments = pd.Series(index = pd.date_range(start='01 Jan 2017',
                                                 end='10 Jan 2017',
                                                 freq='D'),
                           data = 0).to_dict()
    return tb.Timeboard(base_unit_freq='D',
                        start='28 Nov 2016', end='02 May 2017',
                        layout=week5x8,
                        amendments = amendments)


class TestIntervalDaysCountPeriodsM(object):

    def test_interval_d_count_periods_m_part_full_part(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('29 Dec 2016', '01 Apr 2017'))
        assert ivl.count_periods('M') == 2.0/22.0 + 3.0
        assert ivl.count_periods('M', duty='off') == 1.0/9.0 + 3.0 + 1.0/10.0
        assert ivl.count_periods('M', duty='any') == 3.0/31.0 + 3.0 + 1.0/30.0

    def test_interval_d_count_periods_m_with_gap(self):
        week5x8 = tb.Organizer(marker='W', structure=[[1, 1, 1, 1, 1, 0, 0]])
        amendments = pd.Series(index=pd.date_range(start='01 Feb 2017',
                                                   end='28 Feb 2017',
                                                   freq='D'),
                               data=0).to_dict()
        clnd = tb.Timeboard(base_unit_freq='D',
                            start='28 Nov 2016', end='02 May 2017',
                            layout=week5x8,
                            amendments=amendments)
        ivl = clnd.get_interval(('29 Dec 2016', '01 Apr 2017'))
        # in February all days are off -> Feb does not count when duty='on'
        assert ivl.count_periods('M') == 2.0/22.0 + 2.0
        assert ivl.count_periods('M', duty='off') == 1.0/9.0 + 3.0 + 1.0/10.0
        assert ivl.count_periods('M', duty='any') == 3.0/31.0 + 3.0 + 1.0/30.0


    def test_interval_d_count_periods_m_part_part(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('29 Dec 2016', '13 Jan 2017'))
        assert ivl.count_periods('M') == 2.0 / 22.0 + 3.0/15.0
        assert ivl.count_periods('M', duty='off') == 1.0/9.0 + 10.0/16.0
        assert ivl.count_periods('M', duty='any') == 3.0/31.0 + 13.0/31.0

    def test_interval_d_count_periods_m_part_within(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('06 Feb 2017', '12 Feb 2017'))
        assert ivl.count_periods('M') == 5.0 / 20.0
        assert ivl.count_periods('M', duty='off') == 2.0 / 8.0
        assert ivl.count_periods('M', duty='any') == 7.0 / 28.0

    def test_interval_d_count_periods_m_exact(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('01 Jan 2017', '31 Jan 2017'))
        assert ivl.count_periods('M') == 1
        assert ivl.count_periods('M', duty='off') == 1
        assert ivl.count_periods('M', duty='any') == 1
        ivl2 = clnd.get_interval(('09 Jan 2017', '31 Jan 2017'))
        assert ivl2.count_periods('M') == 1
        assert ivl2.count_periods('M', duty='off') == 8.0/16.0
        assert ivl2.count_periods('M', duty='any') == 23.0/31.0
        ivl2 = clnd.get_interval(('01 Jan 2017', '29 Jan 2017'))
        assert ivl2.count_periods('M') == 13.0/15.0
        assert ivl2.count_periods('M', duty='off') == 1
        assert ivl2.count_periods('M', duty='any') == 29.0 / 31.0


class TestIntervalDaysCountPeriodsCornerCases(object):

    def test_interval_d_count_periods_extending_outside_tb(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('29 Nov 2016', '01 Dec 2016'))
        # Part of Nov 2016 is outside the tb
        with pytest.raises(PartialOutOfBoundsError):
            ivl.count_periods('M')
        # however ivl does not have off-duty units,
        # so if duty='off' is given, the result will be zero for any periods,
        # whether they are within the tb or not
        assert   ivl.count_periods('M', duty='off') == 0
        # Part of May 2017 is outside the tb
        ivl = clnd.get_interval(('24 Apr 2017', '01 May 2017'))
        with pytest.raises(PartialOutOfBoundsError):
            ivl.count_periods('M')


    def test_interval_d_count_periods_m_no_such_duty_in_ivl(self):
        clnd = tb_281116_020517_8x5()
        # within a month
        ivl = clnd.get_interval(('01 Jan 2017', '10 Jan 2017'))
        assert ivl.count_periods('M') == 0
        # striding month boundary
        ivl = clnd.get_interval(('31 Dec 2016', '10 Jan 2017'))
        assert ivl.count_periods('M') == 0
        # within a month
        ivl = clnd.get_interval(('30 Jan 2017', '31 Jan 2017'))
        assert ivl.count_periods('M', duty='off') == 0
        # striding month boundary
        ivl = clnd.get_interval(('30 Jan 2017', '03 Feb 2017'))
        assert ivl.count_periods('M', duty='off') == 0

    def test_interval_d_count_periods_w_no_such_duty_in_period(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('02 Jan 2017', '08 Jan 2017'))
        assert ivl.count_periods('W') == 0
        ivl = clnd.get_interval(('02 Jan 2017', '10 Jan 2017'))
        assert ivl.count_periods('W') == 0
        ivl = clnd.get_interval(('02 Jan 2017', '11 Jan 2017'))
        assert ivl.count_periods('W') == 1.0/3.0
        ivl = clnd.get_interval(('02 Jan 2017', '13 Jan 2017'))
        assert ivl.count_periods('W') == 1

    def test_interval_d_count_periods_same_freq(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('30 Mar 2017', '01 Apr 2017'))
        assert ivl.count_periods('D') == 2
        assert ivl.count_periods('D', duty='off') == 1
        assert ivl.count_periods('D', duty='any') == 3

    def test_interval_d_count_periods_higher_freq(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('30 Mar 2017', '01 Apr 2017'))
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('T')

    def test_interval_d_count_periods_unsupported(self):
        clnd = tb_281116_020517_8x5()
        ivl = clnd.get_interval(('30 Mar 2017', '01 Apr 2017'))
        # We support only native calendar periods: T, H, D, W, M, Q, A
        # We do not support periods with multipliers,
        # as it does not make sense in the context of count_periods
        for p in ('5D', '4W', '3M', '2A', '2Q'):
            with pytest.raises(UnacceptablePeriodError):
                ivl.count_periods(p)
        # Neither we support offsets bound to 'start', 'end' or 'business'
        for p in ('MS', 'BM', 'BMS', 'CBM', 'CBMS', 'BQ', 'QS', 'BQS',
                  'BA', 'BS', 'BAS', 'BH'):
            with pytest.raises(UnacceptablePeriodError):
                ivl.count_periods(p)


class TestIntervalDaysCountPeriodsW(object):
    #TODO: test shifted periods like W-TUE
    pass

class TestIntervalDaysCountPeriodsY(object):
    #TODO: test shifted periods like A-MAR
    pass


@pytest.fixture(scope='module')
def clnd_variable_mins(workshift_ref=None):
    if workshift_ref is None:
        workshift_ref = 'start'
    halfhours = tb.Organizer('30T', structure=[0, 1])
    splitter = tb.Organizer(marks=['01 Oct 2017 03:05',
                                   '01 Oct 2017 06:05',
                                   '01 Oct 2017 09:05',
                                   '01 Oct 2017 12:05'],
                            structure=[0, halfhours, 0, halfhours, 0])

    return tb.Timeboard('T', '01 Oct 2017', '01 Oct 2017 14:59',
                        layout=splitter,
                        workshift_ref=workshift_ref)

    #                   start  duration                 end  label  on_duty
    # loc
    # 0   2017-10-01 00:00:00       185 2017-10-01 03:04:59    0.0    False
    # 1   2017-10-01 03:05:00        30 2017-10-01 03:34:59    0.0    False
    # 2   2017-10-01 03:35:00        30 2017-10-01 04:04:59    1.0     True
    # 3   2017-10-01 04:05:00        30 2017-10-01 04:34:59    0.0    False
    # 4   2017-10-01 04:35:00        30 2017-10-01 05:04:59    1.0     True
    # 5   2017-10-01 05:05:00        30 2017-10-01 05:34:59    0.0    False
    # 6   2017-10-01 05:35:00        30 2017-10-01 06:04:59    1.0     True
    # 7   2017-10-01 06:05:00       180 2017-10-01 09:04:59    0.0    False
    # 8   2017-10-01 09:05:00        30 2017-10-01 09:34:59    0.0    False
    # 9   2017-10-01 09:35:00        30 2017-10-01 10:04:59    1.0     True
    # 10  2017-10-01 10:05:00        30 2017-10-01 10:34:59    0.0    False
    # 11  2017-10-01 10:35:00        30 2017-10-01 11:04:59    1.0     True
    # 12  2017-10-01 11:05:00        30 2017-10-01 11:34:59    0.0    False
    # 13  2017-10-01 11:35:00        30 2017-10-01 12:04:59    1.0     True
    # 14  2017-10-01 12:05:00       175 2017-10-01 14:59:59    0.0    False

class TestIntervalCountPeriodsCornerCases(object):

    def test_ivl_count_periods_shorter_than_ws_at_start(self):
        clnd = clnd_variable_mins()
        ivl = Interval(clnd, (0,3))
        # 3H long ws #0 is first in ivl
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='off')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='any')

    def test_ivl_count_periods_shorter_than_ws_at_mid(self):
        clnd = clnd_variable_mins()
        ivl = Interval(clnd, (5, 9))
        # 3H long ws #7 is in the middle of ivl
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='off')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='any')

    def test_ivl_count_periods_shorter_than_ws_at_end(self):
        clnd = clnd_variable_mins()
        ivl = Interval(clnd, (12, 14))
        # 3H long ws #14 is the last in ivl
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='off')
        with pytest.raises(UnacceptablePeriodError):
            ivl.count_periods('H', duty='any')

    def test_ivl_count_periods_avoiding_long_ws(self):
        clnd = clnd_variable_mins()
        ivl = Interval(clnd, (1, 3))
        # ivl contains ws 1, 2, 3
        # ws 1, 2 fall into hour of 03:00; ws 3, 4 fall into hour of 04:00
        assert ivl.count_periods('H') == 1.0 # (1/1 + 0/1)
        assert ivl.count_periods('H', duty='off')  == 2.0
        assert ivl.count_periods('H', duty='any') == 1.5 # (2/2 + 1/2)

    def test_ivl_count_periods_long_ws_caught_by_period(self):
        clnd = clnd_variable_mins('end')
        ivl = Interval(clnd, (1, 3))
        # ivl contains ws 1, 2, 3
        # hour of 03:00 catches ws 0 as ws ref time is end time
        # ws 0 is 3 hours long but it is NOT in the interval so we don't raise
        # ws 0, 1 fall into hour of 03:00; ws 2, 3 fall into hour of 04:00
        assert ivl.count_periods('H') == 1.0 # (0/0 + 1/1)
        assert ivl.count_periods('H', duty='off')  == 1.5 # (1/2 + 1/1)
        assert ivl.count_periods('H', duty='any') == 1.5 # (1/2 + 2/2)


class TestIntervalSchedules(object):
    
    def test_ivl_count_with_schedules(self):
        clnd = tb_12_days()
        sdl = clnd.add_schedule(name='sdl', selector=lambda x: x>1)
        ivl0 = clnd()
        ivl1 = clnd(schedule=sdl)
        assert ivl0.count() == 4
        assert ivl1.count() == 2
        assert ivl0.count(schedule=sdl) == 2
        assert ivl1.count(schedule=clnd.default_schedule) == 4

    def test_ivl_nth_with_schedules(self):
        clnd = tb_12_days()
        sdl = clnd.add_schedule(name='sdl', selector=lambda x: x>1)
        ivl0 = clnd()
        ivl1 = clnd(schedule=sdl)
        ws = ivl0.nth(1)
        assert ws._loc == 4
        assert ws.schedule.name == 'on_duty'
        ws = ivl1.nth(1)
        assert ws._loc == 10
        assert ws.schedule.name == 'sdl'
        ws = ivl0.nth(1,schedule=sdl)
        assert ws._loc == 10
        assert ws.schedule.name == 'sdl'
        ws = ivl1.nth(1,schedule=clnd.default_schedule)
        assert ws._loc == 4
        assert ws.schedule.name == 'on_duty'

    def test_ivl_nth_with_schedules_OOB(self):
        clnd = tb_12_days()
        sdl = clnd.add_schedule(name='sdl', selector=lambda x: x>1)
        ivl0 = clnd()
        ivl1 = clnd(schedule=sdl)
        assert ivl0.nth(2)._loc == 7
        with pytest.raises(OutOfBoundsError):
            ivl1.nth(2)

    def test_ivl_count_periods_with_schedules(self):
        clnd = tb.Timeboard('H', '01 Oct 2017', '02 Oct 2017 23:59',
                            layout=[0, 1, 0, 2])
        sdl = clnd.add_schedule(name='sdl', selector=lambda x: x > 1)
        ivl0 = clnd(('01 Oct 2017 14:00', '02 Oct 2017 23:59'))
        ivl1 = clnd(('01 Oct 2017 14:00', '02 Oct 2017 23:59'), schedule=sdl)
        assert ivl0.count_periods('D') == 5.0/12.0 + 1.0
        assert ivl1.count_periods('D') == 1.5
        assert ivl0.count_periods('D', schedule=sdl) == 1.5
        assert ivl1.count_periods('D', schedule=clnd.default_schedule) == \
                   5.0 / 12.0 + 1.0

    def test_ivl_bad_schedule(self):
        clnd = tb_12_days()
        sdl = clnd.add_schedule(name='sdl', selector=lambda x: x>1)
        with pytest.raises(TypeError):
            clnd(schedule='sdl')


class TestIntervalSum(object):

    def test_ivl_sum_numbers(self):
        clnd = tb. Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                             layout=[1,2],
                             default_selector=lambda label: label>1)
        ivl = tb.Interval(clnd,(2,9))
        assert ivl.sum() == 8
        assert ivl.sum(duty='off') == 4
        assert ivl.sum(duty='any') == 12

        clnd = tb. Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                             layout=[-2, 1.5],
                             default_selector=lambda label: label > 0)
        assert clnd().sum() == 7.5
        assert clnd().sum(duty='off') == -10.0
        assert clnd().sum(duty='any') == -2.5

    def test_ivl_sum_strings(self):
        clnd = tb. Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                             layout=['a', 'b'],
                             default_selector=lambda label: label=='b')
        ivl = tb.Interval(clnd, (2, 9))
        assert ivl.sum() == 'bbbb'
        assert ivl.sum(duty='off') == 'aaaa'
        assert ivl.sum(duty='any') == 'abababab'

    def test_ivl_sum_no_such_duty(self):
        clnd = tb.Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                            layout=[1, 2],
                            )
        ivl = tb.Interval(clnd, (2, 9))
        assert ivl.sum() == 12
        assert ivl.sum(duty='off') == 0
        assert ivl.sum(duty='any') == 12

        clnd = tb.Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                            layout=[1, 2],
                            default_selector=lambda label: label > 2)
        ivl = tb.Interval(clnd, (2, 9))
        assert ivl.sum() == 0
        assert ivl.sum(duty='off') == 12
        assert ivl.sum(duty='any') == 12

    def test_ivl_sum_exotic_fails(self):

        # try some exotic type of labels
        clnd = tb. Timeboard('D', '01 Oct 2017', '10 Oct 2017',
                             layout=[pd.Period('2017', freq='A')])
        with pytest.raises(TypeError):
            clnd().sum()
        with pytest.raises(TypeError):
            clnd().sum(duty='any')
        # however ther is not "off" duty in the interval
        assert clnd().sum(duty='off') == 0


    






