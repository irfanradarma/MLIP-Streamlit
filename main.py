import numpy as np
import matplotlib.pyplot as plt





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

def plot_value(prob_storm, pay_harvest, pay_noharv_storm, pay_noharv_nostorm):
    sensitivities = []
    values = []

    for i in range(101):
        sensitivity = i / 100
        specificity = sensitivity
        sensitivities.append(sensitivity)
        value = value_funct(prob_storm, sensitivity, specificity, pay_harvest, pay_noharv_storm, pay_noharv_nostorm)
        values.append(value)

    plt.plot(sensitivities, values)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel("Sensitivity/Specificity")
    plt.ylabel("Value of Data")
    plt.title("Value of Data vs. Sensitivity/Specificity")
    plt.show()