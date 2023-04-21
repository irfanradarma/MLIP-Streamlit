import numpy as np
import streamlit as st

slider_noble = st.container()
sugar = st.container()
expected = st.container()

TROCKEN = 5
KABINETT = 10
SPATLESE = 15
AUSLESE = 30
BEERENAUSLESE = 40
TROCKENBEEREN = 120

HARVEST_NOW = (TROCKEN * 6000 + KABINETT * 2000 + SPATLESE * 2000) * 12

def pay_noharv_storm(botrytis):
    storm_no_mold = (TROCKEN * 5000 + KABINETT * 1000) * (1 - botrytis)
    storm_mold = (TROCKEN * 5000 + KABINETT * 1000 + TROCKENBEEREN * 2000) * botrytis
    return (storm_no_mold + storm_mold) * 12

def pay_noharv_nostorm(noSugar, typical, highSugar):
    no_storm_no = (TROCKEN * 6000 + KABINETT * 2000 + SPATLESE * 2000) * noSugar
    no_storm_typical = (TROCKEN * 5000 + KABINETT * 1000 + SPATLESE * 2500 + AUSLESE * 1500) * typical
    no_storm_high = (TROCKEN * 4000 + KABINETT * 2500 + SPATLESE * 2000 + AUSLESE * 1000 + BEERENAUSLESE * 500) * highSugar
    return (no_storm_no + no_storm_typical + no_storm_high) * 12

def expected_value(botrytis, noSugar, typical, highSugar):
    storm = pay_noharv_storm(botrytis)
    noStorm = pay_noharv_nostorm(noSugar, typical, highSugar)
    exp_val = 0.5 * (storm) + 0.5 * (noStorm)
    return exp_val

def bayes(metric, prob):
    numerator = metric * prob
    denom = (metric * prob) + (1 - metric) * (1 - prob)
    return numerator / denom, denom

def value_funct(prob_storm, sens, spec, pay_harvest, pay_noharv_storm, pay_noharv_nostorm):
    if spec < 0.5:
        spec = 1 - spec
    prob_no_storm = 1 - prob_storm
    true_neg, pred_neg = bayes(spec, prob_no_storm)
    pred_pos = 1 - pred_neg
    exp_value = (pred_neg * (pay_noharv_nostorm * true_neg + pay_noharv_storm * (1 - true_neg))) + (pred_pos * (pay_harvest)) 
    return max(exp_value - pay_harvest, 0)

with slider_noble:
    st.header('Adjust the Noble Rot probabilities')
    botrytis_prob = st.slider(label='noble rot probability', min_value=0.00, max_value=1.00, value=0.1, step=0.01)

with sugar:
    st.header('Adjust the sugar probabilities')
    col1, col2, col3 = st.columns(3)
    no_sugar = col1.number_input(label="No sugar", value=0.6, min_value=0.0, max_value=1.0)
    typical = col2.number_input(label="Typical sugar", value=0.3, min_value=0.0, max_value=1.0)
    high_sugar = col3.number_input(label="High sugar", value=0.1, min_value=0.0, max_value=1.0)

    if round(no_sugar + typical + high_sugar, 2) != 1.00:
        st.warning('The sum of the probabilities must be 1.')

with expected:
    expected_val = expected_value(botrytis_prob, no_sugar, typical, high_sugar)
    col1, col2 = st.columns(2)
    col1.subheader('Expected Clairvoyance Value')
    if round(no_sugar + typical + high_sugar, 2) != 1.00:
        col1.warning('The sum of the probabilities must be 1.')
    else:
        col1.subheader(f'${expected_val:,.2f}')
    col2.subheader('Value of Clairvoyance')
    if round(no_sugar + typical + high_sugar, 2) != 1.00:
        col2.warning('The sum of the probabilities must be 1.')
    else:
        if expected_val - HARVEST_NOW < 0:
            col2.markdown(f'<p style="color:red;font-size:32px;">${expected_val - HARVEST_NOW:,.2f}</span>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:red;font-size:32px;">DECISION: Do not buy Clairvoyance</span>', unsafe_allow_html=True)
        else:
            col2.subheader(f'${expected_val - HARVEST_NOW:,.2f}')
            st.markdown(f'<p style="color:black;font-size:32px;">DECISION: Buy Clairvoyance</span>', unsafe_allow_html=True)