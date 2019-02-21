import os


def topk_densities(this_out_path, modes):
    densities = []
    for name in os.listdir(this_out_path):
        if name.endswith('.tuples'):
            outfile = os.path.join(this_out_path, name)
            density = blocks_density(outfile, modes)
            densities.append(density)
    sorted_densities = sorted(densities, reverse=True)
    return sorted_densities


'find topk blocks from B1,B2,B3'
def topk(sinout_path, ourout_path, concatout_path, filenum):
    density_file_tuples = []
    for j in range(1, filenum+1):
        sinoutfile = os.path.join(sinout_path, 'block_' + str(j) + '.tuples')
        density = blocks_density(sinoutfile)
        tuple = (density, sinoutfile)
        density_file_tuples.append(tuple)

        ouroutfile = os.path.join(ourout_path, 'block_' + str(j) + '.tuples')
        density = blocks_density(ouroutfile)
        tuple = (density, ouroutfile)
        density_file_tuples.append(tuple)

        concatoutfile = os.path.join(concatout_path, 'block_' + str(j) + '.tuples')
        density = blocks_density(concatoutfile)
        tuple = (density, concatoutfile)
        density_file_tuples.append(tuple)
    sorted_density_file_tuples = sorted(density_file_tuples, key=lambda x: x[0], reverse=True)
    return sorted_density_file_tuples[:filenum]


def blocks_density(file, modes):
    ids = set()
    apps = set()
    it_sts= set()
    mass = 0
    f = open(file, 'r')
    for line in f.readlines():
        cols = line.replace('\n', '').split(',')
        ids.add(cols[0])
        apps.add(cols[1])
        it_sts.add(cols[2])
        mass = mass + int(cols[3])
    blocksize = ids.__len__()+apps.__len__()+it_sts.__len__()
    if blocksize != 0:
        density = (mass/blocksize) * modes
    else:
        density = 0
    return density


if __name__ == '__main__':
    # path = r'/Users/baby/Document/TensorAugmented/data/360data'
    # inject_dir = os.path.join(path, 'inject')
    # acnt, bcnt, popbd = 10000, 1000, 100
    # goals = [1000, 1200, 1400, 1600, 1800, 2000]
    # for goal in goals[:]:
    #     print 'goal: {}'.format(goal)
    #     goal_dir = os.path.join(inject_dir, 'goal=' + str(goal))
    #
    #     output_dir = os.path.join(goal_dir, 'our_accum_output')
    #     output_path = os.path.join(output_dir, '9')
    #     output_file = os.path.join(output_path, 'block_1.tuples')
    #     density = blocks_density(output_file, modes=4)
    #     print density
    #     print ''
    path = r'/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    bins = [0.5, 1, 2]
    for bin in bins:
        print bin
        dirpath = os.path.join(path, 'bin='+str(bin))
        output_dir = os.path.join(dirpath, 'our_accum_output')
        output_path = os.path.join(output_dir, '18')
        output_file = os.path.join(output_path, 'block_1.tuples')
        density = blocks_density(output_file, modes=4)
        print density
        print ''
