from collections import OrderedDict
import os
import gzip
import util


def white_app(path):
    appset = set()
    white_appfile = os.path.join(path, 'white_app.txt')
    with open(white_appfile) as f:
        for line in f:
            appset.add(line.strip())
    return appset


def filter_app(path, gzfiles):
    appset = white_app(path)
    dirpath = os.path.join(path, 'filterUp')
    for name in gzfiles:
        gzfile = os.path.join(dirpath, name)
        name_suffix = name.split('.')[0]
        st, et = name_suffix.split('_')[:2]
        prefix = st+'_'+et
        print prefix
        inifilterUp = os.path.join(dirpath, prefix+'_filterapp.gz')
        with gzip.open(gzfile, 'r') as rgf, gzip.open(inifilterUp, 'w') as wgf:
            for line in rgf:
                cols = line.strip().split('\t')
                dev, app = cols[0], cols[1]
                if app not in appset:
                    wgf.write(line)
        rgf.close()
        wgf.close()


def generate_action_date_dict(filename, actidx, tsidx, delim):
    attribute_dict = OrderedDict()
    with gzip.open(filename, 'rb') as f_in:
        for line in f_in:
            'dev app version action date'
            cols = line.strip().split(delim)
            id = cols[0]
            app = cols[1]
            action = cols[actidx]
            date = cols[tsidx]
            key = id+','+app
            value = action+','+date
            if key not in attribute_dict:
                attribute_dict[key] = [value]
            else:
                attribute_dict[key].append(value)
    return attribute_dict


# (dev, app, inst, uninst)
def generate_inst_uninst_lines(attribute_dict, addval, delval):
    inst_uninst_lines = []
    tuples = []
    for key in attribute_dict:
        value = attribute_dict[key]
        dates = []
        for i in range(value.__len__()):
            action_date = value[i].split(',')
            action = int(action_date[0])
            date = int(action_date[1])
            if action == delval:
                'indicate that not uninst first, add the data'
                if dates.__len__() % 2 != 0:
                    dates.append(date)
            elif action == addval:
                if dates.__len__() % 2 == 0:
                    dates.append(date)

        if dates.__len__() < 2:
            continue
        else:
            id_app = key.split(',')
            for i in range(int(dates.__len__() / 2)):
                tuple = (id_app[0], id_app[1], dates[2 * i], dates[2 * i + 1])
                tuples.append(tuple)
    sorted_tups = sorted(tuples, key=lambda x: x[3])
    for tup in sorted_tups:
        line = tup[0] + ',' + tup[1] + ',' + str(tup[2]) + ',' + str(tup[3])
        inst_uninst_lines.append(line)
    return inst_uninst_lines


def gen_itime_utime_file(path):
    gzfiles = ['20180608_20180614_filterUp.gz', '20180615_20180622_filterUp.gz', '20180623_20180630_filterUp.gz', '20180701_20180707_filterUp.gz']
    filter_app(path, gzfiles)
    'gen itime_utime file'
    filterapp_gzfiles = ['20180608_20180614_filterapp.gz', '20180615_20180622_filterapp.gz','20180623_20180630_filterapp.gz', '20180701_20180707_filterapp.gz']
    filter_path = os.path.join(path, 'filterUp')
    for name in filterapp_gzfiles:
        print name
        filterUp_file = os.path.join(filter_path, name)
        attribute_dict = generate_action_date_dict(filterUp_file, 3, 4, '\t')
        inst_uninst_lines = generate_inst_uninst_lines(attribute_dict, 1, 2)
        name_suffix = name.split('.')[0]
        st, et = name_suffix.split('_')[:2]
        prefix = st + '_' + et
        print name_suffix
        file = os.path.join(path, prefix+'_itime_utime.txt')
        f = open(file, 'w')
        f.writelines(inst_uninst_lines)
    filenames = ['20180608_20180614_itime_utime.txt', '20180615_20180622_itime_utime.txt',
                 '20180623_20180630_itime_utime.txt', '20180701_20180707_itime_utime.txt']
    outname = '20180608_20180707_itime_utime.txt'
    util.concatfiles(path, filenames, outname)


def gen_maped_it_ut_file(path):
    callerdict = {}
    calleedict = {}
    itime_utime_file = os.path.join(path, 'it_ut.txt')
    maped_itime_utime_file = os.path.join(path, 'maped_it_ut.txt')
    caller_mapfile = os.path.join(path, 'caller_map.txt')
    callerf = open(caller_mapfile, 'w')
    callee_mapfile = os.path.join(path, 'callee_map.txt')
    calleef = open(callee_mapfile, 'w')
    startDate = '20180608'
    with open(itime_utime_file, 'r') as iuf, open(maped_itime_utime_file, 'w') as mapiuf:
        for line in iuf:
            caller, callee, it, ut, num = line.strip().split(',')
            if caller not in callerdict:
                callerdict[caller] = callerdict.__len__()
            maped_caller = callerdict[caller]
            if callee not in calleedict:
                calleedict[callee] = calleedict.__len__()
            maped_callee = calleedict[callee]
            maped_it = util.dateDuring(it, startDate, '360')
            maped_ut = util.dateDuring(ut, startDate, '360')

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


def gen_itime_stay_file(path):
    # gen_maped_it_ut_file(path)
    # maped_itime_utime_file = os.path.join(path, 'maped_it_ut.txt')
    maped_itime_utime_file = os.path.join(path, 'infile.txt')
    itime_stay_file = os.path.join(path, 'it_stay.txt')
    utime_mapfile = os.path.join(path, 'utime_map.txt')
    with open(maped_itime_utime_file, 'r') as mapiuf, open(itime_stay_file, 'w') as isf, open(utime_mapfile, 'w') as utmapf:
        for line in mapiuf:
            dev, app, itime, utime, num = line.strip().split(',')
            stay = int(utime) - int(itime)
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


if __name__ == '__main__':
    path = r'/Users/baby/Document/TensorAugmented/data/360data'
    gen_itime_stay_file(path)

