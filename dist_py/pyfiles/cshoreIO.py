import os
import numpy as np
from vfall import vfall_calc

"""
prepared primarily by Spicer Bak and David Young (i believe)
minor modifications by Dylan R. Sanderson (drs)
"""


vf = vfall_calc()

class cshoreIO(object):
    """This class takes care of CSHORE model input and output scripts"""
    def __init__(self):
        """
        This is the class iniation which initalizes the reading dictionaries
        """
        self.ODOC_dict = {}
        self.readIF_dict = {}
        self.OBPROF_dict = {}
        self.OSETUP_dict = {}
        self.meta_dict = {}

    def make_CSHORE_infile(self, fname, BC_dict, meta_dict, cshore_dict):
        """This function creates the input file for CSHORE model

        :param fname: name of the CSHORE infile we are writing
        :param in_dict: header - header for the CHSORE inflile
            :key iline:  single line (I have no idea what this is)
            :key iprofl: toggle to run morphology (0 = no morph, 1 = morph)
            :key isedav:  0 = unlimited sand, 1 = hard bottom
            :key iperm:  0 = no permeability, 1 = permeable
            :key iover:  0 = no overtopping , 1 = include overtopping
            :key iwtran:  0 = no standing water landward of crest, 1 = wave transmission due to overtopping
            :key ipond:  0 = no ponding seaward of SWL
            :key infilt:  1 = include infiltration landward of dune crest
            :key iwcint: 0 = no W & C interaction , 1 = include W & C interaction
            :key iroll: - 0 = no roller, 1 = roller
            :key iwind: - 0 = no wind effect'
            :key itide: - 0 = no tidal effect on currents
            :key iveg: - 1 = include vegitation effect (I'm assuming)
            :key iclay: - this parameter is NOT specified in Brad's run_model, so the code will break if it gets here
            :key dxc: - profile node spacing constant dx
            :key gamma: - shallow water ratio of wave height to water depth (wave breaking parameter?)
            :key d50: - d_50 in mm
            :key wf: - fall velocity of sand grain
            :key sg: - specific gravity of the sand grains
            :key effb: - suspension efficiency due to breaking eB (what is this?)
            :key efff: - suspension efficiency due to friction ef (what is this?)
            :key slp: - suspended load parameter (what is this?)
            :key slpot: - overtopping suspended load parameter (what is this?)
            :key tanphi: - tangent (sediment friction angle - units?)
            :key blp: - bedload parameter (what is this?)
            :key rwh: - numerical rununp wire height (what is this? units?)
            :key ilab: - controls the boundary condition timing. Don't change
            :key nwave: - number of wave time-steps
            :key nsurge: - this ostensibly is the number of water level time steps, but is always set equal to nwave...
            :key timebc_wave: - time-steps of the model in seconds elapsed since model start
            :key Tp: - spectral peak period of the waves at each BC time-step
            :key Hs: - WE ARE USING Hmo NOT Hrms!!!! wave height in m              ------------------- @David
            :key Wsetup: - wave setup in m (hard coded to be 0 at all BC time-steps)
            :key swlbc: - still? water level at the boundary (in m?)
            :key angle: - peak wave angle on the wave energy spectra at each time step (degrees?)
            :key NBINP: - number of bathy profile nodes
            :key NPINP: - I think this is for if we are running with permeable bottom?  Brad doesn't specify this in his run_model script, so it will crash if it gets to here...
            :key x: - x-positions of each node (0 at boundary + as move onshore in FRF coord Units - m?)
            :key zb: - (initial?) bed elevation of each node in survey units (m?)
            :key fw: - bed friction at every node (what friction model is this?!?!? ask Brad??!?!)
            :key x_p: - x for permeable bottom?  Brad doesn't specify this in his run_model script, so it will crash if it gets to here...
            :key zb_p: - elevation for permeable bottom? Brad doesn't specify this in his run_model script, so it will crash if it gets to here...
            :key veg_Cd: - vegetation drag coefficient (what model for drag)
            :key veg_n: - vegetation density (units?!?!?!?!)
            :key veg_dia: - vegetation dia. (units ??!?!?!?!?)
            :key veg_ht: - vegetation height (units?!?!?!?!)
            :key veg_rod: - vegitation erosion limit below sand for failure (what is this?!?!?)
        :param BC_dict:
            :key
            :key
        :param meta_dict: 
            :key
            :key

        :return will save meta data into a pickel for post processing

        """

        # version toggle stuff
        # meta_dict['version'] = 'MOBILE'
        # if meta_dict['version'] == 'FIXED':
        # 	morph = 0
        # elif meta_dict['version'] == 'MOBILE':
        # 	morph = 1
        # elif meta_dict['version'] == 'MOBILE_RESET':
        # 	morph = 1
        # else:
        # 	pass

        in_dict = {'header': ['------------------------------------------------------------',
                              'Reach : %s  Profile : %s  Storm:  %s'  %(meta_dict['Reach'], meta_dict['Profile'], meta_dict['Storm']),
                              '------------------------------------------------------------'],			# the three lines of the header for the input text file
                   'iline': 1,  # single line
                   'iprofl': 1.1,  # 0 = no morph, 1 = run morph
                   'isedav': 0,  # 0 = unlimited sand, 1 = hard bottom
                   'iperm': 0,  # 0 = no permeability, 1 = permeable
                   'iover': 1,  # 0 = no overtopping , 1 = include overtopping
                   'infilt': 0,  # 1 = include infiltration landward of dune crest
                   'iwtran': 0,  # 0 = no standing water landward of crest, 1 = wave transmission due to overtopping
                  
                   'ipond': 0,  # 0 = no ponding seaward of SWL
                   'iwcint': 0,  # 0 = no W & C interaction , 1 = include W & C interaction
                   'iroll': 0,  # 0 = no roller, 1 = roller
                   'iwind': 0,  # 0 = no wind effect'
                   'itide': 0,  # 0 = no tidal effect on currents
                   'iveg': 0,  # 1 = include vegitation effect (I'm assuming)
                   'dx': cshore_dict['dx'],  # constant dx

                   'gamma': cshore_dict['gamma'], # shallow water ratio of wave height to water depth (wave breaking parameter?)
                   'sporo': 0.4,  # sediment porosity
                   'sg': 2.65,  # specific gravity of the sand grains (I changed the order so I could use this in the fall velocity calculator)
                   'temp' : 20,	#water temperature (deg. C)
                   'salin': 0,	#salinity (ppt)

                   'veg_Cd': 1,  # vegitation drag coeff
                   'veg_n': 100,  # vegitation density (units?)
                   'veg_dia': .01,  # vegitation diam (units? mean or median?)
                   'veg_ht': .20,  # vegitation height (units? mean or median?)
                   'veg_rod': .1,  # vegitation erosion limit below sand for failure (what is this?!?!?)
                   'veg_extent': np.array([.7, 1]),  # vegitation coverage as fraction of total domain length (what is this?!?!?)

                   
                   'effb': cshore_dict['effb'],  # suspension efficiency due to breaking eB (what is this?)
                   'efff': 0.005,  # suspension efficiency due to friction ef (what is this?)
                   'slp': .5,  # suspended load parameter (what is this?)
                   'slpot': .1,  # overtopping suspended load parameter (what is this?)
                   'tanphi': .630,  # tangent (sediment friction angle - units?)
                   'blp': 0.001,  # bedload parameter (what is this?)
                   'rwh': .02,  # numerical rununp wire height (what is this? units?)
                   'ilab': 0,  # controls the boundary condition timing. Don't change - supposed to be 0!!!
                   'fw': 0.015}  # bottom friction factor

        in_dict['d50'] = BC_dict['d50']		#d50 in mm
        # in_dict['wf'] = dirtLib.vfall(in_dict['d50'], BC_dict['temp'], BC_dict['salin'], in_dict['sg'])  # fall velocity of sand grain
        in_dict['wf'] = vf.init(in_dict['d50'], in_dict['temp'], in_dict['salin'])	  # note: drs added this; fall velocity of sand grain 
        in_dict['timebc_wave'] = BC_dict['timebc_wave']
        in_dict['timebc_surg'] = in_dict['timebc_wave']  # what is this?  Why is it a separate variable?
        in_dict['nwave'] = len(in_dict['timebc_wave'])  # what is this? this is just the number of time steps I have?!?!?
        in_dict['nsurg'] = in_dict['nwave']  # what is this?  Why is it a separate variable
        # open file with write privilages
        fid = open(fname, 'w')
        # begin Writing file
        fid.write('%i \n' %len(in_dict['header']))

        for ii in range(0, len(in_dict['header'])):
            fid.write('%s \n' %in_dict['header'][ii])

        fid.write('%-8i                                  ->ILINE\n' % in_dict['iline'])
        #fid.write('%-8i                                  ->IPROFL\n' % in_dict['iprofl'])
        fid.write('%s                                       ->IPROFL\n' % in_dict['iprofl'])


        #if in_dict['iprofl'] == 1:
        if np.floor(in_dict['iprofl']) == 1:
            fid.write('%-8i                                  ->ISEDAV\n' % in_dict['isedav'])
        else:
            pass

        fid.write('%-8i                                  ->IPERM\n' % in_dict['iperm'])
        fid.write('%-8i                                  ->IOVER\n' % in_dict['iover'])

        if in_dict['iover']:
            fid.write('%-8i                                  ->IWTRAN\n' % in_dict['iwtran'])
            if in_dict['iwtran'] == 0:
                fid.write('%-8i                                  ->IPOND\n' % in_dict['ipond'])
            else:
                pass
        else:
            pass

        if in_dict['iover'] == 1 and in_dict['iperm'] == 0 and np.floor(in_dict['iprofl']) == 1:
            fid.write('%-8i                                  ->INFILT\n' % in_dict['infilt'])
        else:
            pass

        fid.write('%-8i                                  ->IWCINT\n' % in_dict['iwcint'])
        fid.write('%-8i                                  ->IROLL \n' % in_dict['iroll'])
        fid.write('%-8i                                  ->IWIND \n' % in_dict['iwind'])
        fid.write('%-8i                                  ->ITIDE \n' % in_dict['itide'])
        fid.write('%-8i                                  ->IVEG  \n' % in_dict['iveg'])

        if in_dict['isedav'] == 1 and in_dict['iperm'] == 0 and in_dict['iveg'] == 0:
            fid.write('%-8i                                  ->ICLAY  \n' % in_dict['iclay']) # this parameter is not specified in Brad's run_model...  This will crash if these conditions are met
        else:
            pass

        fid.write('%11.4f                                ->DXC\n' % in_dict['dx'])
        fid.write('%11.4f                                ->GAMMA \n' % in_dict['gamma'])

        if np.floor(in_dict['iprofl']) == 1:
            fid.write('%11.4f%11.4f%11.4f         ->D50 WF SG\n' % (in_dict['d50'], in_dict['wf'], in_dict['sg']))
            fid.write('%11.4f%11.4f%11.4f%11.4f              ->EFFB EFFF SLP\n' % (in_dict['effb'], in_dict['efff'], in_dict['slp'], in_dict['slpot']))
            fid.write('%11.4f%11.4f                    ->TANPHI BLP\n' % (in_dict['tanphi'], in_dict['blp']))
        else:
            pass

        if in_dict['iover']:
            fid.write('%11.4f                               ->RWH \n' % in_dict['rwh'])
        else:
            pass

        fid.write('%-8i                                  ->ILAB\n' % in_dict['ilab'])

        if in_dict['ilab'] == 1:
            fid.write('%-8i                                  ->NWAVE \n' % in_dict['nwave'])
            fid.write('%-8i                                  ->NSURGE \n' % in_dict['nsurg'])
            for ii in range(0, len(BC_dict['Hs'])):
                # fid.write('%11.2f%11.4f%11.4f%11.4f%11.4f%11.4f\n' % (BC_dict['timebc_wave'][ii], BC_dict['Tp'][ii], (np.sqrt(2)/2.0)*BC_dict['Hs'][ii], BC_dict['Wsetup'][ii], BC_dict['swlbc'][ii], BC_dict['angle'][ii]))
                fid.write('%11.2f%11.4f%11.4f%11.4f%11.4f%11.4f\n' % (BC_dict['timebc_wave'][ii], BC_dict['Tp'][ii], BC_dict['Hrms'][ii], BC_dict['Wsetup'][ii], BC_dict['swlbc'][ii], BC_dict['angle'][ii])) #note: drs modified this to read Hrms
        else:
            fid.write('%-8i                                  ->NWAVE \n' %int(in_dict['nwave']-1))
            fid.write('%-8i                                  ->NSURGE \n' %int(in_dict['nsurg']-1))
            for ii in range(0, len(BC_dict['Hs'])):
                # fid.write('%11.2f%11.4f%11.4f%11.4f\n' % (BC_dict['timebc_wave'][ii], BC_dict['Tp'][ii], (np.sqrt(2)/2.0)*BC_dict['Hs'][ii], BC_dict['angle'][ii]))
                fid.write('%11.2f%11.4f%11.4f%11.4f\n' % (BC_dict['timebc_wave'][ii], BC_dict['Tp'][ii], BC_dict['Hrms'][ii], BC_dict['angle'][ii]))	#note: drs modified this to read Hrms
            for ii in range(0, len(BC_dict['swlbc'])):
                fid.write('%11.2f%11.4f\n' %(in_dict['timebc_surg'][ii], BC_dict['swlbc'][ii]))


            #interp zb to cshore grid to remain consistent with matlab scripting bdj 2019-12-05 
            x = BC_dict['x']
            x = np.arange(x[0], x[-1], cshore_dict['dx']).tolist()    # Using np.arange truncates the value at x[-1]  TMS 2021-10-19
            zb = np.interp(x,BC_dict['x'],BC_dict['zb'])
            # now writethe bottom position
            #fid.write('%-8i                             ->NBINP \n' % len(BC_dict['x'])) superceded bdj 2019-12-05 
            fid.write('%-8i                             ->NBINP \n' % len(x))

        if in_dict['iperm'] == 1 or in_dict['isedav'] >= 1:
            fid.write('%-8i                             ->NPINP \n' % len(BC_dict['x_p'])) # this parameter is not specified in Brad's run_model...  This will crash if these conditions are met
        else:
            pass

                
                #for ii in range(0, len(BC_dict['x'])):  superceded bdj 2019-12-05 
        #	fid.write('%11.4f%11.4f%11.4f\n' % (BC_dict['x'][ii], BC_dict['zb'][ii], in_dict['fw']))
        for ii in range(0, len(x)):
            fid.write('%11.4f%11.4f%11.4f\n' % (x[ii],zb[ii], in_dict['fw']))

        if in_dict['iperm'] == 1 or in_dict['isedav'] >= 1:
            for ii in range(0, len(BC_dict['x_p'])):
                fid.write('%11.4f%11.4f\n' % (BC_dict['x_p'][ii], BC_dict['zb_p'][ii])) # this parameter is not specified in Brad's run_model...  This will crash if these conditions are met
        else:
            pass

        if in_dict['iveg'] == 1:
            fid.write('%5.3f                                ->VEGCD\n' % in_dict['veg_Cd'])
            for ii in range(0, len(BC_dict['x'])):
                if BC_dict['x'][ii] >= np.max(BC_dict['x'])*in_dict['veg_extent'][0] and BC_dict['x'][ii] <= np.max(BC_dict['x'])*in_dict['veg_extent'][1]:
                    fid.write('%11.3f%11.3f%11.3f%11.3f\n' % (in_dict['veg_n'], in_dict['veg_dia'], in_dict['veg_ht'], in_dict['veg_rod']))
                else:
                    fid.write('%11.3f%11.3f%11.3f%11.3f\n' % (0, 0, 0, 0))
        else:
            pass

        fid.close()

        # # also save the metadata to a pickle file!
        # dum = fname.split('/infile')
        # with open(os.path.join(dum[0], "metadata.pickle"), "wb") as fid:
        # 	pickle.dump(meta_dict, fid, protocol=pickle.HIGHEST_PROTOCOL)


    def read_CSHORE_ODOC(self, path):
        """This function will Read the ODOC input file

        :param path: return:

        """
        temp_file_name = os.path.join(path, 'ODOC')
        # with open(path + '/ODOC', 'r') as fid:
        with open(temp_file_name, 'r') as fid:
            tot = fid.readlines()
        fid.close()
        tot = np.asarray(list(map(lambda s: s.strip(), tot)))

        # find header
        row_ind = np.asarray(np.argwhere(['ILINE' in s for s in tot])).flatten()
        if len(row_ind) == 0:
            self.ODOC_dict['header'] = tot
            self.ODOC_dict['run_success']= 0
        else:
            self.ODOC_dict['header'] = tot[0:row_ind[0]]

        # find IPROFL
        row_ind = np.asarray(np.argwhere(['IPROFL' in s for s in tot])).flatten()
        row = tot[row_ind[0]]
        self.ODOC_dict['iprofl'] = int(row[row.find('=') + 1:])

        # find ISEDAV
        row_ind = np.asarray(np.argwhere(['ISEDAV' in s for s in tot])).flatten()
        if len(row_ind) == 0:
            self.ODOC_dict['isedav'] = 0
        else:
            row = tot[row_ind[0]]
            self.ODOC_dict['isedav'] = int(row[row.find('=') + 1:row.find('=') + 3])

        # find IPERM
        row_ind = np.asarray(np.argwhere(['IMPERMEABLE' in s for s in tot])).flatten()
        if len(row_ind) == 0:
            self.ODOC_dict['iperm'] = True
        else:
            self.ODOC_dict['iperm'] = False

        # find NBINP
        row_ind = np.asarray(np.argwhere(['NBINP' in s for s in tot])).flatten()
        row = tot[row_ind[0]]
        self.ODOC_dict['nbinp'] = int(row[row.find('=') + 1:])

        # find GAMMA
        row_ind = np.asarray(np.argwhere(['Gamma' in s for s in tot])).flatten()
        row = tot[row_ind[0]]
        self.ODOC_dict['gamma'] = float(row[row.find('=') + 1:])

        # get longshore transport
        dum = tot[np.argwhere(['Transport Rate' in s for s in tot]).flatten()]
        ls_trans = np.zeros(len(dum)) * np.nan
        if len(dum) > 0:
            for ii in range(0, len(dum)):
                row = dum[ii]
                if len(row[row.find('=') + 1:].strip()) > 0:
                    ls_trans[ii] = float(row[row.find('=') + 1:])
                else:
                    ls_trans[ii] = np.nan
            self.ODOC_dict['longshore_transport'] = ls_trans

        # get wave conditions at SB
        row_ind = np.asarray(np.argwhere(['INPUT WAVE' in s for s in tot])).flatten()
        ind_start = row_ind[0] + 4
        row_ind = np.asarray(np.argwhere(['INPUT BEACH AND STRUCTURE' in s for s in tot])).flatten()
        ind_end = row_ind[0] - 1
        wave_cond = tot[ind_start: ind_end]
        time_offshore = np.zeros(len(wave_cond)) * np.nan
        Tp_bc = np.zeros(len(wave_cond)) * np.nan
        Hs_bc = np.zeros(len(wave_cond)) * np.nan
        setup_bc = np.zeros(len(wave_cond)) * np.nan
        wl_bc = np.zeros(len(wave_cond)) * np.nan
        angle_bc = np.zeros(len(wave_cond)) * np.nan
        cnt = 0
        for line in wave_cond:
            dum = line.split()
            time_offshore[cnt] = float(dum[0])
            Tp_bc[cnt] = float(dum[1])
            Hs_bc[cnt] = np.sqrt(2) * float(dum[2])
            setup_bc[cnt] = float(dum[3])
            wl_bc[cnt] = float(dum[4])
            angle_bc[cnt] = float(dum[5])
            cnt = cnt + 1
        # THIS WILL ONLY RETURN THE FIRST AND LAST 10 BC POINTS!!!!
        self.ODOC_dict['time_offshore'] = time_offshore
        self.ODOC_dict['Tp_bc'] = Tp_bc
        self.ODOC_dict['Hs_bc'] = Hs_bc
        self.ODOC_dict['setup_bc'] = setup_bc
        self.ODOC_dict['wl_bc'] = wl_bc
        self.ODOC_dict['angle_bc'] = angle_bc

        # find runup
        dum2p = tot[np.argwhere(['2 percent runup' in s for s in tot]).flatten()]
        dummean = tot[np.argwhere(['Mean runup' in s for s in tot]).flatten()]
        runup_2_percent = np.zeros(len(dum2p)) * np.nan
        runup_mean = np.zeros(len(dum2p)) * np.nan
        if len(dum2p) > 0:
            for ii in range(0, len(dum2p)):
                row1 = dum2p[ii]
                row2 = dummean[ii]
                if len(row1[row1.find('R2P=') + 4:].strip()) > 0:
                    runup_2_percent[ii] = float(row1[row1.find('R2P=') + 4:])
                    runup_mean[ii] = float(row2[row1.find('R2P=') + 4:])
                else:
                    runup_2_percent[ii] = np.nan
                    runup_mean[ii] = np.nan
            self.ODOC_dict['runup_2_percent'] = runup_2_percent
            self.ODOC_dict['runup_mean'] = runup_mean

        # find jdry
        dum = tot[np.argwhere(['JDRY' in s for s in tot]).flatten()]
        jdry = np.zeros(len(dum)) * np.nan
        if len(dum) > 0:
            for ii in range(0, len(dum)):
                row = dum[ii]
                if len(row[row.find('JDRY=') + 5:].strip()) > 0:
                    jdry[ii] = float(row[row.find('JDRY=') + 5:])
                else:
                    jdry[ii] = np.nan
            self.ODOC_dict['jdry'] = jdry

        # find SWL at sea boundary
        dum = tot[np.argwhere([' SWL=' in s for s in tot]).flatten()]
        swl = np.zeros(len(dum)) * np.nan
        if len(dum) > 0:
            for ii in range(0, len(dum)):
                row = dum[ii]
                if len(row[row.find(' SWL=') + 5:].strip()) > 0:
                    swl[ii] = float(row[row.find(' SWL=') + 5:])
                else:
                    swl[ii] = np.nan
            self.ODOC_dict['swl'] = swl

        # find node number of SWL
        dum = tot[np.argwhere([' JSWL=' in s for s in tot]).flatten()]
        jswl = np.zeros(len(dum)) * np.nan
        if len(dum) > 0:
            for ii in range(0, len(dum)):
                row = dum[ii]
                if len(row[row.find(' JSWL=') + 6:].strip()) > 0:
                    jswl[ii] = float(row[row.find(' JSWL=') + 6:])
                else:
                    jswl[ii] = np.nan
            self.ODOC_dict['jswl'] = jswl

        # find jr
        dum = tot[np.argwhere(['JR=' in s for s in tot]).flatten()]
        jr = np.zeros(len(dum)) * np.nan
        if len(dum) > 0:
            for ii in range(0, len(dum)):
                row = dum[ii]
                if len(row[row.find('JR=') + 3:].strip()) > 0:
                    jr[ii] = float(row[row.find('JR=') + 3:])
                else:
                    jr[ii] = np.nan
            self.ODOC_dict['jr'] = jr

        # swash zone bottom slope
        row_ind = np.asarray(np.argwhere(['Swash zone bottom slope' in s for s in tot])).flatten()
        dum_slp = tot[row_ind]
        dum_x1 = tot[row_ind + 1]
        dum_x2 = tot[row_ind + 2]
        dum_z1 = tot[row_ind + 3]
        dum_z2 = tot[row_ind + 4]
        if len(dum_slp) > 0:
            slp = np.zeros(len(dum_slp)) * np.nan
            x1 = np.zeros(len(dum_x1)) * np.nan
            x2 = np.zeros(len(dum_x2)) * np.nan
            z1 = np.zeros(len(dum_z1)) * np.nan
            z2 = np.zeros(len(dum_z2)) * np.nan
            cnt = 0
            for ii in range(0, len(dum_slp)):
                if len(dum_slp[ii][dum_slp[ii].find('=') + 1:].strip()) > 0:
                    slp[cnt] = float(dum_slp[ii][dum_slp[ii].find('=') + 1:])
                    x1[cnt] = float(dum_x1[ii][dum_slp[ii].find('=') + 1:])
                    x2[cnt] = float(dum_x2[ii][dum_slp[ii].find('=') + 1:])
                    z1[cnt] = float(dum_z1[ii][dum_slp[ii].find('=') + 1:])
                    z2[cnt] = float(dum_z2[ii][dum_slp[ii].find('=') + 1:])
                else:
                    slp[cnt] = np.nan
                    x1[cnt] = np.nan
                    x2[cnt] = np.nan
                    z1[cnt] = np.nan
                    z2[cnt] = np.nan
                cnt = cnt + 1
            self.ODOC_dict['slprun'] = slp
            self.ODOC_dict['x1run'] = x1
            self.ODOC_dict['x2run'] = x2
            self.ODOC_dict['z1run'] = z1
            self.ODOC_dict['z2run'] = z2

    def read_CSHORE_infile(self, path):
        """

        :param path: 

        """
        temp_file_name = os.path.join(path, 'infile')
        # with open(path + '\\infile', 'r') as fid:
        with open(temp_file_name, 'r') as fid:
            tot = fid.readlines()
        fid.close()
        tot = np.asarray(list(map(lambda s: s.strip(), tot)))

        # find IOVER
        row_ind = np.asarray(np.argwhere(['IOVER' in s for s in tot])).flatten()
        row = tot[row_ind[0]]
        self.readIF_dict['iover'] = float(row[0:row.find('-') - 1])

        # find IVEG
        row_ind = np.asarray(np.argwhere(['IVEG' in s for s in tot])).flatten()
        row = tot[row_ind[0]]
        self.readIF_dict['iveg'] = float(row[0:row.find('-') - 1])

        # find effB, effF, and blp
        if self.ODOC_dict['iprofl'] == 1:
            # EFFB and EFFF
            row_ind = np.asarray(np.argwhere(['EFFB' in s for s in tot])).flatten()
            row = tot[row_ind[0]]
            dum = row[0:row.find('-') - 1].split()
            self.readIF_dict['effB'] = float(dum[0])
            self.readIF_dict['effF'] = float(dum[1])
            # BLP and TANPHI
            row_ind = np.asarray(np.argwhere(['BLP' in s for s in tot])).flatten()
            row = tot[row_ind[0]]
            dum = row[0:row.find('-') - 1].split()
            self.readIF_dict['tanphi'] = float(dum[0])
            self.readIF_dict['blp'] = float(dum[1])
            # ILAB
            row_ind = np.asarray(np.argwhere(['ILAB' in s for s in tot])).flatten()
            row = tot[row_ind[0]]
            row[0:row.find('-') - 1]
            self.readIF_dict['ilab'] = float(row[0:row.find('-') - 1])

        # find vegetation extent
        if self.readIF_dict['iveg'] == 1:
            row_ind = np.asarray(np.argwhere(['VEGCD' in s for s in tot])).flatten()
            dum = tot[row_ind[0] + 1:row_ind[0] + int(self.ODOC_dict['nbinp']) + 1]
            veg_n = np.zeros(len(dum))
            veg_dia = np.zeros(len(dum))
            veg_ht = np.zeros(len(dum))
            veg_rod = np.zeros(len(dum))
            cnt = 0
            for item in dum:
                row = item.split()
                veg_n[cnt] = float(row[0])
                veg_dia[cnt] = float(row[1])
                veg_ht[cnt] = float(row[2])
                veg_rod[cnt] = float(row[3])
                cnt = cnt + 1
            self.readIF_dict['veg_n'] = veg_n
            self.readIF_dict['veg_dia'] = veg_dia
            self.readIF_dict['veg_ht'] = veg_ht
            self.readIF_dict['veg_rod'] = veg_rod

        #now we are going to read the BC stuff from the infile, because Brad's ODOC bc stuff ONLY HAS THE FIRST AND LAST 10!?!?! WTFWTFWTF
        # find NSURGE
        row_ind_1 = np.asarray(np.argwhere(['NSURGE' in s for s in tot])).flatten()
        row_ind_2 = np.asarray(np.argwhere(['NBINP' in s for s in tot])).flatten()
        rows = tot[row_ind_1[0]+1:row_ind_2[0]]
        #get me the length of all the rows
        row_len = np.array([len(s.split()) for s in rows])
        assert 6 not in row_len, 'ilab must be set to 0 for simulation to run'
        #sort by length
        row_swlbc = rows[row_len == 2]
        row_waves = rows[row_len == 4]
        num_pts = len(row_swlbc)

        time_offshore = np.zeros(num_pts)
        Tp_bc = np.zeros(num_pts)
        Hs_bc = np.zeros(num_pts)
        setup_bc = np.zeros(num_pts) # the model must just assume this is zero, because this information IS NOT contained in the infile if ilab == 0
        wl_bc = np.zeros(num_pts)
        angle_bc = np.zeros(num_pts)

        for ii in range(0, len(row_waves)):
            dum_swlbc = row_swlbc[ii].split()
            wl_bc[ii] = dum_swlbc[1]
            dum_waves = row_waves[ii].split()
            time_offshore[ii] = dum_waves[0]
            Tp_bc[ii] = dum_waves[1]
            Hs_bc[ii] = str(np.sqrt(2) * float(dum_waves[2]))
            angle_bc[ii] = dum_waves[3]

        self.readIF_dict['time_offshore'] = time_offshore
        self.readIF_dict['Tp_bc'] = Tp_bc
        self.readIF_dict['Hs_bc'] = Hs_bc
        self.readIF_dict['setup_bc'] = setup_bc
        self.readIF_dict['wl_bc'] = wl_bc
        self.readIF_dict['angle_bc'] = angle_bc

    def read_CSHORE_OBPROF(self, path):
        """

        :param path: 

        """
        temp_file_name = os.path.join(path, 'OBPROF')
        # with open(path + '\\OBPROF', 'r') as fid:
        with open(temp_file_name, 'r') as fid:
            tot = fid.readlines()
        fid.close()
        tot = np.asarray(list(map(lambda s: s.strip(), tot)))

        if 'FIXED' in path:
            list1 = range(0, 1)
        elif 'MOBILE' in path:
            list1 = range(0, len(self.readIF_dict['time_offshore']))
        # else:
            # print('You need to update read_CSHORE_OBPROF in inputOutput to accept the version you have specified!')

        self.OBPROF_row_counter = tot[0].split()[1]

                #print self.OBPROF_row_counter

        for ii in range(0, len(self.readIF_dict['time_offshore'])):
                        
            self.OBPROF_dict['morph%s' % str(ii + 1)] = {}
            # row1 = tot[(self.ODOC_dict['nbinp'] + 1) * ii]
            row1 = tot[(int(self.OBPROF_row_counter)+1)*ii]
                        #print row1
            if len(row1.split()) == 3:
                N = int(row1.split()[1])
                tme = float(row1.split()[2])
            elif len(row1.split()) == 2:
                N = float(row1.split()[0])
                N = int(N)
                tme = float(row1.split()[1])

            if self.readIF_dict['iveg'] > 1 and ii > 0 and self.ODOC_dict['isedav'] == 0:
                dum = tot[(self.ODOC_dict['nbinp'] + 1) * ii + 1:(self.ODOC_dict['nbinp'] + 1) * ii + N + 1]
                iveg = np.zeros(N)
                x = np.zeros(N)
                zb = np.zeros(N)
                for ss in range(0, N):
                    iveg[ss] = float(dum[ss].split()[2])
                    x[ss] = float(dum[ss].split()[0])
                    zb[ss] = float(dum[ss].split()[1])
                self.OBPROF_dict['morph%s' % str(ii + 1)]['ivegetated'] = iveg
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb_p'] = []
                self.OBPROF_dict['morph%s' % str(ii + 1)]['x'] = x
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb'] = zb
                self.OBPROF_dict['morph%s' % str(ii + 1)]['time'] = tme
            elif self.ODOC_dict['isedav'] == 1:
                dum = tot[(self.ODOC_dict['nbinp'] + 1) * ii + 1:(self.ODOC_dict['nbinp'] + 1) * ii + N + 1]
                zb_p = np.zeros(N)
                x = np.zeros(N)
                zb = np.zeros(N)
                for ss in range(0, N):
                    zb_p[ss] = float(dum[ss].split()[2])
                    x[ss] = float(dum[ss].split()[0])
                    zb[ss] = float(dum[ss].split()[1])
                self.OBPROF_dict['morph%s' % str(ii + 1)]['ivegetated'] = []
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb_p'] = zb_p
                self.OBPROF_dict['morph%s' % str(ii + 1)]['x'] = x
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb'] = zb
                self.OBPROF_dict['morph%s' % str(ii + 1)]['time'] = tme
            else:
                # dum = tot[(self.ODOC_dict['nbinp'] + 1) * ii + 1:(self.ODOC_dict['nbinp'] + 1) * ii + N + 1]
                dum = tot[(N+1)*ii + 1:(N+1)*ii+N+1]				# note: drs added this.
                x = np.zeros(N)
                zb = np.zeros(N)
                for ss in range(0, N):
                    x[ss] = float(dum[ss].split()[0])
                    zb[ss] = float(dum[ss].split()[1])
                self.OBPROF_dict['morph%s' % str(ii + 1)]['ivegetated'] = []
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb_p'] = []
                self.OBPROF_dict['morph%s' % str(ii + 1)]['x'] = x
                self.OBPROF_dict['morph%s' % str(ii + 1)]['zb'] = zb
                self.OBPROF_dict['morph%s' % str(ii + 1)]['time'] = tme
                        
    def read_CSHORE_OSETUP(self, path):
        """

        :param path: 
        
        note: drs modified read_CSHORE_OSETUP. originally set up to read OSETUP file for 'nbinp' lines. in the case of
            CSHORE/Beach-fx implementation, 'nbinp' is smaller than the actual number of setup steps. this is because
            'nbinp' is equal to the number of initially fed profile steps. CSHORE does (i believe) a smoothing routine to 
            get the profile to the number of spacing related to 'dxc'. creating profiles using 'file_creation.py' creates 
            unequal spacing in the profile (for example 0 to upland width is two points, not equally spaced). 
        """
        temp_file_name = os.path.join(path, 'OSETUP')
        # with open(path + '/OSETUP', 'r') as fid:
        with open(temp_file_name, 'r') as fid:
            tot = fid.readlines()
        fid.close()
        tot = np.asarray(list(map(lambda s: s.strip(), tot)))
        ind_track = 0
        for ii in range(0, len(self.readIF_dict['time_offshore'])-1):
            self.OSETUP_dict['hydro%s' % str(ii + 1)] = {}
            row1 = tot[ind_track]

            if float(row1.split()[0]) == 1:
                N = int(row1.split()[1])
                tme = float(row1.split()[-1])
            else:
                N = int(row1.split()[0])

            dum = tot[ind_track + 1:ind_track + 1 + N + 1]
            # x = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            # setup = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            # depth = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            # sigma = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            # Hs = np.zeros(self.ODOC_dict['nbinp']) * np.nan  # note: we are feeding it Hmo!!!!!!!

            x = np.zeros(N) * np.nan
            setup = np.zeros(N) * np.nan
            depth = np.zeros(N) * np.nan
            sigma = np.zeros(N) * np.nan
            Hs = np.zeros(N) * np.nan  # note: we are feeding it Hmo!!!!!!!			

            for ss in range(0, N):
            # for ss in range(0, self.ODOC_dict['nbinp']):
                x[ss] = float(dum[ss].split()[0])
                setup[ss] = float(dum[ss].split()[1])
                depth[ss] = float(dum[ss].split()[2])
                sigma[ss] = float(dum[ss].split()[3])
                Hs[ss] = np.sqrt(8) * np.sqrt(2) * sigma[ss]

            ind_track = ind_track + N + 1

            self.OSETUP_dict['hydro%s' % str(ii + 1)]['x'] = x
            self.OSETUP_dict['hydro%s' % str(ii + 1)]['setup'] = setup
            self.OSETUP_dict['hydro%s' % str(ii + 1)]['depth'] = depth
            self.OSETUP_dict['hydro%s' % str(ii + 1)]['sigma'] = sigma
            self.OSETUP_dict['hydro%s' % str(ii + 1)]['Hs'] = Hs
            self.OSETUP_dict['hydro%s' % str(ii + 1)]['time_end'] = tme

    def load_CSHORE_results(self, path):
        """

        :param path: 

        """

        self.read_CSHORE_ODOC(path)
        self.read_CSHORE_infile(path)
        self.read_CSHORE_OBPROF(path)
        self.read_CSHORE_OSETUP(path)

        # all this does is take the dicts I created from my output text files a reformats them
        # params

        params = {}
        bc = {}
        hydro = {}
        veg = {}
        morpho = {}
        sed = {}

        params['header'] = self.ODOC_dict['header']
        params['iprofl'] = self.ODOC_dict['iprofl']
        params['isedav'] = self.ODOC_dict['isedav']
        params['iperm'] = self.ODOC_dict['iperm']
        params['nbinp'] = self.ODOC_dict['nbinp']
        params['gamma'] = self.ODOC_dict['gamma']
        params['iover'] = self.readIF_dict['iover']
        params['iveg'] = self.readIF_dict['iveg']
        if 'MOBILE' in path:
            params['effB'] = self.readIF_dict['effB']
            params['effF'] = self.readIF_dict['effF']
            params['tanphi'] = self.readIF_dict['tanphi']
            params['blp'] = self.readIF_dict['tanphi']
            params['ilab'] = self.readIF_dict['ilab']
        else:
            pass

        num_steps = len(self.OSETUP_dict.keys())
        params['num_steps'] = num_steps

        # veg
        if params['iveg'] == 1:
            veg['n'] = self.readIF_dict['veg_n']
            veg['dia'] = self.readIF_dict['veg_dia']
            veg['ht'] = self.readIF_dict['veg_ht']
            veg['rod'] = self.readIF_dict['veg_rod']
        else:
            veg['n'] = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            veg['dia'] = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            veg['ht'] = np.zeros(self.ODOC_dict['nbinp']) * np.nan
            veg['rod'] = np.zeros(self.ODOC_dict['nbinp']) * np.nan

        # from OSETUP
        #note: drs modified this. using a matrix with nan of certain size was not working. 
        #	using a dict instead due to the fact that values from OSETUP are not the same size 
        #	(e.g. at time 0 len(setup)=630, at time 10, len(setup) = 631)

        # time_end = np.zeros([num_steps, 1]) * np.nan
        # x = np.zeros([num_steps, self.ODOC_dict['nbinp']]) * np.nan
        # setup = np.zeros([num_steps, self.ODOC_dict['nbinp']]) * np.nan
        # depth = np.zeros([num_steps, self.ODOC_dict['nbinp']]) * np.nan
        # sigma = np.zeros([num_steps, self.ODOC_dict['nbinp']]) * np.nan
        # Hs = np.zeros([num_steps, self.ODOC_dict['nbinp']]) * np.nan

        time_end = {}
        x = {}
        setup = {}
        depth = {}
        sigma = {}
        Hs = {}

        for ii in range(0, num_steps):
            # OSETUP
            temp_dict_setup = self.OSETUP_dict['hydro%s' % str(ii + 1)]
            time_end[ii] = temp_dict_setup['time_end']
            x[ii] = temp_dict_setup['x']
            setup[ii] = temp_dict_setup['setup']
            depth[ii] = temp_dict_setup['depth']
            sigma[ii] = temp_dict_setup['sigma']
            Hs[ii] = temp_dict_setup['Hs']

        hydro['time_end'] = time_end
        hydro['x'] = x
        hydro['mwl'] = setup
        hydro['depth'] = depth
        hydro['sigma'] = sigma
        hydro['Hs'] = Hs

        # morpho
        # from OBPROF
        time = np.zeros([num_steps + 1, 1]) * np.nan

        if 'FIXED' in path:
            list = range(0, 1)
            # from OBPROF
            x = np.zeros([1, self.ODOC_dict['nbinp']]) * np.nan
            zb = np.zeros([1, self.ODOC_dict['nbinp']]) * np.nan
            zb_p = np.zeros([1, self.ODOC_dict['nbinp']]) * np.nan
            ivegetated = np.zeros([1, self.ODOC_dict['nbinp']]) * np.nan
        elif 'MOBILE' in path:
            list = range(0, num_steps + 1)
            # from OBPROF
            x = np.zeros([num_steps + 1, self.ODOC_dict['nbinp']]) * np.nan
            zb = np.zeros([num_steps + 1, self.ODOC_dict['nbinp']]) * np.nan
            zb_p = np.zeros([num_steps + 1, self.ODOC_dict['nbinp']]) * np.nan
            ivegetated = np.zeros([num_steps + 1, self.ODOC_dict['nbinp']]) * np.nan
        else:																										#note: drs modified this
            x = np.zeros([num_steps + 1, int(self.OBPROF_row_counter)]) * np.nan
            zb = np.zeros([num_steps + 1, int(self.OBPROF_row_counter)]) * np.nan
            zb_p = np.zeros([num_steps + 1, int(self.OBPROF_row_counter)]) * np.nan
            ivegetated = np.zeros([num_steps + 1, int(self.OBPROF_row_counter)]) * np.nan

        for ii in range(0, num_steps+1):
            # OBPROF
            temp_dict_prof = self.OBPROF_dict['morph%s' % str(ii + 1)]
            time[ii] = temp_dict_prof['time']
            x[ii] = temp_dict_prof['x']
            zb[ii] = temp_dict_prof['zb']
            if len(temp_dict_prof['zb_p']) > 0:
                zb_p[ii] = temp_dict_long['zb_p']
            if len(temp_dict_prof['ivegetated']) > 0:
                ivegetated[ii] = temp_dict_long['ivegetated']

        morpho['time'] = time
        morpho['x'] = x
        morpho['zb'] = zb
        morpho['zb_p'] = zb_p
        morpho['ivegetated'] = ivegetated


        # bc
        bc['time_offshore'] = self.readIF_dict['time_offshore']
        bc['Tp_offshore'] = self.readIF_dict['Tp_bc']
        bc['Hs_offshore'] = self.readIF_dict['Hs_bc']
        bc['wave_setup_offshore'] = self.readIF_dict['setup_bc']
        bc['strm_tide_offshore'] = self.readIF_dict['wl_bc']
        bc['angle_offshore'] = self.readIF_dict['angle_bc']

        return params, bc, veg, hydro, sed, morpho


