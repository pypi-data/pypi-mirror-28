# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Widget for plotting impulse and general transient responses
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import logging
logger = logging.getLogger(__name__)

from ..compat import (QCheckBox, QWidget, QComboBox, QLineEdit, QLabel, QEvent,
                      Qt, QHBoxLayout, QFrame, pyqtSlot)

import numpy as np
import scipy.signal as sig

import pyfda.filterbroker as fb
from pyfda.pyfda_lib import expand_lim, to_html, safe_eval
from pyfda.pyfda_rc import params # FMT string for QLineEdit fields, e.g. '{:.3g}'
from pyfda.plot_widgets.mpl_widget import MplWidget
#from mpl_toolkits.mplot3d.axes3d import Axes3D


class PlotImpz(QWidget):
    """
    Construct a widget for plotting impulse and general transient responses
    """
    def __init__(self, parent):
        super(PlotImpz, self).__init__(parent)

        self.ACTIVE_3D = False
        # initial settings for line edit widgets
        self.stim_freq = 0.02
        self.A = 1.0
        self.bottom = -80
        self._construct_UI()

    def _construct_UI(self):
        self.chkLog = QCheckBox(self)
        self.chkLog.setObjectName("chkLog")
        self.chkLog.setToolTip("<span>Logarithmic scale for y-axis.</span>")
        self.chkLog.setChecked(False)
        self.lblLog = QLabel("Log. y-axis", self)

        self.lblLogBottom = QLabel("Bottom = ", self)
        self.ledLogBottom = QLineEdit(self)
        self.ledLogBottom.setText(str(self.bottom))
        self.ledLogBottom.setToolTip("<span>Minimum display value for log. scale.</span>")
        self.lbldB = QLabel("dB")
        
        self.lblPltStim = QLabel(self)
        self.lblPltStim.setText("Stimulus:")
        self.chkPltStim = QCheckBox("Show", self)
        self.chkPltStim.setChecked(False)
        self.chkPltStim.setToolTip("Show stimulus signal.")
        
        self.lblStimulus = QLabel("Type = ", self)
        self.cmbStimulus = QComboBox(self)
        self.cmbStimulus.addItems(["Pulse","Step","StepErr", "Cos", "Sine", "Rect", "Saw", "RandN", "RandU"])
        self.cmbStimulus.setToolTip("Select stimulus type.")

        self.lblAmp = QLabel("<i>A</i>&nbsp; =", self)
        self.ledAmp = QLineEdit(self)
        self.ledAmp.setText(str(self.A))
        self.ledAmp.setToolTip("Stimulus amplitude.")
        self.ledAmp.setObjectName("stimAmp")

        self.lblFreq = QLabel("<i>f</i>&nbsp; =", self)
        self.ledFreq = QLineEdit(self)
        self.ledFreq.setText(str(self.stim_freq))
        self.ledFreq.setToolTip("Stimulus frequency.")
        self.ledFreq.setObjectName("stimFreq")

        self.lblFreqUnit = QLabel("f_S", self)

        self.lblNPoints = QLabel("<i>N</i>&nbsp; =", self)

        self.ledNPoints = QLineEdit(self)
        self.ledNPoints.setText("0")
        self.ledNPoints.setToolTip("<span>Number of points to calculate and display. "
                                   "N = 0 selects automatically.</span>")

        layHControls = QHBoxLayout()
        
        layHControls.addWidget(self.lblNPoints)
        layHControls.addWidget(self.ledNPoints)
        layHControls.addStretch(2)
        layHControls.addWidget(self.chkLog)
        layHControls.addWidget(self.lblLog)
        layHControls.addStretch(1)
        layHControls.addWidget(self.lblLogBottom)
        layHControls.addWidget(self.ledLogBottom)
        layHControls.addWidget(self.lbldB)
        layHControls.addStretch(2)
        layHControls.addWidget(self.lblPltStim)
        layHControls.addWidget(self.chkPltStim)
        layHControls.addStretch(1)
        layHControls.addWidget(self.lblStimulus)
        layHControls.addWidget(self.cmbStimulus)
        layHControls.addStretch(2)
        layHControls.addWidget(self.lblAmp)
        layHControls.addWidget(self.ledAmp)
        layHControls.addWidget(self.lblFreq)
        layHControls.addWidget(self.ledFreq)
        layHControls.addWidget(self.lblFreqUnit)

        layHControls.addStretch(10)
        
        # This widget encompasses all control subwidgets:
        self.frmControls = QFrame(self)
        self.frmControls.setObjectName("frmControls")
        self.frmControls.setLayout(layHControls)

        #----------------------------------------------------------------------
        # mplwidget
        #----------------------------------------------------------------------
        self.mplwidget = MplWidget(self)
        self.mplwidget.layVMainMpl.addWidget(self.frmControls)
        self.mplwidget.layVMainMpl.setContentsMargins(*params['wdg_margins'])
        self.setLayout(self.mplwidget.layVMainMpl)

        #----------------------------------------------------------------------
        # SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.chkLog.clicked.connect(self.draw)
        self.ledNPoints.editingFinished.connect(self.draw)
        self.ledLogBottom.editingFinished.connect(self.draw)
        self.chkPltStim.clicked.connect(self.draw)
        self.cmbStimulus.activated.connect(self.draw)
        self.ledAmp.editingFinished.connect(self.draw)
        self.ledFreq.installEventFilter(self)
        
        self.mplwidget.mplToolbar.sig_tx.connect(self.process_signals)

        self.draw() # initial calculation and drawing

#------------------------------------------------------------------------------
    @pyqtSlot(object)
    def process_signals(self, sig_dict):
        """
        Process signals coming from the navigation toolbar
        """
        if 'update_view' in sig_dict:
            self.update_view()
        elif 'enabled' in sig_dict:
            self.enable_ui(sig_dict['enabled'])
        elif 'home' in sig_dict:
            self.draw()
        else:
            pass

#------------------------------------------------------------------------------
    def enable_ui(self, enabled):
        """
        Triggered when the toolbar is enabled or disabled
        """
        self.frmControls.setEnabled(enabled)
        if enabled:
            # self.init_axes() # called by self.draw
            self.draw()

#------------------------------------------------------------------------------
    def eventFilter(self, source, event):
        """
        Filter all events generated by the QLineEdit widgets. Source and type
        of all events generated by monitored objects are passed to this eventFilter,
        evaluated and passed on to the next hierarchy level.

        - When a QLineEdit widget gains input focus (QEvent.FocusIn`), display
          the stored value from filter dict with full precision
        - When a key is pressed inside the text field, set the `spec_edited` flag
          to True.
        - When a QLineEdit widget loses input focus (QEvent.FocusOut`), store
          current value normalized to f_S with full precision (only if
          `spec_edited`== True) and display the stored value in selected format
        """

        def _store_entry(source):
            if self.spec_edited:
                self.stim_freq = safe_eval(source.text(), self.stim_freq * fb.fil[0]['f_S'],
                                            return_type='float') / fb.fil[0]['f_S']
                self.spec_edited = False # reset flag
                self.draw()
                
        if isinstance(source, QLineEdit): # could be extended for other widgets
            if event.type() == QEvent.FocusIn:
                self.spec_edited = False
                self.load_dict()
            elif event.type() == QEvent.KeyPress:
                self.spec_edited = True # entry has been changed
                key = event.key()
                if key in {Qt.Key_Return, Qt.Key_Enter}:
                    _store_entry(source)
                elif key == Qt.Key_Escape: # revert changes
                    self.spec_edited = False                    
                    source.setText(str(params['FMT'].format(self.stim_freq * fb.fil[0]['f_S'])))
                
            elif event.type() == QEvent.FocusOut:
                _store_entry(source)
                source.setText(str(params['FMT'].format(self.stim_freq * fb.fil[0]['f_S'])))
        # Call base class method to continue normal event processing:
        return super(PlotImpz, self).eventFilter(source, event)

#-------------------------------------------------------------        
    def load_dict(self):
        """
        Reload textfields from filter dictionary 
        Transform the displayed frequency spec input fields according to the units
        setting (i.e. f_S). Spec entries are always stored normalized w.r.t. f_S 
        in the dictionary; when f_S or the unit are changed, only the displayed values
        of the frequency entries are updated, not the dictionary!

        load_dict() is called during init and when the frequency unit or the
        sampling frequency have been changed.

        It should be called when sigSpecsChanged or sigFilterDesigned is emitted
        at another place, indicating that a reload is required.
        """

        # recalculate displayed freq spec values for (maybe) changed f_S
        logger.debug("exec load_dict")
        if not self.ledFreq.hasFocus():
            # widget has no focus, round the display
            self.ledFreq.setText(
                str(params['FMT'].format(self.stim_freq * fb.fil[0]['f_S'])))
        else:
            # widget has focus, show full precision
            self.ledFreq.setText(str(self.stim_freq * fb.fil[0]['f_S']))

#------------------------------------------------------------------------------
    def init_axes(self):
        # clear the axes and (re)draw the plot
        #
        try:
            self.mplwidget.fig.delaxes(self.ax_r)
            self.mplwidget.fig.delaxes(self.ax_i)
        except (KeyError, AttributeError, UnboundLocalError):
            pass

        if self.cmplx:
            self.ax_r = self.mplwidget.fig.add_subplot(211)
            self.ax_r.clear()
            self.ax_r.get_xaxis().tick_bottom() # remove axis ticks on top
            self.ax_r.get_yaxis().tick_left() # remove axis ticks right

            self.ax_i = self.mplwidget.fig.add_subplot(212, sharex = self.ax_r)
            self.ax_i.clear()
            self.ax_i.get_xaxis().tick_bottom() # remove axis ticks on top
            self.ax_i.get_yaxis().tick_left() # remove axis ticks right

        else:
            self.ax_r = self.mplwidget.fig.add_subplot(111)
            self.ax_r.clear()
            self.ax_r.get_xaxis().tick_bottom() # remove axis ticks on top
            self.ax_r.get_yaxis().tick_left() # remove axis ticks right


        self.mplwidget.fig.subplots_adjust(hspace = 0.5)  

        if self.ACTIVE_3D: # not implemented / tested yet
            self.ax3d = self.mplwidget.fig.add_subplot(111, projection='3d')

#------------------------------------------------------------------------------
    def update_view(self):
        """
        place holder; should update only the limits without recalculating
        the impulse respons
        """
        self.draw()

#------------------------------------------------------------------------------
    def draw(self):
        if self.mplwidget.mplToolbar.enabled:
            self.draw_impz()

#------------------------------------------------------------------------------
    def draw_impz(self):
        """
        (Re-)calculate h[n] and draw the figure
        """
        log = self.chkLog.isChecked()
        stim = str(self.cmbStimulus.currentText())
        periodic_sig = stim in {"Cos", "Sine","Rect", "Saw"}
        self.lblLogBottom.setVisible(log)
        self.ledLogBottom.setVisible(log)
        self.lbldB.setVisible(log)
        
        self.lblFreq.setVisible(periodic_sig)
        self.ledFreq.setVisible(periodic_sig)
        self.lblFreqUnit.setVisible(periodic_sig)

        self.lblFreqUnit.setText(to_html(fb.fil[0]['freq_specs_unit']))
        self.load_dict()
        
        self.bb = np.asarray(fb.fil[0]['ba'][0])
        self.aa = np.asarray(fb.fil[0]['ba'][1])
        if min(len(self.aa), len(self.bb)) < 2:
            logger.error('No proper filter coefficients: len(a), len(b) < 2 !')
            return

        sos = np.asarray(fb.fil[0]['sos'])
        antiCausal = 'zpkA' in fb.fil[0]
        causal     = not (antiCausal)

        self.f_S  = fb.fil[0]['f_S']
        
        N_entry = safe_eval(self.ledNPoints.text(), 0, return_type='int', sign='pos')
        N = self.calc_n_points(N_entry)
        if N_entry != 0: # automatic calculation
            self.ledNPoints.setText(str(N))

        self.A = safe_eval(self.ledAmp.text(), self.A, return_type='float')
        self.ledAmp.setText(str(self.A))

        t = np.linspace(0, N/self.f_S, N, endpoint=False)

        title_str = r'Impulse Response' # default
        H_str = r'$h[n]$' # default

        # calculate h[n]
        if stim == "Pulse":
            x = np.zeros(N)
            x[0] = self.A # create dirac impulse as input signal
        elif stim == "Step":
            x = self.A * np.ones(N) # create step function
            title_str = r'Step Response'
            H_str = r'$h_{\epsilon}[n]$'
        elif stim == "StepErr":
            x = self.A * np.ones(N) # create step function
            title_str = r'Settling Error'
            H_str = r'$h_{\epsilon, \infty} - h_{\epsilon}[n]$'
            
        elif stim in {"Cos"}:
            x = self.A * np.cos(2 * np.pi * t * float(self.ledFreq.text()))
            if stim == "Cos":
                title_str = r'Transient Response to Cosine Signal'
                H_str = r'$y_{\cos}[n]$'

        elif stim in {"Sine", "Rect"}:
            x = self.A * np.sin(2 * np.pi * t * float(self.ledFreq.text()))
            if stim == "Sine":
                title_str = r'Transient Response to Sine Signal'
                H_str = r'$y_{\sin}[n]$'
            else:
                x = self.A * np.sign(x)
                title_str = r'Transient Response to Rect. Signal'
                H_str = r'$y_{rect}[n]$'

        elif stim == "Saw":
            x = self.A * sig.sawtooth(t * (float(self.ledFreq.text())* 2*np.pi))
            title_str = r'Transient Response to Sawtooth Signal'
            H_str = r'$y_{saw}[n]$'

        elif stim == "RandN":
            x = self.A * np.random.randn(N)
            title_str = r'Transient Response to Gaussian Noise'
            H_str = r'$y_{gauss}[n]$'

        elif stim == "RandU":
            x = self.A * (np.random.rand(N)-0.5)
            title_str = r'Transient Response to Uniform Noise'
            H_str = r'$y_{uni}[n]$'

        else:
            logger.error('Unknown stimulus "{0}"'.format(stim))
            return

        if len(sos) > 0 and (causal): # has second order sections and is causal
            h = sig.sosfilt(sos, x)
        elif (antiCausal):
            h = sig.filtfilt(self.bb, self.aa, x, -1, None)
        else: # no second order sections or antiCausals for current filter
            h = sig.lfilter(self.bb, self.aa, x)

        dc = sig.freqz(self.bb, self.aa, [0])

        if stim == "StepErr":
            h = h - abs(dc[1]) # subtract DC value from response

        h = np.real_if_close(h, tol = 1e3)  # tol specified in multiples of machine eps
        self.cmplx = np.any(np.iscomplex(h))
        if self.cmplx:
            h_i = h.imag
            h = h.real
            H_i_str = r'$\Im\{$' + H_str + '$\}$'
            H_str = r'$\Re\{$' + H_str + '$\}$'
        if log:
            self.bottom = safe_eval(self.ledLogBottom.text(), self.bottom, return_type='float')
            self.ledLogBottom.setText(str(self.bottom))
            H_str = r'$|$ ' + H_str + '$|$ in dB'
            h = np.maximum(20 * np.log10(abs(h)), self.bottom)
            if self.cmplx:
                h_i = np.maximum(20 * np.log10(abs(h_i)), self.bottom)
                H_i_str = r'$\log$ ' + H_i_str + ' in dB'
        else:
            self.bottom = 0

        self.init_axes()

        #================ Main Plotting Routine =========================
        [ml, sl, bl] = self.ax_r.stem(t, h, bottom=self.bottom, markerfmt='o', label = '$h[n]$')
        stem_fmt = params['mpl_stimuli']
        if self.chkPltStim.isChecked():
            [ms, ss, bs] = self.ax_r.stem(t, x, bottom=self.bottom, label = 'Stim.', **stem_fmt)
            ms.set_mfc(stem_fmt['mfc'])
            ms.set_mec(stem_fmt['mec'])
            ms.set_ms(stem_fmt['ms'])
            ms.set_alpha(stem_fmt['alpha'])
            for stem in ss:
                stem.set_linewidth(stem_fmt['lw'])
                stem.set_color(stem_fmt['mec'])
                stem.set_alpha(stem_fmt['alpha'])
            bs.set_visible(False) # invisible bottomline
        expand_lim(self.ax_r, 0.02)
        self.ax_r.set_title(title_str)

        if self.cmplx:
            [ml_i, sl_i, bl_i] = self.ax_i.stem(t, h_i, bottom=self.bottom,
                                                markerfmt='d', label = '$h_i[n]$')
            self.ax_i.set_xlabel(fb.fil[0]['plt_tLabel'])
            # self.ax_r.get_xaxis().set_ticklabels([]) # removes both xticklabels
            # plt.setp(ax_r.get_xticklabels(), visible=False) 
            # is shorter but imports matplotlib, set property directly instead:
            [label.set_visible(False) for label in self.ax_r.get_xticklabels()]
            self.ax_r.set_ylabel(H_str + r'$\rightarrow $')
            self.ax_i.set_ylabel(H_i_str + r'$\rightarrow $')
        else:
            self.ax_r.set_xlabel(fb.fil[0]['plt_tLabel'])
            self.ax_r.set_ylabel(H_str + r'$\rightarrow $')


        if self.ACTIVE_3D: # not implemented / tested yet

            # plotting the stems
            for i in range(len(t)):
              self.ax3d.plot([t[i], t[i]], [h[i], h[i]], [0, h_i[i]],
                             '-', linewidth=2, alpha=.5)

            # plotting a circle on the top of each stem
            self.ax3d.plot(t, h, h_i, 'o', markersize=8,
                           markerfacecolor='none', label='$h[n]$')

            self.ax3d.set_xlabel('x')
            self.ax3d.set_ylabel('y')
            self.ax3d.set_zlabel('z')

        self.redraw()
        
#------------------------------------------------------------------------------
    def redraw(self):
        """
        Redraw the canvas when e.g. the canvas size has changed
        """
        self.mplwidget.redraw()

#------------------------------------------------------------------------------        
    def calc_n_points(self, N_user = 0):
        """
        Calculate number of points to be displayed, depending on type of filter 
        (FIR, IIR) and user input. If the user selects 0 points, the number is
        calculated automatically.
        
        An improvement would be to calculate the dominant pole and the corresponding
        settling time.
        """

        if N_user == 0: # set number of data points automatically
            if fb.fil[0]['ft'] == 'IIR':
                N = 100
            else:
                N = min(len(self.bb),  100) # FIR: N = number of coefficients (max. 100)
        else:
            N = N_user

        return N

#------------------------------------------------------------------------------

def main():
    import sys
    from ..compat import QApplication

    app = QApplication(sys.argv)
    mainw = PlotImpz(None)
    app.setActiveWindow(mainw) 
    mainw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
