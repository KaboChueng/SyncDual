import os
import math
import util
import find_topk_blocks


def genApnameDict(wifi_path):
    apname_dir = os.path.join(wifi_path, 'apname')
    apname_dict = {}
    for filename in os.listdir(apname_dir):
        csvfile = os.path.join(apname_dir, filename)
        print csvfile
        if os.path.getsize(csvfile):
            with open(csvfile, 'r') as csvf:
                for line in csvf:
                    cols = line.strip().split(',')
                    if cols.__len__() == 4:
                        ap, apname = cols[2], cols[3]
                        apname_dict[ap] = apname
    return apname_dict


def mactoIp(apmac):
    ipwords =[]
    words = eval(apmac).strip().split()
    for word in words:
        ip_word = str(int(word, 16))
        ipwords.append(ip_word)
    ap_ip = '.'.join(ipwords)
    return ap_ip


def genMaxApname(wifi_path, bin):
    binpath = os.path.join(wifi_path, 'bin=' + str(bin))
    filenum = 10
    apnamedict = genApnameDict(wifi_path)
    for i in range(1, filenum+1):
        freq_apfile = os.path.join(binpath, str(i)+'freq_ap.txt')
        freqf = open(freq_apfile, 'r')
        for line in freqf.readlines()[:10]:
            max_apmac = line.strip().split(',')[0]
            print max_apmac
            ap_ip = mactoIp(max_apmac)
            if ap_ip in apnamedict:
                apname = apnamedict[ap_ip]
            else:
                apname = ''
            print 'block:{}, apname:{}'.format(i, apname)


def wifi_susp(wifi_path, bin):
    our_accum_output = os.path.join(wifi_path, 'our_accum_output')
    k = 18
    last_our_output = os.path.join(our_accum_output, str(k))
    firBlock_file = os.path.join(last_our_output, 'block_1.tuples')
    densefile = os.path.join(wifi_path, 'bin='+str(bin)+'_dense_block.txt')

    ap_mapfile = os.path.join(wifi_path, 'app_map.txt')
    apdict = genMapfileDict(ap_mapfile)
    mobile_mapfile = os.path.join(wifi_path, 'dev_map.txt')
    mobiledict = genMapfileDict(mobile_mapfile)

    valdict = {}
    with open(firBlock_file, 'r') as firF, open(densefile, 'w') as densef:
        for line in firF:
            cols = line.strip().split(',')
            mobile, ap, st, et = cols[:4]
            key = (mobile, ap, st, et)
            if key not in valdict:
                valdict[key] = 1
            else:
                valdict[key] = valdict[key] + 1
        sorted_items = sorted(valdict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        for item in sorted_items:
            key, value = item[0], item[1]
            densef.write(','.join((mobiledict[key[0]], apdict[key[1]], genReadableTime(int(key[2]), bin),
                                  genReadableTime(int(key[3]), bin), str(value))))
            densef.write('\n')
    densef.close()
    readTensor.read_itime_utime_file(densefile)
    density = find_topk_blocks.blocks_density(densefile, modes=4)
    print density


def genSpike(path, blockfile, stride, t1):
    dev_mapfile = os.path.join(path, 'dev_map.txt')
    devmapdict = genMapfileDict(dev_mapfile)
    app_mapfile = os.path.join(path, 'app_map.txt')
    appmapdict = genMapfileDict(app_mapfile)
    dirpath = os.path.join(path, 'stride={},t1={}'.format(stride, t1))
    spike_appfile = os.path.join(dirpath, 'spike_app.txt')
    spike_devfile = os.path.join(dirpath, 'spike_dev.txt')
    devset = set()
    appset = set()
    with open(blockfile, 'r') as bf, open(spike_appfile, 'w') as sa, open(spike_devfile, 'w') as sd:
        for line in bf:
            dev, app = line.strip().split(',')[:2]
            devset.add(dev)
            appset.add(app)
        bf.close()
        for dev in devset:
            maped_dev = devmapdict[dev]
            sd.write(maped_dev+'\n')
        for app in appset:
            maped_app = appmapdict[app]
            sa.write(maped_app+'\n')
        sa.close()
        sd.close()


'gen sort file: mobile count'
def genFreqSortFile(wifi_path, bin):
    binpath = os.path.join(wifi_path, 'bin=' + str(bin))
    our_accum_output = os.path.join(binpath, 'our_accum_output')
    k, filenum = 18, 10
    last_our_output = os.path.join(our_accum_output, str(k))
    for i in range(1, 2):
        firBlock_file = os.path.join(last_our_output, 'block_'+str(i)+'.tuples')
        mobile_mapfile = os.path.join(binpath, 'dev_map.txt')
        mobile_map_dict = genMapfileDict(mobile_mapfile)
        ap_mapfile = os.path.join(binpath, 'app_map.txt')
        ap_map_dict = genMapfileDict(ap_mapfile)

        mobile_freq_dict, ap_freq_dict, time_freq_dict = {}, {}, {}
        with open(firBlock_file, 'r') as firf:
            for line in firf:
                cols = line.strip().split(',')
                maped_mobile, maped_ap, st, et = cols[:4]
                if maped_mobile not in mobile_freq_dict:
                    mobile_freq_dict[maped_mobile] = 1
                else:
                    mobile_freq_dict[maped_mobile] = mobile_freq_dict[maped_mobile] + 1
                if maped_ap not in ap_freq_dict:
                    ap_freq_dict[maped_ap] = 1
                else:
                    ap_freq_dict[maped_ap] = ap_freq_dict[maped_ap] + 1
                timetup = (st, et)
                if timetup not in time_freq_dict:
                    time_freq_dict[timetup] = 1
                else:
                    time_freq_dict[timetup] = time_freq_dict[timetup] + 1
        sorted_mobile_items = sorted(mobile_freq_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        sorted_ap_items = sorted(ap_freq_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        sorted_time_items = sorted(time_freq_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

        mobilefile = os.path.join(binpath, str(i)+'freq_mobile.txt')
        apfile = os.path.join(binpath, str(i)+'freq_ap.txt')
        timefile = os.path.join(binpath, str(i)+'freq_time.txt')

        with open(mobilefile, 'w') as mof, open(apfile, 'w') as apf, open(timefile, 'w') as timef:
            for item in sorted_mobile_items:
                mof.write(','.join((mobile_map_dict[item[0]], str(item[1]))))
                mof.write('\n')
            for item in sorted_ap_items:
                ap_mac = ap_map_dict[item[0]]
                apf.write(','.join((ap_mac, str(item[1]))))
                apf.write('\n')
            for item in sorted_time_items:
                st, et = item[0][0], item[0][1]
                stdate, etdate = genReadableTime(int(st), bin), genReadableTime(int(et), bin)
                timef.write(','.join((stdate, etdate, str(item[1]))))
                timef.write('\n')
        mof.close()
        apf.close()
        timef.close()


def genReadableTime(t, bin):
    stdate = '03-01 00:00'
    ts1, ts2 = t * bin, (t+1) * bin
    date1 = changeDate(ts1, stdate)
    date2 = changeDate(ts2, stdate)

    month_day, hour_min1 = date1.split(' ')
    hour_min2 = date2.split(' ')[1]
    date = month_day + ' ' + hour_min1 + '~' + hour_min2
    return date


def changeDate(ts, stdate):
    month1 = int(ts / (30 * 24))
    day1 = int(ts / 24) - month1 * 30
    hour1 = ts - month1 * 30 * 24 - day1 * 24
    min1 = math.fmod(hour1, 1)
    hour1 = int(hour1)
    st_month_day, st_hour_min = stdate.split(' ')
    st_month = int(st_month_day[:2])
    st_day = int(st_month_day[-2:])
    st_hour = int(st_hour_min[:2])
    et_month = '0' + str(st_month + month1)
    et_day = st_day + day1
    if et_day <= 9:
        et_day = '0' + str(et_day)
    else:
        et_day = str(et_day)
    et_hour = str(st_hour + hour1)
    if min1 == 0.5:
        et_min = '30'
    else:
        et_min = '00'
    etdate = et_month + '-' + et_day + ' ' + et_hour + ':' + et_min
    return etdate


def alertSuspDev(path, alert_path):
    itime_utime_dir = os.path.join(path, 'itime_utime')
    dev_mapfile = os.path.join(itime_utime_dir, 'app_map.txt')
    devmapf = open(dev_mapfile, 'r')
    devdict = {}
    for line in devmapf:
        dev, maped_dev = line.strip().split(',')
        devdict[maped_dev] = dev
    devfile = os.path.join(alert_path, 'app.txt')
    devf = open(devfile, 'r')
    line = devf.readline().strip()
    devset = set(line.split(' '))
    maped_devfile = os.path.join(alert_path, 'maped_app.txt')
    mapedf = open(maped_devfile, 'w')
    for dev in devset:
        mapedf.write(devdict[dev] + '\n')
    mapedf.close()


def concatSuspDev(susp_path):
    suspfile = os.path.join(susp_path, 'susp_dev.txt')
    susf = open(suspfile, 'w')
    susp_set = set()
    for name in os.listdir(susp_path):
        file = os.path.join(susp_path, name)
        with open(file, 'r') as f:
            for line in f:
                dev = line.strip()
                if dev not in susp_set:
                    susf.write(dev+'\n')
                    susp_set.add(dev)
        f.close()
    susf.close()


def genSuspApname(wifi_path):
    apname_dict = genApnameDict(wifi_path)
    bins = [0.5, 2]
    for bin in bins:
        print 'bin:{}'.format(bin)
        binpath = os.path.join(wifi_path, 'bin=' + str(bin))
        susp_apfile = os.path.join(binpath, 'susp_mobile.txt')
        susp_apnamefile = os.path.join(binpath, 'susp_apname.txt')
        with open(susp_apfile, 'r') as suspf, open(susp_apnamefile, 'w') as suspw:
            for line in suspf:
                apmac, num = line.strip().split(',')
                ap_ip = mactoIp(apmac)
                apname = apname_dict[ap_ip]
                suspw.write(','.join((apname, num)))
                suspw.write('\n')
        suspw.close()
        suspf.close()


def genApClassroomDict(wifi_path):
    apname_dir = os.path.join(wifi_path, 'apname')
    classroom_dict = {}
    for filename in os.listdir(apname_dir):
        csvfile = os.path.join(apname_dir, filename)
        if os.path.getsize(csvfile):
            print csvfile
            with open(csvfile, 'r') as csvf:
                for line in csvf:
                    words = line.strip().split(',')
                    if words.__len__() == 4:
                        ap, apname = words[2:4]
                        cols = eval(apname).strip().split('_')[:-1]
                        classroom = '_'.join(cols)
                        classroom_dict[ap] = classroom
    return classroom_dict


if __name__ == '__main__':
    'invoke 360'
    path = r'/Users/baby/Document/TensorAugmented/data/360data/itime_utime'
    # suspDev(path)
    alert_path = '/Users/baby/eclipse-workspace/dense-alert(tensorAugmented)/files'
    # alertSuspDev(path, alert_path)
    susp_path = os.path.join(path, 'itime_utime/susp_apps')
    # concatSuspDev(susp_path)
    stride, t1 = 1, 1
    spikepath = os.path.join(path, 'stride=1,t1=1/our_accum_output/3/newfiles')
    blockfile = os.path.join(spikepath, 'block_1.tuples')
    # genSpike(path, blockfile, stride, t1)

    'invoke wifi'
    wifi_path = '/Users/baby/Document/TensorAugmented/data/wifi/0301_0430'
    genApClassroomDict(wifi_path)













