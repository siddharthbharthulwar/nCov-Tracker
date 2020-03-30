# nCov-Tracker

Mathematical and statistical toolkit for tracking and monitoring the 2020 outbreak of COVID-19. Current functions include exponential and logistic regression for all regions, as well as future forecasting based on minimizing cost functions. Implementations of the SIR epidemological model and an LSTM-based RNN for enhanced feature tracking are underway. 

Currently I'm writing this for researchers in Porto, but feel free to use this for future predictions. Note that the JHU dataset is updated at 6 PM MST (+/- a few minutes), but may only reflect the previous day's data. As of 3/28/2020, the JHU dataset doesn't include the data from individual states in the US, but this should change soon.

This project is also a submission for the IB Computer Science Standard Level Internal Assessment, so theres's that. 

Dependencies:
- NumPy
- Pandas
- Matplotlib
- Python 3.6 +
- Tkinter (should be included within the base Python 3.xx package)

TODO:
- Fix Interface
- Add Shifting Weight Tracking for better predictions
- Train and implement LTSM Deep Learning Models for Dynamic Weights
- Build to exe
