import pylab as plt
import blimpy as bl
import turbo_seti as ts
from turbo_seti.find_event.plot_event import overlay_drift, plot_waterfall
import os

def runcmd(cmd):
    print(cmd)
    os.system(cmd)

def test_plot_voyager_fscrunch():
    print("\n===== test_plot_voyager_fscrunch =====")
    ###
    ## turboSETI Voyager1.single_coarse.fine_res.h5 -f 32 -M 1
    ###
    fs, dr = 32, 4
    watfiles   = ['Voyager1.single_coarse.fine_res.h5', 'Voyager1.single_coarse.fine_res.flipped.h5']
    datfiles   = ['Voyager1.single_coarse.fine_res.dat', 'Voyager1.single_coarse.fine_res.flipped.dat']
    shortnames = ['voyager', 'voyager_flipped']

    if not os.path.exists('./figs/'):
        os.mkdir('./figs')
    for ii in range(len(watfiles)):
        watfile, datfile, shortname = watfiles[ii], datfiles[ii], shortnames[ii]

        if os.path.exists(datfile):
            os.remove(datfile)

        runcmd(f"turboSETI {watfile} -f {fs} -M {dr}")

        tbl = ts.read_dat(datfile)
        wf  = bl.Waterfall(watfile)
        tduration = (wf.n_ints_in_file - 1)* wf.header['tsamp']

        for ii in range(len(tbl)):
            tblrow = tbl.iloc[ii]
            print(tblrow)
            f0, fstart, fstop = tblrow['Freq'], tblrow['FreqStart'], tblrow['FreqEnd']
            drate, fs = tblrow['DriftRate'], tblrow['Fscrunch']
            plt.clf()
            plot_waterfall(wf, wf.header['source_name'], f_start=fstart, f_stop=fstop, f_scrunch=fs)
            overlay_drift(f0, fstart, fstop, drate, tduration)
            plt.savefig(f"figs/{shortname}_{ii}.png")

if __name__ == "__main__":
    test_plot_voyager_fscrunch()