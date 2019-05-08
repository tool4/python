#!/bin/python

filepath = 'last_wgpw_pure.txt'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    #it's dumb to mix pol and eng, fixme!
    zmiana_all = float(0)
    all_cnt = 0
    zmiana_positive = float(0)
    pos_cnt = 0
    zmiana_chosen = float(0)
    chs_cnt = 0
    while line:
        list = line.split(",")

        name = list[0].strip()
        kurs_str = list[1].strip()
        zmiana_str = list[2].strip()[:-1]
        cz_str = list[6].strip()
        cwk_str = list[7].strip()

        kurs = 0.0
        if(kurs_str and len(kurs_str) > 0):
            kurs = float(kurs_str)

        zmiana = 0.0
        if(zmiana_str and len(zmiana_str) > 0):
            zmiana = float(zmiana_str)

        cz = 0.0
        if(cz_str and len(cz_str) > 0):
            cz = float(cz_str)

        cwk = float(0)
        if(cwk_str and len(cwk_str) > 0):
            cwk = float(cwk_str)

        if( cz > 0 and cwk > 0):
            if( cz < 10 and cwk < 1):  #promising?
                print(name, ": ", kurs, ", zmiana: ", zmiana, "%, C/Z: ", cz, ", C/WK: ", cwk)
                zmiana_chosen += zmiana
                chs_cnt += 1
            zmiana_positive += zmiana
            pos_cnt += 1
        zmiana_all += zmiana
        all_cnt += 1
        line = fp.readline()
        cnt += 1

print( "Calkowita zmiana, suma: ", zmiana_all, "%, srednia: ", zmiana_all / all_cnt)
print( "zmiana spolek na plusie: ", zmiana_positive, "%, srednia: ", zmiana_positive / pos_cnt)
print( "zmiana wybranych spolek: ", zmiana_chosen, "%, srednia: ", zmiana_chosen / chs_cnt)
