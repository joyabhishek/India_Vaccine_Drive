from flask import Flask, render_template,request
import pandas as pd
from nvd3 import discreteBarChart

app = Flask(__name__)

def barChart(xData, yData, gid):
	chart = discreteBarChart(width=800, height=400, x_axis_format=None, resize =True, name=gid)
	xdata = xData
	ydata1 = yData

	chart.add_serie(name="Serie 1", y=ydata1, x=xdata)
	chart.buildcontent()
	return  chart.htmlcontent

@app.route('/', methods=["GET","POST"])
def index():
	df = pd.read_csv('Benef_Sessions_AEFI.csv')
	df_cumm = pd.read_csv('CumulativeVaccineCount.csv')
	df_single = pd.read_csv('SingleDayVaccineCount.csv')

	df_cumm = df_cumm.dropna()
	
	#Getting total vaccinated and Total AEFI
	totalBeneficiaries = df.iloc[0,-1]
	totalAEFI = df.iloc[2,-1]

	#Getting state wise latest cumulative beneficisries
	states = list(df_cumm['States/UN'].values)
	Date = df_cumm.iloc[:,-1].name
	vaccinated = list(df_cumm.iloc[:,-1].values)

	#Getting Date VS cumulative beneficiaries and sessions in total India
	dates = [" ".join(i.split('-')[:2]) for i in df.columns[1:]]
	cummVaccinated = [int("".join(i.split(','))) for i in df.iloc[0,1:].values]
	cummSessions = [int("".join(i.split(','))) for i in df.iloc[1,1:].values]

	#Get AEFI for requested date	
	dateReqvaccine = []
	dateReqInfo = None
	dateReqAEFI = None
	if request.method == "POST":
		dateReqInfo = request.form.get("date")
		print(f"Got Date: {dateReqInfo}")
		dateReqInfo = "-".join(dateReqInfo.split()) + "-21"
		print(f"Got Date: {dateReqInfo}")
		if dateReqInfo in df_single.columns:
			dateReqvaccine = list(df_single[dateReqInfo].values)
		dateReqAEFI = df[dateReqInfo][2]
		print(f"{dateReqvaccine} AEFI: {dateReqAEFI}")
	elif request.method == "GET":
		dateReqInfo = df_single.iloc[:,-1].name
		dateReqvaccine = list(df_single.iloc[:,-1].values)
		dateReqAEFI = df[dateReqInfo][2]
		
	#TODO: Fix the graph
	print(f"Total Beneficiaries:{totalBeneficiaries} Total AEFI: {totalAEFI}")
	return render_template("index.html",totalBeneficiaries=totalBeneficiaries, totalAEFI=totalAEFI, StatesVaccinated=zip(states,vaccinated), Date=Date, graph=barChart(dates,cummVaccinated,'g'), graph1=barChart(dates,cummSessions,'g1'), dates=dates,dateReqvaccine =  zip(states, dateReqvaccine) if len(dateReqvaccine) > 0 else None,
	dateReqInfo = dateReqInfo,
	dateReqAEFI = dateReqAEFI) 