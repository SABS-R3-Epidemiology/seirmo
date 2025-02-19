import pandas as pd

data_path = 'examples/epiabm_rt_inference/northern_ireland/NI_outputs/'

true_rt_df_r1 = pd.read_csv(data_path + 'data_r_1/secondary_infections_E_1.csv')
true_rt_r1 = true_rt_df_r1['R_t'].values
pd.save_csv(data_path + 'data_r_1/true_rt.csv', true_rt_r1)

true_rt_df_r2 = pd.read_csv(data_path + 'data_r_2/secondary_infections_E_1.csv')
true_rt_r2 = true_rt_df_r2['R_t'].values
pd.save_csv(data_path + 'data_r_2/true_rt.csv', true_rt_r2)


time_data_r1 = pd.read_csv(data_path + 'data_r_1/inf_status_history.csv')
time_data_r02 = pd.read_csv(data_path + 'data_r_02/inf_status_history.csv')

# Get the initial infection
initial_infection_time_r1 = 0
for i in range(3, 9):
    initial_infection_time_r1 += time_data_r1.iloc[0, 1:].value_counts().get(i, 0)

# Generate the incidences of the true infection data
incidences_true_r1 = []
for ind, row in time_data_r1.iterrows():
    if ind < len(time_data_r1) - 1:
        incidence = 0
        element_zero = []
        for i in range(1, len(row)):
            if row[i] == 1:
                element_zero.append(i)
        if len(element_zero) > 0:
            for i in element_zero:
                if time_data_r1.iloc[ind + 1, i] > 2 and time_data_r1.iloc[ind + 1, i] < 9:
                    incidence += 1
        incidences_true_r1.append(incidence)
    else:
        break
incidences_true_r1.insert(0, initial_infection_time_r1)

initial_infection_time_r02 = 0
for i in range(3, 9):
    initial_infection_time_r02 += time_data_r1.iloc[0, 1:].value_counts().get(i, 0)

# Generate the incidences of the true infection data
incidences_true_r02 = []
for ind, row in time_data_r02.iterrows():
    if ind < len(time_data_r02) - 1:
        incidence = 0
        element_zero = []
        for i in range(1, len(row)):
            if row[i] == 1:
                element_zero.append(i)
        if len(element_zero) > 0:
            for i in element_zero:
                if time_data_r02.iloc[ind + 1, i] > 2 and time_data_r02.iloc[ind + 1, i] < 9:
                    incidence += 1
        incidences_true_r02.append(incidence)
    else:
        break
incidences_true_r02.insert(0, initial_infection_time_r02)

# Save the incidences data to CSV files
pd.DataFrame(incidences_true_r1).to_csv(data_path + 'incidences_true_r1.csv', index=False, header=False)
pd.DataFrame(incidences_true_r02).to_csv(data_path + 'incidences_true_r02.csv', index=False, header=False)