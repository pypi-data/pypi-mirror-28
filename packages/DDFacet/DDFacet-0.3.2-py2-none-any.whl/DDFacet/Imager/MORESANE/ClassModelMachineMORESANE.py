'''
DDFacet, a facet-based radio imaging package
Copyright (C) 2013-2016  Cyril Tasse, l'Observatoire de Paris,
SKA South Africa, Rhodes University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import numpy as np
from DDFacet.Other import MyLogger
from DDFacet.Other import ClassTimeIt
from DDFacet.Other import ModColor
log=MyLogger.getLogger("ClassModelMachineMoresane")
from DDFacet.Array import NpParallel
from DDFacet.Array import ModLinAlg
from DDFacet.ToolsDir import ModFFTW
from DDFacet.ToolsDir import ModToolBox
from DDFacet.Other import ClassTimeIt
from DDFacet.Other import MyPickle
from DDFacet.Other import reformat

from DDFacet.ToolsDir.GiveEdges import GiveEdges
from DDFacet.Imager import ClassModelMachine as ClassModelMachinebase
from DDFacet.ToolsDir import ModFFTW
import scipy.ndimage
from SkyModel.Sky import ModRegFile
from pyrap.images import image
from SkyModel.Sky import ClassSM
import os

class ClassModelMachine(ClassModelMachinebase.ClassModelMachine):
    def __init__(self,*args,**kwargs):
        ClassModelMachinebase.ClassModelMachine.__init__(self, *args, **kwargs)
        # self.GD=GD
        # if Gain is None:
        #     self.Gain=self.GD["Deconv"]["Gain"]
        # else:
        #     self.Gain=Gain
        # self.GainMachine=GainMachine
        # self.DicoSMStacked={}
        # self.DicoSMStacked["Comp"]={}
        if self.GD is not None:
            self.SolveParam = self.GD["MORESANE"]["MOSolvePars"]
            print>>log,"Solved parameters: %s"%(str(self.SolveParam))
            self.NParam=len(self.SolveParam)
        

    def setRefFreq(self,RefFreq): # ,AllFreqs):
        self.RefFreq=RefFreq
        self.DicoSMStacked["RefFreq"]=RefFreq
#        self.DicoSMStacked["AllFreqs"]=np.array(AllFreqs)
        # print "ModelMachine:",self.RefFreq, self.DicoSMStacked["RefFreq"], self.DicoSMStacked["AllFreqs"]



    def ToFile(self,FileName,DicoIn=None):
        print>>log, "Saving dico model to %s"%FileName
        if DicoIn is None:
            D=self.DicoSMStacked
        else:
            D=DicoIn

        #D["PM"]=self.PM
        D["ModelShape"]=self.ModelShape
        D["Type"]="GA"  # WILL CHANGE WHEN REFACTORING MODELMACHINE
        D["SolveParam"]=self.SolveParam

        MyPickle.Save(D,FileName)


    def FromFile(self,FileName):
        print>>log, "Reading dico model from %s"%FileName
        self.DicoSMStacked=MyPickle.Load(FileName)
        self.FromDico(self.DicoSMStacked)


    def FromDico(self,DicoSMStacked):
        #self.PM=self.DicoSMStacked["PM"]
        self.DicoSMStacked=DicoSMStacked
        self.RefFreq=self.DicoSMStacked["RefFreq"]
        self.ModelShape=self.DicoSMStacked["ModelShape"]
        try:
            self.SolveParam=self.DicoSMStacked["SolveParam"]
        except:
            print>>log, "SolveParam is not in the keyword lists of DicoSMStacked"
            print>>log, "  setting SolveParam to [S]"
            self.SolveParam=["S"]
            
        self.NParam=len(self.SolveParam)

    def setModelShape(self,ModelShape):
        self.ModelShape=ModelShape

    def setThreshold(self,Th):
        self.Th=Th

        
    def GiveIndividual(self,ListPixParms):
        NParms=self.NParam
        OutArr=np.zeros((NParms,len(ListPixParms)),np.float32)
        DicoComp=self.DicoSMStacked["Comp"]

        for iPix in range(len(ListPixParms)):
            x,y=ListPixParms[iPix]

            xy=x,y
            try:
                Vals=DicoComp[xy]["Vals"][0]
                OutArr[:,iPix]=Vals[:]
                del(DicoComp[xy])
            except:
                pass

        return OutArr.flatten()


    def AppendIsland(self,ListPixParms,V,JonesNorm=None):
        ListPix=ListPixParms
        Vr=V.reshape((self.NParam,V.size/self.NParam))
        NPixListParms=len(ListPixParms)

        
        #S=self.PM.ArrayToSubArray(V,Type="S")

        #S[np.abs(S)<self.Th]=0
        #S-=self.Th*np.sign(S)
        SolveParam=np.array(self.SolveParam)
        iS=np.where(SolveParam=="S")[0][0]
        S=Vr[iS]
        #S*=self.GainMachine.GiveGain()

        if JonesNorm is not None:
            Vr[iS,:]/=np.sqrt(JonesNorm).flat[0]

        for (x,y),iComp in zip(ListPix,range(NPixListParms)):
            if S[iComp]==0: continue
            Vals=np.array(Vr[:,iComp]).copy()
            self.AppendComponentToDictStacked((x,y),Vals)


    def AppendComponentToDictStacked(self,key,Vals):
        DicoComp=self.DicoSMStacked["Comp"]

        try:
            DicoComp[key]["Vals"].append(Vals)
        except:
            DicoComp[key]={}
            DicoComp[key]["Vals"]=[]
            DicoComp[key]["Vals"].append(Vals)


    def GiveModelImage(self,FreqIn=None):

        RefFreq=self.DicoSMStacked["RefFreq"]
        if FreqIn is None:
            FreqIn=np.array([RefFreq])

        #if type(FreqIn)==float:
        #    FreqIn=np.array([FreqIn]).flatten()
        #if type(FreqIn)==np.ndarray:

        FreqIn=np.array([FreqIn.ravel()]).flatten()


        # print "ModelMachine GiveModelImage:",FreqIn, RefFreq



        DicoComp=self.DicoSMStacked["Comp"]
        _,npol,nx,ny=self.ModelShape
        N0=nx

        nchan=FreqIn.size
        ModelImage=np.zeros((nchan,npol,nx,ny),dtype=np.float32)
        DicoSM={}
        SolveParam=np.array(self.SolveParam)
        for x,y in DicoComp.keys():
            ListSols=DicoComp[(x,y)]["Vals"]#/self.DicoSMStacked[key]["SumWeights"]

            for iSol in range(len(ListSols)):
                ThisSol=ListSols[iSol]

                #print>>log,((x,y),iSol,ThisSol)

                iS=np.where(SolveParam=="S")[0]
                S=ThisSol[iS]
                
                ThisAlpha=0
                iAlpha=np.where(SolveParam=="Alpha")[0]
                if iAlpha.size!=0:
                    ThisAlpha=ThisSol[iAlpha]

                for ch in range(nchan):
                    Flux=S*(FreqIn[ch]/RefFreq)**(ThisAlpha)

                    for pol in range(npol):
                        ModelImage[ch,pol,x,y]+=Flux
                    
        # vmin,vmax=np.min(self._MeanDirtyOrig[0,0]),np.max(self._MeanDirtyOrig[0,0])
        # vmin,vmax=-1,1
        # #vmin,vmax=np.min(ModelImage),np.max(ModelImage)
        # pylab.clf()
        # ax=pylab.subplot(1,3,1)
        # pylab.imshow(self._MeanDirtyOrig[0,0],interpolation="nearest",vmin=vmin,vmax=vmax)
        # pylab.subplot(1,3,2,sharex=ax,sharey=ax)
        # pylab.imshow(self._MeanDirty[0,0],interpolation="nearest",vmin=vmin,vmax=vmax)
        # pylab.colorbar()
        # pylab.subplot(1,3,3,sharex=ax,sharey=ax)
        # pylab.imshow( ModelImage[0,0],interpolation="nearest",vmin=vmin,vmax=vmax)
        # pylab.colorbar()
        # pylab.draw()
        # pylab.show(False)
        # print np.max(ModelImage[0,0])
        # # stop

 
        return ModelImage
        

        
    def setListComponants(self,ListScales):
        self.ListScales=ListScales




    def GiveSpectralIndexMap(self,CellSizeRad=1.,GaussPars=[(1,1,0)],DoConv=True):

        
        dFreq=1e6
        f0=self.DicoSMStacked["AllFreqs"].min()
        f1=self.DicoSMStacked["AllFreqs"].max()
        M0=self.GiveModelImage(f0)
        M1=self.GiveModelImage(f1)
        if DoConv:
            M0=ModFFTW.ConvolveGaussian(M0,CellSizeRad=CellSizeRad,GaussPars=GaussPars)
            M1=ModFFTW.ConvolveGaussian(M1,CellSizeRad=CellSizeRad,GaussPars=GaussPars)
        
        Np=1000
        indx,indy=np.int64(np.random.rand(Np)*M0.shape[0]),np.int64(np.random.rand(Np)*M0.shape[1])
        med=np.median(np.abs(M0[:,:,indx,indy]))

        Mask=((M1>100*med)&(M0>100*med))
        alpha=np.zeros_like(M0)
        alpha[Mask]=(np.log(M0[Mask])-np.log(M1[Mask]))/(np.log(f0/f1))
        return alpha

        
    def CleanNegComponants(self,box=20,sig=3,RemoveNeg=True):
        print>>log, "Cleaning model dictionary from negative components with (box, sig) = (%i, %i)"%(box,sig)
        ModelImage=self.GiveModelImage(self.DicoSMStacked["RefFreq"])[0,0]
        
        Min=scipy.ndimage.filters.minimum_filter(ModelImage,(box,box))
        Min[Min>0]=0
        Min=-Min

        if RemoveNeg==False:
            Lx,Ly=np.where((ModelImage<sig*Min)&(ModelImage!=0))
        else:
            print>>log, "  Removing neg components too"
            Lx,Ly=np.where( ((ModelImage<sig*Min)&(ModelImage!=0)) | (ModelImage<0))

        for icomp in range(Lx.size):
            key=Lx[icomp],Ly[icomp]
            try:
                del(self.DicoSMStacked["Comp"][key])
            except:
                print>>log, "  Component at (%i, %i) not in dict "%key

    def CleanMaskedComponants(self,MaskName):
        print>>log, "Cleaning model dictionary from masked components using %s"%(MaskName)
        im=image(MaskName)
        MaskArray=im.getdata()[0,0].T[::-1]
        for (x,y) in self.DicoSMStacked["Comp"].keys():
            if MaskArray[x,y]==0:
                del(self.DicoSMStacked["Comp"][(x,y)])

    def ToNPYModel(self,FitsFile,SkyModel,BeamImage=None):
        #R=ModRegFile.RegToNp(PreCluster)
        #R.Read()
        #R.Cluster()
        #PreClusterCat=R.CatSel
        #ExcludeCat=R.CatExclude


        AlphaMap=self.GiveSpectralIndexMap(DoConv=False)
        ModelMap=self.GiveModelImage()
        nch,npol,_,_=ModelMap.shape

        for ch in range(nch):
            for pol in range(npol):
                ModelMap[ch,pol]=ModelMap[ch,pol][::-1]#.T
                AlphaMap[ch,pol]=AlphaMap[ch,pol][::-1]#.T

        if BeamImage is not None:
            ModelMap*=(BeamImage)


        im=image(FitsFile)
        pol,freq,decc,rac=im.toworld((0,0,0,0))

        Lx,Ly=np.where(ModelMap[0,0]!=0)
        
        X=np.array(Lx)
        Y=np.array(Ly)

        #pol,freq,decc1,rac1=im.toworld((0,0,1,0))
        dx=abs(im.coordinates().dict()["direction0"]["cdelt"][0])

        SourceCat=np.zeros((X.size,),dtype=[('Name','|S200'),('ra',np.float),('dec',np.float),('Sref',np.float),('I',np.float),('Q',np.float),\
                                           ('U',np.float),('V',np.float),('RefFreq',np.float),('alpha',np.float),('ESref',np.float),\
                                           ('Ealpha',np.float),('kill',np.int),('Cluster',np.int),('Type',np.int),('Gmin',np.float),\
                                           ('Gmaj',np.float),('Gangle',np.float),("Select",np.int),('l',np.float),('m',np.float),("Exclude",bool),
                                           ("X",np.int32),("Y",np.int32)])
        SourceCat=SourceCat.view(np.recarray)

        IndSource=0

        SourceCat.RefFreq[:]=self.DicoSMStacked["RefFreq"]
        _,_,nx,ny=ModelMap.shape
        
        for iSource in range(X.shape[0]):
            x_iSource,y_iSource=X[iSource],Y[iSource]
            _,_,dec_iSource,ra_iSource=im.toworld((0,0,y_iSource,x_iSource))
            SourceCat.ra[iSource]=ra_iSource
            SourceCat.dec[iSource]=dec_iSource
            SourceCat.X[iSource]=(nx-1)-X[iSource]
            SourceCat.Y[iSource]=Y[iSource]
            
            #print self.DicoSMStacked["Comp"][(SourceCat.X[iSource],SourceCat.Y[iSource])]
            # SourceCat.Cluster[IndSource]=iCluster
            Flux=ModelMap[0,0,x_iSource,y_iSource]
            Alpha=AlphaMap[0,0,x_iSource,y_iSource]
            # print iSource,"/",X.shape[0],":",x_iSource,y_iSource,Flux,Alpha
            SourceCat.I[iSource]=Flux
            SourceCat.alpha[iSource]=Alpha


        SourceCat=(SourceCat[SourceCat.ra!=0]).copy()
        np.save(SkyModel,SourceCat)
        self.AnalyticSourceCat=ClassSM.ClassSM(SkyModel)

    def DelAllComp(self):
        for key in self.DicoSMStacked["Comp"].keys():
            del(self.DicoSMStacked["Comp"][key])


    def PutBackSubsComps(self):
        #if self.GD["Data"]["RestoreDico"] is None: return

        SolsFile=self.GD["DDESolutions"]["DDSols"]
        if not(".npz" in SolsFile):
            Method=SolsFile
            ThisMSName=reformat.reformat(os.path.abspath(self.GD["Data"]["MS"]),LastSlash=False)
            SolsFile="%s/killMS.%s.sols.npz"%(ThisMSName,Method)
        DicoSolsFile=np.load(SolsFile)
        SourceCat=DicoSolsFile["SourceCatSub"]
        SourceCat=SourceCat.view(np.recarray)
        #RestoreDico=self.GD["Data"]["RestoreDico"]
        RestoreDico=DicoSolsFile["ModelName"][()][0:-4]+".DicoModel"
        
        print>>log, "Adding previously subtracted components"
        ModelMachine0=ClassModelMachine(self.GD)

        
        ModelMachine0.FromFile(RestoreDico)

        

        _,_,nx0,ny0=ModelMachine0.DicoSMStacked["ModelShape"]
        
        _,_,nx1,ny1=self.ModelShape
        dx=nx1-nx0

        

        for iSource in range(SourceCat.shape[0]):
            x0=SourceCat.X[iSource]
            y0=SourceCat.Y[iSource]
            
            x1=x0+dx
            y1=y0+dx
            
            if not((x1,y1) in self.DicoSMStacked["Comp"].keys()):
                self.DicoSMStacked["Comp"][(x1,y1)]=ModelMachine0.DicoSMStacked["Comp"][(x0,y0)]
            else:
                self.DicoSMStacked["Comp"][(x1,y1)]+=ModelMachine0.DicoSMStacked["Comp"][(x0,y0)]
                
