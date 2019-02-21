# -*- coding:utf-8 -*-
import matplotlib
# matplotlib.use('Qt5Agg)')

import matplotlib.pyplot as plt
import os
import find_topk_blocks
import numpy as np
from matplotlib import ticker
import findSusp

'draw dcube/our algorithm all file densities'
def drawDensities(list1, figpath):
    colors = ['b', 'g', 'r', 'y', 'orchid', 'c', 'k',
              'turquoise', 'grey', 'darkviolet']
    marks = ['.', 'h', 'o', 'v', '^', '<', '>', 'p', 's', '+']
    labels = ['our algotithm', 'dcube algorithm']
    plt.figure(figsize=(10, 10))
    plt.ylabel('density')
    xs = [j for j in range(list1.__len__())]
    plt.plot(xs, list1, marker=marks[0], color=colors[0])
    plt.legend()
    plt.grid()
    path = os.path.join(figpath+'.png')
    plt.savefig(path)


def drawDensityDiffers(ourout_path, realout_path, k, filenum, figpath):
    all_differs = []
    for i in range(1, filenum+1):
        differs = []
        print(str(i) + '\n')
        for j in range(1, k+1):
            this_ourout_path = os.path.join(ourout_path, str(j))
            this_ourout_file = os.path.join(this_ourout_path, 'block_'+str(i) + '.tuples')
            densities1 = find_topk_blocks.blocks_density(this_ourout_file, modes=4)

            this_realout_path = os.path.join(realout_path, str(j))
            this_realout_file = os.path.join(this_realout_path, 'block_'+str(i) + '.tuples')
            densities2 =find_topk_blocks.blocks_density(this_realout_file, modes=4)
            differ = densities2 - densities1
            print (differ)
            differs.append(differ)
        all_differs.append(differs)
    colors = ['b', 'g', 'r', 'y', 'orchid']
    marks = ['.', 'h', 'o', 'v', '^']
    xs = [i for i in range(1, k+1)]
    xs_ticks = np.arange(1, k + 1, 1)
    pernum = 3
    recurrence = int(filenum/pernum)
    for i in range(recurrence):
        plt.figure(figsize=(10, 5))
        plt.ylabel('density of (dcube - our)')
        plt.xlabel('delta T')
        plt.title('density differences')
        plt.xticks(xs_ticks)
        # plt.ylim([-10, 50])
        for j in range(pernum):
            block_idx = i * pernum + j
            differs = all_differs[block_idx]
            plt.plot(xs, differs, marker=marks[j], color=colors[j], label='block '+str(block_idx+1))
            plt.legend(loc='best')
        plt.savefig(figpath+'/'+str(i))


def drawMaxDensity(our_accum_output, k=18):
    densities = []
    for i in range(k+1):
        each_output_path = os.path.join(our_accum_output, str(i))
        firBlock_file = os.path.join(each_output_path, 'block_1.tuples')
        density = find_topk_blocks.blocks_density(firBlock_file, modes=4)
        densities.append(density)
    plt.figure(figsize=(10, 10))
    plt.ylabel('density')
    plt.title('tensor maximum density curve')
    xs = [i for i in range(k+1)]
    plt.plot(xs, densities, marker='o', color='blue')
    plt.legend()
    path = os.path.join(our_accum_output, 'maxdensity.png')
    plt.savefig(path)


def drawInjectDensity(list1, list2, list3):
    colors = ['r', 'g', 'k']
    marks = ['<', '^', 'x']
    linestyles = [':', '--', '-']
    labels = ['our algotithm', 'Dcube', 'DenseStream']
    plt.title('360data inject result')
    plt.figure(figsize=(15, 15))
    plt.ylabel('F measure')
    plt.xlabel('density')
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    xs = [0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.25, 0.3, 1]
    densities = [list1, list2, list3]
    for i in range(3):
        plt.plot(xs, densities[i], marker=marks[i], color=colors[i], label=labels[i],
                 linestyle=linestyles[i], markersize=10)
        plt.legend(loc='best')
    # plt.show()
    plt.savefig('360inject.png')


def drawDistribution(wifi_path, bin, filenum, k, figpath, label):
    binpath = os.path.join(wifi_path, 'bin=' + str(bin))
    path = os.path.join(binpath, 'our_accum_output/' + str(k))
    for j in range(1, filenum+1):
        name = 'block_'+str(j)+'.tuples'
        blockfile = os.path.join(path, name)
        callerdict = {}
        callercounts = {}
        classroom_counts = {}
        ap_mapfile = os.path.join(binpath, 'app_map.txt')
        apnamedict = findSusp.genMapfileDict(ap_mapfile)
        classroomdict = findSusp.genApClassroomDict(wifi_path)
        stcounts = {}
        etcounts = {}
        with open(blockfile, 'r') as bf:
            for line in bf:
                caller, callee, st, et = line.strip().split(',')[:4]
                if caller not in callerdict:
                    callerdict[caller] = callerdict.__len__()
                maped_caller = callerdict[caller]
                ap_mac = apnamedict[callee]
                ap_ip = findSusp.mactoIp(ap_mac)
                classroom = classroomdict[ap_ip]
                print classroom
                if classroom not in classroom_counts:
                    classroom_counts[classroom] = 1
                else:
                    classroom_counts[classroom] = classroom_counts[classroom] + 1

                if maped_caller not in callercounts:
                    callercounts[maped_caller] = 1
                else:
                    callercounts[maped_caller] = callercounts[maped_caller] + 1
                if st not in stcounts:
                    stcounts[st] = 1
                else:
                    stcounts[st] = stcounts[st] + 1
                if et not in etcounts:
                    etcounts[et] = 1
                else:
                    etcounts[et] = etcounts[et] + 1
        caller_xs = [i for i in range(callercounts.__len__())]
        caller_ys = [callercounts[i] for i in range(callercounts.__len__())]
        classroom_xs, classroom_ys = [], []
        for key in classroom_counts:
            classroom_xs.append(key)
            classroom_ys.append(classroom_counts[key])
        st_xs = []
        st_ys = []
        for key in stcounts:
            st_xs.append(int(key))
            st_ys.append(stcounts[key])
        et_xs = []
        et_ys = []
        for key in etcounts:
            et_xs.append(int(key))
            et_ys.append(etcounts[key])
        plt.figure()
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        plt.subplot(2, 2, 1)
        plt.bar(caller_xs, caller_ys, width=0.1, facecolor='lightskyblue', edgecolor='lightskyblue')
        plt.ylabel('count')
        plt.title('mobile')
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # 将坐标轴的base number设置为一位。

        plt.subplot(2, 2, 2)
        plt.bar(classroom_xs, classroom_ys, width=0.1, facecolor='lightskyblue', edgecolor='lightskyblue')
        plt.ylabel('count')
        plt.title('ap')
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # 将坐标轴的base number设置为一位。
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # 将坐标轴的base number设置为一位。

        plt.subplot(2, 2, 3)
        plt.bar(st_xs, st_ys, width=0.1, facecolor='lightskyblue', edgecolor='lightskyblue')
        plt.ylabel('count')
        plt.title('connect time')
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # 将坐标轴的base number设置为一位。

        plt.subplot(2, 2, 4)
        plt.bar(et_xs, et_ys, width=0.1, facecolor='lightskyblue', edgecolor='lightskyblue')
        plt.ylabel('count')
        plt.title('disconnect time')
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # 将坐标轴的base number设置为一位。

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=0.4, hspace=0.4)
        plt.legend()
        fname = os.path.join(figpath, label+'_'+str(j)+'.png')
        plt.savefig(fname)


def drawStaytimeDistri(wifi_path, bin, filenum, k,  figpath, label):
    binpath = os.path.join(wifi_path, 'bin=' + str(bin))
    path = os.path.join(binpath, 'our_accum_output/' + str(k))
    ap_mapfile = os.path.join(path, 'app_map.txt')
    apdict = findSusp.genMapfileDict(ap_mapfile)
    for j in range(1, filenum+1):
        name = 'block_'+str(j)+'.tuples'
        blockfile = os.path.join(path, name)
        staycounts = {}
        with open(blockfile, 'r') as bf:
            for line in bf:
                caller, callee, st, et = line.strip().split(',')[:4]
                maped_callee = apdict[callee]
                if not maped_callee == '"00 00 00 00 00 00 "':
                    stay = int(et) - int(st)
                    if stay not in staycounts:
                        staycounts[stay] = 1
                    else:
                        staycounts[stay] = staycounts[stay] + 1
        stay_xs = []
        stay_ys = []
        for key in staycounts:
            stay_xs.append(int(key))
            stay_ys.append(staycounts[key])
        print stay_xs
        print stay_ys
        plt.figure()
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-1, 1))
        plt.bar(stay_xs, stay_ys,facecolor='blue', edgecolor='blue')
        plt.ylabel('count')
        plt.title('staytime')
        plt.xlim([-1, stay_xs.__len__()])
        ax = plt.gca()
        ax.yaxis.set_major_formatter(formatter)
        plt.legend()
        fname = os.path.join(figpath, label + '_' + str(j) + '.png')
        plt.savefig(fname)


if __name__ == '__main__':
    'draw wifi density differs'
    path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    filenum, k, figpath, bin = 10, 30, 'wifi_figs', 1
    binpath = os.path.join(path, 'bin={}'.format(bin))
    drawDistribution(path, bin, filenum, k, figpath, label='wifi_bin=1_distri')
    # drawStaytimeDistri(binpath, wifi_path, filenum, figpath, label='wifi_bin=1')

    # path = '/Users/baby/Document/TensorAugmented/data/360data'
    # spikepath = os.path.join(path, 'itime_utime/stride=1,t1=1/our_accum_output/3/newfiles')
    # k, figpath = 1, 18, '360figs'
    # drawDistribution(spikepath, k, figpath, label='360 spike')









