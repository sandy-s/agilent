import pygtk
pygtk.require('2.0')
import gtk
import serial

class Agilent661xC:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate, rtscts=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        self.serial.write("*cls\r\n")
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        main_box = gtk.VBox(False, 10)
        self.window.add(main_box)

        instrument_box = gtk.HBox(False, 10)
        main_box.pack_start(instrument_box)

        frame = gtk.Frame("Instrument")
        instrument_id = self.read_id()
        frame.add(gtk.Label(instrument_id))
        instrument_box.pack_start(frame)

        frame = gtk.Frame("Version")
        frame.add(gtk.Label(self.read_version()))
        instrument_box.pack_start(frame)

        box = gtk.HBox(False, 10)
        main_box.pack_start(box)

        self.set_voltage = gtk.Label()
        frame = gtk.Frame("Set Voltage")
        frame.add(self.set_voltage)
        box.pack_start(frame, False, False, 10)

        self.set_current = gtk.Label()
        frame = gtk.Frame("Set Current")
        frame.add(self.set_current)
        box.pack_start(frame, False, False, 10)

        self.voltage = gtk.Label()
        frame = gtk.Frame("Voltage")
        frame.add(self.voltage)
        box.pack_start(frame, False, False, 10)

        self.current = gtk.Label()
        frame = gtk.Frame("Current")
        frame.add(self.current)
        box.pack_start(frame, False, False, 10)

        self.output = gtk.Label()
        frame = gtk.Frame("Output")
        frame.add(self.output)
        box.pack_start(frame, False, False, 10)

        gtk.timeout_add(300, self.update)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title((instrument_id.split(','))[0] + ' ' + (instrument_id.split(','))[1])
        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.serial.close()
        gtk.main_quit()

    def update(self):
        markup_span = '<span size="30000" color="green" bgcolor="black">'
        self.set_voltage.set_markup(markup_span + self.read_set_voltage() + '</span>')
        self.set_current.set_markup(markup_span + self.read_set_current() + '</span>')
        self.voltage.set_markup(markup_span + self.read_voltage() + '</span>')
        self.current.set_markup(markup_span + self.read_current() + '</span>')
        output = 'off'
        if self.read_output() == 1:
            output = 'on'
        self.output.set_markup(markup_span + output + '</span>')
        return True

    def read_id(self):
        self.serial.write("*idn?\r\n")
        return self.serial.readline().rstrip('\r\n')

    def read_version(self):
        self.serial.write("syst:vers?\r\n")
        return self.serial.readline().rstrip('\r\n')

    def read_set_voltage(self):
        self.serial.write("volt?\r\n")
        return '{:.5f}'.format(float(self.serial.readline()))

    def read_voltage(self):
        self.serial.write("meas:volt?\r\n")
        return '{:f}'.format(float(self.serial.readline()))

    def read_set_current(self):
        self.serial.write("curr?\r\n")
        return '{:.5f}'.format(float(self.serial.readline()))

    def read_current(self):
        self.serial.write("meas:curr?\r\n")
        return '{:f}'.format(float(self.serial.readline()))

    def read_output(self):
        self.serial.write("outp?\r\n")
        return int(self.serial.readline())

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = Agilent661xC("/dev/ttyUSB13", 9600)
    app.main()
        