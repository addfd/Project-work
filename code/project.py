import customtkinter
import serial
import time
port = '/dev/ttyUSB0' # - порт к которому подключена arduino
arduino = serial.Serial(port, 9600)
time.sleep(0.5)
# arduino.write(b'done')
# while True:
#    t = str(arduino.readline())
#    print(t)
#    if t == b'DONE!\r\n':
#        break

pin = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
mode = ["servo", "led"]
init_pin = []
current_mode = mode[0]
current_device = None
# ----------------------------- функция которая будет возврощать количество классов заданого типа

def len_class(sclass, sp):
    n = 0
    for i in sp:
        if isinstance(i, type(sclass)):
            n += 1
    return n

# --------------------------------------------------------------------------------- led

class MyLed:

    def __init__(self, app, name="", pin=0, len=0, numi=0):
        self.app = app
        self.name = name
        self.pin = pin
        self.len = len
        self.numi = numi  # - индекс ленты в списке на arduino
        self.ind = 0  # - индекс устройства что бы arduino знало что делать

        self.brightness = 100
        self.r = 100
        self.g = 100
        self.b = 100


    def slider_event(self, value):
        self.brightness = value

    def chr(self, value):
        self.r = value

    def chg(self, value):
        self.g = value

    def chb(self, value):
        self.b = value

    def updateledb(self):
        if isinstance(self.r or self.g or self.b, (float, int, str, list, dict, tuple)):  # - пока оставим так
            self.app.aplled.configure(fg_color='#%02x%02x%02x' % (int(self.r), int(self.g), int(self.b)))  # - применить цвет на кнопку

    def main_elem(self, destroy=False): # - елементы интерфейса для управления
        if not destroy:
            self.app.label1 = customtkinter.CTkLabel(self.app, text="Яркость:", fg_color="transparent")
            self.app.label1.grid(row=1, column=0, padx=5, pady=(10, 20), sticky="w")
            self.app.slider = customtkinter.CTkSlider(self.app, from_=10, to=240, command=self.slider_event)
            self.app.slider.grid(row=1, column=0, padx=(60, 0), pady=(10, 20), sticky="w")

            self.app.label2 = customtkinter.CTkLabel(self.app, text="Цвет:", fg_color="transparent")
            self.app.label2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.app.aplled = customtkinter.CTkButton(self.app, text="Посмотреть цвет", command=self.updateledb)
            self.app.aplled.grid(row=2, column=0, padx=(40, 0), pady=5, sticky="w")

            self.app.label3 = customtkinter.CTkLabel(self.app, text="R:", fg_color="transparent")
            self.app.label3.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.app.f = customtkinter.CTkSlider(self.app, from_=10, to=240, command=self.chr)
            self.app.f.grid(row=3, column=0, padx=(20, 0), pady=5, sticky="w")

            self.app.label4 = customtkinter.CTkLabel(self.app, text="G:", fg_color="transparent")
            self.app.label4.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            self.app.ff = customtkinter.CTkSlider(self.app, from_=10, to=240, command=self.chg)
            self.app.ff.grid(row=4, column=0, padx=(20, 0), pady=5, sticky="w")

            self.app.label = customtkinter.CTkLabel(self.app, text="B:", fg_color="transparent")
            self.app.label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
            self.app.fff = customtkinter.CTkSlider(self.app, from_=10, to=240, command=self.chb)
            self.app.fff.grid(row=5, column=0, padx=(20, 0), pady=5, sticky="w")
        else:
            self.app.label1.destroy()
            self.app.slider.destroy()

            self.app.label2.destroy()
            self.app.aplled.destroy()

            self.app.label3.destroy()
            self.app.f.destroy()

            self.app.label4.destroy()
            self.app.ff.destroy()

            self.app.label.destroy()
            self.app.fff.destroy()

    def init_elem(self, destroy=False):   # - елементы интерфейса инициализации
        if not destroy:
            self.app.f = customtkinter.CTkLabel(self.app, text="Len:", fg_color="transparent")
            self.app.f.grid(row=1, column=0, padx=(200, 5), pady=(10, 20), sticky="w")
            self.app.ff = customtkinter.CTkEntry(self.app, width=30, border_width=0)
            self.app.ff.grid(row=1, column=0, padx=(230, 300), pady=(10, 20), sticky="w")
            self.app.fff = customtkinter.CTkLabel(self.app, text="Pin:", fg_color="transparent")
            self.app.fff.grid(row=0, column=0, padx=(200, 5), pady=(10, 20), sticky="w")
            self.app.ffff = customtkinter.CTkEntry(self.app, width=30, border_width=0)
            self.app.ffff.grid(row=0, column=0, padx=(230, 300), pady=(10, 20), sticky="w")
        else:
            self.app.f.destroy()
            self.app.ff.destroy()
            self.app.fff.destroy()
            self.app.ffff.destroy()

    def send(self):
        numi = bytes(str(self.numi), 'utf-8')
        ind = bytes(str(self.ind), 'utf-8')
        fd = bytes(str(int(self.brightness)), 'utf-8')
        arduino.write(ind + b' ' + numi + b' 0 ' + fd)
        print(ind + b' ' + numi + b' 0 ' + fd)
        time.sleep(0.4)
        rr = bytes(str(int(self.r)), 'utf-8')
        gg = bytes(str(int(self.g)), 'utf-8')
        bb = bytes(str(int(self.b)), 'utf-8')
        arduino.write(ind + b' ' + numi + b' 1 ' + rr + b' ' + gg + b' ' + bb)
        print(ind + b' ' + numi + b' 1 ' + rr + b' ' + gg + b' ' + bb)

    def init_nope(self, sp):
        name = self.app.label1.get()
        pin = int(self.app.ffff.get())
        len = int(self.app.ff.get())

        p = bytes(str(pin), 'utf-8')
        fd = bytes(str(len), 'utf-8')  # - длинна светодиодов
        numi = bytes(str(len_class(self, sp)), 'utf-8')
        arduino.write(b'0 ' + p + b' ' + fd + b' ' + numi)
        print(b'0 ' + p + b' ' + fd + b' ' + numi)
        return MyLed(self.app, name, pin, len, len_class(self, sp))

class MyServo:

    def __init__(self, app, name="", pin=0, numi=0):
        self.app = app
        self.pin = pin
        self.name = name
        self.numi = numi
        self.ind = 1

    def main_elem(self, destroy=False): # - елементы интерфейса для управления
        if not destroy:
            self.app.f = customtkinter.CTkLabel(self.app, text="Degree:", fg_color="transparent")
            self.app.f.grid(row=0, column=0, padx=(200, 5), pady=(10, 20), sticky="w")
            self.app.ff = customtkinter.CTkEntry(self.app, width=50, border_width=0)
            self.app.ff.grid(row=0, column=0, padx=(260, 300), pady=(10, 20), sticky="w")
        else:
            self.app.f.destroy()
            self.app.ff.destroy()

    def init_elem(self, destroy=False):   # - елементы интерфейса инициализации
        if not destroy:
            self.app.f = customtkinter.CTkLabel(self.app, text="Pin:", fg_color="transparent")
            self.app.f.grid(row=0, column=0, padx=(200, 5), pady=(10, 20), sticky="w")
            self.app.ff = customtkinter.CTkEntry(self.app, width=30, border_width=0)
            self.app.ff.grid(row=0, column=0, padx=(230, 300), pady=(10, 20), sticky="w")
        else:
            self.app.f.destroy()
            self.app.ff.destroy()

    def send(self):
        numi = bytes(str(self.numi), 'utf-8')
        ind = bytes(str(self.ind), 'utf-8')
        fd = bytes(str(self.app.ff.get()), 'utf-8')
        arduino.write(ind + b' ' + numi + b' ' + fd)
        print(ind + b' ' + numi + b' ' + fd)

    def init_nope(self, sp):
        name = self.app.label1.get()
        pin = int(self.app.ff.get())

        p = bytes(str(pin), 'utf-8')
        numi = bytes(str(len_class(self, sp)), 'utf-8')
        arduino.write(b'1 ' + p + b' ' + numi)
        print(b'1 ' + p + b' ' + numi)
        return MyServo(self.app, name, pin, len_class(self, sp))



# -------------------------------------------------------------------------------
class_list = [MyServo, MyLed] # - список классов требуется для вывода интерфеса еще не инициализированных устройств
# ------------------------------------------------------------------------------------
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.ad = MyLed(self, 1, 15)
        self.init_device = []
        self.class_list = []
        for i in class_list:
            self.class_list.append(i(self))
        self.title("Arduino test project")
        self.geometry("800x400")
        self.grid_columnconfigure((0, 1), weight=1)

        self.done = customtkinter.CTkButton(self, text="Done", command=self.button_done)
        self.done.grid(row=5, column=2, padx=5, pady=(10, 20), sticky="w")

        self.create_init_hab(False)

    def button_apply_init(self):  # инициализация устройств
        global current_mode, init_pin, mode
        print("Mode:", current_mode)
        """if current_mode == "led":
            init.append(self.ff.get())
            p = bytes(current_pin, 'utf-8')
            fd = bytes(self.ff.get(), 'utf-8') # - длинна светодиодов
            self.init_device.append(MyLed(self, pin, fd))
            arduino.write(b'0 ' + p + b' ' + fd + b' 0')
            print(b'0 ' + p + b' ' + fd + b' 0')
        init_pin.append(" ".join(init))
        print("List init pin:", init_pin)"""
        self.init_device.append(self.class_list[mode.index(current_mode)].init_nope(self.init_device))
        init_pin.append(self.label1.get())

    def button_apply(self):  # 1
        global current_device, init_pin
        self.init_device[init_pin.index(current_device)].send()

    def button_done(self):
        arduino.write(b'done')
        print(b'done')
        self.create_init_hab(True)
        self.create_main_hab(False)

    # ------------------------------------------------------------------------------------------------------------------

    def create_init_hab(self, delete):
        if delete:
            self.button.destroy()
            self.optionmenumode.destroy()
            self.label.destroy()
            self.label1.destroy()
            self.class_list[mode.index(current_mode)].init_elem(destroy=True)
        else:
            self.class_list[0].init_elem()
            self.button = customtkinter.CTkButton(self, text="Применить", command=self.button_apply_init)
            self.button.grid(row=0, column=2, padx=5, pady=(10, 20), sticky="w")


            def optionmenu_callback_mode(choice):  # - тип выбранного устройства
                global current_mode
                self.class_list[mode.index(current_mode)].init_elem(destroy=True)
                self.class_list[mode.index(choice)].init_elem()
                current_mode = choice



            self.label = customtkinter.CTkLabel(self, text="Name:", fg_color="transparent")
            self.label.grid(row=1, column=0, padx=5, pady=(10, 20), sticky="w")
            self.label1 = customtkinter.CTkEntry(self, width=100, border_width=0)
            self.label1.grid(row=1, column=0, padx=(50, 300), pady=(10, 20), sticky="w")

            self.optionmenumode = customtkinter.CTkOptionMenu(self, values=mode, command=optionmenu_callback_mode)
            self.optionmenumode.grid(row=0, column=0, padx=5, pady=(10, 20), sticky="nw")



        # ------------------------------------------------------------------------------------------------------------------

    def create_main_hab(self, delete):
        if delete:
            pass # - пока у нас нет возможности вернутся назад
        else:
            global current_device, init_pin
            current_device = init_pin[0]
            self.init_device[0].main_elem()
            self.button = customtkinter.CTkButton(self, text="Применить", command=self.button_apply)
            self.button.grid(row=0, column=2, padx=5, pady=(10, 20), sticky="w")

            def optionmenu_callback_pin(choice):  # - текущее устройство
                global current_device, init_pin
                self.init_device[init_pin.index(current_device)].main_elem(destroy=True)
                self.init_device[init_pin.index(choice)].main_elem()
                current_device = choice

            self.optionmenupin = customtkinter.CTkOptionMenu(self, values=init_pin,
                                                             command=optionmenu_callback_pin)
            self.optionmenupin.grid(row=0, column=0, padx=5, pady=(10, 20), sticky="w")


app = App()
#customtkinter.set_appearance_mode("dark")
app.mainloop()
