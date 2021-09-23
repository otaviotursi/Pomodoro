import PySimpleGUI as sg
from threading import Event, Thread
import threading
from multiprocessing import Process
from psgtray import SystemTray

from win10toast import ToastNotifier
import time
from datetime import datetime, timedelta



class interface:
    def __init__(self):

        sg.theme('DarkAmber')
        tooltip = 'Tooltip'

        menu_def = ['', ['Show Window', 'Hide Window', '---',  'INICIAR', '---', 'ZERAR', '---', 'Exit']]
        layout = [[sg.Text('00:00', font=('Helvetica', 60), justification='center', key='-OUTPUT-')],      
                [sg.Button('INICIAR', key='-START-'), sg.Button('ZERAR', key='-BREAK-'), sg.Button('FECHAR', key='-STOP-')]]      

        self.janela = sg.Window('Pomodoro', layout, finalize=True, enable_close_attempted_event=True)      

        tray = SystemTray(menu_def, single_click_events=False, window=self.janela, tooltip=tooltip, icon='icon.png')
        # tray.show_message('System Tray', 'System Tray Icon Started!')
        
        while True:
            event, values = self.janela.read() 
            self.sinalParar = False

            print(event, values)       
            if event == tray.key:
                event = values[event]
            
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == '-STOP-':
                break
            elif event == '-START-':
                print("Aqui 1")
                threading.Thread(target=self.iniciarContagemPomo, args=(), daemon=True).start()
            elif event == 'INICIAR':
                print("Aqui 1 1")
                threading.Thread(target=self.iniciarContagemPomo, args=(), daemon=True).start()
            elif event == '-BREAK-':
                print("Aqui 2")
                self.sinalParar = True
            elif event == 'ZERAR':
                print("Aqui 2 2")
                self.sinalParar = True

            elif event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                self.janela.un_hide()
                self.janela.bring_to_front()
            elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
                self.janela.hide()
                tray.show_icon()
            elif event == 'Hide Icon':
                tray.hide_icon()
            elif event == 'Show Icon':
                tray.show_icon()
            elif event == 'Change Tooltip':
                tray.set_tooltip(values['-IN-'])


        tray.close()            # optional but without a close, the icon may "linger" until moused over
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
            # notifica a pessoa com um tempo de 25min
            toaster.show_toast("Pomodoro",
            "Iniciando contagem por 25min.",
            duration=5)
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
            duration=5)
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