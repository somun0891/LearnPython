import streamlit as st 
import random

st.title('Welcome to Number guess')

st.write('### where you guess a number ')


num = random.randrange(0,10)

guess = st.slider('guess a number',0,10)
btn_Start = st.button('Start')

if btn_Start:
  if guess == num:
      st.write('you won')
      st.balloons()
  else:
     st.write('you lost, Try again!')
     st.snow()

btn_show = st.button('show number')
if btn_show:
    st.write('the number was ',num)

    
