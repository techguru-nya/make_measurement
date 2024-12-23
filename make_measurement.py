#!/usr/bin/env python
# coding: utf-8

# # Read_A2L

# In[20]:


def READ_A2L(file):
    outputs = {}

    f = open(file, 'r')
    datalist = f.readlines()
    f.close()

    start = '/begin MEASUREMENT'
    end = '/end MEASUREMENT'
    mesurements = extract_textlist(datalist, start, end)

    for data in mesurements:
        start = '/begin DEFAULT_EVENT_LIST'
        end = '/end DEFAULT_EVENT_LIST'
        data2 = extract_textlist(data, start, end)
        signal = data[0]
        signal = signal.replace(' ', '')
        signal = signal.replace('\n', '')
        event = data2[0][0]
        event = event.replace(' ', '')
        event = event.replace('\n', '')
        event = event.replace('EVENT', '')
        outputs[signal] = event
    
    return outputs


def extract_textlist(textlist, start, end):
    outputs = []
    output = []
    count = 0
    for data in textlist:
        if start in data:
            count = 1
        elif end in data:
            count = 0
            outputs.append(output)
            output = []
        elif count != 0:
            count += 1

        if count > 1:
            output.append(data)
    
    return outputs


# # REMOVE_KEY

# In[21]:


def REMOVE_KEY(d_Sig, d_Key, l_Key):
    sig_list = d_Sig.copy()
    sig_list = list(sig_list.keys())
    l_Remove = []
    
    for K in l_Key:
        if K in d_Key:
            l_Remove += d_Key[K]
        
    for K in l_Remove:
        sig_list.remove(K)
    
    sig_select = {}
    for sig in sig_list:
        sig_select[sig] = d_Sig[sig]
    
    return sig_select


# # SEARCH_not_GLOBAL_KEY

# In[22]:


def SEARCH_not_GLOBAL_KEY(d_Sig): 
    d_Glo = {}
    l_Key = []
    
    for S in d_Sig:
        if '.' in S:
            S_ = S.split('.')
            d_Glo[S] = S_[-1]
            l_Key.append(S_[-1])
    
    l_Key_set = set(l_Key)
    
    d_Key = {}
    
    for K in l_Key_set:
        l_ = []
        
        for S in d_Glo:
            if K == d_Glo[S]:
                l_.append(S)
        
        d_Key[K] = l_     
    
    return d_Key


# # SEARCH_GLOBAL_KEY

# In[23]:


def SEARCH_GLOBAL_KEY(d_Sig): 
    d_Glo = {}
    l_Key = []
    
    for S in d_Sig:
        if '.' not in S:
            S_ = S.split('_')
            d_Glo[S] = S_[0]
            l_Key.append(S_[0])
    
    l_Key_set = set(l_Key)
    
    d_Key = {}
    
    for K in l_Key_set:
        l_ = []
        
        for S in d_Glo:
            if K == d_Glo[S]:
                l_.append(S)
        
        d_Key[K] = l_     
    
    return d_Key


# # REVIEW

# In[24]:


def REVIEW_FUN(d_Sig, N): 
    d_not_Global = SEARCH_not_GLOBAL_KEY(d_Sig)

    Out = ''
    
    for K in d_not_Global:
        if len(d_not_Global[K]) > N:
            # Out += f"'{K}':{len(d_not_Global[K])}, "
            Out += f"'{K}', "
    
    print(Out)


# In[25]:


def REVIEW_GLO(d_Sig, N):
    d_Global = SEARCH_GLOBAL_KEY(d_Sig)

    Out = ''
    
    for K in d_Global:
        if len(d_Global[K]) < 30 and len(d_Global[K]) > 10:
            print(K, len(d_Global[K]))
            Out += f"'{K}':{len(d_Global[K])}, "

            for i, P in enumerate(d_Global[K]):
                print(i, P)
                
    print(Out)


# # WRITE_TXT

# In[26]:


def WRITE_TXT(File, d_Sig, a2l, plt_list, remove_fun_list, remove_global_list):
    Text = ''
    
    l_Comment = Comment_w_File(a2l, plt_list, remove_fun_list, remove_global_list)
    
    for T in l_Comment:
        Text += T + '\n'
        
    Text += '\n'
    
    for S in d_Sig:
        Text += S + ';' + d_Sig[S] + '\n'
        
    f = open(File, 'w')
    f.write(Text)
    f.close()

    print(File)
    

def Comment_w_File(a2l, plt_list, remove_fun_list, remove_global_list):
    outputs = []
    
    output = f'// A2L-file: {a2l}'
    outputs.append(output)
    
    output = f'// remove modules: '
    for i, fun in enumerate(remove_fun_list):
        if i == 0:
            output += f'{fun}'
        else:
            output += f', {fun}'
    outputs.append(output)        

    output = f'// remove global-keys: '
    for i, glo in enumerate(remove_global_list):
        if i == 0:
            output += f'{glo}'
        else:
            output += f', {glo}'
    outputs.append(output)
    
    output = f'// add PLT-file: '
    for i, plt in enumerate(plt_list):
        if i == 0:
            output += f'{plt}'
        else:
            output += f', {plt}'
    outputs.append(output)
    
    return outputs


# # Add_Signal_with_PLT

# In[27]:


def Add_Signal_with_PLT(sig_data, sig_data_all, files):    
    sig_list = Read_PLT(files)
    
    for sig in sig_list:
        if sig not in sig_data and sig in sig_data_all:
            sig_data[sig] = sig_data_all[sig]
    
    return sig_data
    

def Read_PLT(Files):
    Signals = []
    
    for File in Files:
        f = open(File, 'r', encoding="ascii")
        l_line_plt = f.readlines()

        for line in l_line_plt:
            line = line.replace("\n", "")
            l_line = line.split(" ")

            if l_line[0] != "" and "//" not in l_line[0] and "+" not in l_line[0] and "*" not in l_line[0]:
                Sig = GetKey(l_line)
                if Sig != '~' and Sig not in Signals:
                    Signals.append(GetKey(l_line))
        f.close()

    return Signals


def GetKey(l_in):
    Out = l_in[0]
    
    for Text in l_in:
        l_Text = Text.split("=")
        
        if l_Text[0] == "key":
            Out = l_Text[1]
            
    return Out


# # RUN

# In[ ]:


# import Make_CFG as cfg


# # In[37]:


# DIR = 'c:\\mt\\Honda\\3BWT\\HILS\\'

# # FILE_A2L = f'{DIR}APL_Asap_BB88667_15030300_ESP103DAA88667XCP_XCP.a2l'
# # FILE_OUT = f'{DIR}3DAA_BB88667_15030300_ESP103DAA88667.cfg'

# FILE_A2L = f'{DIR}APL_Asap_BB88574_08040500_ESP3BVT88574XCPSec_XCP.a2l'
# FILE_OUT = f'{DIR}3BWT_BB88574_08040500_ESP3BVT88574.cfg'

# PLT_LIST = [f'{DIR}BfmDecoderESP.PLT']

# l_REMOVE_w_FUN = ['ABP20ms', 'ACM_ESP9_Mc_DS10_20ms', 'ACM_ESP9_Mc_DS10_5ms', 'ADCMeasureValue', 'AEB5ms', 'AEBPre5ms_Esp', 'AID5ms', 'APB_BSW_Ctrl_20ms', 'APB_Coor_Centralized', 'APB_Ctrl_20ms', 'APB_Hsb_10ms', 'APB_Mon_20ms', 'APB_Sic_5ms', 'APB_Wrp_10ms', 'ActValue1', 'ActValue1_Ampere', 'ActValue2', 'ActValue2_Ampere', 'ActuatorTestRequestConverter', 
#                   'BAT_Request_Converter_HFA', 'BB87973_09000800_ESP10DG8B87973XCP_Calibration_No_Parameters_0', 'BB88667_15030300_ESP103DAA88667XCP_Calibration_No_Parameters_0','BTM120ms', 'Boost_Postprocessing_Main', 'Boost_Preprocessing_Main', 'CM_AEB', '_Body_34AA_KA_FWD_0_0_1_1_0_0', '_Body_34AA_KA_FWD_0_0_0_0_0_0', '_Body_34AA_KA_FWD_0_0_0_0_1_1', '_Body_34AA_KA_FWD_0_0_1_1_2_2', '_Body_34AA_KA_FWD_0_1_0_1_0_1', 'BB89921_16020200_ESP1034AA89921XCP_Calibration_No_Parameters_0', 'Buffer0', 'Buffer1', 'Buffer2', 'Buffer3', 'Buffer4', 'BB88574_08040500_ESP3BVT88574XCPSec_Calibration_No_Parameters_0', 
#                   'CM_APB_HONDA', 'CM_EBP5ms_AxleSplit', 'CM_HDC_Postprocessing', 'CM_HDC_Preprocessing_Extended', 'CM_HDC_vDes', 'CM_HHCPlus', 'CM_HSM', 'CM_INS_SignalExport', 'CM_LDI4HondaMMS', 'CM_LDM_With_AxleSplit', 'CM_LTM', 'CM_PT_Honda_AxleSplitModel_2IFActuator', 'CM_SASClass3_N3C3_Driver_20ms_woCal', 'CM_SspWss', 'CM_SspWss_SignalExport', 'CM_TCS_AxleSplit_Honda', 'CM_TCS_CUS', 'CM_TCS_ESP', 'CM_VDC_ESP10_GBEV_AxleSplit_wMMS', 'CSM_CoreHoldService', 'CSM_CoreParkPawlService', 'CSM_CoreParkService', 'CSM_InterTaskPrimary', 'CSM_Post_LDM_DynamicArbitrator', 'CSM_PreCore', 'CSM_RequestWrapper', 'CSM_ReverseGearSwitchMonitoring', 'CSM_SafetyConnector20ms', 'CSM_SafetyConnector5ms', 'CSM_VSE', 'CSM_Wrapper', 'CSM_WrapperBrakeSystem', 'CSM_WrapperPowertrain', 'Connector_pTgtLimit_ESP', 'CM_AVH', 'CDP20ms', 'Connector_VDC_TCS_Evo0507', 'CM_Boost_HBB_LowVac_ON', 'ClutchPedalMonitoring', 'CM_SASClass3_N3C3_Driver_20ms', 'CM_Boost_ESPVacB_HBBLowVac', 'CM_Honda_ADAS_GIF_Pre5ms', 'CM_LTM_ESP9', 'CM_CDD_Standalone', 
#                   'DDR_20ms', 'DragTorqueController_preprocessing_5ms', 'Duration', 'Duration_Sec', 'Duty_u8',
#                   'EBP5ms', 'Esp10Cust_Honda_SignalExport',
#                   'FOF5ms', 
#                   'GRC20ms',
#                   'HAZ_HazardWarning20ms', 'HBA_Main', 'HBB_HBC_Main', 'HDC_Main', 'HDC_STM', 'HDC_VxRef', 'HFC_Main', 'HGT_PATA_Task20ms', 'HHC20ms', 'HRB_Main','HSM20ms', 'Honda_ESS_20ms', 'Honda_MAEPS_20ms',
#                   'INS_Standalone_20ms', 'INS_Standalone_40ms',
#                   'LDI5ms', 'LDI_Arbitration', 'LDI_NoEstimation', 'LDI_TaskInterpolation', 'LDMConfiguration', 'LDMCoor', 'LDMCoor_Arbitrator_mesg', 'LDMFxVehConnectorESP5ms', 'LTCSas_40ms', 'LVMM5ms', 'Ltm_ESP9_Mod', 'LFI',
#                   'MBP_20ms', 'MBP_40ms', 'MVR_Main', 'Mode',
#                   'PBCA20ms', 'PMC_ESP9_20ms', 'PTActuator_20ms_SW9_AxleSplit', 'PTModel_20ms_AxleSplit', 'ParkBrakeControl_T10ms_VDA_2', 'Pressure_SW',
#                   'Qualifier_N',
#                   'RFE_CoreMueEstimation_20ms', 'RFE_MueReleaseModule', 'RxValue', 'RevGearMon_20ms', 
#                   'SSP_OBD_0', 'SasClass3_20ms', 'SspWssEsp_120ms', 'SspWssEsp_20ms', 'SspWssEsp_5ms', 'SspWssWithDir_20', 'Status', 'StandstillLibrary_20ms', 'SSMDriveOffPlayingWithGasLogic', 
#                   'TCS_Core', 'TCS_Core_CBDS', 'TCS_Core_Mon', 'TCS_Core_Out', 'TSC_SignalProcessing_ESPhevX', 'TxValue', 'TaskBaseCtrlx4Variant', 'TaskBaseCtrlx1Variant', 'TaskBaseCtrlx4', 
#                   'VDC_CCC', 'VDC_EUC', 'VDC_LAC_MassEstimation', 'VDC_LAC_VCH', 'VDC_TSM', 'VWPQ26Esp9CE_TaskBaseCtrlx24Variant',  
#                   '_PBC_BoschCbi_VDA_2',
#                   'ctCallsTotal_u32', 'current_task_cnt',
#                   'gross', 'gross_max',
#                   'id',
#                   'loadPer64k_u16',
#                   'resp_time', 'resp_time_max',
#                   'slack_time', 'slack_time_min', 'slack_time_min_resettable', 'slack_time_min_resettable_task_cnt', 'slack_time_min_task_cnt', 'state',
#                   'tiAvrgRT_u32', 'tiCurRT_u32', 'tiMaxRT_u32', 'tiMinRT_u32', 'ts_activation', 'ts_end', 'ts_start'] 

# l_REMOVE_w_GLOBAL = ['APBBUT', 'APBMotorLeft', 'APBMotorRight', 'ASCETADAPTER', 'Apb',
#                      'BAT',
#                      'CAX', 'CBCABS', 'CBDS', 'CCO', 'CSM', 'CanSBox', 'CanSM', 'CmdMbWheelTar', 'ComM', 'CtrlMode',
#                      'DEM', 'DISP', 'Dcm', 'Det', 'DiaMIDStatus',
#                      'ETA', 'EV',
#                      'FAULTYEVENT', 'FBC1', 'Fsl',
#                      'HMIGeneratorOutputState', 'HSV', 'HSW09', 'Honda',
#                      'IUMPR',
#                      'LCOPre', 'LDM', 'LDMCoor', 'LDMCor', 'LdmRequestMode', 'Ltm',
#                      'MEM', 'MPropPhys', 'MbDrvLdmReqWhl', 'MbWheelTtl', 'Mbp', 'MesRBNet', 'MonResER',
#                      'NetRXVar', 'NetTXVar', 'NvM',
#                      'OOL', 'ORDABS', 'OmegaF',
#                      'PbcDevelopmentMessage', 'PbcIn', 'PbcOut',
#                      'RBACM', 'RBADC', 'RBAPBMOT', 'RBAPLPLANT', 'RBAPPLIF', 'RBCBDS', 'RBDHP', 'RBDIO', 'RBGTM', 'RBHYDR', 'RBINS', 'RBMAD', 'RBMESG', 'RBMICAPB', 'RBPduHandler', 'RBRFP', 'RBRFPActDatLowend', 'RBSUPPLYBASE', 'RBSYS', 'RBVLV', 'RBVMI', 'RBVoltageHandler', 'RBWAU', 'RBWSS',
#                      'SMM', 'STM', 'SsmSelCon', 'Strategy',
#                      'VIRTUALNODEINVALID', 'VIRTUALNODEINVALIDFILTERED', 'VIRTUALNODENOTAVAILABLE', 'VIRTUALNODENOTINITIALIZED', 'VIRTUALNODESUSPICIOUS', 'VLC', 'VSE',
#                      'WSS',
#                      'Xc',
#                      'cc',
#                      'g', 'gs',
#                      'int',
#                      'ls',
#                      'pDrv',
#                      'rb', 'rba', 'rbgtm', 'rbvlv',
#                      'vF']


# # In[ ]:


# d_SIG_All = cfg.READ_A2L(FILE_A2L)
# print(f'All: {len(d_SIG_All)}')

# d_GLOBAL_KEY = cfg.SEARCH_GLOBAL_KEY(d_SIG_All)
# d_SIG = cfg.REMOVE_KEY(d_SIG_All, d_GLOBAL_KEY, l_REMOVE_w_GLOBAL)
# print(f'Removed in Global: {len(d_SIG)}')

# d_not_GLOBAL_KEY = cfg.SEARCH_not_GLOBAL_KEY(d_SIG)
# d_SIG = cfg.REMOVE_KEY(d_SIG, d_not_GLOBAL_KEY, l_REMOVE_w_FUN)
# print(f'Removed in Function: {len(d_SIG)}')
# cfg.REVIEW_FUN(d_SIG, 10)

# d_SIG = cfg.Add_Signal_with_PLT(d_SIG, d_SIG_All, PLT_LIST)
# print(f'Added with PLT: {len(d_SIG)}')

# cfg.WRITE_TXT(FILE_OUT, d_SIG, FILE_A2L, PLT_LIST, l_REMOVE_w_FUN, l_REMOVE_w_GLOBAL)


# # In[ ]:




