import os
import util
import numpy as np
from scipy.sparse import csr_matrix
import random
import process360
import processWifi


def inject_360CliqueCamo(it_ut_file, infile, acnt, bcnt, goal, popbd):
    'fetch user item from whole data'
    ids, apps, itimes, utimes, lines = util.read_it_ut_file(it_ut_file)
    tups = []
    for i in range(lines.__len__()):
        tup = (int(ids[i]), int(apps[i]), int(itimes[i]), int(utimes[i]))
        tups.append(tup)
    nums = [1 for i in range(ids.__len__())]
    M = csr_matrix((nums, (ids, apps)))
    M2 = M.tolil()
    (m, n) = M2.shape
    colSum = M2.sum(0).getA1()
    targetcands = np.argwhere(colSum < popbd).flatten()
    print targetcands.__len__()
    targets = random.sample(list(targetcands), bcnt)
    fraudcands = np.arange(m, dtype=int)  # users can be hacked
    fraudsters = random.sample(list(fraudcands), acnt)

    option_itimes = [10, 11, 12]
    option_stays = [7, 8, 9]
    for j in targets:
        itime = random.choice(option_itimes)
        stay = random.choice(option_stays)
        utime = itime + stay
        num = int(goal/fraudsters.__len__())
        # print 'install date:{}, uninstall date:{}'.format(str(itime), str(utime))
        if num >= 1:
            for i in range(num):
                exeusers = random.sample(fraudsters, fraudsters.__len__())
                for i in exeusers:
                    intup = (i, j, itime, utime)
                    tups.append(intup)
        exeusers = random.sample(fraudsters, goal - num*fraudsters.__len__())
        for i in exeusers:
            intup = (i, j, itime, utime)
            tups.append(intup)
    sorted_tups = sorted(tups, key=lambda x: x[3])
    with open(infile, 'w') as inf:
        for tup in sorted_tups:
            inf.write(','.join((str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]), '1')))
            inf.write('\n')
    inf.close()
    return fraudsters, targets


def inject_wifiCliqueCamo(it_ut_file, infile, acnt, bcnt, goal, popbd, bin):
    'fetch user item from whole data'
    ids, apps, its, uts, lines = util.read_it_ut_file(it_ut_file)
    tups = []
    for i in range(lines.__len__()):
        tup = (int(ids[i]), int(apps[i]), int(its[i]), int(uts[i]))
        tups.append(tup)
    nums = [1 for i in range(ids.__len__())]
    M = csr_matrix((nums, (ids, apps)))
    M2 = M.tolil()
    (m, n) = M2.shape
    colSum = M2.sum(0).getA1()
    targetcands = np.argwhere(colSum < popbd).flatten()
    print targetcands.__len__()
    targets = random.sample(list(targetcands), bcnt)
    fraudcands = np.arange(m, dtype=int)  # users can be hacked
    fraudsters = random.sample(list(fraudcands), acnt)
    per = 24/bin
    option_itimes = range(20*per, 22*per+1)
    option_stays = range(7*per, 9*per+1)
    for j in targets:
        itime = random.choice(option_itimes)
        stay = random.choice(option_stays)
        utime = itime + stay
        num = int(goal / fraudsters.__len__())
        for i in range(num):
            exeusers = random.sample(fraudsters, fraudsters.__len__())
            for i in exeusers:
                intup = (i, j, itime, utime)
                tups.append(intup)
        exeusers = random.sample(fraudsters, goal - num * fraudsters.__len__())
        for i in exeusers:
            intup = (i, j, itime, utime)
            tups.append(intup)
    sorted_tups = sorted(tups, key=lambda x: x[3])
    with open(infile, 'w') as inf:
        for tup in sorted_tups:
            inf.write(','.join((str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]), '1')))
            inf.write('\n')
    inf.close()
    return fraudsters, targets


def write_trueset_tofile(path, fraudsters, targets):
    lines = []
    for fraudster in fraudsters:
        line = str(fraudster)+'\n'
        lines.append(line)
    'trueA: users'
    trueA_file = os.path.join(path, 'trueA.txt')
    f1 = open(trueA_file, 'w')
    f1.writelines(lines)
    f1.close()

    lines = []
    for target in targets:
        line = str(target) + '\n'
        lines.append(line)
    trueB_file = os.path.join(path, 'trueB.txt')
    f2 = open(trueB_file, 'w')
    f2.writelines(lines)
    f2.close()


def inject360():
    'inject 360'
    path = r'/Users/baby/Document/TensorAugmented/data/360data'
    it_ut_file = os.path.join(path, 'maped_it_ut.txt')
    inject_dir = os.path.join(path, 'inject')
    acnt, bcnt, popbd = 10000, 1000, 100
    goals = [1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 5000, 6000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal='+str(goal))
        if not os.path.exists(goal_dir):
            os.mkdir(goal_dir)
        infile = os.path.join(goal_dir, 'infile.txt')
        fraudsters, targets = inject_360CliqueCamo(it_ut_file, infile, acnt, bcnt, goal, popbd)
        write_trueset_tofile(goal_dir, fraudsters, targets)
        process360.gen_itime_stay_file(goal_dir)


def inject_wifi():
    path = r'/Users/baby/Document/TensorAugmented/data/wifi'
    bin = 1
    dirpath = os.path.join(path, 'bin={}'.format(bin))
    it_ut_file = os.path.join(dirpath, 'maped_it_ut.txt')
    inject_dir = os.path.join(dirpath, 'inject')
    if not os.path.exists(inject_dir):
        os.mkdir(inject_dir)
    acnt, bcnt, popbd = 30000, 100, 1000
    goals = [3000, 6000, 9000, 12000, 20000, 30000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal='+str(goal))
        if not os.path.exists(goal_dir):
            os.mkdir(goal_dir)
        infile = os.path.join(goal_dir, 'infile.txt')
        fraudsters, targets = inject_wifiCliqueCamo(it_ut_file, infile, acnt, bcnt, goal, popbd, bin)
        write_trueset_tofile(goal_dir, fraudsters, targets)
        process360.gen_itime_stay_file(goal_dir)
        # print 'our result'
        # output_dir = os.path.join(goal_dir, 'our_accum_output')
        # verifyInject(goal_dir, output_dir, k=9, filenum=1)
        # print 'real result'
        # output_dir = os.path.join(goal_dir, 'real_accum_output')
        # verifyInject(goal_dir, output_dir, k=9, filenum=1)
        # verifyAlert(goal_dir)
        # print ' '


if __name__ == '__main__':
    # inject360()
    inject_wifi()


