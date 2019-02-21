import math
import os
import result_analysis


# def invoke_dcube(file_path, output_path):
#     if os.path.isdir(file_path):
#         files = os.listdir(file_path)
#         for file in files:
#             output = os.path.join(output_path, file)
#             os.mkdir(output)


def concat_block_tuples(sinout_path, ourout_path, concatfile, filenum):
    all_tuples = []
    for j in range(1, filenum+1):
        sinoutfile = os.path.join(sinout_path, 'block_'+str(j)+'.tuples')
        sinf = open(sinoutfile, 'r')
        tuples = sinf.readlines()
        all_tuples.extend(tuples)
        sinf.close()
        ouroutfile = os.path.join(ourout_path, 'block_' + str(j) + '.tuples')
        ourf = open(ouroutfile, 'r')
        tuples = ourf.readlines()
        all_tuples.extend(tuples)
        sinf.close()
    f = open(concatfile, 'w')
    all_tuples_set = set(all_tuples)
    f.writelines(list(all_tuples_set))
    f.close()


if __name__ == '__main__':
    concat_single_output = r'E:\360data\20180601_20180614\dcube\itime_staytime\cut_file\concat_single_output'
    accumu_outputs_path = r'E:\360data\20180601_20180614\dcube\itime_staytime\cut_file\accumulation_files_dcube_outputs'
    filenum = 12
    concat_block_tuples(concat_single_output, accumu_outputs_path, filenum)

