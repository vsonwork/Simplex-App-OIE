import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(
	page_title = "Simplex App",
	page_icon = "1️⃣",
	layout="wide"
)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://raw.githubusercontent.com/vsonwork/Simplex-App-OIE/main/img/background_main.jpg?token=GHSAT0AAAAAACBEEOWHVKVZSZE5WPCU7ZVCZDC4CBQ");
background-size: 150%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://raw.githubusercontent.com/vsonwork/Simplex-App-OIE/main/img/background_sida.webp?token=GHSAT0AAAAAACBEEOWGKNFY6SERGIVWB3W6ZDC4CIA");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
</style>
"""

st.title("Problem")


with st.sidebar:
	n = st.number_input('How many decision variables are the problem?', value = 3, min_value = 1, max_value = 9, step = 1)
	constraint = st.number_input('How many constraints? ', value = 3, min_value = 1, max_value = 15, step = 1)
	option = st.selectbox(
	    'Which is the objective of the function?',
	    ('Maximize', 'Minimize'))

str_constraints = []
str_object = []
var_constraint = []
num_cols_var = [1] + [.8,.2,.2] * n
num_cols_constraint = [0.8,0.2,0.2] * (n - 1) + [0.8,0.2,1,0.8]
num_cols_var_constraint = [.1, .3, .1] * (n - 1) + [.1,.3] 

cols_var = st.columns(num_cols_var)
cols_constraint = st.columns(num_cols_constraint)
cols_var_constraint = st.columns(num_cols_var_constraint)

var = 1
for i, col in enumerate(cols_var):
	if i != 0:
		if (i-1) % 3 == 0:
			str_object.append(col.text_input("", label_visibility = "collapsed", key=i))
		elif (i-1) % 3 == 1:
			col.latex(f"x_{var}")
			var += 1
		elif i != n*3:
			col.latex("+")
	else:
		if option == "Minimize":
			col.latex("min \hspace{0.5cm} z \hspace{0.2cm}= ")
		else:
			col.latex("max \hspace{0.5cm} z \hspace{0.2cm}= ")



for j in range(constraint):
	var = 1
	for i, col in enumerate(cols_constraint):
		if i <= n*3 - 2:
			if i % 3 == 0:
				str_constraints.append(col.text_input("", label_visibility = "collapsed", key=i*constraint + j + 100**2))
			elif i % 3 == 1:
				col.latex(f"x_{var}")
				var += 1
			else:
				col.latex("+")

		elif i == n*3 - 1:
			str_constraints.append(col.selectbox("", ['≤', '≥', '='], label_visibility = "collapsed", key = i*constraint + j + n*constraint))
		else:
			str_constraints.append(col.text_input("", label_visibility = "collapsed", key=i*constraint + j + n*constraint))


latex_var_constraint = "\\\\"
for i, col in enumerate(cols_var_constraint):
	if i % 3 == 0:
		j = int(i/3) + 1
		col.latex(f"x_{j}")
		latex_var_constraint += "x_{" +str(j) + "}"
	elif i % 3 == 1:
		temp = col.selectbox("", ['≥ 0', '≤ 0'], label_visibility = "collapsed", key = 100**3 + i)
		latex_var_constraint += temp
		var_constraint.append(temp)
	else:
		col.latex(",")
		latex_var_constraint += ','

st.divider()
if (st.button( "Start")):
	def change_arr2D(str_object, str_constraints):
	    if option == "Minimize":
	        arr_var = [eval(val) for val in str_object]
	    else:
	        arr_var = [-eval(val) for val in str_object]
	    arr_constraint = [str_constraints[i:i+n+2] for i in range(0, (n+2)*constraint, n+2)]
	    return arr_var, arr_constraint

	def pos_neg(num_str, i):
		if eval(num_str) >= 0:
			if i == 0:
				text = num_str + "x_{" + str(i+1) + "}"
			else:
				text = "+" + num_str + "x_{" + str(i+1) + "}"
		else:
			text = num_str + "x_{" + str(i+1) + "}"
		return text


	def P_LaTeX(n, constraint, str_object, arr_constraint):
		P = [[''] for i in range(constraint+1)]
		if option == "Maximize":
		    op = "max \hspace{0.2cm} z="
		else:
		    op = "min \hspace{0.2cm} z="
		for i in range(n):
		    if i == 0:
		        P[i][i] += op
		    for j in range(constraint + 1):
		        if j == 0:
		            P[j][0] += pos_neg(str_object[i], i)
		        else:
		            P[j][0] += pos_neg(arr_constraint[j-1][i], i)

		for i in range(constraint):
		    P[i+1][0] += arr_constraint[i][-2] + arr_constraint[i][-1]
		latex_str = '\\\\'.join([P[i][0] for i in range(len(P))])
		st.latex('(P):\\begin{cases}' + ''.join(latex_str)  + latex_var_constraint+ '\\end{cases}')

	def simplex(arr, first = None, C = None, id = -1):
	    temp = arr[0].copy()
	    temp[0] = 0
	    if any(arr[1:,0] == 0):
	        index = next(i for i, x in enumerate(temp) if x < 0)
	    else:
	        index = temp.argmin()
	    
	    for i in range(len(arr)-1):
	        if arr[1+i, index] > 0:
	            if id == -1:
	                f_min = arr[1+i, 0]/arr[1+i, index]
	                id = 1+i
	            elif (f_min > arr[1+i, 0]/arr[1+i, index]):
	                f_min = arr[1+i, 0]/arr[1+i, index]
	                id = 1+i
	            

	    if id != -1:
	        if C or first: C[id-1] = -first[index]
	        arr[id] /= arr[id, index]        
	        for i in range(len(arr)):
	            if i != id:
	                arr[i] -= arr[id] * arr[i, index]
	    else:
	    	if option == "Minimize":
	    		result = "Solution is unbounded ⇒ " + "$(P): z = -\infty$"
	    	else:
	    		result = "Solution is unbounded ⇒ " + "$(P): z = +\infty$"
	    	exit(st.markdown(f'__<p style="color:#e5fce2; text-align:left; height: 45px; font-size:1.5rem; background:  hsl(89, 85%, 53%, .2); border-radius: 8px;"> &ensp; {result} </p>__', unsafe_allow_html=True))
	        

	    return arr

	def simpex_TwoPhase(arr, C):
		first = arr[0].copy()
		arr[0] = 0.0
		#st.write(C)
		for i in range(len(C)):
			arr[0] += arr[i+1] * np.array(C[i])

		#st.dataframe(pd.DataFrame(arr))
		while arr[0][0]:
			if arr[0, 1:].min() < 0: 
				arr = simplex(arr, first, C)
				#st.dataframe(pd.DataFrame(arr))
				if abs(arr[0][0]) <= 1.0e-14: arr[0][0] = 0
			else:
				break
		if arr[0][0] != 0: 
			exit(st.markdown('__<p align=center style="color:#e5fce2; text-align:left; height: 45px; font-size:1.5rem; background:  hsl(350, 31%, 55%, .5); border-radius: 8px;"> &ensp; There is no solution to the problem. </p>__', unsafe_allow_html=True))
			
			arr[0] = 0.0    
		for i in range(len(C)):
			arr[0] += arr[i+1] * np.array(C[i])
		arr[0] += first

		for j in range(1, len(arr[0])):
			if sum(arr[i][j] == 0 for i in range(1, len(arr))) == len(arr) - 2 and sum(arr[i][j] == 1 for i in range(1, len(arr))) == 1:
				arr[0][j] = 0  
		return arr

	def preprocessing(arr_var, arr_constraint, var_constraint, n = n, constraint = constraint):
	    new_arr = [[eval(val) for idx, val in enumerate(row) if idx != n] for row in arr_constraint]
	    
	    for i in range(n):
	        if var_constraint[i] == "≤ 0":
	            arr_var[i] = -arr_var[i]
	            for j in range(constraint):
	                new_arr[j][i] = -new_arr[j][i]


	    for i in range(constraint):
	        if new_arr[i][n] < 0:
	            new_arr[i] = [-val for val in new_arr[i]]
	            if arr_constraint[i][n] == "≤":
	                arr_constraint[i][n] = "≥"
	            elif arr_constraint[i][n] == "≥":
	                arr_constraint[i][n] = "≤"
	    
	    num = [1,0,0]
	    C = [0.0] * constraint
	    for i in range(constraint):
	        if arr_constraint[i][n] == "≤":
	            new_arr[i].append(1.0)
	            num[0] += 1
	            for j in range(constraint):
	                if j != i:
	                    new_arr[j].append(0.0)
	        elif arr_constraint[i][n] == "≥":
	            num[1] += 1
	            new_arr[i].append(-1.0)
	            C[i] = -1.0
	            for j in range(constraint):
	                if j != i:
	                    new_arr[j].append(0.0)
	        else:
	            C[i] = -1.0
	            num[2] += 1
	    arr_var = arr_var + [0.0] * (num[0] + num[1])
	    new_arr.insert(0, arr_var)
	    arr = np.array(new_arr)
	    #print(arr)
	    new_order = [n] + [i for i in range(arr.shape[1]) if i != n]
	    arr = arr[:, new_order]
	    
	    
	    return simpex_TwoPhase(arr.copy(), C) if num[1] > 0 or num[2] > 0 else arr

	
	def calculator(arr, option):
	    while (1):
	        if arr[0, 1:].min() < 0: 
	            arr = simplex(arr)
	        else:
	            break

	    
	    var = list()
	    problem = 0
	    for i in range(1, n+1):
	    	if arr[0][i] == 0:
	    		num = [0,0]
	    		for j in range(1, len(arr)):
	    			if arr[j][i] == 1: 
	    				num[0] += 1
	    				index = j
	    			if arr[j][i] == 0: num[1] += 1
	    		if num[0] == 1 and num[1] == constraint - 1:
	    			var.append(arr[index][0] if var_constraint[i-1] == "≥ 0" else -arr[index][0])
	    		else:
	    			problem = 1
	    			var.append(0)
	    	else:
	    		var.append(0)
	    
	    return arr[0,0] if option == "Maximize" else -arr[0,0], var, problem

	def is_real_number(num):
	    try:
	        eval(num)
	        return True
	    except SyntaxError:
	        return False

	str_object = ["0" if val == "" else val for val in str_object]
	str_constraints = ["0" if val == "" else val for val in str_constraints]

	for val in str_object:
		if is_real_number(val) == False:
			exit(st.error("ERROR: You must fill in all the fields with real numbers."))

	arr_var, arr_constraint = change_arr2D(str_object, str_constraints)
	if any(not is_real_number(arr_constraint[j][i]) for i in range(n + 2) if i != n for j in range(constraint)):
		exit(st.error("ERROR: You must fill in all the fields with real numbers."))

	P_LaTeX(n, constraint, str_object, arr_constraint)


	arr = preprocessing(arr_var, arr_constraint, var_constraint)	

	def isVariable(a):
		return 1 if abs(a - round(a)) <= 1e-10 else 0

	obj, variables, problem = calculator(arr, option)
	st.divider()

	if problem == 1:
		st.markdown('__<p style="font-family:sans-serif; color:White; font-size: 20px;"> There are infinitely many values . One of them: </p>__', unsafe_allow_html=True)
	else:
		st.markdown('__<p style="font-family:sans-serif; color:White; font-size: 20px;"> Optimal solution: </p>__', unsafe_allow_html=True)

	for i, var in enumerate(variables):
		if isVariable(var):
			st.markdown(f"&ensp;&ensp;$x_{i+1} = {round(var)}$")
		else:
			st.markdown(f"&ensp;&ensp;$x_{i+1} = {var}$")

	if isVariable(obj):
		result = "The optimal value $(P): z = " + str(round(obj)) +"$"
	else:
		result = "The optimal value $(P): z = " + str(obj) + "$"

	st.markdown(f'__<p style="color:#e5fce2; text-align:left; height: 45px; font-size:1.5rem; background:  hsl(188, 100%, 37%, .5); border-radius: 8px;"> &ensp; {result} </p>__', unsafe_allow_html=True)
	

	if n == 2:
		plt.style.use('_mpl-gallery')

		# make data
		x = np.linspace(variables[0] - 10, variables[0] + 10, 100)


		# plot
		fig, ax = plt.subplots(figsize=(8,5))

		for i in range(constraint): 
			if eval(arr_constraint[i][1]) < 0:
				f = f"${arr_constraint[i][0]}x_1 {arr_constraint[i][1]}x_2 = {arr_constraint[i][3]}$"
			else:
				f = f"${arr_constraint[i][0]}x_1 + {arr_constraint[i][1]}x_2 = {arr_constraint[i][3]}$"
			ax.plot(x, (eval(arr_constraint[i][3]) - eval(arr_constraint[i][0])*x)/eval(arr_constraint[i][1]), linewidth=1.5, label=f)

		ax.axhline(0, color='black')  

		ax.axvline(0, color='black') 
		plt.plot(variables[0], variables[1], 'ro')

		ax.set(xlim=(variables[0] - 5, variables[0] + 5), 
		       ylim=(variables[1] - 5, variables[1] + 5))
		
		plt.xlabel("$x_1$")

		plt.ylabel("$x_2$")
		plt.legend()

		_, col_plot, _ = st.columns([1, 4, 1], gap="small")
		col_plot.pyplot(fig)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
		
