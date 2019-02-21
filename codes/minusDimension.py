import os
import find_topk_blocks
import draw
import numpy as np
import findSusp


def minusDimension(path, k, filenum):
    outputpath = os.path.join(path, 'our_accum_output')
    devset, appset, itimeset, utimeset = set(), set(), set(), set()
    maxdensities = []

    outputdir = os.path.join(outputpath, str(0))
    densities = find_topk_blocks.topk_densities(outputdir, modes=4)
    print 'tensor:{}, max densitiy:{}'.format(0, densities[0])
    maxdensities.append(densities[0])

    for idx in range(1, k+1):
        devset, appset, itimeset, utimeset = computeDimension(outputpath, idx-1, filenum, devset, appset, itimeset, utimeset)
        outputdir = os.path.join(outputpath, str(idx))
        newpath = os.path.join(outputdir, 'newfiles')
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        for j in range(1, filenum + 1):
            blockfile = os.path.join(outputdir, 'block_' + str(j) + '.tuples')
            newfile = os.path.join(newpath, 'new_'+str(j)+'.tuples')
            with open(blockfile, 'r') as blockf, open(newfile, 'w') as newf:
                for line in blockf:
                    dev, app, itime, utime = line.strip().split(',')[:4]
                    if utime not in utimeset:
                        newf.write(line)
            newf.close()
        densities = find_topk_blocks.topk_densities(newpath, modes=4)
        print 'tensor:{}, max densitiy:{}'.format(idx, densities[0])
        maxdensities.append(densities[0])
    m, s = np.mean(maxdensities), np.std(maxdensities)
    print 'mean:{}, std:{}, thres:{}'.format(m, s, m+2*s)
    draw.drawDensities(maxdensities, k)


def computeDimension(path, tensoridx, filenum, devset, appset, itimeset, utimeset):
    outputpath = os.path.join(path, str(tensoridx))
    for j in range(1, filenum + 1):
        blockfile = os.path.join(outputpath, 'block_' + str(j) + '.tuples')
        with open(blockfile, 'r') as blockf:
            for line in blockf:
                dev, app, itime, utime = line.strip().split(',')[:4]
                devset.add(dev)
                appset.add(app)
                itimeset.add(itime)
                utimeset.add(utime)
    return devset, appset, itimeset, utimeset


def test(dirpath, k):
    outputpath = os.path.join(dirpath, 'single_files_output')
    maxs = []
    for idx in range(1, k + 1):
        outputdir = os.path.join(outputpath, str(idx))
        densities = find_topk_blocks.topk_densities(outputdir, modes=4)
        maxs.append(densities[0])
        print 'tensor:{}, max densitiy:{}'.format(idx, densities[0])
    m, s = np.mean(maxs), np.std(maxs)
    print 'mean:{}, std:{}, thres:{}'.format(m, s, m + 2*s)


'find susp block according to density thres'
def genSusp(itime_utime_dir, binpath, tensor_idx):
    our_accum_output = os.path.join(binpath, 'our_accum_output')
    susp_output = os.path.join(our_accum_output, str(tensor_idx))
    newfile_path = os.path.join(susp_output, 'newfiles')
    blockfile = os.path.join(newfile_path, 'new_1.tuples')
    devset, appset = genSet(blockfile)
    dev_mapfile = os.path.join(itime_utime_dir, 'dev_map.txt')
    devdict = findSusp.genMapfileDict(dev_mapfile)
    app_mapfile = os.path.join(itime_utime_dir, 'app_map.txt')
    appdict = findSusp.genMapfileDict(app_mapfile)
    susp_devfile = os.path.join(our_accum_output, 'susp_dev.txt')
    susp_appfile = os.path.join(our_accum_output, 'susp_app.txt')
    with open(susp_devfile, 'w') as devf, open(susp_appfile, 'w') as appf:
        for dev in devset:
            devf.write(devdict[dev]+'\n')
        for app in appset:
            appf.write(appdict[app] + '\n')
    devf.close()
    appf.close()


def genSet(file):
    devset = set()
    appset = set()
    with open(file, 'r') as f:
        for line in f:
            dev, app = line.strip().split(',')[:2]
            if dev not in devset:
                devset.add(dev)
            if app not in appset:
                appset.add(app)
    return devset, appset


if __name__ == '__main__':
    path = r'/Users/baby/Document/TensorAugmented/data/360data'
    dirpath = os.path.join(path, 'itime_utime')
    stride, t1 = 1, 1
    binpath = os.path.join(dirpath, 'stride={},t1={}'.format(stride, t1))
    k, filenum = 29, 10
    # minusDimension(binpath, k, filenum)

    genSusp(dirpath, binpath, tensor_idx=3)




