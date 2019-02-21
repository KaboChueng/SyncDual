import os


def sin_block_overlap(block_tuple_file1, block_tuple_file2):
    f1 = open(block_tuple_file1, 'r')
    f2 = open(block_tuple_file2, 'r')
    id1 = set()
    id2 = set()
    app1 = set()
    app2 = set()
    inst_st1 = set()
    inst_st2 = set()
    tups1 = set()
    tups2 = set()
    for line in f1.readlines():
        cols = line.strip().split(',')
        id = cols[0]
        id1.add(id)
        app = cols[1]
        app1.add(app)
        inst_st = cols[2]
        inst_st1.add(inst_st)
        tup = (id, app, inst_st)
        tups1.add(tup)
    for line in f2.readlines():
        cols = line.strip().split(',')
        id = cols[0]
        id2.add(id)
        app = cols[1]
        app2.add(app)
        inst_st = cols[2]
        inst_st2.add(inst_st)
        tup = (id, app, inst_st)
        tups2.add(tup)
    id_overlap = id1.intersection(id2).__len__()
    print (str(id1.__len__()) + ' ' + str(id2.__len__()) + ' id overlap: ' + str(id_overlap))
    app_overlap = app1.intersection(app2).__len__()
    print (str(app1.__len__()) + ' ' + str(app2.__len__()) + ' app overlap: ' + str(app_overlap))
    inst_st_overlap = inst_st1.intersection(inst_st2).__len__()
    print (str(inst_st1.__len__()) + ' ' + str(inst_st2.__len__()) + ' inst_st overlap: ' + str(
        inst_st_overlap))
    tuple_overlap = tups1.intersection(tups2).__len__()
    print (str(tups1.__len__()) + ' ' + str(tups2.__len__()) + ' tuple overlap: ' + str(tuple_overlap))
    return id1, id2, app1, app2, inst_st1, inst_st2, tups1, tups2


def sin_blocks_overlap(ourout_path, realout_path, blockidx):
    id1 = set()
    id2 = set()
    app1 = set()
    app2 = set()
    inst_st1 = set()
    inst_st2 = set()
    tups1 = set()
    tups2 = set()
    for i in range(1, 5):
        print ('until tensor: ' +str(i))
        this_ourout_path = os.path.join(ourout_path, str(i))
        file1 = os.path.join(this_ourout_path, 'block_'+str(blockidx)+'.tuples')
        this_realout_path = os.path.join(realout_path, str(i))
        file2 = os.path.join(this_realout_path, 'block_'+str(blockidx)+'.tuples')
        idset1, idset2, appset1, appset2, inst_st_set1, inst_st_set2, tupleset1, tupleset2 = \
            sin_block_overlap(file1, file2)
        id1 = id1.union(idset1)
        id2 = id2.union(idset2)
        app1 = app1.union(appset1)
        app2 = app2.union(appset2)
        inst_st1 = inst_st1.union(inst_st_set1)
        inst_st2 = inst_st2.union(inst_st_set2)
        tups1 = tups1.union(tupleset1)
        tups2 = tups2.union(tupleset2)

        id_overlap = id1.intersection(id2).__len__()
        print ('id overlap: '+ str(id_overlap))
        app_overlap = app1.intersection(app2).__len__()
        print ('app overlap: ' + str(app_overlap))
        inst_st_overlap = inst_st1.intersection(inst_st2).__len__()
        print ('inst_st overlap: ' + str(inst_st_overlap))
        tuple_overlap = tups1.intersection(tups2)
        print ('tuple overlap: ' + str(tuple_overlap))


# add all blocks
def accum_block_overlap(this_ourout_path, this_realout_path, filenum):
    id1 = set()
    id2 = set()
    app1 = set()
    app2 = set()
    inst_st1 = set()
    inst_st2 = set()
    tups1 = set()
    tups2 = set()
    for i in range(1, 1+filenum):
        file1 = os.path.join(this_ourout_path, 'block_' + str(i) + '.tuples')
        file2 = os.path.join(this_realout_path, 'block_' + str(i) + '.tuples')
        idset1, idset2, appset1, appset2, inst_st_set1, inst_st_set2, tupleset1, tupleset2 = \
            sin_block_overlap(file1, file2)
        id1 = id1.union(idset1)
        id2 = id2.union(idset2)
        app1 = app1.union(appset1)
        app2 = app2.union(appset2)
        inst_st1 = inst_st1.union(inst_st_set1)
        inst_st2 = inst_st2.union(inst_st_set2)
        tups1 = tups1.union(tupleset1)
        tups2 = tups2.union(tupleset2)
    id_overlap = id1.intersection(id2).__len__()
    # print (str(id1.__len__())+' '+str(id2.__len__()) + ' all blocks id overlap: ' + str(id_overlap))
    # app_overlap = app1.intersection(app2).__len__()
    # print (str(app1.__len__())+' '+str(app2.__len__()) + ' all blocks app overlap: ' + str(app_overlap))
    # inst_st_overlap = inst_st1.intersection(inst_st2).__len__()
    # print (str(inst_st1.__len__())+' '+str(inst_st2.__len__()) + ' all blocks inst_st overlap: ' + str(inst_st_overlap))
    # tuple_overlap = tups1.intersection(tups2).__len__()
    # print (str(tups1.__len__())+' '+str(tups2.__len__()) + ' all blocks tuple overlap: ' + str(tuple_overlap))
    return id1, id2, app1, app2, inst_st1, inst_st2, tups1, tups2


# add all blocks of files
def accum_blocks_overlap(ourout_path, realout_path):
    id1 = set()
    id2 = set()
    app1 = set()
    app2 = set()
    inst_st1 = set()
    inst_st2 = set()
    tups1 = set()
    tups2 = set()
    for i in range(0, 5):
        print ('until tensor: ' + str(i+1))
        this_ourout_path = os.path.join(ourout_path, str(i))
        this_realout_path = os.path.join(realout_path, str(i))
        one_id1, one_id2, one_app1, one_app2, one_inst_st1, one_inst_st2, one_tups1, one_tups2 = \
            accum_block_overlap(this_ourout_path, this_realout_path, 20)
        id1 = id1.union(one_id1)
        id2 = id2.union(one_id2)
        app1 = app1.union(one_app1)
        app2 = app2.union(one_app2)
        inst_st1 = inst_st1.union(one_inst_st1)
        inst_st2 = inst_st2.union(one_inst_st2)
        tups1 = tups1.union(one_tups1)
        tups2 = tups2.union(one_tups2)
        id_overlap = id1.intersection(id2).__len__()
        print (str(id1.__len__())+' '+str(id2.__len__()) +' all blocks id overlap: ' + str(id_overlap))
        app_overlap = app1.intersection(app2).__len__()
        print (str(app1.__len__())+' '+str(app2.__len__()) + ' all blocks app overlap: ' + str(app_overlap))
        inst_st_overlap = inst_st1.intersection(inst_st2).__len__()
        print (str(inst_st1.__len__())+' '+str(inst_st2.__len__()) + ' all blocks inst_st overlap: ' + str(inst_st_overlap))
        tuple_overlap = tups1.intersection(tups2).__len__()
        print (str(tups1.__len__())+' '+str(tups2.__len__()) + ' all blocks tuple overlap: ' + str(tuple_overlap))


def result_analysis(ourout_path, realout_path, k, filenum):
    # accum_blocks_overlap(ourout_path, realout_path)
    for i in range(1, k):
        print ('k: '+str(i))
        this_ourout_path = os.path.join(ourout_path, str(i))
        this_realout_path = os.path.join(realout_path, str(i))
        for j in range(1, 1+filenum):
            print ('block: ' + str(j))
            this_ourout_file = os.path.join(this_ourout_path, 'block_' + str(j) + '.tuples')
            this_realout_file = os.path.join(this_realout_path, 'block_' + str(j) + '.tuples')
            sin_block_overlap(this_ourout_file, this_realout_file)
        # for filenum in range(1, 6):
        #     print filenum
        #     accum_block_overlap(this_ourout_path, this_realout_path, filenum)



if __name__=='__main__':
    path = '/Users/baby/Document/TensorAugmented/360data'
    # dirpath = os.path.join(path, 'itime_staytime')
    dirpath = os.path.join(path, 'itime_utime')
    ourout_path = os.path.join(dirpath, 'our_accum_output')
    # ourout_path = os.path.join(dirpath, 'concat_sinout_files_output')
    realout_path = os.path.join(dirpath, 'real_accum_output')


