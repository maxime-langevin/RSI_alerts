# import required libraries
import os
import smtplib
from email.message import EmailMessage
import requests
import yfinance as yf
import numpy as np
import pandas as pd 

def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

stocks_SBF120 = ["AC.PA", 
                 "ADP.PA", "AF.PA", "AI.PA", "ALO.PA", "ATE.PA",
                 "MT.PA", "AKE.PA", "ATO.PA", "CS.PA", "BEN.PA", "BB.PA", "BNP.PA", 
                 "BON.PA", "EN.PA", "BVI.PA", "CAP.PA","CA.PA", "CO.PA", 
                  "CU.PA", "CNP.PA", "ACA.PA", "BN.PA", "DSY.PA", "DBG.PA", "DEXB.PA", "EAD.PA", "EDF.PA", "EEN.PA", "FGR.PA", "ERA.PA", "EI.PA", "ELE.PA", "RF.PA", "ERF.PA", "ETL.PA", "FIM.PA", "FDR.PA", "FTE.PA", "GSZ.PA", "GFC.PA", "GTO.PA", "GET.PA", "RIA.PA", "HAV.PA", "RMS.PA", "ICAD.PA", "ILD.PA", "NK.PA", "IMS.PA", "ING.PA", "IPN.PA", "IPS.PA", "DEC.PA", "LI.PA", "OR.PA", "LG.PA", "MMB.PA", "LR.PA", "MC.PA", "MAU.PA", "MMT.PA", "ML.PA", "KN.PA", "NEO.PA", "NEX.PA", "NXI.PA", "COX.PA", "ORP.PA", "PAJ.PA", "RI.PA", "UG.PA", "PP.PA", "PUB.PA", "RCO.PA", "RNO.PA", "RXL.PA", "RHA.PA", "SK.PA", "SAF.PA", "SAFT.PA", "SGO.PA", "SAN.PA", "SU.PA", "SCR.PA", "SCHP.PA", "SECH.PA", "SESG.PA", "SIL.PA", "GLE.PA", "SW.PA", "SOI.PA", "SPR.PA", "GENP.PA", "STM.PA", "SEV.PA", "TEC.PA", "RCF.PA", "TFI.PA", "HO.PA", "TMS.PA", "FP.PA", "UBI.PA", "UL.PA", "FR.PA", "VK.PA", "VIE.PA", "RIN.PA", "DG.PA", "VIV.PA", "MF.PA", "ZC.PA"]

stocks_cac40 = ["AC.PA", "AI.PA", "ALU.PA", "ALO.PA", "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "CAP.PA", "CA.PA", "ACA.PA", "BN.PA", "DEXB.PA", "EAD.PA", "EDF.PA", "EI.PA", "FTE.PA", "GSZ.PA", "OR.PA", "LG.PA", "LR.PA", "MMB.PA", "MC.PA", "ML.PA", "RI.PA", "UG.PA", "PP.PA", "RNO.PA", "SGO.PA", "SAN.PA",
                "SU.PA", "GLE.PA", "STM.PA", "TEC.PA", "FP.PA", "UL.PA", "VK.PA", "VIE.PA", "DG.PA", "VIV.PA"]

interesting_stocks_SBF120 = []
for s in stocks_SBF120:
    try:
        msft = yf.Ticker(s)
        hist = msft.history(period="50d")
        rsi_stock = list(rsi(hist))[-1]
        info = msft.get_info()
        if rsi_stock<30:
            interesting_stocks_SBF120.append(s + ": " + info["sector"])
    except:
        pass
    
interesting_stocks_cac40 = []
for s in stocks_cac40:
    try:
        msft = yf.Ticker(s)
        hist = msft.history(period="50d")
        rsi_stock = list(rsi(hist))[-1]
        info = msft.get_info()
        if rsi_stock<30:
            interesting_stocks_cac40.append(s + ": " + info["sector"])
    except:
        pass
    
# Fetch dog image
dog_url = requests.get('https://dog.ceo/api/breeds/image/random').json()['message']

cac40 = "\n Stocks from the CAC40 with below 30 RSI: \n"
for s in interesting_stocks_cac40:
    cac40 += s
    cac40 += '\n'

sbf120 = "\n Stocks from the SBF120 with below 30 RSI: \n"
for s in interesting_stocks_SBF120:
    sbf120 += s
    sbf120 += '\n'
# Message to send if HTML is disabled

message_body = ""
message_body += cac40
message_body += sbf120

html_message = ""

html_message += cac40
html_message += sbf120

# Google Auth secrets
user = os.environ.get('EMAIL_USER')
password = os.environ.get('EMAIL_PASSWORD')


# Email content
msg = EmailMessage()

msg['Subject'] = '🐕'
msg['From'] = user
msg['To'] = ['maximelangevin5@gmail.com']
msg.set_content(message_body)
msg.add_alternative(html_message, subtype='html')

# Send Email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(user, password)

    smtp.send_message(msg)


