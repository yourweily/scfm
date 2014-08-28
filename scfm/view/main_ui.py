import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class AppMainForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Structured Cash flow Modeler')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.textbox.setText('1 2 3 4')
        self.on_draw()


    def add_actions(self, target, actions):
        '''
        Add actions to target object
        Params:
        target - target object
        actions - a sequence of actions
        '''
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    def create_menu(self):        
        # define a menu 
        self.file_menu = self.menuBar().addMenu("&File")
        # define menu item
        load_file_action = self.create_action("&Load raw file", slot=self.load_file, shortcut="Ctrl+F", tip="Load raw file")
        export_plot_action = self.create_action("&Export chart", slot=self.export_chart, shortcut="Ctrl+S", tip="Export chart to local file")
        quit_action = self.create_action("&Quit", slot=self.close,shortcut="Ctrl+Q", tip="Close the application")
        # add the menu items under the menu
        self.add_actions(self.file_menu,(load_file_action, export_plot_action, None, quit_action))
        
        # configuration menu
        self.configure_menu = self.menuBar().addMenu("&Configure")
        config_load_meta_action= self.create_action("Load saved configuration", slot=self.load_config, shortcut="Ctrl+L", tip="load saved configuration")
        config_raw_data_meta_action = self.create_action("&Raw data meta", slot=self.config_raw_data, shortcut="Ctrl+R", tip="Load data from raw file")
        # sub - general meta
        self.asset_meta_menu = self.configure_menu.addMenu("Asset general meta")
        config_asset_meta_CPR_action = self.create_action("C&PR", slot=self.config_asset_meta_CPR, shortcut="Alt+P", tip="Configure asset's CPR")
        config_asset_meta_CDR_action = self.create_action("C&DR", slot=self.config_asset_meta_CDR, shortcut="Alt+D", tip="Configure asset's CDR")
        self.add_actions(self.asset_meta_menu, (config_asset_meta_CPR_action, config_asset_meta_CDR_action))

        config_asset_FICO_meta_action = self.create_action("Asset FICO based meta", slot=self.config_asset_FICO_meta, shortcut="Ctrl+F", tip="configure asset's meta based on FICO range")
        config_tranch_meta_action = self.create_action("Tranch list", slot=self.config_tranch_list, shortcut="Ctrl+T", tip="Manage the tranches")
        
        config_save_meta_action = self.create_action("Save current configuration", slot=self.save_config, shortcut="Ctrl+C", tip="Store configuration for reloading later.")
        self.add_actions(self.configure_menu, (config_load_meta_action, config_raw_data_meta_action,config_asset_FICO_meta_action,None, config_tranch_meta_action, None, config_save_meta_action)  )

        # help main menu
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",slot=self.on_about, shortcut='F1', tip='About the demo')
        self.add_actions(self.help_menu, (about_action,))

# actions for each menu item
    def load_file(self):
        return

    def export_chart(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = (QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def load_config(self):
        return

    def config_raw_data(self):
        return
    
    def config_asset_meta_CPR(self):
        return
    def config_asset_meta_CDR(self):
        return
    
    def config_asset_FICO_meta(self):
        return
    
    def config_tranch_list(self):
        return

    def save_config(self):
        return

    def on_about(self):
        msg = """ Structured Cash Flow Modeler
        Author:Wei Li
        Email: Weily.li@gmail.com
        Copyright: 
        """
        QMessageBox.about(self, "Structured Cash Flow Modeler", msg.strip())
        
        
    def create_status_bar(self):
        self.status_text = QLabel("status")
        self.statusBar().addWidget(self.status_text, 1)

    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        QMessageBox.information(self, "Click!", msg)
    
    def on_draw(self):
        """ Redraws the figure
        """
        str = (self.textbox.text())
        self.data = [int(s) for s in str.split()]
        
        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
        self.axes.grid(self.grid_cb.isChecked())
        
        self.axes.bar(
            left=x, 
            height=self.data, 
            width=self.slider.value() / 100.0, 
            align='center', 
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()
    
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Other GUI controls
        # 
        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)
        self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)
        
        self.textbox2 = QLineEdit()
        
        self.textbox3 = QLineEdit()
        self.textbox4 = QLineEdit()
        self.textbox2.setMinimumWidth(200)
        self.textbox3.setMinimumWidth(200)
        self.textbox4.setMinimumWidth(200)
           
        self.connect(self.textbox2, SIGNAL('editingFinished ()'), self.on_draw)
        self.connect(self.textbox3, SIGNAL('editingFinished ()'), self.on_draw)
        self.connect(self.textbox4, SIGNAL('editingFinished ()'), self.on_draw)
        
        self.draw_button = QPushButton("&Draw")
        self.connect(self.draw_button, SIGNAL('clicked()'), self.on_draw)
        
        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.on_draw)
        
        slider_label = QLabel('Bar width (%):')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(20)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)
        
        #
        # Layout with box sizers
        # 
        hbox = QHBoxLayout()
        
        for w in [  self.textbox,self.draw_button, self.grid_cb,
                    slider_label, self.slider]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
    
    
    
def main():
    app = QApplication(sys.argv)
    form = AppMainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()    