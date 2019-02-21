import os
import block_concat
import util
import slideStride
import datetime
import draw


import sys
reload(sys)
sys.setdefaultencoding('utf8')


'multiple: window/stride'
def slidewindow_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path,  ourout_path, multiple):
    k = os.listdir(sinfile_path).__len__()
    for j in range(k):
        if j == multiple - 1:
            filenames = [str(i)+'.txt' for i in range(0, j+1)]
            outname = '{}~{}.txt'.format(0, j)
            util.concat_same_path_files(sinfile_path, filenames, outname)
            windowfile = os.path.join(sinfile_path, outname)
            this_ourout_path = os.path.join(ourout_path, 'win0')
            if not os.path.exists(this_ourout_path):
                os.mkdir(this_ourout_path)
            'invoke dcube for sin file'
            os.system('cd dcube-master && ./run_single.sh' + ' ' +
                      windowfile + ' '+this_ourout_path+' ' + '3 ari density 10')
            util.delAttri(this_ourout_path)

            this_realout_path = os.path.join(realout_path, 'win0')
            'invoke dcube for accumfile'
            os.system('cd dcube-master && ./run_single.sh' + ' '
                      + windowfile + ' ' + this_realout_path + ' ' + '3 ari density 10')
            util.delAttri(this_realout_path)

        if j >= multiple:
            sinfile = os.path.join(sinfile_path, str(j) + '.txt')
            this_sinout_path = os.path.join(sinout_path, str(j))
            if not os.path.exists(this_sinout_path):
                os.mkdir(this_sinout_path)
            os.system('cd dcube-master && ./run_single.sh' + ' ' +
                      sinfile + ' ' + this_sinout_path + ' ' + '3 ari density 10')
            util.delAttri(this_sinout_path)

            'last window outfile'
            last_ourout_path = os.path.join(ourout_path, 'win{}'.format(j-multiple))
            'concat data of next stride'
            concatfile = os.path.join(concat_file_path, str(j) + '.txt')
            block_concat.concat_block_tuples(this_sinout_path, last_ourout_path, concatfile, 10)
            'del content in sliding_out stride'
            out_stridefile = os.path.join(sinfile_path, '{}.txt'.format(j-multiple))
            delContentInFile(concatfile, out_stridefile)

            'compute this window block'
            this_ourout_path = os.path.join(ourout_path, 'win{}'.format(j-multiple+1))
            if not os.path.exists(this_ourout_path):
                os.mkdir(this_ourout_path)
            'invoke dcube for concatfile'
            os.system('cd dcube-master && ./run_single.sh' + ' '
                      + concatfile + ' ' + this_ourout_path + ' ' + '3 ari density 10')
            util.delAttri(this_ourout_path)

            accumfile = os.path.join(accumfile_path, '{}.txt'.format(j))
            this_realout_path = os.path.join(realout_path, 'win{}'.format(j-multiple+1))
            'invoke dcube for accumfile'
            os.system('cd dcube-master && ./run_single.sh' + ' '
                      + accumfile + ' ' + this_realout_path + ' ' + '3 ari density 10')
            util.delAttri(this_realout_path)


def delContentInFile(blockfile, sinfile):
    it_sts = util.read_it_st_file(sinfile)[2]
    lines = []
    with open(blockfile, 'r') as bf:
        for line in bf:
            it_st = line.strip().split(',')[2]
            if it_st not in it_sts:
                lines.append(line)
    bf.close()
    bfw = open(blockfile, 'w')
    bfw.writelines(lines)
    bfw.close()


def invoke_inject_wifi():
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    bins = [0.5, 1]
    for bin in bins[1:]:
        binpath = os.path.join(path, 'bin={}'.format(bin))
        file = os.path.join(binpath, 'maped_it_st.txt')
        ts_perday = 24/bin
        stride, window = 2, 2
        stride_win_path = os.path.join(binpath, 'stride={},win={}'.format(stride, window))
        if not os.path.exists(stride_win_path):
            os.mkdir(stride_win_path)
        slideStride.stride_cutfile(file, binpath, stride_win_path, stride=2 * ts_perday, t1=2 * ts_perday)

        sinfile_path = os.path.join(stride_win_path, 'single_files')
        if not os.path.exists(sinfile_path):
            os.mkdir(sinfile_path)
        sinout_path = os.path.join(stride_win_path, 'single_files_output')
        if not os.path.exists(sinout_path):
            os.mkdir(sinout_path)
        accumfile_path = os.path.join(stride_win_path, 'accum_files')
        if not os.path.exists(accumfile_path):
            os.mkdir(accumfile_path)
        realout_path = os.path.join(stride_win_path, 'real_accum_output')
        if not os.path.exists(realout_path):
            os.mkdir(realout_path)
        concat_file_path = os.path.join(stride_win_path, 'concat_sinout_files')
        if not os.path.exists(concat_file_path):
            os.mkdir(concat_file_path)
        ourout_path = os.path.join(stride_win_path, 'our_accum_output')
        if not os.path.exists(ourout_path):
            os.mkdir(ourout_path)
        slidewindow_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                                 concat_file_path, ourout_path, multiple=window / stride)


def invoke_wifi(bin):
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    binpath = os.path.join(path, 'bin={}'.format(bin))
    file = os.path.join(binpath, 'maped_it_st.txt')
    ts_perday = 24/bin
    stride, window = 1, 3
    stride_win_path = os.path.join(binpath, 'stride={},win={}'.format(stride, window))
    if not os.path.exists(stride_win_path):
        os.mkdir(stride_win_path)
    slideStride.stride_cutfile(file, binpath, stride_win_path, stride=2*ts_perday, t1=2*ts_perday)

    sinfile_path = os.path.join(stride_win_path, 'single_files')
    if not os.path.exists(sinfile_path):
        os.mkdir(sinfile_path)
    sinout_path = os.path.join(stride_win_path, 'single_files_output')
    if not os.path.exists(sinout_path):
        os.mkdir(sinout_path)
    accumfile_path = os.path.join(stride_win_path, 'accum_files')
    if not os.path.exists(accumfile_path):
        os.mkdir(accumfile_path)
    realout_path = os.path.join(stride_win_path, 'real_accum_output')
    if not os.path.exists(realout_path):
        os.mkdir(realout_path)
    concat_file_path = os.path.join(stride_win_path, 'concat_sinout_files')
    if not os.path.exists(concat_file_path):
        os.mkdir(concat_file_path)
    ourout_path = os.path.join(stride_win_path, 'our_accum_output')
    if not os.path.exists(ourout_path):
        os.mkdir(ourout_path)
    window, stride = 6, 2
    slidewindow_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path, ourout_path, multiple=window/stride)


def invoke_inject_360():
    'invoke inject 360'
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    inject_dir = os.path.join(path, 'inject')
    goals = [1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 5000, 6000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
        infile = os.path.join(goal_dir, 'maped_it_stay.txt')
        if not os.path.exists(goal_dir):
            os.mkdir(goal_dir)
        dirpath = os.path.join(goal_dir, 'window')
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        stride, window = 2, 6
        stride_win_path = os.path.join(dirpath, 'stride={},win={}'.format(stride, window))
        if not os.path.exists(stride_win_path):
            os.mkdir(stride_win_path)
        slideStride.stride_cutfile(infile, goal_dir, stride_win_path, stride, stride)

        sinfile_path = os.path.join(stride_win_path, 'single_files')
        if not os.path.exists(sinfile_path):
            os.mkdir(sinfile_path)
        sinout_path = os.path.join(stride_win_path, 'single_files_output')
        if not os.path.exists(sinout_path):
            os.mkdir(sinout_path)
        accumfile_path = os.path.join(stride_win_path, 'accum_files')
        if not os.path.exists(accumfile_path):
            os.mkdir(accumfile_path)
        realout_path = os.path.join(stride_win_path, 'real_accum_output')
        if not os.path.exists(realout_path):
            os.mkdir(realout_path)
        concat_file_path = os.path.join(stride_win_path, 'concat_sinout_files')
        if not os.path.exists(concat_file_path):
            os.mkdir(concat_file_path)
        ourout_path = os.path.join(stride_win_path, 'our_accum_output')
        if not os.path.exists(ourout_path):
            os.mkdir(ourout_path)
        slidewindow_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                              concat_file_path, ourout_path, multiple=window/stride)


def invoke_360(window, stride):
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    file = os.path.join(path, 'maped_it_stay.txt')
    binpath = os.path.join(path, 'stride={},win={}'.format(stride, window))
    if not os.path.exists(binpath):
        os.mkdir(binpath)
    slideStride.stride_cutfile(file, path, binpath, stride, stride)

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
    slidewindow_invoke_dcube(sinfile_path, sinout_path, accumfile_path, realout_path,
                             concat_file_path, ourout_path, multiple=window/stride)


def result_360analisis(window, stride):
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    k = int((30 - window)/stride)
    binpath = os.path.join(path, 'stride={},win={}'.format(stride, window))
    our_accum_output = os.path.join(binpath, 'our_accum_output')
    densities = util.densitySpike(our_accum_output, k)
    figpath = '360_win={},stride={}'.format(window,stride)
    # draw.drawDensities(densities, figpath)


if __name__ == '__main__':
    win_stride_tuples = [(1, 1), (2, 1), (3, 1),(6, 2), (4, 1), (4, 2)]
    for tup in win_stride_tuples:
        window, stride = tup[0], tup[1]
        print 'stride={},win={}'.format(stride, window)
        # invoke_360(window, stride)
        result_360analisis(window, stride)


