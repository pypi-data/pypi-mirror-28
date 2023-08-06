#!/bin/env python
# -*- coding: utf-8 -*-

"""
This package produces a button that closes all subplots upon click.

.. versioncreated:: 1.0

.. codeauthor:: Oliver James Hall <ojh251@student.bham.ac.uk>
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def show():
        '''
        A class that plots a button to instantly close all subplots. Useful when
        plotting a large number of comparisons.

        Returns:
            matplotlib.figure.Figure: 2 by 1 plot containing a 'close all' button.

            matplotlib.widgets.Button: A button widget required for button function.
        '''
        fig, ax = plt.subplots(figsize=(2,1))   #Build the plot with button
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        closeax =plt.axes([0.1,0.1,0.8,0.8])    #Define button axes

        #Build the button
        button = Button(closeax, 'Close Plots', color='white', hovercolor='r')

        #When clicked, call the close() function
        button.on_clicked(close)

        #Display all graph
        plt.show()

def close(event):
    ''' A simple plt.close('all') function called on click.'''
    plt.close('all')
