#! python
import csv
import pandas as pd
import os
import re

'''
This is a python script to summarize Study 3 (Virtual Audience) data.

study3_2023-03-15: initial version
study3_2023-03-17: working version
- sex code: F=female, M=male
- vaud appr code: C=critical, E=encouraging
- vaud size code: S=small, L=large
- p_nr on questionnaire paper-qualtrics file must be ordered from 1-102
- pprsa, fpe, bfne, sen, tr, apl, cp values are added to the infoperpprt_list
study3_2023-03-22: complete version to be released
- physiodata values are added to the infoperpprt_list
- export data scripts are added
study3_2024-06-03: extended version
- allow HRV_rmssd extraction
    
Note:
Pandas was used for only a few parts, which was managed by Anaconda.
Spyder was used for the editor.
https://pandas.pydata.org/docs/getting_started/install.html
https://docs.continuum.io/anaconda/install/

~ELF
'''


'''
The main class for the data per participant
'''
class InfoPerPpt:
    def __init__(self, p_nr, age, sex, vaud_appr, vaud_size, vbl_fb, nonvbl_fb,\
                 prpsa, fpe, bfne, sen_pre, tr_pre,\
                 hr_prp, hr_prp1, hr_prp2, hr_prp3, hr_prp4, hr_prp5,\
                 hr_spc, hr_spc1, hr_spc2, hr_spc3, hr_spc4, hr_spc5,\
                 sc_prp, sc_prp1, sc_prp2, sc_prp3, sc_prp4, sc_prp5,\
                 sc_spc, sc_spc1, sc_spc2, sc_spc3, sc_spc4, sc_spc5,\
                 skt_prp, skt_prp1, skt_prp2, skt_prp3, skt_prp4, skt_prp5,\
                 skt_spc, skt_spc1, skt_spc2, skt_spc3, skt_spc4, skt_spc5,\
                 sen_post, tr_post, apl, cp,\
                 hrv_prp, hrv_prp1, hrv_prp2, hrv_prp3, hrv_prp4, hrv_prp5,\
                 hrv_spc, hrv_spc1, hrv_spc2, hrv_spc3, hrv_spc4, hrv_spc5 ):
        self.p_nr = p_nr #1
        self.age = age #2
        self.sex = sex #3
        self.vaud_appr = vaud_appr #4
        self.vaud_size = vaud_size #5
        self.vbl_fb = vbl_fb #6
        self.nonvbl_fb = nonvbl_fb #7
        self.prpsa = prpsa #8
        self.fpe = fpe #9
        self.bfne = bfne #10
        self.sen_pre = sen_pre #11
        self.tr_pre = tr_pre #12
        self.hr_prp = hr_prp #13
        self.hr_prp1 = hr_prp1
        self.hr_prp2 = hr_prp2
        self.hr_prp3 = hr_prp3
        self.hr_prp4 = hr_prp4
        self.hr_prp5 = hr_prp5
        self.hr_spc = hr_spc #14
        self.hr_spc1 = hr_spc1
        self.hr_spc2 = hr_spc2
        self.hr_spc3 = hr_spc3
        self.hr_spc4 = hr_spc4
        self.hr_spc5 = hr_spc5
        self.sc_prp = sc_prp #15
        self.sc_prp1 = sc_prp1
        self.sc_prp2 = sc_prp2
        self.sc_prp3 = sc_prp3
        self.sc_prp4 = sc_prp4
        self.sc_prp5 = sc_prp5
        self.sc_spc = sc_spc #16
        self.sc_spc1 = sc_spc1
        self.sc_spc2 = sc_spc2
        self.sc_spc3 = sc_spc3
        self.sc_spc4 = sc_spc4
        self.sc_spc5 = sc_spc5
        self.skt_prp = skt_prp #17
        self.skt_prp1 = skt_prp1
        self.skt_prp2 = skt_prp2
        self.skt_prp3 = skt_prp3
        self.skt_prp4 = skt_prp4
        self.skt_prp5 = skt_prp5
        self.skt_spc = skt_spc #18
        self.skt_spc1 = skt_spc1
        self.skt_spc2 = skt_spc2
        self.skt_spc3 = skt_spc3
        self.skt_spc4 = skt_spc4
        self.skt_spc5 = skt_spc5
        self.sen_post = sen_post #19
        self.tr_post = tr_post #20
        self.apl = apl #21
        self.cp = cp #22
        self.hrv_prp = hrv_prp
        self.hrv_prp1 = hrv_prp1
        self.hrv_prp2 = hrv_prp2
        self.hrv_prp3 = hrv_prp3
        self.hrv_prp4 = hrv_prp4
        self.hrv_prp5 = hrv_prp5
        self.hrv_spc = hrv_spc
        self.hrv_spc1 = hrv_spc1
        self.hrv_spc2 = hrv_spc2
        self.hrv_spc3 = hrv_spc3
        self.hrv_spc4 = hrv_spc4
        self.hrv_spc5 = hrv_spc5
        

'''
info_perppt_list is a list that will store the InfoPerPpt objects.
The list is initiated below.
'''
infoperppt_list = []
for i in range(102): #number of participants
    infoperppt_list.append(InfoPerPpt(i+1, "", "", "", "", "", "",\
                                      "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "",\
                                      "", "", "", "", "", "",\
                                      "", "", "", "", "", ""))


'''
Filepaths
'''
qs_unity_dir = "./input/questionnaire_unity/"
qs_paperqualtrics = "./input/Questionnaire Paper-Qualtrics 2023-03-17.csv"
physio_dir = "./input/physiodata/"


'''
The pandas data frame of the paper-qualtrics questionnaire file
'''
pq = pd.read_csv(qs_paperqualtrics)



'''
A function to get ppt nr, age, sex from unity questionnaire files
'''
def get_pptinfo_from_unityqs(filename):
    splitted_format = filename.split(".")
    splitted_dir = splitted_format[0].split("_")
    return splitted_dir


'''
A function to get experiment conditions from unity questionnaire files
'''
def get_conditions_from_unityqs(filename):
    with open(dirpath + "/" + filename) as csvfile:
        thedata = csv.reader(csvfile, delimiter=',')
        count = 0
        returning_array = []
        for row in thedata:
            if count <2:
                count += 1
            elif count == 2:
                returning_array = [row[1], row[2]] #appearance, size
            else:
                returning_array = []
    return returning_array

'''
A function to get the unity questionnaire values

It doesn't use pandas because the column number is not consistent per rows,
there is an extra commas at the end of row 2 and 3 of the csv files
'''
def get_unity_questionnaire_values(filename):
    with open(dirpath + filename) as csvfile:
        thedata = csv.reader(csvfile, delimiter=',')
        count = 0
        sen_pre = []
        tr_pre = []
        sen_post = []
        tr_post = []
        apl = []
        cp = []
        cp_mean = -1
        for row in thedata:
            if count < 3:
                if count == 1:
                    sen_pre = [row[3], row[4], row[5]]
                    tr_pre = [row[6], row[7]]
                elif count == 2:
                    sen_post = [row[3], row[4], row[5]]
                    tr_post = [row[6], row[7]]
                    apl = [row[8], row[9], row[10], row[11]]
                    cp = [row[12], row[13], row[14], row[15], row[16], cp_mean]
                else:
                    foo="bar"
                count += 1
            else:
                foo="bar"
        #reverse cp question number 3
        if cp[2] == 1:
            cp[2] = 7
        elif cp[2] == 2:
            cp[2] = 6
        elif cp[2] == 3:
            cp[2] = 5
        elif cp[2] == 4:
            cp[2] = 4
        elif cp[2] == 5:
            cp[2] = 3
        elif cp[2] == 6:
            cp[2] = 2
        elif cp[2] == 7:
            cp[2] = 1
        else:
            foo="bar"
        #reverse cp question number 5
        if cp[4] == 1:
            cp[4] = 7
        elif cp[4] == 2:
            cp[4] = 6
        elif cp[4] == 3:
            cp[4] = 5
        elif cp[4] == 4:
            cp[4] = 4
        elif cp[4] == 5:
            cp[4] = 3
        elif cp[4] == 6:
            cp[4] = 2
        elif cp[4] == 7:
            cp[4] = 1
        else:
            foo="bar"
        #calculate cp mean
        cp[5] = (int(cp[0])+int(cp[1])+int(cp[2])+int(cp[3])+int(cp[4]))/5
    return sen_pre, tr_pre, sen_post, tr_post, apl, cp



'''
Assign the basic ppt info and questionnaire values to infoperppt_list
'''
for dirpath, dirnames, filenames in os.walk(qs_unity_dir):
    for fn in filenames:
        afn = get_pptinfo_from_unityqs(fn)
        #            0 1               2  3  4
        #fn example: Q_20220505-143542_P1_26_Male.csv
        print("Processing " + fn + "...")
        for e in infoperppt_list:
            if e.p_nr == int(re.findall(r'\d+',afn[2])[0]):
                #populate basic info from unity questionnaire files
                e.age = afn[3]
                e.sex = afn[4]
                if e.sex == "Female":
                    e.sex = "F"
                elif e.sex == "Male":
                    e.sex = "M"
                else:
                    e.sex = ""
                    print("Sex is neither Female nor Male for P" + e.p_nr)
                e.vaud_appr = get_conditions_from_unityqs(fn)[0]
                if e.vaud_appr == "Encouraging":
                    e.vaud_appr = "E"
                elif e.vaud_appr == "Critical":
                    e.vaud_appr = "C"
                else:
                    e.vaud_appr = ""
                    print("vaud_appr is neither Encouraging nor Critical for P" + e.p_nr)
                e.vaud_size = get_conditions_from_unityqs(fn)[1]
                if e.vaud_size == "Small":
                    e.vaud_size = "S"
                elif e.vaud_size == "Big":
                    e.vaud_size = "L"
                else:
                    e.vaud_size = ""
                    print("Virtual audience appearance is neither Small nor Big for P" + e.p_nr)
                #populate the paper-qualtrics questionnaire objects
                e.prpsa = pq['A_SUM'][e.p_nr-1] #p_nr-1 cuz index starts 0 on dfs
                e.fpe = pq['B_AVG'][e.p_nr-1]
                e.bfne = pq['C_AVG'][e.p_nr-1]
                #populate the unity questionnaire objects
                e.sen_pre = get_unity_questionnaire_values(fn)[0]
                e.tr_pre = get_unity_questionnaire_values(fn)[1]
                e.sen_post = get_unity_questionnaire_values(fn)[2]
                e.tr_post = get_unity_questionnaire_values(fn)[3]
                e.apl = get_unity_questionnaire_values(fn)[4]
                e.cp = get_unity_questionnaire_values(fn)[5]
            else:
                foo="bar"


'''
Variables to help retrieving values from physiodata files
'''
#general column names
_datasource = "dataSource"
_epochname = "epochName"
_hr = "HR_mean"
_sc = "SCL_filt_mean"
_skt = "mean"
_hrv = "HRV_rmssd"

#hr columns
_hr_col = -1
_hr_datasource_col = -1
_hr_epochname_col = -1
_hrv_col = -1

#sc column names
_sc_col = -1
_sc_datasource_col = -1
_sc_epochname_col = -1

#skt column names
_skt_col = -1
_skt_datasource_col = -1
_skt_epochname_col = -1


'''
A function to get participant number from physiodata files
'''
def get_pptnr_from_physio(datasource):
    ppt = datasource.split("_")
    ppt_nr = -1
    if len(ppt) == 3:
        ppt_nr = ppt[2].split("P")[1]
    else:
        ppt_nr = -1
    return ppt_nr


'''
Assign the physiodata values to infoperppt_list
'''
for dirpath, dirnames, filenames in os.walk(physio_dir):
    for fn in filenames:
        #get the relevant physiodata column numbers by using dataframe
        if fn == "ECG_RESULTS.txt":
            print(dirpath + "/" + fn)
            hr_df = pd.read_csv(dirpath+"/"+ fn, sep='\t')
            _hr_datasource_col = hr_df.columns.get_loc(_datasource)
            _hr_epochname_col = hr_df.columns.get_loc(_epochname)
            _hr_col = hr_df.columns.get_loc(_hr)
            _hrv_col = = hr_df.columns.get_loc(_hrv)
        elif fn == "SC_RESULTS.txt":
            print(dirpath + "/" + fn)
            sc_df = pd.read_csv(dirpath + "/" + fn, sep='\t')
            _sc_datasource_col = sc_df.columns.get_loc(_datasource)
            _sc_epochname_col = sc_df.columns.get_loc(_epochname)
            _sc_col = sc_df.columns.get_loc(_sc)
        elif fn == "SKT_RESULTS.txt":
            print(dirpath + "/" + fn)
            skt_df = pd.read_csv(dirpath + "/" + fn, sep='\t')
            _skt_datasource_col = skt_df.columns.get_loc(_datasource)
            _skt_epochname_col = skt_df.columns.get_loc(_epochname)
            _skt_col = skt_df.columns.get_loc(_skt)
        else:
            foo="bar"
        #assign the values to infoperppt_list
        with open(dirpath+"/"+fn) as physiofile:
            if fn == "ECG_RESULTS.txt":
                hr_data = csv.reader(physiofile, delimiter='\t')
                for row in hr_data:
                    #only include rows that are not headers
                    if row[_hr_datasource_col] != _datasource:
                        _ppt_nr = get_pptnr_from_physio(row[_hr_datasource_col])
                        for e in infoperppt_list:
                            #if the ppt nr in the current ECG_RESULTS row is
                            #the same with the ppt nr in the infoperppt_list
                            if int(_ppt_nr) == e.p_nr:
                                epoch = row[_hr_epochname_col].split("_")[2]#length should be 3
                                if epoch == "prep":
                                    e.hr_prp = row[_hr_col]
                                    e.hrv_prp = row[_hrv_col]
                                elif epoch == "prep1":
                                    e.hr_prp1 = row[_hr_col]
                                    e.hrv_prp1 = row[_hrv_col]
                                elif epoch == "prep2":
                                    e.hr_prp2 = row[_hr_col]
                                    e.hrv_prp2 = row[_hrv_col]
                                elif epoch == "prep3":
                                    e.hr_prp3 = row[_hr_col]
                                    e.hrv_prp3 = row[_hrv_col]
                                elif epoch == "prep4":
                                    e.hr_prp4 = row[_hr_col]
                                    e.hrv_prp4 = row[_hrv_col]
                                elif epoch == "prep5":
                                    e.hr_prp5 = row[_hr_col]
                                    e.hrv_prp5 = row[_hrv_col]
                                elif epoch == "speech":
                                    e.hr_spc = row[_hr_col]
                                    e.hrv_spc = row[_hrv_col]
                                elif epoch == "speech1":
                                    e.hr_spc1 = row[_hr_col]
                                    e.hrv_spc1 = row[_hrv_col]
                                elif epoch == "speech2":
                                    e.hr_spc2 = row[_hr_col]
                                    e.hrv_spc2 = row[_hrv_col]
                                elif epoch == "speech3":
                                    e.hr_spc3 = row[_hr_col]
                                    e.hrv_spc3 = row[_hrv_col]
                                elif epoch == "speech4":
                                    e.hr_spc4 = row[_hr_col]
                                    e.hrv_spc4 = row[_hrv_col]
                                elif epoch == "speech5":
                                    e.hr_spc5 = row[_hr_col]
                                    e.hrv_spc5 = row[_hrv_col]
                                else:
                                    foo="bar"
                            else:
                                foo="bar"
                    else:
                        foo="bar"
            elif fn == "SC_RESULTS.txt":
                sc_data = csv.reader(physiofile, delimiter='\t')
                for row in sc_data:
                    #only include rows that are not headers
                    if row[_sc_datasource_col] != _datasource:
                        _ppt_nr = get_pptnr_from_physio(row[_sc_datasource_col])
                        for e in infoperppt_list:
                            #if the ppt nr in the current ECG_RESULTS row is
                            #the same with the ppt nr in the infoperppt_list
                            if int(_ppt_nr) == e.p_nr:
                                epoch = row[_sc_epochname_col].split("_")[2]#length should be 3
                                if epoch == "prep":
                                    e.sc_prp = row[_sc_col]
                                elif epoch == "prep1":
                                    e.sc_prp1 = row[_sc_col]
                                elif epoch == "prep2":
                                    e.sc_prp2 = row[_sc_col]
                                elif epoch == "prep3":
                                    e.sc_prp3 = row[_sc_col]
                                elif epoch == "prep4":
                                    e.sc_prp4 = row[_sc_col]
                                elif epoch == "prep5":
                                    e.sc_prp5 = row[_sc_col]
                                elif epoch == "speech":
                                    e.sc_spc = row[_sc_col]
                                elif epoch == "speech1":
                                    e.sc_spc1 = row[_sc_col]
                                elif epoch == "speech2":
                                    e.sc_spc2 = row[_sc_col]
                                elif epoch == "speech3":
                                    e.sc_spc3 = row[_sc_col]
                                elif epoch == "speech4":
                                    e.sc_spc4 = row[_sc_col]
                                elif epoch == "speech5":
                                    e.sc_spc5 = row[_sc_col]
                                else:
                                    foo="bar"
                            else:
                                foo="bar"
                    else:
                        foo="bar"
            elif fn == "SKT_RESULTS.txt":
                skt_data = csv.reader(physiofile, delimiter='\t')
                for row in skt_data:
                    #only include rows that are not headers
                    if row[_skt_datasource_col] != _datasource:
                        _ppt_nr = get_pptnr_from_physio(row[_skt_datasource_col])
                        for e in infoperppt_list:
                            #if the ppt nr in the current ECG_RESULTS row is
                            #the same with the ppt nr in the infoperppt_list
                            if int(_ppt_nr) == e.p_nr:
                                epoch = row[_skt_epochname_col].split("_")[2]#length should be 3
                                if epoch == "prep":
                                    e.skt_prp = row[_skt_col]
                                elif epoch == "prep1":
                                    e.skt_prp1 = row[_skt_col]
                                elif epoch == "prep2":
                                    e.skt_prp2 = row[_skt_col]
                                elif epoch == "prep3":
                                    e.skt_prp3 = row[_skt_col]
                                elif epoch == "prep4":
                                    e.skt_prp4 = row[_skt_col]
                                elif epoch == "prep5":
                                    e.skt_prp5 = row[_skt_col]
                                elif epoch == "speech":
                                    e.skt_spc = row[_skt_col]
                                elif epoch == "speech1":
                                    e.skt_spc1 = row[_skt_col]
                                elif epoch == "speech2":
                                    e.skt_spc2 = row[_skt_col]
                                elif epoch == "speech3":
                                    e.skt_spc3 = row[_skt_col]
                                elif epoch == "speech4":
                                    e.skt_spc4 = row[_skt_col]
                                elif epoch == "speech5":
                                    e.skt_spc5 = row[_skt_col]
                                else:
                                    foo="bar"
                            else:
                                foo="bar"
                    else:
                        foo="bar"


#for e in infoperppt_list:
#    print(e.p_nr, e.sen_pre, e.tr_pre, e.sen_post, e.tr_post, e.apl, e.cp)

'''
Export the data
'''
outputsummaryfile = "./output/study3summary.csv"
sumheader = ['p_nr', 'age', 'sex', 'vaud_appr', 'vaud_size', 'vbl_fb', 'nonvbl_fb',\
             'prpsa', 'fpe', 'bfne',\
             'sen1_pre', 'sen2_pre', 'sen3_pre',\
             'tr1_pre', 'tr2_pre',\
             'hr_prp', 'hr_prp1', 'hr_prp2', 'hr_prp3', 'hr_prp4', 'hr_prp5',\
             'hr_spc', 'hr_spc1', 'hr_spc2', 'hr_spc3', 'hr_spc4', 'hr_spc5',\
             'sc_prp', 'sc_prp1', 'sc_prp2', 'sc_prp3', 'sc_prp4', 'sc_prp5',\
             'sc_spc', 'sc_spc1', 'sc_spc2', 'sc_spc3', 'sc_spc4', 'sc_spc5',\
             'skt_prp', 'skt_prp1', 'skt_prp2', 'skt_prp3', 'skt_prp4', 'skt_prp5',\
             'skt_spc', 'skt_spc1', 'skt_spc2', 'skt_spc3', 'skt_spc4', 'skt_spc5',\
             'sen1_post', 'sen2_post', 'sen3_post',\
             'tr1_post', 'tr2_post',\
             'apl1','apl2', 'apl3', 'apl4',\
             'cp1', 'cp2', 'cp3_rev', 'cp4', 'cp5_rev', 'cp_mean',\
             'hrv_prp', 'hrv_prp1', 'hrv_prp2', 'hrv_prp3', 'hrv_prp4', 'hrv_prp5',\
             'hrv_spc', 'hrv_spc1', 'hrv_spc2', 'hrv_spc3', 'hrv_spc4', 'hrv_spc5']
with open(outputsummaryfile, 'w', newline='') as sumfile:    
    writersum = csv.DictWriter(sumfile, fieldnames = sumheader)
    writersum.writeheader()
    
for e in infoperppt_list:
    print("Exporting data P", e.p_nr)
    with open(outputsummaryfile, 'a', newline='') as sumfile:    
        writersum = csv.DictWriter(sumfile, fieldnames = sumheader)
        writersum.writerow({\
                    'p_nr': e.p_nr,
                    'age': e.age,
                    'sex': e.sex,
                    'vaud_appr': e.vaud_appr,
                    'vaud_size': e.vaud_size,
                    'vbl_fb': e.vbl_fb,
                    'nonvbl_fb': e.nonvbl_fb,
                    'prpsa': e.prpsa, 
                    'fpe': e.fpe, 
                    'bfne': e.bfne,
                    'sen1_pre': e.sen_pre[0], 
                    'sen2_pre': e.sen_pre[1], 
                    'sen3_pre': e.sen_pre[2],
                    'tr1_pre': e.tr_pre[0], 
                    'tr2_pre': e.tr_pre[1],
                    'hr_prp': e.hr_prp,
                    'hr_prp1': e.hr_prp1,
                    'hr_prp2': e.hr_prp2,
                    'hr_prp3': e.hr_prp3,
                    'hr_prp4': e.hr_prp4,
                    'hr_prp5': e.hr_prp5,
                    'hr_spc': e.hr_spc,
                    'hr_spc1': e.hr_spc1,
                    'hr_spc2': e.hr_spc2,
                    'hr_spc3': e.hr_spc3,
                    'hr_spc4': e.hr_spc4,
                    'hr_spc5': e.hr_spc5,
                    'sc_prp': e.sc_prp,
                    'sc_prp1': e.sc_prp1,
                    'sc_prp2': e.sc_prp2,
                    'sc_prp3': e.sc_prp3,
                    'sc_prp4': e.sc_prp4,
                    'sc_prp5': e.sc_prp5,
                    'sc_spc': e.sc_spc,
                    'sc_spc1': e.sc_spc1,
                    'sc_spc2': e.sc_spc2,
                    'sc_spc3': e.sc_spc3,
                    'sc_spc4': e.sc_spc4,
                    'sc_spc5': e.sc_spc5,
                    'skt_prp': e.skt_prp,
                    'skt_prp1': e.skt_prp1,
                    'skt_prp2': e.skt_prp2,
                    'skt_prp3': e.skt_prp3,
                    'skt_prp4': e.skt_prp4,
                    'skt_prp5': e.skt_prp5,
                    'skt_spc': e.skt_spc,
                    'skt_spc1': e.skt_spc1,
                    'skt_spc2': e.skt_spc2,
                    'skt_spc3': e.skt_spc3,
                    'skt_spc4': e.skt_spc4,
                    'skt_spc5': e.skt_spc5,
                    'sen1_post': e.sen_post[0],
                    'sen2_post': e.sen_post[1],
                    'sen3_post': e.sen_post[2],
                    'tr1_post': e.tr_post[0],
                    'tr2_post': e.tr_post[1],
                    'apl1': e.apl[0],
                    'apl2': e.apl[1],
                    'apl3': e.apl[2],
                    'apl4': e.apl[3],
                    'cp1': e.cp[0],
                    'cp2': e.cp[1],
                    'cp3_rev': e.cp[2],
                    'cp4': e.cp[3],
                    'cp5_rev': e.cp[4],
                    'cp_mean': e.cp[5],
                    'hrv_prp': e.hrv_prp,
                    'hrv_prp1': e.hrv_prp1,
                    'hrv_prp2': e.hrv_prp2,
                    'hrv_prp3': e.hrv_prp3,
                    'hrv_prp4': e.hrv_prp4,
                    'hrv_prp5': e.hrv_prp5,
                    'hrv_spc': e.hrv_spc,
                    'hrv_spc1': e.hrv_spc1,
                    'hrv_spc2': e.hrv_spc2,
                    'hrv_spc3': e.hrv_spc3,
                    'hrv_spc4': e.hrv_spc4,
                    'hrv_spc5': e.hrv_spc5
                    })