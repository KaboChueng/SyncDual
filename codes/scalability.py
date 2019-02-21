import os
import readTensor
import datetime
import slideWindow


def verify_360Scala(dirpath, suffix, stride):
    file = os.path.join(dirpath, suffix)
    rows, cols, nums, tss, lines = readTensor.read_itime_utime_file(file)
    maxts = max(tss)
    print maxts
    intervals = [i for i in range(stride, maxts, stride*2)]
    print intervals
    tempfile = os.path.join(dirpath, 'temp')
    for interval in intervals[2:]:
        start = datetime.datetime.now()
        print 'interval:{}'.format(interval)
        for i in range(tss.__len__()):
            nowts = int(tss[i])
            if nowts == interval:
                print 'edges: {}'.format(i)
                tempf = open(tempfile, 'w')
                tempf.writelines(lines[:i])
                tempf.close()
                slideWindow.invoke_360(tempfile)
                end = datetime.datetime.now()
                print 'running time: {}'.format(end - start)
                break


if __name__ == '__main__':
    path = '/Users/baby/Document/TensorAugmented/data/360data'
    dirpath = os.path.join(path, 'itime_utime')
    suffix = 'maped_20180608_20180707_itime_utime.txt'
    verify_360Scala(dirpath, suffix, stride=2)

