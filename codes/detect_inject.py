import slideStride
import slideWindow
import os


def verifyInject(goal_dir, output_dir, k, filenum):
    output_path = os.path.join(output_dir, str(k))
    trueA_file = os.path.join(goal_dir, 'trueA.txt')
    trueset = set()
    with open(trueA_file, 'r') as f:
        for line in f:
            trueset.add(line.strip())
    devs = set()
    for i in range(1, filenum+1):
        blockfile = os.path.join(output_path, 'block_'+str(i)+'.tuples')
        with open(blockfile, 'r') as bf:
            for line in bf:
                dev = line.strip().split(',')[0]
                devs.add(dev)
        fscore = calFscore(devs, trueset)
        print 'until file: {}, F1: {}'.format(i, fscore)


def verifyAlert(goal_dir):
    trueA_file = os.path.join(goal_dir, 'trueA.txt')
    trueset = set()
    with open(trueA_file, 'r') as f:
        for line in f:
            trueset.add(line.strip())
    devfile = os.path.join(goal_dir, 'dev.txt')
    devf = open(devfile, 'r')
    predset = set(devf.readline().strip().split(' '))
    fscore = calFscore(predset, trueset)
    print 'F1: {}'.format(fscore)


def calFscore(predset, trueset):
    correct = 0
    for p in predset:
        if p in trueset: correct += 1
    pre = 0 if len(predset) == 0 else float(correct) / len(predset)
    rec = 0 if len(trueset) == 0 else float(correct) / len(trueset)
    print 'pre: {}, rec: {}'.format(pre, rec)
    if pre + rec > 0:
        F = 2 * pre * rec / (pre + rec)
    else:
        F = 0
    return F


def verify360():
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    inject_dir = os.path.join(path, 'inject')
    goals = [1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 5000, 6000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))

        dirpath = os.path.join(goal_dir, 'stride')
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        stride, t1 = 2, 3
        binpath = os.path.join(dirpath, 'stride={},t1={}'.format(stride, t1))
        if not os.path.exists(binpath):
            os.mkdir(binpath)
        print 'our result'
        output_dir = os.path.join(binpath, 'our_accum_output')
        verifyInject(goal_dir, output_dir, k=14, filenum=1)
        print 'real result'
        output_dir = os.path.join(binpath, 'real_accum_output')
        verifyInject(goal_dir, output_dir, k=14, filenum=1)
        # verifyAlert(binpath)
        print ' '


def verify_wifi():
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    bins = [0.5, 1]
    for bin in bins:
        binpath = os.path.join(path, 'bin={}'.format(bin))
        print 'our result'
        output_dir = os.path.join(binpath, 'our_accum_output')
        verifyInject(binpath, output_dir, k=14, filenum=1)
        print 'real result'
        output_dir = os.path.join(binpath, 'real_accum_output')
        verifyInject(binpath, output_dir, k=14, filenum=1)
        verifyAlert(binpath)
        print ' '


def detect_360():
    slideStride.invoke_inject_360()
    verify360()


def detect_wifi():
    slideWindow.invoke_inject_wifi()
    slideStride.invoke_inject_wifi()
    verify_wifi()


if __name__ == '__main__':
    detect_360()