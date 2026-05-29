import streamlit as st
import requests


'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

#pickup_datetime = st.text_input('Please enter date and time as YYYY-MM-DD hour:minute:second ')
pickup_datetime = st.datetime_input('Please enter date and time as YYYY-MM-DD hour:minute:second ', value="now")

st.write('The pick up date and time is', pickup_datetime)


passenger_count = st.text_input('Please enter the number of passangers ')

st.write('The number of passengers is', passenger_count)

#st.write("## Put in the pick up and drop off location here or further down with the map")

pickup_longitude = st.text_input('Please enter pick up location: longitude ')

st.write('The pick up location longitude is', pickup_longitude)

pickup_latitude = st.text_input('Please enter pick up location: latitude ')

st.write('The pick up location latitude is', pickup_latitude)

dropoff_longitude = st.text_input('Please enter drop off location: longitude ')

st.write('The drop off location longitude is', dropoff_longitude)

dropoff_latitude = st.text_input('Please enter drop off location: latitude ')

st.write('The drop off location latitude is', dropoff_latitude)



'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifareapi-1091606282523.europe-west1.run.app'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

# dict with the input
dictionary = {"pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count}

# API Call and json output
prediction = None
full_url = f"{url}/predict"
if st.button("Predict fare"):
    response = requests.get(full_url, params=dictionary)
    st.balloons()
    #st.progress(0, text="Prediction in Progress", width="stretch")
    prediction = response.json()

st.write("### Prediction")
if prediction == None:
    st.write("No prediction")
else:
    st.write("The predicted fare: ", round(prediction["fare"], 2), "$")
