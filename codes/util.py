import os
import numpy as np
import find_topk_blocks


def dateDuring(date1, date2, label):
    if label == '360':
        month1 = int(date1[4:6])
        day1 = int(date1[6:8])
        month2 = int(date2[4:6])
        day2 = int(date2[6:8])
        during = (month1 - month2)*30 + day1 - day2
    else:
        during = int(date1) - int(date2)
    return during


def addDate(date, days):
    year = date[:4]
    month = date[4: 6]
    day = date[6: 8]
    daynum = int(day)+days
    if daynum > 30:
        month2 = str(int(month)+1)
        if month2.__len__() == 1:
            month2 = '0' + month2
        day2 = str(daynum - 30)
        if day2.__len__() == 1:
            day2 = '0'+day2
        date2 = year + month2 + day2
    else:
        date2 = year + month + str(daynum)
    return date2


'file: (caller, callee, it_st)'
def read_it_st_file(file):
    callers = []
    callees = []
    it_sts = []
    lines = []
    with open(file, 'r') as f:
        for line in f:
            words = line.strip().split(',')
            callers.append(words[0])
            callees.append(words[1])
            it_sts.append(words[2])
            lines.append(line)
    f.close()
    print set(callers).__len__(), set(callees).__len__(), lines.__len__()
    return callers, callees, it_sts, lines


'file: (caller, callee, it_st)'
def read_it_ut_file(file):
    callers = []
    callees = []
    itimes = []
    utimes = []
    lines = []
    with open(file, 'r') as f:
        for line in f:
            words = line.strip().split(',')
            callers.append(words[0])
            callees.append(words[1])
            itimes.append(words[2])
            utimes.append(words[3])
            lines.append(line)
    f.close()
    # print set(callers).__len__(), set(callees).__len__(), lines.__len__()
    return callers, callees, itimes, utimes, lines


def delAttri(path):
    for name in os.listdir(path):
        if name.endswith(".attributes"):
            os.remove(os.path.join(path, name))


def concatfiles(infiles, outfile):
    newlines = []
    for infile in infiles:
        with open(infile, 'rb') as inf:
            for line in inf:
                newlines.append(line)
    f_out = open(outfile, 'wb')
    f_out.writelines(newlines)
    f_out.close()


def concat_paths_files(inpaths, outfile):
    lines = []
    for path in inpaths:
        filenames = os.listdir(path)
        for name in filenames:
            file = os.path.join(path, name)
            f = open(file, 'r')
            lines.extend(f.readlines())
    outf = open(outfile, 'w')
    lineset = set(lines)
    outf.writelines(list(lineset))
    outf.close()


def concat_same_path_files(path, filenames, outname):
    lines = []
    for name in filenames:
        file = os.path.join(path, name)
        f = open(file, 'r')
        lines.extend(f.readlines())
    outfile = os.path.join(path, outname)
    outf = open(outfile, 'w')
    lineset = set(lines)
    outf.writelines(list(lineset))
    outf.close()


def gen_maped_it_st_file(path, infile, outfile):
    it_st_dict = {}
    it_st_mapfile = os.path.join(path, 'it_st_map.txt')
    it_stf = open(it_st_mapfile, 'w')
    with open(infile, 'r') as inf, open(outfile, 'w') as outf:
        for line in inf:
            caller, callee, it_st, num = line.strip().split(',')
            if it_st not in it_st_dict:
                it_st_dict[it_st] = it_st_dict.__len__()
            maped_it_st = it_st_dict[it_st]
            it_stf.write(','.join((it_st, str(maped_it_st))))
            it_stf.write('\n')
            outf.write(','.join((str(caller), str(callee), str(maped_it_st), num)))
            outf.write('\n')
    inf.close()
    outf.close()
    it_stf.close()


def genMapfileDict(mapfile):
    valdict = {}
    with open(mapfile, 'r') as mapf:
        for line in mapf:
            val, mapval = line.strip().split(',')
            valdict[mapval] = val
    return valdict


def genReversefiledict(mapfile):
    valdict = {}
    with open(mapfile, 'r') as mapf:
        for line in mapf:
            val, mapval = line.strip().split(',')
            valdict[val] = mapval
    return valdict


'for stride'
def densitySpeedSpike(our_accum_outputs, k):
    speeds = []
    our_accum_output = os.path.join(our_accum_outputs, str(1))
    blockfile = os.path.join(our_accum_output, 'block_1.tuples')
    last_density = find_topk_blocks.blocks_density(blockfile, modes=3)
    for i in range(2, k+1):
        our_accum_output = os.path.join(our_accum_outputs, str(i))
        blockfile = os.path.join(our_accum_output, 'block_1.tuples')
        density = find_topk_blocks.blocks_density(blockfile, modes=3)
        speed = density - last_density
        last_density = density
        speeds.append(speed)
    thres = np.mean(speeds) + 2 * np.std(speeds)
    spikes = [idx+2 for idx, x in enumerate(speeds) if x >= thres]
    print speeds
    print thres
    print spikes
    return speeds


'for sliding window'
def densitySpike(our_accum_outputs, k):
    densities = []
    for i in range(1, k+1):
        our_accum_output = os.path.join(our_accum_outputs, 'win{}'.format(i))
        blockfile = os.path.join(our_accum_output, 'block_1.tuples')
        density = find_topk_blocks.blocks_density(blockfile, modes=3)
        densities.append(density)
    print densities
    thres = np.mean(densities) + 3*np.std(densities)
    print thres
    spikes = [i for i in range(1, k+1) if densities[i-1] >= thres]
    print spikes
    return densities