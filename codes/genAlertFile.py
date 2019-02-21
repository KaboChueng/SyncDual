import os
import util


def gen_densealert_file(tensor, alertfile):
    with open(tensor, 'rb') as te, open(alertfile, 'wb') as alertf:
        for line in te:
            cols = line.strip().split(',')
            id = cols[0]
            app = cols[1]
            itime = cols[2]
            utime = cols[3]
            alertf.write(','.join((id, app, itime, utime, '1', '-')))
            alertf.write('\n')
    te.close()
    alertf.close()


def genTensor(path):
    it_st_mapfile = os.path.join(path, 'it_st_map.txt')
    it_st_dict = util.genMapfileDict(it_st_mapfile)
    utime_mapfile = os.path.join(path, 'utime_map.txt')
    utime_dict = util.genReversefiledict(utime_mapfile)
    maped_it_stay_file = os.path.join(path, 'maped_it_stay.txt')
    tensor = os.path.join(path, 'tensor')
    with open(maped_it_stay_file, 'r') as mapitf, open(tensor, 'w') as te:
        for line in mapitf:
            caller, callee, it_st, num = line.strip().split(',')
            utime = utime_dict[it_st_dict[it_st]]
            te.write(','.join((caller, callee, it_st, num, utime, '-')))
            te.write('\n')
    te.close()


def gen_inject360_alertfile():
    path = r'/Users/baby/Document/TensorAugmented/data/360data'
    inject_dir = os.path.join(path, 'inject')
    goals = [1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 5000]
    for goal in goals:
        print 'goal: {}'.format(goal)
        goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
        genTensor(goal_dir)


def gen_injectwifi_alertfile():
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'

    bins = [0.5, 1]
    for bin in bins[1:]:
        binpath = os.path.join(path, 'bin={}'.format(bin))
        inject_dir = os.path.join(binpath, 'inject')
        goals = [3000, 6000, 9000, 12000, 20000, 30000]
        for goal in goals:
            print 'goal: {}'.format(goal)
            goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
            genTensor(goal_dir)


if __name__ == '__main__':
    gen_inject360_alertfile()


