# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 17:50:53 2021

@author: ipekh
"""
class aminoacid:
    def __init__(this, str):
        this.fulltext = str
        s1 = str.split('-')
        this.acceptor = s1[0]
        this.donor = s1[1]
        this.hydrogenAtomType = s1[2]
        s2 = this.acceptor.split('_')
        this.acceptorType = s2[0]
        this.acceptorIndex = s2[1].split('@')[0]
        this.acceptorAtom = s2[1].split('@')[1]
        s3 = this.donor.split('_')
        this.donorType = s3[0]
        this.donorIndex = s3[1].split('@')[0]
        this.donorAtom = s3[1].split('@')[1]
        this.frame = 0
        
    def addFrame(this):
        this.frame += 1
        
    def frac(this):
        return this.frame/200
    
    def getDonorH(this):
        return this.donor.split('@')[0] + '@' + this.hydrogenAtomType
        


class hbond_reader:
    def __init__(this, path):
        this.filename = path
        this.aminoacids = dict()
        this.rowFrame = dict()
        this.createAminos()
    
    def Write_Avghbond(this):
        #This method should calculate statistics for each hbond and write the “avghbond.dat” except for the
        #last two column.
        acceptors = list()
        donors = list()
        hdonors = list()
        frames = list()
        frac = list()
        orderedList = sorted(list(this.aminoacids.values()), key=lambda x: x.frame, reverse=True)
        for y in orderedList:
            acceptors.append(str(y.acceptor))
            donors.append(str(y.donor))
            hdonors.append(str(y.getDonorH()))
            frames.append(str(y.frame))
            frac.append(y.frac())
        data = {'Acceptor':acceptors, 'DonorH':hdonors, 'Donor':donors, 'Frames':frames, 'Frac':frac}
        from pandas import DataFrame
        df = DataFrame(data)
        df.to_csv("avghbond.dat", sep='\t', columns= ['Acceptor', 'DonorH', 'Donor', 'Frames', 'Frac'], encoding='utf-8', header=True)
        
    def Write_hbondnumber(this):
        #This method should calculate total number of hbonds in each time frame and writes
        #“hbond_number_tseries.dat” file .
        from collections import OrderedDict
        od = OrderedDict(sorted(this.rowFrame.items()))
        data = {'Frame':od.keys(), 'Total Number of Hbonds':od.values()}
        from pandas import DataFrame
        df = DataFrame(data)
        df.to_csv("hbond_number_tseries.dat", sep='\t', encoding='utf-8', header=True, index=False)
        
    def Check_intraaminoacid(this):
        #This methods should check if any hbond forms between the atoms of the same amino acid
        #index and prints these hbonds and number of frames that these hbonds forms. If the method
        #does not find any of this type hbonds, it should print “no intra amino acid hbond found”.
        #To do this, basically you need to find hbonds that have the same DonorAminoasitIndex and
        #AcceptorAminoasitIndex.
        flag = False
        for x in this.aminoacids.values():
            if x.acceptorIndex == x.donorIndex:
                print(x.acceptorType, "with index :", x.acceptorIndex, " has",  x.frame, "number of frames :")
                flag = True
        if flag == False:
            print("no intra amino acid hbond found")
        
    def Find_highest_donortype(this):
        #This method should find the amino acid type that gives the highest number of hbond donor.
        donorDict = dict()
        for x in list(this.aminoacids.values()):
            if x.donorType in donorDict:
                val = donorDict[x.donorType] + 1
                donorDict[x.donorType] = val
            else:
                donorDict[x.donorType] = 1
        from collections import Counter
        k = Counter(donorDict)
        high = k.most_common(1)
        print("amino acid type that gives the highest number of hbond donor is", high[0][0])
                
        
    def createAminos(this):
        from pandas import read_csv
        
        data = read_csv(this.filename, header=0, delim_whitespace=True)
        header = list(data.columns.values)
        for i, val in enumerate(header):
            if i != 0:
                aa = aminoacid(val)
                this.aminoacids[i] = aa
                
        ix=1
        for index, row in data.iterrows():
            totalFrame = 0
            for i, val in enumerate(list(row)):
                totalFrame += int(val)
                if i != 0:
                    aa = this.aminoacids[i]
                    if val == 1:
                        aa.addFrame()
                    this.aminoacids[i] = aa
            this.rowFrame[ix]=totalFrame
            ix += 1
                    
hbond = hbond_reader("C:\\Users\\ipekh\\Desktop\\Big Data Homeworks\\Advances in Data Science\\midterm_data\\allhbond.dat")
hbond.Write_Avghbond()
hbond.Write_hbondnumber()
hbond.Check_intraaminoacid()
hbond.Find_highest_donortype()