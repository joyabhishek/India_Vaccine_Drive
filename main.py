from flask import Flask, render_template,request
import pandas as pd
from nvd3 import discreteBarChart
import locale
locale.setlocale(locale.LC_NUMERIC, '')

app = Flask(__name__)

def barChart(xData, yData, gid):
	
	chart = discreteBarChart(width=800, height=400, x_axis_format=None, resize =True, name=gid)
	xdata = xData
	ydata1 = yData

	chart.add_serie(name="Serie 1", y=ydata1, x=xdata)
	chart.buildcontent()
	return  chart.htmlcontent

def formatNumbers(nums):
	return [locale.format("%d", num, grouping=True) for num in nums]

def getLatestDate(df):
	return sorted(list(df.columns[2:]))[-1]

@app.route('/', methods=["GET","POST"])
def index():
	df = pd.read_csv('Benef_Sessions_AEFI_Latest.csv')
	df_cumm = pd.read_csv('CumulativeVaccineCount_Latest.csv')
	df_single = pd.read_csv('SingleDayVaccineCount_Latest.csv')

	df_cumm = df_cumm.dropna()
	

	#Getting total vaccinated and Total AEFI
	Benef_Sessions_AEFI_Latestdate = getLatestDate(df)
	totalBeneficiaries = df[Benef_Sessions_AEFI_Latestdate][0]
	totalAEFI = locale.format("%d", df.iloc[2][1:].astype('int').sum(), grouping=True)

	#Getting state wise latest cumulative beneficisries
	Date = getLatestDate(df_cumm) #Get latest date
	states = list(df_cumm.sort_values(by=[Date],ascending=False)['States/UN'].values)
	vaccinated = formatNumbers(list(df_cumm.sort_values(by=[Date],ascending=False)[Date].values))

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
			dateReqvaccine = formatNumbers(list(df_single[df_single[dateReqInfo] > 0].sort_values(by=[dateReqInfo],ascending=False)[dateReqInfo].values))
			dateReqstates = list(df_single[df_single[dateReqInfo] > 0].sort_values(by=[dateReqInfo],ascending=False)['States/UN'].values)
		dateReqAEFI = df[dateReqInfo][2]
		print(f"{dateReqvaccine} AEFI: {dateReqAEFI}")
	elif request.method == "GET":
		dateReqInfo = getLatestDate(df_single)
		#dateReqInfo = df_single.iloc[:,-1].name
		dateReqstates = list(df_single[df_single[dateReqInfo] > 0].sort_values(by=[dateReqInfo],ascending=False)['States/UN'].values)
		dateReqvaccine = formatNumbers(list(df_single[df_single[dateReqInfo] > 0].sort_values(by=[dateReqInfo],ascending=False)[dateReqInfo].values))
		# list(df_single.iloc[:,-1].values)
		dateReqAEFI = df[dateReqInfo][2]
		
	#TODO:  
	#Get the total population,
	print(f"Total Beneficiaries:{totalBeneficiaries} Total AEFI: {totalAEFI}")
	return render_template("index.html",totalBeneficiaries=totalBeneficiaries, totalAEFI=totalAEFI, StatesVaccinated=zip(states,vaccinated), Date=Date, graph=barChart(dates,cummVaccinated,'g'), graph1=barChart(dates,cummSessions,'g1'), dates=dates,dateReqvaccine =  zip(dateReqstates, dateReqvaccine) if len(dateReqvaccine) > 0 else None,
	dateReqInfo = dateReqInfo,
	dateReqAEFI = dateReqAEFI) 