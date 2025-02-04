import streamlit as st
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import pandas as pd
import requests


st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(
    page_title="Pencarian Status Terupdate",
    initial_sidebar_state="expanded",
)

list2 = []

with st.expander("Input AuthToken"):
    at = st.text_input("")

st.title("Pencarian Status Terupdate ")
default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0), datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=1)
col1, col2 = st.columns([3, 1])
with col1:
    date_range_string = date_range_picker(picker_type=PickerType.time,
                                            start=default_start, end=default_end,
                                            key='time_range_picker')
    if date_range_string:
            start, end = date_range_string
    else:
        start = " "
        end = " "



with col2:
    option = st.selectbox(
        "Jenis Scan :",
        ("---","Scan Kirim","Scan Sampai","Pack",'Unpack','Scan Kirim Mobil','Scan Sampai Mobil','Scan kirim AF','Scan sampai AF'))
    if option == "Scan Kirim":
        scanType = 2
    if option == "Scan Sampai":
        scanType = 3
    if option == "Pack":
        scanType = 9
    if option == "Unpack":
        scanType = 10
    if option == "Scan Kirim Mobil":
        scanType = 11
    if option == "Scan Sampai Mobil":
        scanType = 12
    if option == "Scan kirim AF":
        scanType = 15
    if option == "Scan sampai AF":
        scanType = 16
    if option == "---":
        scanType = " "

payload = {
    "current": 1,
    "size": 50000,
    "type": 1,
    "inputStartTime": start,
    "inputEndTime": end,
    "scanType": scanType,
    "codeType": 0,
    "billCodes": [],
    "scanFinanceCode": [],
    "scanSiteCode": ["SOC999"],
    "countryId": "1"
}


headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "authtoken": f"{at}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "Content-Type": "application/json",
    "lang": "ID",
    "langtype": "ID"
}

try:
    list = []
    url = "https://jmsgw.jntexpress.id/operatingplatform/waybill/pageQueryLastStatus"
    if option == "---":
        False
    else:
        response = requests.request("POST", url, json=payload, headers=headers)
        rjson = response.json()
        
        for x in rjson["data"]["records"]:
            awb = x["waybillNo"]
            scanTime = x["scanTime"]
            scanUser = x["scanUser"]
            packageCode = x["packageCode"]
            nineCharCode = x["nineCharCode"]
            scanType = x["scanType"]
            previousOrNextSiteCode = x['previousOrNextSiteCode']
            destinationName = x["destinationName"]
            receiverProvinceName = x["receiverProvinceName"]
            expressTypeName = x["expressTypeName"]
            final = {'No.Waybill' : awb,'Nomor_Bagging':packageCode,'Jenis_Scan':scanType,'Waktu_Scan' :scanTime,
                    "Discan_Oleh":scanUser,'Lokasi Sebelumnya / Berikutnya': previousOrNextSiteCode,
                    'Tujuan' :destinationName,"Provinsi Tujuan" :receiverProvinceName,
                    "NLC":nineCharCode,"Jenis Layanan":expressTypeName}
            list.append(final)

        df = pd.DataFrame(list)
        on = st.toggle("Filter Dlg")
        if on:
            df = df[df["Discan_Oleh"].str.contains('Pb Maret 03|Pb Maret 05|Pb Maret 06|Pb Maret 15|Pb Maret 16|Kr_rohmad|dlg')==False]
        st.dataframe(df,hide_index=True)
        st.caption(f"{len(df.index)}" + " Data")
except:
    False
