import PySimpleGUIQt as sg
# import PySimpleGUIWx as sg
# import PySimpleGUI as sg
from threading import Event, Thread
import threading
from multiprocessing import Process

navAbrir = 'True'
from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta


# toaster.show_toast("Example two",
# "This notification is in it's own thread!",
# icon_path=None,
# duration=5,
# threaded=True)
# # Wait for threaded notification to finish
# while toaster.notification_active(): time.sleep(0.1)

# menu_def = ['BLANK', ['&Start', '---', '&Stop', '---', 'E&xit']]

# tray = sg.SystemTray(menu=menu_def, filename=r'icon.png')

# def contador(contTemp):
#     contTemp += 1
#     print(contTemp)
#     time.sleep(1)


# tray.ShowMessage('title', 'message', time=1000000)

# while True:  # The event loop
#     menu_item = tray.read()
#     print('99', menu_item)
#     if menu_item == 'Exit':
#         break
#     elif menu_item == 'Start':
#         sg.popup('Iniciando o Pomodoro')
#     elif menu_item == 'Stop':
#         sg.popup('Finalizando o Pomodoro')


class interface:
    def __init__(self):

        sg.theme('DarkAmber')

        layout = [[sg.Text('00:00', font=('Helvetica', 60), justification='center', key='-OUTPUT-')],      
                [sg.Button('INICIAR', key='-START-'), sg.Button('ZERAR', key='-BREAK-')]]      

        self.janela = sg.Window('Pomodoro', layout)      

        while True:
            event, values = self.janela.read() 
            self.sinalParar = False

            print(event, values)       
            if event == sg.WIN_CLOSED or event == 'Exit':
                break      
            elif event == '-START-':
                print("Aqui 1")
                threading.Thread(target=self.iniciarContagemPomo, args=(), daemon=True).start()
            elif event == '-BREAK-':
                print("Aqui 2")
                self.sinalParar = True

        self.janela.close()

    def iniciarContagemPomo(self):
        print("aqui5")
        # define um temporizador de 25 minutos
        contadorTempo = datetime.today() - timedelta(hours=0, minutes=-0.5)
        self.contadorTempo = contadorTempo.strftime('%H:%M:%S')
        self.janela["-OUTPUT-"].update('25:00')

        threading.Thread(target=self.notificarInicioPomo, args=(), daemon=True).start()
        self.contarTempo('Pomo')
        
    def notificarInicioPomo(self):
        try:
            sg.SystemTray.notify('Notification Title', 'This is the notification message')
            # notifica a pessoa com um tempo de 25min
            toaster.show_toast("Pomodoro",
            "Iniciando contagem por 25min.",
            duration=10)
        except Exception as e:
            print("Erro toaster", e)

    def iniciarContagemPausa(self):
        # define um temporizador de 5 minutos para a pausa
        contadorTempo = datetime.today() - timedelta(hours=0, minutes=-0.5)
        self.contadorTempo = contadorTempo.strftime('%H:%M:%S')
        self.janela["-OUTPUT-"].update('5:00')

        threading.Thread(target=self.notificarInicioPausa, args=(), daemon=True).start()
        self.contarTempo('Pausa')
        
    def notificarInicioPausa(self):
        try:
            # notifica a pessoa com um tempo de 5min
            toaster.show_toast("Pomodoro",
            "Iniciando pausa de 5 min.",
            duration=10)
        except Exception as e:
            print("Erro toaster", e)

    def contarTempo(self, tipo):
        while 1:
            # decrementa o temporizador, quando chega em zero, ele pausa a execução e inicia o temporizador de pausa
            time.sleep(1)

            now1 = datetime.now().strftime('%H:%M:%S')
            diferenca = datetime.strptime(self.contadorTempo, '%H:%M:%S') - datetime.strptime(now1, '%H:%M:%S')
            self.janela["-OUTPUT-"].update(str(diferenca)[2:7])

            if '00:00' == str(diferenca)[2:7]:
                print("aqui3")
                if tipo == 'Pomo':
                    self.iniciarContagemPausa()
                else:
                    self.iniciarContagemPomo()

            if self.sinalParar:
                print('aqui4', self.sinalParar)
                self.janela["-OUTPUT-"].update('25:00')
                break

if __name__ == '__main__':
    toaster = ToastNotifier()
    interface()