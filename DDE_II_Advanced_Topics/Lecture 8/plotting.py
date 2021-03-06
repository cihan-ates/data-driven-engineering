from __future__ import (absolute_import, division, print_function, unicode_literals)

#Fundamentals
import statistics
import numpy as np
from collections import namedtuple
import filterpy.stats as stats
from numpy.random import randn
from filterpy.stats import plot_gaussian_pdf, gaussian
import random

#filtering

#https://filterpy.readthedocs.io/en/latest/#filterpy-gh
from filterpy.gh import GHFilter
#https://filterpy.readthedocs.io/en/latest/discrete_bayes/discrete_bayes.html
from filterpy.discrete_bayes import predict, normalize
from filterpy.discrete_bayes import update
#https://filterpy.readthedocs.io/en/latest/#filterpy-kalman
import filterpy.kalman as kf
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

#Data generation for Kalman filter:
import copy
import math
#Plotting
import matplotlib as mpl
import plotly.graph_objects as go
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt


def plotter(data_y,hypothesis_y, error_1, error_2):
  fig = go.Figure()
  # Add traces
  fig.add_trace(go.Scatter(y=data_y,
                      mode='markers',
                      name='data',
                      error_y=dict(
                      type='data',
                      symmetric=False,
                      array=error_1,
                      arrayminus=error_2)))
  
  fig.add_trace(go.Scatter(y=hypothesis_y,
                      mode='lines',
                      name='hypothesis'))

  fig.update_layout(
      autosize=False,
      width=800,
      height=300,
      margin=dict(
          l=5,
          r=5,
          b=10,
          t=10,
          pad=4
      ),
      paper_bgcolor="White",
  )
  fig.show()

def plotter_2(measurements, predictions, estimations,true_data):
  fig = go.Figure()
  colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
  # Add traces
  fig.add_trace(go.Scatter(x=list(range(1,len(estimations))) , y=measurements,
                      mode='markers',
                      name='measurements',line=dict(color='red', width=2)))
  fig.add_trace(go.Scatter(x=list(range(1,len(estimations))) , y=predictions,
                      mode='lines+markers',
                      name='predictions',
                      line=dict(color=colors[2], width=2,dash='dash')))
  fig.add_trace(go.Scatter(x=list(range(0,len(estimations))) , y=estimations,
                      mode='lines+markers',
                      name='estimations',
                      line=dict(color=colors[1], width=2,dash='dot'))) 
  fig.add_trace(go.Scatter(x=list(range(0,len(estimations))) , y=true_data,
                      mode='lines',
                      line=dict(color=colors[0], width=2),
                      name='Truth'))

  fig.update_layout(
      autosize=False,
      width=800,
      height=300,
      margin=dict(
          l=5,
          r=5,
          b=10,
          t=10,
          pad=4
      ),
      paper_bgcolor="White",
  )
  fig.show()

# Aux. function for plotting:
def plot_products(g1, g2): 
    plt.figure(figsize=(7,3), dpi=100)
    product = gaussian_multiply(g1, g2)

    xs = np.arange(5, 15, 0.1)
    ys = [stats.gaussian(x, g1.mean, g1.var) for x in xs]
    plt.plot(xs, ys, label='$\mathcal{N}$'+'$({},{})$'.format(g1.mean, g1.var))

    ys = [stats.gaussian(x, g2.mean, g2.var) for x in xs]
    plt.plot(xs, ys, label='$\mathcal{N}$'+'$({},{})$'.format(g2.mean, g2.var))

    ys = [stats.gaussian(x, product.mean, product.var) for x in xs]
    plt.plot(xs, ys, label='product', ls='--')
    plt.legend();


def show_legend():
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
def plot_predictions(p, rng=None, label='Prediction'):
    if rng is None:
        rng = range(len(p))
    plt.scatter(rng, p, marker='v', s=40, edgecolor='r',
                facecolor='None', lw=2, label=label)
    
def plot_filter(xs, ys=None, dt=None, c='C0', label='Filter', var=None, **kwargs):
    """ plot result of KF with color `c`, optionally displaying the variance
    of `xs`. Returns the list of lines generated by plt.plot()"""

    if ys is None and dt is not None:
        ys = xs
        xs = np.arange(0, len(ys) * dt, dt)
    if ys is None:
        ys = xs
        xs = range(len(ys))

    lines = plt.plot(xs, ys, color=c, label=label, **kwargs)
    if var is None:
        return lines

    var = np.asarray(var)
    std = np.sqrt(var)
    std_top = ys+std
    std_btm = ys-std

    plt.plot(xs, ys+std, linestyle=':', color='k', lw=2)
    plt.plot(xs, ys-std, linestyle=':', color='k', lw=2)
    plt.fill_between(xs, std_btm, std_top,
                     facecolor='yellow', alpha=0.2)

    return lines

def plot_measurements(xs, ys=None, dt=None, color='k', lw=1, label='Measurements',
                      lines=False, **kwargs):
    """ Helper function to give a consistant way to display
    measurements in the book.
    """
    if ys is None and dt is not None:
        ys = xs
        xs = np.arange(0, len(ys)*dt, dt)

    plt.autoscale(tight=False)
    if lines:
        if ys is not None:
            return plt.plot(xs, ys, color=color, lw=lw, ls='--', label=label, **kwargs)
        else:
            return plt.plot(xs, color=color, lw=lw, ls='--', label=label, **kwargs)
    else:
        if ys is not None:
            return plt.scatter(xs, ys, edgecolor=color, facecolor='none',
                        lw=2, label=label, **kwargs),
        else:
            return plt.scatter(range(len(xs)), xs, edgecolor=color, facecolor='none',
                        lw=2, label=label, **kwargs),


def plot_track(xs, ys=None, dt=None, label='Track', c='k', lw=2, **kwargs):
    if ys is None and dt is not None:
        ys = xs
        xs = np.arange(0, len(ys)*dt, dt)
    if ys is not None:
        return plt.plot(xs, ys, color=c, lw=lw, ls=':', label=label, **kwargs)
    else:
        return plt.plot(xs, color=c, lw=lw, ls=':', label=label, **kwargs)
        

def plot_tracks_2(ps, actual,y_lim=None,
               xlabel='time', ylabel='position',
               title='Kalman Filter', count=10):

    plot_track(actual, c='k')
    plot_filter(range(1, count + 1), ps)

    plt.legend(loc=4)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


gaussian = namedtuple('Gaussian', ['mean', 'var'])
gaussian.__repr__ = lambda s: '????(??={:.3f}, ??????={:.3f})'.format(s[0], s[1])

def gaussian_multiply(g1, g2):
    #Note that we are using tuples:
    mean = (g1.var * g2.mean + g2.var * g1.mean) / (g1.var + g2.var)
    variance = (g1.var * g2.var) / (g1.var + g2.var)
    return gaussian(mean, variance)

def update(prior, likelihood):
    posterior = gaussian_multiply(likelihood, prior)
    return posterior


