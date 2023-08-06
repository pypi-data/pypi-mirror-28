def analysis():
	from pydoc import help  # can type in the python console `help(name of function)` to get the documentation
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt
	import seaborn as sns
	from sklearn.preprocessing import scale
	from sklearn.decomposition import PCA
	from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
	from scipy import stats
	from IPython.display import display, HTML
	import os
	np.set_printoptions(suppress=True)
	DISPLAY_MAX_ROWS = 20  # number of max rows to print for a DataFrame
	pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)

	this_dir, this_filename = os.path.split(__file__)
	DATA_PATH = os.path.join(this_dir, "data", "Profilingdata_combined_nozero_3basic.csv")

	data0 = pd.read_csv(DATA_PATH, sep=',', thousands=',',header=0)
	data1 = data0.copy()
	data1.columns = ["V"+str(i) for i in range(1, len(data1.columns)+1)]  # rename column names to be similar to R naming convention
	data1.V1 = data1.V1.astype(str)
	# replace % to float
	data1[['V2', 'V3', 'V4', 'V5']] = data1[['V2', 'V3', 'V4', 'V5']].replace('%','',regex=True).astype('float')/100

	data1_sub_cpu = data1.loc[:, "V1":"V6"]
	# obtain subset with different applications
	data1_sub_cpu_canny = data1_sub_cpu[:48]
	data1_sub_cpu_harris = data1_sub_cpu[48:104]
	data1_sub_cpu_optical = data1_sub_cpu[104:151]

	# returns a numpy array from dataframe
	values_canny = data1_sub_cpu_canny.values
	values_optical = data1_sub_cpu_optical.values
	values_harris = data1_sub_cpu_harris.values

	# first column: time stamps of applications
	x_canny = values_canny[:,0]
	x_harris = values_harris[:,0]
	x_optical = values_optical[:,0]

	# can be optimized with using loop or dummy
	y1_canny = values_canny[:,1]
	y2_canny = values_canny[:,2]
	y3_canny = values_canny[:,3]
	y4_canny = values_canny[:,4]
	y5_canny = values_canny[:,5]

	y1_harris = values_harris[:,1]
	y2_harris = values_harris[:,2]
	y3_harris = values_harris[:,3]
	y4_harris = values_harris[:,4]
	y5_harris = values_harris[:,5]

	y1_optical = values_optical[:,1]
	y2_optical = values_optical[:,2]
	y3_optical = values_optical[:,3]
	y4_optical = values_optical[:,4]
	y5_optical = values_optical[:,5]
	print("Obtaining CPU Utilization of Canny")

	import matplotlib
	#matplotlib.use('Agg')
	matplotlib.pyplot.switch_backend('agg')
	import matplotlib.pyplot as plt
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y1_canny, label="CPU_A15_user")
	plt.plot(x_canny, y2_canny, label="CPU_A15_System")
	plt.plot(x_canny, y3_canny, label="CPU_A7_user")
	plt.plot(x_canny, y4_canny, label="CPU_A7_System")
	plt.plot(x_canny, y5_canny, label="CPU_Time_Idle")
	plt.legend(shadow=True, fancybox=True)
	plt.title("CPU Utilization of Canny")
	plt.savefig("./figures/CPU_Utilization_of_Canny.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Comparison of CPU_A15_user")
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y1_canny, label="canny_CPU_A15_user")
	plt.plot(x_harris, y1_harris, label="harris_CPU_A15_user")
	plt.plot(x_optical, y1_optical, label="optical_CPU_A15_user")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Comparison of CPU_A15_user")
	plt.savefig("./figures/Comparison_of_CPU_A15_user.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Comparison of CPU_A15_System")
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y2_canny, label="canny_CPU_A15_System")
	plt.plot(x_harris, y2_harris, label="harris_CPU_A15_System")
	plt.plot(x_optical, y2_optical, label="optical_CPU_A15_System")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Comparison of CPU_A15_System")
	plt.savefig("./figures/Comparison_of_CPU_A15_System.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Comparison of CPU_A7_user")
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y3_canny, label="canny_CPU_A7_user")
	plt.plot(x_harris, y3_harris, label="harris_CPU_A7_user")
	plt.plot(x_optical, y3_optical, label="optical_CPU_A7_user")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Comparison of CPU_A7_user")
	plt.savefig("./figures/Comparison_of_CPU_A7_user.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Comparison of CPU_A7_System")
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y4_canny, label="canny_CPU_A7_System")
	plt.plot(x_harris, y4_harris, label="harris_CPU_A7_System")
	plt.plot(x_optical, y4_optical, label="optical_CPU_A7_System")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Comparison of CPU_A7_System")
	plt.savefig("./figures/Comparison_of_CPU_A7_System.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Comparison of CPU_Time_Idle")
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y5_canny, label="canny_CPU_Time_Idle")
	plt.plot(x_harris, y5_harris, label="harris_CPU_Time_Idle")
	plt.plot(x_optical, y5_optical, label="optical_CPU_Time_Idle")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Comparison of CPU_Time_Idle")
	plt.savefig("./figures/Comparison_of_CPU_Time_Idle.eps", format='eps', dpi=1000, bbox_inches='tight')

	# normalize raw data
	# data2 -- normalized dataset
	data2 = data1.copy()
	from sklearn.preprocessing import MinMaxScaler
	scaler = MinMaxScaler()
	scaled_values = scaler.fit_transform(data2.loc[:, "V2":"V21"])
	data2.loc[:, "V2":"V21"] = scaled_values
	data2_sub_memory = data2.loc[:, "V18":"V21"]

	# canny memory subset
	data2_sub_mem_canny = data2_sub_memory[:48]
	values_canny_mem = data2_sub_mem_canny.values # returns a numpy array
	y1_canny_mem = values_canny_mem[:,0]
	y2_canny_mem = values_canny_mem[:,1]
	y3_canny_mem = values_canny_mem[:,2]
	y4_canny_mem = values_canny_mem[:,3]

	print("Obtaining Canny Memory Utilization")
	import matplotlib
	#matplotlib.use('Agg')
	matplotlib.pyplot.switch_backend('agg')
	import matplotlib.pyplot as plt
	plt.figure(figsize=(12,3))
	plt.plot(x_canny, y1_canny_mem, label="Mem_Cached")
	plt.plot(x_canny, y2_canny_mem, label="Mem_Free")
	plt.plot(x_canny, y3_canny_mem, label="Mem_Slab")
	plt.plot(x_canny, y4_canny_mem , label="Mem_Used")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Canny memory")
	plt.savefig("./figures/Memory_Utilization_of_Canny.eps", format='eps', dpi=1000, bbox_inches='tight')

	data2_sub_mem_harris = data2_sub_memory[48:104]
	values_harris_mem = data2_sub_mem_harris.values

	y1_harris_mem = values_harris_mem[:,0]
	y2_harris_mem = values_harris_mem[:,1]
	y3_harris_mem = values_harris_mem[:,2]
	y4_harris_mem = values_harris_mem[:,3]

	data2_sub_mem_optical = data2_sub_memory[104:151]
	values_optical_mem = data2_sub_mem_optical.values
	y1_optical_mem = values_optical_mem[:,0]
	y2_optical_mem = values_optical_mem[:,1]
	y3_optical_mem = values_optical_mem[:,2]
	y4_optical_mem = values_optical_mem[:,3]

	print("Obtaining Harris Memory Utilization")
	plt.figure(figsize=(12,3))
	plt.plot(x_harris, y1_harris_mem, label="Mem_Cached")
	plt.plot(x_harris, y2_harris_mem, label="Mem_Free")
	plt.plot(x_harris, y3_harris_mem, label="Mem_Slab")
	plt.plot(x_harris, y4_harris_mem, label="Mem_Used")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Harris memory")
	plt.savefig("./figures/Memory_Utilization_of_Harris.eps", format='eps', dpi=1000, bbox_inches='tight')

	print("Obtaining Optical Memory Utilization")
	plt.figure(figsize=(12,3))
	plt.plot(x_optical, y1_optical_mem, label="Mem_Cached")
	plt.plot(x_optical, y2_optical_mem, label="Mem_Free")
	plt.plot(x_optical, y3_optical_mem, label="Mem_Slab")
	plt.plot(x_optical, y4_optical_mem, label="Mem_Used")
	plt.legend(shadow=True, fancybox=True)
	plt.title("Optical memory")
	plt.savefig("./figures/Memory_Utilization_of_Optical.eps", format='eps', dpi=1000, bbox_inches='tight')
