"""See how to create a transistor object."""
# imports
import transistordatabase as tdb
import os
import numpy as np


# Template to generate a transistor
def template_example(database, path):
    """Template to create a transistor object.
    database: DatabaseManager object
    path: path to the csv files. This is needed for csv2array function to find the csv files
    """
    ####################################
    # transistor parameters
    ####################################
    # let's see if the data exist in the transistor_loaded object
    # if not, we will load the data from a csv files
    # if the data exist, we will use the data from the transistor_loaded object
    # check if the data exist in the transistor_loaded object, if not load the data from the csv files
    
    if not hasattr(transistor_loaded, 'c_iss'):
        c_iss_normal = tdb.csv2array(f'{path}/transistor_c_iss.csv', first_x_to_0=True)
        c_iss_detail = tdb.csv2array(f'{path}/transistor_c_iss_detail.csv', first_x_to_0=True)
        c_iss_merged = tdb.merge_curve(c_iss_normal, c_iss_detail)

    else:
        c_iss_merged = np.array([transistor_loaded.c_iss[0].graph_v_c[0]])
        c_iss_merged = np.append(c_iss_merged, np.array([transistor_loaded.c_iss[0].graph_v_c[1]]), axis=0)
        
    if not hasattr(transistor_loaded, 'c_oss'):
        c_oss_normal = tdb.csv2array(f'{path}/transistor_c_oss.csv', first_x_to_0=True)
        c_oss_detail = tdb.csv2array(f'{path}/transistor_c_oss_detail.csv', first_x_to_0=True)
        c_oss_merged = tdb.merge_curve(c_oss_normal, c_oss_detail)
    else:
        c_oss_merged = np.array([transistor_loaded.c_oss[0].graph_v_c[0]])
        c_oss_merged = np.append(c_oss_merged, np.array([transistor_loaded.c_oss[0].graph_v_c[1]]), axis=0)

    if not hasattr(transistor_loaded, 'c_rss'):
        c_rss_normal = tdb.csv2array(f'{path}/transistor_c_rss.csv', first_x_to_0=True)
        c_rss_detail = tdb.csv2array(f'{path}/transistor_c_rss_detail.csv', first_x_to_0=True)
        c_rss_merged = tdb.merge_curve(c_rss_normal, c_rss_detail)
    else:
        c_rss_merged = np.array([transistor_loaded.c_rss[0].graph_v_c[0]])
        c_rss_merged = np.append(c_rss_merged, np.array([transistor_loaded.c_rss[0].graph_v_c[1]]), axis=0)

    if not hasattr(transistor_loaded, 'graph_v_ecoss'):
        v_ecoss = tdb.csv2array(f'{path}/transistor_V_Eoss.csv')
    else:
        v_ecoss = transistor_loaded.graph_v_ecoss

    # Create argument dictionaries
    transistor_args = {'name': 'CREE_C3M0016120K',
                       'type': 'SiC-MOSFET',
                       'author': 'Nikolas Förster',
                       'comment': '',
                       'manufacturer': 'Wolfspeed',
                       'datasheet_hyperlink': 'https://www.wolfspeed.com/downloads/dl/file/id/1483/product/0/c3m0016120k.pdf',
                       'datasheet_date': '2019-04',
                       'datasheet_version': "unknown",
                       'housing_area': 367e-6,
                       'cooling_area': 160e-6,
                       'housing_type': 'TO247',
                       'v_abs_max': 1200,
                       'i_abs_max': 250,
                       'i_cont': 115,
                       'c_iss': {"t_j": 25, "graph_v_c": c_iss_merged},  # insert csv here
                       'c_oss': {"t_j": 25, "graph_v_c": c_oss_merged},  # insert csv here
                       'c_rss': {"t_j": 25, "graph_v_c": c_rss_merged},  # insert csv here
                       'c_oss_er': None,    # if given will be provided as : {"c_o": 180e-12 , "v_gs": 0 ,"v_ds": 800V }
                       'c_oss_tr': None,    # if given will be provided as : {"c_o": 20e-12 , "v_gs": 0 ,"v_ds": 800V }
                       'c_iss_fix': 6085e-12,
                       'c_oss_fix': 230e-12,
                       'c_rss_fix': 13e-12,
                       'graph_v_ecoss': v_ecoss,
                       'r_g_int': 2.6,
                       'r_th_cs': 0,
                       'r_th_diode_cs': 0,
                       'r_th_switch_cs': 0,
                       }

    ####################################
    # switch parameters
    ####################################
    # Metadata
    comment = "SiC switch"  # Optional
    manufacturer = "CREE"  # Optional
    technology = "unknown"  # Semiconductor technology. e.g. IGBT3/IGBT4/IGBT7  # Optional

    # Channel parameters, Ids current is in A, Vgs voltage is in V and Tj temperature is in degree Celsius
    # First we will check if the data exist in the transistor_loaded object and load them into a dictionary
    channel = {}
    if hasattr(transistor_loaded.switch, 'channel'):
        for i in range(len(transistor_loaded.switch.channel)):
            t_j = transistor_loaded.switch.channel[i].t_j
            v_g = transistor_loaded.switch.channel[i].v_g
            channel[f"channel_{t_j}_{v_g}"] = {"t_j": t_j, 'v_g': v_g, "graph_v_i": transistor_loaded.switch.channel[i].graph_v_i}
    # Now Let's look for files that start with switch_channel_ and end with .csv
    # note that the file name should be in the format switch_channel_tj_vg.csv where tj is the temperature in degree Celsius(if the votlage is negative it should be written as m40 instead of -40) and vg is the gate voltage in volt
    for file in os.listdir(path):
        if file.startswith("switch_channel_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            t_j = int(tdb.temp_to_numeric(file.split("_")[2]))
            if t_j == 0:
                t_j = 25
            v_g = int(tdb.volt_to_numeric(file.split("_")[3]))
            # check if the data exist in the transistor_loaded object, if not load the data from the csv files
            if f"channel_{t_j}_{v_g}" not in channel:
                channel[f"channel_{t_j}_{v_g}"] = {"t_j": t_j, 'v_g': v_g, "graph_v_i": tdb.csv2array(f'{path}/{file}.csv', first_xy_to_00=True)}

    '''previous code
    channel_m40_15 = {"t_j": -40, 'v_g': 15, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_m40_15V.csv', first_xy_to_00=True)}  # insert csv here
    channel_m40_13 = {"t_j": -40, 'v_g': 13, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_m40_13V.csv', first_xy_to_00=True)}  # insert csv here
    channel_m4_11 = {"t_j": -40, 'v_g': 11, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_m40_11V.csv', first_xy_to_00=True)}  # insert csv here
    channel_m40_9 = {"t_j": -40, 'v_g': 9, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_m40_9V.csv', first_xy_to_00=True)}  # insert csv here
    channel_m40_7 = {"t_j": -40, 'v_g': 7, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_m40_7V.csv', first_xy_to_00=True)}  # insert csv here
    # channel data 25 degree
    channel_25_15 = {"t_j": 25, 'v_g': 15, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_25_15V.csv', first_xy_to_00=True)}  # insert csv here
    channel_25_13 = {"t_j": 25, 'v_g': 13, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_25_13V.csv', first_xy_to_00=True)}  # insert csv here
    channel_25_11 = {"t_j": 25, 'v_g': 11, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_25_11V.csv', first_xy_to_00=True)}  # insert csv here
    channel_25_9 = {"t_j": 25, 'v_g': 9, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_25_9V.csv', first_xy_to_00=True)}  # insert csv here
    channel_25_7 = {"t_j": 25, 'v_g': 7, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_25_7V.csv', first_xy_to_00=True)}  # insert csv here
    # channel data 175 degree
    channel_175_15 = {"t_j": 175, 'v_g': 15, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_175_15V.csv', first_xy_to_00=True)}  # insert csv here
    channel_175_13 = {"t_j": 175, 'v_g': 13, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_175_13V.csv', first_xy_to_00=True)}  # insert csv here
    channel_175_11 = {"t_j": 175, 'v_g': 11, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_175_11V.csv', first_xy_to_00=True)}  # insert csv here
    channel_175_9 = {"t_j": 175, 'v_g': 9, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_175_9V.csv', first_xy_to_00=True)}  # insert csv here
    channel_175_7 = {"t_j": 175, 'v_g': 7, "graph_v_i": tdb.csv2array(f'{path}/switch_channel_175_7V.csv', first_xy_to_00=True)}  # insert csv here
    '''

    # switching parameters
    e_on = {}
    if hasattr(transistor_loaded.switch, 'e_on'):
        for i in range(len(transistor_loaded.switch.e_on)):
            t_j = transistor_loaded.switch.e_on[i].t_j
            v_g = transistor_loaded.switch.e_on[i].v_g
            v_supply = transistor_loaded.switch.e_on[i].v_supply
            r_g = transistor_loaded.switch.e_on[i].r_g
            e_on[f"e_on_{t_j}_{v_supply}"] = {"dataset_type": "graph_i_e",
                                                    "t_j": t_j,
                                                    'v_g': v_g,
                                                    'v_supply': v_supply,
                                                    'r_g': r_g,
                                                    "graph_i_e": transistor_loaded.switch.e_on[i].graph_i_e}
    for file in os.listdir(path):
        if file.startswith("switch_switching_eon_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            r_g = tdb.res_to_numeric(file.split("_")[3])
            v_supply = int(tdb.volt_to_numeric(file.split("_")[4]))
            t_j = int(tdb.temp_to_numeric(file.split("_")[5]))
            v_g = int(tdb.volt_to_numeric(file.split("_")[6]))
            if f"e_on_{t_j}_{v_supply}" not in e_on:
                e_on[f"e_on_{t_j}_{v_supply}"] = {"dataset_type": "graph_i_e",
                                                      "t_j": t_j,
                                                      'v_g': v_g,
                                                      'v_supply': v_supply,
                                                      'r_g': r_g,
                                                      "graph_i_e": tdb.csv2array(f'{path}/{file}.csv')}
    ''' previous code
    e_on_25_600 = {"dataset_type": "graph_i_e",
                   "t_j": 25,
                   'v_g': 15,
                   'v_supply': 600,
                   'r_g': 2.5,
                   "graph_i_e": tdb.csv2array(f'{path}/switch_switching_eon_2.5Ohm_600V_25deg_15V.csv')}  # insert csv here
    e_on_25_800 = {"dataset_type": "graph_i_e",
                   "t_j": 25,
                   'v_g': 15,
                   'v_supply': 800,
                   'r_g': 2.5,
                   "graph_i_e": tdb.csv2array(f'{path}/switch_switching_eon_2.5Ohm_800V_25deg_15V.csv')}  # insert csv here
    '''
    e_off = {}
    if hasattr(transistor_loaded.switch, 'e_off'):
        for i in range(len(transistor_loaded.switch.e_off)):
            t_j = transistor_loaded.switch.e_off[i].t_j
            v_g = transistor_loaded.switch.e_off[i].v_g
            v_supply = transistor_loaded.switch.e_off[i].v_supply
            r_g = transistor_loaded.switch.e_off[i].r_g
            e_off[f"e_off_{t_j}_{v_supply}"] = {"dataset_type": "graph_i_e",
                                                 "t_j": t_j,
                                                 'v_g': v_g,
                                                 'v_supply': v_supply,
                                                 'r_g': r_g,
                                                 "graph_i_e": transistor_loaded.switch.e_off[i].graph_i_e}
    for file in os.listdir(path):
        if file.startswith("switch_switching_eoff_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            r_g = tdb.res_to_numeric(file.split("_")[3])
            v_supply = int(tdb.volt_to_numeric(file.split("_")[4]))
            t_j = int(tdb.temp_to_numeric(file.split("_")[5]))
            v_g = int(tdb.volt_to_numeric(file.split("_")[6]))
            if f"e_off_{t_j}_{v_supply}" not in e_off:
                e_off[f"e_off_{t_j}_{v_supply}"] = {"dataset_type": "graph_i_e",
                                                    "t_j": t_j,
                                                    'v_g': v_g,
                                                    'v_supply': v_supply,
                                                    'r_g': r_g,
                                                    "graph_i_e": tdb.csv2array(f'{path}/{file}.csv')}
    ''' previous code
    e_off_25_600 = {"dataset_type": "graph_i_e",
                    "t_j": 25,
                    'v_g': -4,
                    'v_supply': 600,
                    'r_g': 2.5,
                    "graph_i_e": tdb.csv2array(f'{path}/switch_switching_eoff_2.5Ohm_600V_25deg_-4V.csv')}  # insert csv here
    e_off_25_800 = {"dataset_type": "graph_i_e",
                    "t_j": 25,
                    'v_g': -4,
                    'v_supply': 800,
                    'r_g': 2.5,
                    "graph_i_e": tdb.csv2array(f'{path}/switch_switching_eoff_2.5Ohm_800V_25deg_-4V.csv')}  # insert csv here
    '''
    charge_curve = {}
    if hasattr(transistor_loaded.switch, 'charge_curve'):
        for i in range(len(transistor_loaded.switch.charge_curve)):
            i_channel = transistor_loaded.switch.charge_curve[i].i_channel
            t_j = transistor_loaded.switch.charge_curve[i].t_j
            v_supply = transistor_loaded.switch.charge_curve[i].v_supply
            i_g = transistor_loaded.switch.charge_curve[i].i_g
            graph_q_v = transistor_loaded.switch.charge_curve[i].graph_q_v
            charge_curve[f"charge_curve_{i_channel}_{t_j}_{v_supply}_{i_g}"] = {"i_channel": i_channel,
                                                                                 "t_j": t_j,
                                                                                 "v_supply": v_supply,
                                                                                 "i_g": i_g,
                                                                                 "graph_q_v": graph_q_v}
    for file in os.listdir(path):
        if file.endswith("gate_charge.csv"):
            file = file.split(".csv")[0]
            i_channel = 20
            t_j = 25
            v_supply = 800
            i_g = 50e-3
            if f"charge_curve_{i_channel}_{t_j}_{v_supply}_{i_g}" not in charge_curve:
                charge_curve[f"charge_curve_{i_channel}_{t_j}_{v_supply}_{i_g}"] = {"i_channel": i_channel,
                                                                                     "t_j": t_j,
                                                                                     "v_supply": v_supply,
                                                                                     "i_g": i_g,
                                                                                     "graph_q_v": tdb.csv2array(f'{path}/{file}.csv', first_x_to_0=True)}
    ''' previous code  
    switch_gate_charge_curve_800 = {
        'i_channel': 20,
        't_j': 25,
        'v_supply': 800,
        'i_g': 50e-3,
        'graph_q_v': tdb.csv2array(f'{path}/gate_charge.csv', first_x_to_0=True)
    }  # insert csv here
    '''
    ron_args = {}
    if hasattr(transistor_loaded.switch, 'r_channel_th'):
        for i in range(len(transistor_loaded.switch.r_channel_th)):
            i_channel = transistor_loaded.switch.r_channel_th[i].i_channel
            v_g = transistor_loaded.switch.r_channel_th[i].v_g
            dataset_type = transistor_loaded.switch.r_channel_th[i].dataset_type
            r_channel_nominal = transistor_loaded.switch.r_channel_th[i].r_channel_nominal
            graph_t_r = transistor_loaded.switch.r_channel_th[i].graph_t_r
            ron_args[f"ron_args_{i_channel}_{v_g}"] = {"i_channel": i_channel,
                                                       "v_g": v_g,
                                                       "dataset_type": dataset_type,
                                                       "r_channel_nominal": r_channel_nominal,
                                                       "graph_t_r": graph_t_r}
    for file in os.listdir(path):
        if file.startswith("switch_on_res_vg_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            v_g = int(tdb.volt_to_numeric(file.split("_")[4]))
            i_channel = 75
            dataset_type = "t_r"
            r_channel_nominal = 16e-3
            if f"ron_args_{i_channel}_{v_g}" not in ron_args:
                ron_args[f"ron_args_{i_channel}_{v_g}"] = {"i_channel": i_channel,
                                                         "v_g": v_g,
                                                         "dataset_type": dataset_type,
                                                         "r_channel_nominal": r_channel_nominal,
                                                         "graph_t_r": tdb.csv2array(f'{path}/{file}.csv')}
    ''' previous code
    switch_ron_args_11 = {
        'i_channel': 75,
        'v_g': 11,
        'dataset_type': 't_r',
        'r_channel_nominal': 16e-3,
        'graph_t_r': tdb.csv2array(f'{path}/switch_on_res_vg_11V.csv')
    }  # insert csv here
    switch_ron_args_13 = {
        'i_channel': 75,
        'v_g': 13,
        'dataset_type': 't_r',
        'r_channel_nominal': 16e-3,
        'graph_t_r': tdb.csv2array(f'{path}/switch_on_res_vg_13V.csv')
    }  # insert csv here
    switch_ron_args_15 = {
        'i_channel': 75,
        'v_g': 15,
        'dataset_type': 't_r',
        'r_channel_nominal': 16e-3,
        'graph_t_r': tdb.csv2array(f'{path}/switch_on_res_vg_15V.csv')
    }  # insert csv here
    '''

    # switch foster parameters
    switch_foster_args = {
        # 'r_th_vector': r_th_vector,
        'r_th_total': 0.27,
        # 'c_th_vector': c_th_vector,
        # 'c_th_total': c_th_total,
        # 'tau_vector': tau_vector,
        # 'tau_total': tau_total,
        # 'graph_t_rthjc': graph_t_rthjc
    }
    # switch_foster_args = None
    soa = {}
    if hasattr(transistor_loaded.switch, 'soa'):
        for i in range(len(transistor_loaded.switch.soa)):
            t_c = transistor_loaded.switch.soa[i].t_c
            time_pulse = transistor_loaded.switch.soa[i].time_pulse
            graph_i_v = transistor_loaded.switch.soa[i].graph_i_v
            soa[f"soa_t_pulse_{time_pulse}"] = {'t_c': t_c, 'time_pulse': time_pulse, 'graph_i_v': graph_i_v}
    for file in os.listdir(path):
        if file.startswith("soa_t_pulse_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            time_pulse = tdb.time_to_numeric(file.split("_")[3])
            t_c = 25
            if f"soa_t_pulse_{time_pulse}" not in soa:
                soa[f"soa_t_pulse_{time_pulse}"] = {'t_c': t_c, 'time_pulse': time_pulse, 'graph_i_v': tdb.csv2array(f'{path}/{file}.csv')}
    ''' previous code
    soa_t_pulse_100ms = {'t_c': 25, 'time_pulse': 100e-3, 'graph_i_v': tdb.csv2array(f'{path}/soa_t_pulse_100ms.csv')}
    soa_t_pulse_1ms = {'t_c': 25, 'time_pulse': 1e-3, 'graph_i_v': tdb.csv2array(f'{path}/soa_t_pulse_1ms.csv')}
    soa_t_pulse_100us = {'t_c': 25, 'time_pulse': 100e-6, 'graph_i_v': tdb.csv2array(f'{path}/soa_t_pulse_100us.csv')}
    soa_t_pulse_10us = {'t_c': 25, 'time_pulse': 10e-6, 'graph_i_v': tdb.csv2array(f'{path}/soa_t_pulse_10us.csv')}
    '''
    # Bring the switch_args together
    switch_args = {
        'comment': comment,
        'manufacturer': manufacturer,
        'technology': technology,
        't_j_max': 175,
        'channel': list(channel.values()),
        'e_on': list(e_on.values()),
        'e_off': list(e_off.values()),
        'charge_curve': list(charge_curve.values()),
        'r_channel_th': list(ron_args.values()),
        'thermal_foster': switch_foster_args,
        'soa': list(soa.values())
    }

    ####################################
    # diode parameters
    ####################################
    comment = 'comment diode'
    manufacturer = 'manufacturer diode'
    technology = 'technology diode'

    # Channel parameters
    channel = {}
    if hasattr(transistor_loaded.diode, 'channel'):
        for i in range(len(transistor_loaded.diode.channel)):
            t_j = transistor_loaded.diode.channel[i].t_j
            v_g = transistor_loaded.diode.channel[i].v_g
            channel[f"channel_{t_j}_{v_g}"] = {"t_j": t_j, 'v_g': v_g, "graph_v_i": transistor_loaded.diode.channel[i].graph_v_i}
    for file in os.listdir(path):
        if file.startswith("diode_channel_") and file.endswith(".csv"):
            file = file.split(".csv")[0]
            t_j = int(tdb.temp_to_numeric(file.split("_")[2]))
            v_g = int(tdb.volt_to_numeric(file.split("_")[3].split("vgs")[0]))
            if f"channel_{t_j}_{v_g}" not in channel:
                channel[f"channel_{t_j}_{v_g}"] = {"t_j": t_j, 'v_g': v_g, "graph_v_i": tdb.csv2array(f'{path}/{file}.csv', first_xy_to_00=True)}

    ''' previous code
    channel_25_0 = {"t_j": 25,
                    'v_g': 0,
                    "graph_v_i": tdb.csv2array(f'{path}/diode_channel_25_0vgs.csv',
                    first_xy_to_00=True,
                    second_y_to_0=True,
                    mirror_xy_data=True)
                    
    }  # insert csv here
    channel_25_neg2 = {"t_j": 25, 'v_g': -2, "graph_v_i": tdb.csv2array(f'{path}/diode_channel_25_-2vgs.csv',
                                                                        first_xy_to_00=True, second_y_to_0=True, mirror_xy_data=True)}  # insert csv here
    channel_25_neg4 = {"t_j": 25, 'v_g': -4, "graph_v_i": tdb.csv2array(f'{path}/diode_channel_25_-4vgs.csv',
                                                                        first_xy_to_00=True, second_y_to_0=True, mirror_xy_data=True)}  # insert csv here

    channel_175_0 = {"t_j": 175, 'v_g': 0, "graph_v_i": tdb.csv2array(f'{path}/diode_channel_175_0vgs.csv',
                                                                      first_xy_to_00=True, second_y_to_0=True, mirror_xy_data=True)}  # insert csv here
    channel_175_neg2 = {"t_j": 175, 'v_g': -2, "graph_v_i": tdb.csv2array(f'{path}/diode_channel_175_-2vgs.csv',
                                                                          first_xy_to_00=True, second_y_to_0=True, mirror_xy_data=True)}  # insert csv here
    channel_175_neg4 = {"t_j": 175, 'v_g': -4, "graph_v_i": tdb.csv2array(f'{path}/diode_channel_175_-4vgs.csv',
                                                                          first_xy_to_00=True, second_y_to_0=True, mirror_xy_data=True)}  # insert csv here
    '''
    
    # diode foster parameters
    diode_foster_args = {
        # 'r_th_vector': r_th_vector,
        'r_th_total': 0,
        # 'c_th_vector': c_th_vector,
        # 'c_th_total': c_th_total,
        # 'tau_vector': tau_vector,
        # 'tau_total': tau_total,
        # 'graph_t_rthjc': graph_t_rthjc
    }

    diode_args = {'comment': comment,
                  'manufacturer': manufacturer,
                  'technology': technology,
                  't_j_max': 175,
                  'channel': list(channel.values()),
                  'e_rr': [],
                  'thermal_foster': diode_foster_args}

    ####################################
    # create transistor object
    ####################################
    return tdb.Transistor(transistor_args, switch_args, diode_args, possible_housing_types=database.housing_types,
                          possible_module_manufacturers=database.module_manufacturers)


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    db = tdb.DatabaseManager()
    db.set_operation_mode_json(path)

    # update the database
    # db.update_from_fileexchange(True)
    transistor_loaded = db.load_transistor('CREE_C3M0016120K')

    transistor = template_example(db, path)
    # Now save this transistor to the database local folder
    db_path = os.path.join(os.getcwd(), 'database')
    db.export_single_transistor_to_json(transistor, db_path)

    ####################################
    # Method examples
    ####################################

    # transistor methods #
    # transistor.wp.switch_v_channel, transistor.wp.switch_r_channel = transistor.calc_lin_channel(175, 15, 40, 'switch')
    # linearization at 175 degree, 15V gatevoltage, 40A channel current
    # print(f"{transistor.wp.switch_v_channel = } V")
    # print(f"{transistor.wp.switch_r_channel = } Ohm")
    # print(transistor.calc_v_eoss())
    # transistor.plot_v_eoss()
    # transistor.plot_v_qoss()

    # connect transistors in parallel
    # parallel_transistors = db.parallel_transistors(transistor, 3)
    # db.export_single_transistor_to_json(parallel_transistors, os.getcwd())

    # switch methods #
    # transistor.switch.plot_energy_data()
    # transistor.switch.plot_all_channel_data()
    # transistor.switch.plot_channel_data_vge(15)
    # transistor.switch.plot_channel_data_temp(175)

    # diode methods #
    # transistor.diode.plot_energy_data()
    # transistor.diode.plot_all_channel_data()

    ####################################
    # exporter example
    ####################################

    # Windows users: export datasheet
    # html_str = transistor.export_datasheet()

    # Linux users: export datasheet as html
    # look for CREE_C3M0016120K.html in template_example folder.
    # html_str = transistor.export_datasheet(build_collection=True)
    # Html_file = open(f"{transistor.name}.html", "w")
    # Html_file.write(html_str)
    # Html_file.close()

    # Export to MATLAB
    # transistor.export_matlab()

    # Export to SIMULINK
    # NOTE: Exporter is only working for IGBTs. This Template contains a SiC-MOSFET!
    # transistor.export_simulink_loss_model()

    # Export to PLECS
    # transistor.export_plecs()

    # Export to geckoCIRCUITS
    # transistor.export_geckocircuits(True, 600, 15, -4, 2.5, 2.5)

    ####################################
    # Database example
    ####################################

    # update the database
    # db.update_from_fileexchange(True)

    # print ALL database content
    # db.print_tdb()

    # print database content of housing and datasheet hyperlink
    # db.print_tdb(['housing_type','datasheet_hyperlink'])

    # load transistor
    # optional argument: collection. If no collection is specified, it connects to local TDB
    # transistor_loaded = db.load_transistor('CREE_C3M0016120K')
    # print(transistor_loaded.switch.t_j_max)

    # export to json
    # optional argument: path. If no path is specified, saves exports to local folder
    # db.export_single_transistor_to_json(transistor, os.getcwd())

    ####################################
    # Examples to fill-in transistor.wp-class
    ####################################
    # full-automated example
    # transistor.quickstart_wp()

    # half-automated example
    # transistor.update_wp(125, 15, 50)

    # non-automated example
    # # calculate energy and charge in c_oss
    # transistor.wp.e_oss = transistor.calc_v_eoss()
    # transistor.wp.q_oss = transistor.calc_v_qoss()
    #
    # # switch, linearize channel and search for loss curves
    # transistor.wp.switch_v_channel, transistor.wp.switch_r_channel = transistor.calc_lin_channel(25, 15, 150, 'switch')
    # transistor.wp.e_on = transistor.get_object_i_e('e_on', 25, 15, 600, 2.5).graph_i_e
    # transistor.wp.e_off = transistor.get_object_i_e('e_off', 25, -4, 600, 2.5).graph_i_e
    #
    # # diode, linearize channel and search for loss curves
    # transistor.wp.diode_v_channel, transistor.wp.diode_r_channel = transistor.calc_lin_channel(25, -4, 150, 'diode')
