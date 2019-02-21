# -*- coding: utf-8 -*-
import os
import gzip
import datetime


def white_app(appfile):
    f = open(appfile, 'r')
    apps = []
    for line in f.readlines():
        app = line.split(' ')[0]
        apps.append(app)
    return apps


# 过滤白名单app
def filter_white_app(file1, file2, frame_app_list):
    f2 = open(file2, 'w')
    with open(file1, 'r') as f1:
        for line in f1:
            app = line.split("\t")[1]
            if app not in frame_app_list:
                f2.write(line)
    f1.close()
    f2.close()


# 过滤版本升级的行为,观察挨着的two lines
def filter_version_upgrade(initfile, filterUp_file):
    f2 = gzip.open(filterUp_file, 'w')
    with gzip.open(initfile, 'r') as f1:
        line1 = f1.readline()
        for line2 in f1:
            words1 = line1.split('\t')
            id1 = words1[0]
            app1 = words1[1]
            version1 = int(words1[2])
            action1 = int(words1[3])
            date1 = words1[4]
            words2 = line2.split('\t')
            id2 = words2[0]
            app2 = words2[1]
            version2 = int(words2[2])
            action2 = int(words2[3])
            date2 = words2[4]
            if (id1 == id2 and app1 == app2 and version1 < version2 and
                   action1 == 2 and action2 == 1 and date1 == date2):
                'skip next line'
                line1 = f1.next()
            else:
                f2.write(line1)
                line1 = line2
    f1.close()
    f2.close()


# 'gen app/dev mapfile'
# def generate_id_app_mapfile(tensor, idfile):
#     'tensor: m2,app,action, version, ts'
#     id_dict = {}
#     with open(tensor, 'r') as f1, open(idfile, 'w') as f2:
#         for line in f1:
#             cols = line.strip().split('\t')
#             id = cols[0]
#             if id not in id_dict:
#                 id_dict[id] = id_dict.__len__()
#             maped_id = id_dict[id]
#             f2.write(','.join((id, str(maped_id))))
#             f2.write('\n')
#     f1.close()
#     f2.close()


'clear data of one date'
def cleardata(inputpath, inname, outname):
    infile = os.path.join(inputpath, inname)
    outfile = os.path.join(inputpath, outname)
    f_out = gzip.open(outfile, 'wb')
    lines = []
    with gzip.open(infile, 'rb') as f_in:
        for line in f_in:
            words1 = line.strip().split('\t')
            date1 = words1[4]
            if date1 == '20180614':
                continue
            else:
                lines.append(line)
    f_out.writelines(lines)
    f_in.close()
    f_out.close()


'concat gz'
def concatGz(path, infiles, outfile):
    lines = []
    for infile in infiles:
        ingz = os.path.join(path, infile)
        with gzip.open(ingz, 'rb') as f1:
            for line in f1:
                lines.append(line)
    outgz = os.path.join(path, outfile)
    f_out = gzip.open(outgz, 'wb')
    f_out.writelines(lines)
    f_out.close()


if __name__ == "__main__":
    path = r'/Users/baby/Document/TensorAugmented/data/360data'
    initfile = os.path.join(path, 'ins_20180701_20180707.gz')
    filter_path = os.path.join(path, 'filterUp')
    filterUp_file = os.path.join(filter_path, '20180701_20180707_filterUp.gz')
    filter_version_upgrade(initfile, filterUp_file)

    # filterUp1 = os.path.join(path, '20180608_20180614_filterUp.gz')
    # filterUp2 = os.path.join(path, '20180615_20180622_filterUp.gz')
    # outfile = os.path.join(path, '20180608_20180622_filterUp.gz')
    # genFirstLargeBlock(filterUp1, filterUp2, outfile)






