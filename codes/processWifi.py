import os
import process360
import util
import datetime


def processDate(ts, bin):
    per = 3600*bin
    return int(ts/per)


def genDateDict(path, bin):
    datedict = {}
    filenames = os.listdir(path)
    filenames.sort()
    for filename in os.listdir(path):
        csvfile = os.path.join(path, filename)
        print csvfile
        if os.path.getsize(csvfile):
            with open(csvfile, 'r') as csvf:
                for line in csvf:
                    cols = line.strip().split(',')
                    if cols.__len__() == 4:
                        ts = processDate(int(cols[0]), bin)
                        dev_ip, ap_ip = cols[2], cols[3]
                        key = dev_ip+','+ap_ip
                        if key not in datedict:
                            datedict[key] = [ts]
                        else:
                            datedict[key].append(ts)
    print('dict length:'.format(datedict.__len__()))
    return datedict


def genStEtLines(datedict):
    tuples, st_et_lines = [], []
    for key in datedict:
        dates = datedict[key]
        length = dates.__len__()
        if length == 1:
            continue
        else:
            sorted_dates = sorted(dates)
            dev_ip, ap_ip = key.split(',')
            st = sorted_dates[0]
            st_idx = 0
            for i in range(1, length):
                date = sorted_dates[i]
                'ask every 5 min'
                if i == length-1 and i - st_idx > 0:
                    et = date
                    print('st:{},et:{}'.format(st, et))
                    tuple = (dev_ip, ap_ip, st, et)
                    tuples.append(tuple)
                else:
                    'margin larger than 30 minutes, must disconnect'
                    if date - sorted_dates[i - 1] >= 1:
                        et = sorted_dates[i-1]
                        tuple = (dev_ip, ap_ip, st, et)
                        tuples.append(tuple)
                        st = date
                        st_idx = i
    sorted_tups = sorted(tuples, key=lambda x: x[3])
    for tup in sorted_tups:
        line = ','.join((tup[0], tup[1], str(tup[2]), str(tup[3])))
        st_et_lines.append(line)
    return st_et_lines


def genStartDate(file):
    itimes= []
    with open(file, 'r') as f:
        for line in f:
            itime, utime = line.strip().split(',')[2:4]
            itimes.append(int(itime))
    itime_st = str(min(itimes))
    return itime_st


def delWrongMac(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            ap_mac = line.strip().split(',')[1]
            if ap_mac == '"00 00 00 00 00 00 "':
                continue
            else:
                lines.append(line)
    f.close()
    fw = open(file, 'w')
    fw.writelines(lines)
    fw.close()


def gen_maped_it_ut_file(path, startDate):
    callerdict = {}
    calleedict = {}
    itime_utime_file = os.path.join(path, 'it_ut.txt')
    maped_itime_utime_file = os.path.join(path, 'maped_it_ut.txt')
    caller_mapfile = os.path.join(path, 'caller_map.txt')
    callerf = open(caller_mapfile, 'w')
    callee_mapfile = os.path.join(path, 'callee_map.txt')
    calleef = open(callee_mapfile, 'w')
    with open(itime_utime_file, 'r') as iuf, open(maped_itime_utime_file, 'w') as mapiuf:
        for line in iuf:
            caller, callee, it, ut, num = line.strip().split(',')
            if caller not in callerdict:
                callerdict[caller] = callerdict.__len__()
            maped_caller = callerdict[caller]
            if callee not in calleedict:
                calleedict[callee] = calleedict.__len__()
            maped_callee = calleedict[callee]
            maped_it = int(it) - startDate
            maped_ut = int(ut) - startDate
            mapiuf.write(','.join((str(maped_caller), str(maped_callee), str(maped_it), str(maped_ut), num)))
            mapiuf.write('\n')
            callerf.write(','.join((caller, str(maped_caller))))
            callerf.write('\n')
            calleef.write(','.join((callee, str(maped_callee))))
            calleef.write('\n')
        iuf.close()
        mapiuf.close()
        callerf.close()
        calleef.close()


def gen_itime_stay_file(path, startDate):
    # gen_maped_it_ut_file(path, startDate)
    maped_itime_utime_file = os.path.join(path, 'maped_it_ut.txt')
    itime_stay_file = os.path.join(path, 'it_stay.txt')
    utime_mapfile = os.path.join(path, 'utime_map.txt')
    with open(maped_itime_utime_file, 'r') as mapiuf, open(itime_stay_file, 'w') as isf, open(utime_mapfile, 'w') as utmapf:
        for line in mapiuf:
            dev, app, itime, utime, num = line.strip().split(',')
            stay = util.dateDuring(utime, itime, label='wifi')
            it_st = str(itime) + str(stay)
            utmapf.write(','.join((it_st, utime)))
            utmapf.write('\n')
            it_st_line = ','.join((dev, app, it_st, num))
            isf.write(it_st_line)
            isf.write('\n')
    mapiuf.close()
    isf.close()
    utmapf.close()
    maped_itime_stay_file = os.path.join(path, r'maped_it_stay.txt')
    util.gen_maped_it_st_file(path, itime_stay_file, maped_itime_stay_file)


def sortUtime(binpath):
    maped_it_ut_file = os.path.join(binpath, 'it_ut.txt')
    tuples = []
    with open(maped_it_ut_file, 'r') as mapiuf:
        for line in mapiuf:
            cols = line.strip().split(',')
            tup = (cols[0], cols[1], cols[2], int(cols[3]), cols[4])
            tuples.append(tup)
    sorted_tups = sorted(tuples, key=lambda x: x[3])
    lines = []
    for tup in sorted_tups:
        line = tup[0] + ',' + tup[1] + ',' + tup[2] + ',' + str(tup[3])+','+'1'+'\n'
        lines.append(line)
    new_maped_it_ut_file = os.path.join(binpath, 'it_ut.txt')
    newmapf = open(new_maped_it_ut_file, 'w')
    newmapf.writelines(lines)
    newmapf.close()


if __name__ == '__main__':
    path = '../../data/wifi'
    csvpath = os.path.join(path, 'csvfiles')
    bins = [0.5, 1]
    startDates = [844352, 422176]
    for i in range(bins.__len__()):
        print bins[i]
        binpath = os.path.join(path, 'bin=' + str(bins[i]))
        startDate = startDates[i]
        if not os.path.exists(binpath):
            os.mkdir(binpath)
        # sortUtime(binpath)
        gen_itime_stay_file(binpath, startDate)






