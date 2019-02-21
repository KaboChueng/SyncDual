import os
import util
import shutil
import draw



't1: first block days'
def stride_cutfile(file, path, binpath, stride, t1):
    utime_mapfile = os.path.join(path, 'utime_map.txt')
    utmapf = open(utime_mapfile, 'r')
    ut_maplines = utmapf.readlines()
    single_file_path = os.path.join(binpath, 'single_files')
    if not os.path.exists(single_file_path):
        os.mkdir(single_file_path)
    accum_file_path = os.path.join(binpath, 'accum_files')
    if not os.path.exists(accum_file_path):
        os.mkdir(accum_file_path)
    ids, apps, it_sts, lines = util.read_it_st_file(file)
    idx1, k, isB1, accum_lines = 0, 0, False, []
    length = lines.__len__()
    start_ut = 0
    for i in range(1, length):
        utime = int(ut_maplines[i].strip().split(',')[1])
        if not isB1:
            if utime - start_ut >= t1:
                single_lines = lines[idx1: i]
                accum_lines.extend(single_lines)
                single_file = os.path.join(single_file_path, '0.txt')
                sinf = open(single_file, 'w')
                sinf.writelines(accum_lines)

                start_ut = utime
                idx1 = i
                k = k + 1
                isB1 = True
        else:
            if utime - start_ut >= stride:
                print('k: '+str(k))
                single_lines = lines[idx1: i]
                single_file = os.path.join(single_file_path, str(k)+'.txt')
                sinf = open(single_file, 'w')
                sinf.writelines(single_lines)

                accum_lines.extend(single_lines)
                start_ut = utime
                idx1 = i
                k = k + 1
    single_lines = lines[idx1: length]
    single_file = os.path.join(single_file_path, str(k) + '.txt')
    sinf = open(single_file, 'w')
    sinf.writelines(single_lines)
    accum_file = os.path.join(accum_file_path, str(k) + '.txt')
    accumf = open(accum_file, 'w')
    accum_lines.extend(single_lines)
    accumf.writelines(accum_lines)


def stride_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path,  ourout_path):
    k = os.listdir(sinfile_path).__len__()
    sinfile = os.path.join(sinfile_path, '0.txt')
    this_our_path = os.path.join(ourout_path, '0')
    if not os.path.exists(this_our_path):
        os.mkdir(this_our_path)
    'invoke dcube for sin file'
    os.system('cd dcube-master && ./run_single.sh' + ' ' +
              sinfile + ' ' + this_our_path + ' ' + '3 ari density 10')
    os.remove(sinfile)
    util.delAttri(this_our_path)
    if k == 0:
        return
    for j in range(1, k):
        sinfile = os.path.join(sinfile_path, str(j)+'.txt')
        this_sinout_path = os.path.join(sinout_path, str(j))
        if not os.path.exists(this_sinout_path):
            os.mkdir(this_sinout_path)
        'invoke dcube for sin file'
        os.system('cd dcube-master && ./run_single.sh' + ' ' +
                  sinfile + ' '+this_sinout_path+' ' + '3 ari density 10')
        util.delAttri(this_sinout_path)

        last_ourout_path = os.path.join(ourout_path, str(j-1))
        concatfile = os.path.join(concat_file_path, str(j) + '.txt')
        inpaths = [this_sinout_path, last_ourout_path]
        util.concat_paths_files(inpaths, concatfile)
        this_ourout_path = os.path.join(ourout_path, str(j))
        if not os.path.exists(this_ourout_path):
            os.mkdir(this_ourout_path)
        'invoke dcube for concatfile'
        os.system('cd dcube-master && ./run_single.sh' + ' '
                  + concatfile + ' ' + this_ourout_path + ' ' + '3 ari density 10')
        util.delAttri(this_ourout_path)

        shutil.rmtree(this_sinout_path)
        os.remove(concatfile)
    shutil.rmtree(concat_file_path)

    accumfile = os.path.join(accumfile_path, str(j)+'.txt')
    this_realout_path = os.path.join(realout_path, str(j))
    'invoke dcube for accumfile'
    os.system('cd dcube-master && ./run_single.sh' + ' '
              + accumfile + ' ' + this_realout_path + ' ' + '3 ari density 10')
    util.delAttri(this_realout_path)



def invoke_inject_wifi():
    path = '/Users/baby/Document/TensorAugmented/data/wifi'
    bins = [0.5, 1]
    for bin in bins[1:]:
        binpath = os.path.join(path, 'bin={}'.format(bin))
        file = os.path.join(binpath, 'maped_it_stay.txt')
        inject_dir = os.path.join(binpath, 'inject')
        goals = [3000, 6000, 9000, 12000, 20000, 30000]
        for goal in goals:
            print 'goal: {}'.format(goal)
            goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
            ts_perday = 24/bin
            dirpath = os.path.join(goal_dir, 'stride')
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            stride, t1 = 3, 3
            stride_t1_path = os.path.join(dirpath, 'stride={},t1={}'.format(stride, t1))
            if not os.path.exists(stride_t1_path):
                os.mkdir(stride_t1_path)
            stride_cutfile(file, goal_dir, stride_t1_path, stride*ts_perday, t1*ts_perday)

            sinfile_path = os.path.join(stride_t1_path, 'single_files')
            if not os.path.exists(sinfile_path):
                os.mkdir(sinfile_path)
            sinout_path = os.path.join(stride_t1_path, 'single_files_output')
            if not os.path.exists(sinout_path):
                os.mkdir(sinout_path)
            accumfile_path = os.path.join(stride_t1_path, 'accum_files')
            if not os.path.exists(accumfile_path):
                os.mkdir(accumfile_path)
            realout_path = os.path.join(stride_t1_path, 'real_accum_output')
            if not os.path.exists(realout_path):
                os.mkdir(realout_path)
            concat_file_path = os.path.join(stride_t1_path, 'concat_sinout_files')
            if not os.path.exists(concat_file_path):
                os.mkdir(concat_file_path)
            ourout_path = os.path.join(stride_t1_path, 'our_accum_output')
            if not os.path.exists(ourout_path):
                os.mkdir(ourout_path)
            stride_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                                     concat_file_path, ourout_path)


def invoke_wifi(bin):
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    binpath = os.path.join(path, 'bin={}'.format(bin))
    file = os.path.join(binpath, 'maped_it_stay.txt')
    ts_perday = 24/bin
    dirpath = os.path.join(binpath, 'stride')
    stride, t1 = 2, 2
    stride_t1_path = os.path.join(dirpath, 'stride={},t1={}'.format(stride, t1))
    stride_cutfile(file, binpath, stride_t1_path, stride=2*ts_perday, t1=2*ts_perday)

    sinfile_path = os.path.join(stride_t1_path, 'single_files')
    if not os.path.exists(sinfile_path):
        os.mkdir(sinfile_path)
    sinout_path = os.path.join(stride_t1_path, 'single_files_output')
    if not os.path.exists(sinout_path):
        os.mkdir(sinout_path)
    accumfile_path = os.path.join(stride_t1_path, 'accum_files')
    if not os.path.exists(accumfile_path):
        os.mkdir(accumfile_path)
    realout_path = os.path.join(stride_t1_path, 'real_accum_output')
    if not os.path.exists(realout_path):
        os.mkdir(realout_path)
    concat_file_path = os.path.join(stride_t1_path, 'concat_sinout_files')
    if not os.path.exists(concat_file_path):
        os.mkdir(concat_file_path)
    ourout_path = os.path.join(stride_t1_path, 'our_accum_output')
    if not os.path.exists(ourout_path):
        os.mkdir(ourout_path)
    stride_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path, ourout_path)


def invoke_inject_360():
    'invoke inject 360'
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    inject_dir = os.path.join(path, 'inject')
    goals = [1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 5000, 6000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
        file = os.path.join(goal_dir, 'maped_it_stay.txt')
        t1, stride = 3, 2
        dirpath = os.path.join(goal_dir, 'stride')
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        binpath = os.path.join(dirpath, 'stride={},t1={}'.format(stride, t1))
        if not os.path.exists(binpath):
            os.mkdir(binpath)
        stride_cutfile(file, goal_dir, binpath, stride, t1)

        sinfile_path = os.path.join(binpath, 'single_files')
        if not os.path.exists(sinfile_path):
            os.mkdir(sinfile_path)
        sinout_path = os.path.join(binpath, 'single_files_output')
        if not os.path.exists(sinout_path):
            os.mkdir(sinout_path)
        accumfile_path = os.path.join(binpath, 'accum_files')
        if not os.path.exists(accumfile_path):
            os.mkdir(accumfile_path)
        realout_path = os.path.join(binpath, 'real_accum_output')
        if not os.path.exists(realout_path):
            os.mkdir(realout_path)
        concat_file_path = os.path.join(binpath, 'concat_sinout_files')
        if not os.path.exists(concat_file_path):
            os.mkdir(concat_file_path)
        ourout_path = os.path.join(binpath, 'our_accum_output')
        if not os.path.exists(ourout_path):
            os.mkdir(ourout_path)
        stride_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                              concat_file_path, ourout_path)


def invoke_360(stride, t1):
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    file = os.path.join(path, 'maped_it_stay.txt')
    binpath = os.path.join(path, 'stride={},t1={}'.format(stride, t1))
    if not os.path.exists(binpath):
        os.mkdir(binpath)
    stride_cutfile(file, path, binpath, stride, t1)

    sinfile_path = os.path.join(binpath, 'single_files')
    if not os.path.exists(sinfile_path):
        os.mkdir(sinfile_path)
    sinout_path = os.path.join(binpath, 'single_files_output')
    if not os.path.exists(sinout_path):
        os.mkdir(sinout_path)
    accumfile_path = os.path.join(binpath, 'accum_files')
    if not os.path.exists(accumfile_path):
        os.mkdir(accumfile_path)
    realout_path = os.path.join(binpath, 'real_accum_output')
    if not os.path.exists(realout_path):
        os.mkdir(realout_path)
    concat_file_path = os.path.join(binpath, 'concat_sinout_files')
    if not os.path.exists(concat_file_path):
        os.mkdir(concat_file_path)
    ourout_path = os.path.join(binpath, 'our_accum_output')
    if not os.path.exists(ourout_path):
        os.mkdir(ourout_path)
    stride_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path, ourout_path)


def result_360analisis(stride, t1):
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    k = int((30 - t1)/stride)
    binpath = os.path.join(path, 'stride={},t1={}'.format(stride, t1))
    our_accum_output = os.path.join(binpath, 'our_accum_output')
    speeds = util.densitySpeedSpike(our_accum_output, k)
    figpath = '360_t1={},stride={}'.format(t1, stride)
    # draw.drawDensities(speeds, figpath)


if __name__ == '__main__':
    stride_t1_tuples = [(2, 1), (3, 1), (4, 2), (1, 1)]
    for tup in stride_t1_tuples:
        t1, stride = tup[0], tup[1]
        print 'stride={},t1={}'.format(stride, t1)
        # invoke_360(stride, t1)
        result_360analisis(stride, t1)

