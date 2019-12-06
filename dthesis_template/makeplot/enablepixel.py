from ROOT import TH2F, gStyle
import ROOT
import json
import numpy as np



def jsonread():
    f = open("./data/016012_std_digitalscan_KEK53-4/rd53a_test.json.after", 'r')
    json_data = json.load(f)
    pix_list = ["Col", "Enable", "Hitbus", "InjEn", "TDAC"]
    col_list = np.linspace(1., 2., 2.)
    row_list = np.linspace(1., 180., 180.)
    print(col_list)

    h2D = TH2F("h2D", "", 400, 1, 400, 192, 1, 192)
    gStyle.SetPalette(1)
#    ["PixelConfig"][{"Col", "Enable", "Hitbus", "InjEn", "TDAC"},{}]
    for col in col_list:
        print(col)
        print("Col:{} \t".format(col))#json_data["RD53A"]["PixelConfig"][col]))
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in row_list:
            enable = colnum["Enable"][int(row)]
            if enable == 1:
                h2D.Fill(col, row)
    h2D.Draw("col")

if __name__=='__main__':
    main()


