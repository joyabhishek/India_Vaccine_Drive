from flask import Flask, render_template
import pandas as pd
from nvd3 import discreteBarChart

app = Flask(__name__)

def barChart(xData, yData):
	chart = discreteBarChart(width=700, height=400, x_axis_format=None, name='Hi')
	xdata = xData
	ydata1 = yData

	chart.add_serie(name="Serie 1", y=ydata1, x=xdata)
	chart.buildcontent()
	return  chart.htmlcontent

@app.route('/')
def index():
	df = pd.read_csv('Benef_Sessions_AEFI.csv')
	df_cumm = pd.read_csv('CumulativeVaccineCount.csv')
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

	print(f"Total Beneficiaries:{totalBeneficiaries} Total AEFI: {totalAEFI}")
	return render_template("index.html",totalBeneficiaries=totalBeneficiaries, totalAEFI=totalAEFI, StatesVaccinated=zip(states,vaccinated), Date=Date, graph=barChart(dates,cummVaccinated)) 