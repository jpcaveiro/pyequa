Predicting Plant Growth Based on Environmental Factors

**Response (Dependent) Variable:**  
- **Plant Growth Rate (cm/week)** – Measured as the increase in height per week.

**Regressors (Independent Variables):**  
1. **Sunlight Exposure (hours/day)** – Average daily sunlight received by the plant.  



The linear regression equation would be:  

\[
\text{Growth Rate} = \beta_0 + \beta_1 (\text{Sunlight}) + \beta_2 (\text{Nitrogen}) + \beta_3 (\text{Watering}) + \epsilon
\]  

Where:  
- \( \beta_0 \) = Intercept (baseline growth rate)  ****
- \( \beta_1, \beta_2, \beta_3 \) = Regression coefficients for each predictor  
- \( \epsilon \) = Random error term  

**Hypothetical Interpretation:**  
If the fitted model is:  

\[
\text{Growth Rate} = 0.5 + 0.2 (\text{Sunlight}) + 0.1 (\text{Nitrogen}) + 0.3 (\text{Watering})
\]  

- **Sunlight:** Each additional hour of sunlight per day increases growth by {b1} cm/week, holding other factors constant.  
- **Nitrogen:** A 1 mg/kg increase in soil nitrogen increases growth by {b2} cm/week, all else equal.  
- **Watering:** Each additional weekly watering increases growth by **0.3 cm/week**, assuming sunlight and nitrogen are fixed.  


**Application in Biology:**  
This model could help biologists or agronomists optimize plant growth conditions by quantifying how much each factor contributes. The significance of each regressor can be tested using **p-values** or **confidence intervals**, and the overall model fit can be assessed using \( R^2 \).

Would you like a real dataset or an extension (e.g., nonlinear effects or interactions)?

Coefficients:

<table style="border-collapse: collapse; width: 100%; display: inline-table; border: 10" border="5" >
    <colgroup>
      <col style="width: 25%">
      <col style="width: 15%;">
      <col style="width: 15%;">
      <col style="width: 15%;">
      <col style="width: 15%;">
      <col style="width: 15%;">
    </colgroup>
    <tbody>
      <tr>
        <td></td>
        <td>Estimate</td>
        <td>Std. Error</td>
        <td>t value</td>
        <td>Pr(>|t|)</td>
        <td>(interpretation)</td>
      </tr>
      <tr>
        <td>(intercept)</td>
        <td>\(\hat\beta_0\)</td>
        <td>{b0_std}</td>
        <td>{b0_tobs}</td>
        <td>{b0_pvalue}</td>
        <td>{b0_interpretation}</td>
      </tr>
      <tr>
        <td>Sunlight</td>
        <td>{b1}</td>
        <td>{b1_std}</td>
        <td>{b1_tobs}</td>
        <td>{b1_pvalue}</td>
        <td>{b1_interpretation}</td>
      </tr>
      <tr>
        <td>Nitrogen</td>
        <td>{b2}</td>
        <td>{b2_std}</td>
        <td>{b2_tobs}</td>
        <td>{b2_pvalue}</td>
        <td>{b2_interpretation}</td>
      </tr>
      <tr>
        <td>Watering</td>
        <td>{b2}</td>
        <td>{b2_std}</td>
        <td>{b2_tobs}</td>
        <td>{b2_pvalue}</td>
        <td>{b2_interpretation}</td>
      </tr>
    </tbody>
  </table>

* Multiple R-squared: {rsquared},	Adjusted R-squared:  {rsquared_adjusted} 

Conclusão com \(\alpha=0.05\): {rejeitarh0}
