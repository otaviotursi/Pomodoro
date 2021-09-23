'''
    Programa simples desenvolvido para estudo e melhorar o tempo de execução das minhas tarefas diarias utilizando o método de Pomodoro. 
    Método esse que você deve ficar 25 minutos totalmente imerso na sua tarefa e 5 minutos de descanso, se repetindo conforme o outro ciclo acaba.
    O projeto funciona em Background, ou seja você pode fechar ele, que ele ficará no menu de icones ocultos funcionando.
'''

import PySimpleGUI as sg
import threading
from psgtray import SystemTray
import time
from datetime import datetime, timedelta



class interface:
    def __init__(self):
        #GUI 
        sg.theme('DarkAmber')
        tooltip = '-Pomodoro-'

        menu_def = ['', ['Mostrar Janela', 'Esconder Janela', '---',  'INICIAR', '---', 'PARAR', '---', 'FECHAR']]
        layout = [[sg.Text('00:00', font=('Helvetica', 60), justification='center', key='-OUTPUT-')],      
                [sg.Button('INICIAR', key='-START-'), sg.Button('PARAR', key='-BREAK-'), sg.Button('FECHAR', key='-CLOSE-')]]      

        self.janela = sg.Window('Pomodoro', layout, finalize=True, enable_close_attempted_event=True, element_justification='c', icon=r'icon.ico')      
        
        # NOTIFICAÇÃO
        self.tray = SystemTray(menu_def, single_click_events=False, window=self.janela, tooltip=tooltip, icon='icon.ico')
        
        # CICLO WHILE DE EVENTOS
        while True:
            event, values = self.janela.read() 
            self.sinalParar = False

            print(event, values)       
            if event == self.tray.key:
                event = values[event]

            if event in (sg.WIN_CLOSED, 'FECHAR', '-CLOSE-'):
                break
            elif event in ('-START-', 'INICIAR'):
                threading.Thread(target=self.iniciarContagemPomo, args=(), daemon=True).start()
            elif event in ('-BREAK-', 'PARAR'):
                self.sinalParar = True
            elif event in ('Mostrar Janela', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                self.janela.un_hide()
                self.janela.bring_to_front()
            elif event in ('Esconder Janela', sg.WIN_CLOSE_ATTEMPTED_EVENT):
                self.janela.hide()
                self.tray.show_icon()
            elif event == 'Hide Icon':
                self.tray.hide_icon()
            elif event == 'Show Icon':
                self.tray.show_icon()
            elif event == 'Change Tooltip':
                self.tray.set_tooltip(values['-IN-'])


        self.tray.close()
        self.janela.close()

    def iniciarContagemPomo(self):
        # define um temporizador de 25 minutos
        contadorTempo = datetime.today() - timedelta(hours=0, minutes=-25)
        self.contadorTempo = contadorTempo.strftime('%H:%M:%S')
        self.janela["-OUTPUT-"].update('25:00')

        threading.Thread(target=self.notificarInicioPomo, args=(), daemon=True).start()
        self.contarTempo('Pomo')
        
    def notificarInicioPomo(self):
        try:
            # notifica a pessoa que o programa esta funcionando
            self.tray.show_message('Pomodoro', 'Iniciando contagem por 25 minutos!')
        except Exception as e:
            print("Erro toaster", e)

    def iniciarContagemPausa(self):
        # define um temporizador de 5 minutos para a pausa
        contadorTempo = datetime.today() - timedelta(hours=0, minutes=-5)
        self.contadorTempo = contadorTempo.strftime('%H:%M:%S')
        self.janela["-OUTPUT-"].update('5:00')

        threading.Thread(target=self.notificarInicioPausa, args=(), daemon=True).start()
        self.contarTempo('Pausa')
        
    def notificarInicioPausa(self):
        try:
            # notifica a pessoa que o programa esta funcionando
            self.tray.show_message('Pomodoro', 'Iniciando pausa por 5 minutos!')
        except Exception as e:
            print("Erro toaster", e)

    def contarTempo(self, tipo):
        while 1:
            # decrementa o temporizador de tarefa, quando chega em zero, ele pausa a execução e inicia o temporizador de pausa
            time.sleep(1)

            now1 = datetime.now().strftime('%H:%M:%S')
            diferenca = datetime.strptime(self.contadorTempo, '%H:%M:%S') - datetime.strptime(now1, '%H:%M:%S')
            print('diferenca: ', diferenca)
            self.janela["-OUTPUT-"].update(str(diferenca)[2:7])

            # mudar tooltip
            if tipo == "Pomo":
                status = 'Trabalhar'
            else:
                status = 'Pausa'
            self.tray.set_tooltip(f'-Pomodoro-\nTempo: {str(diferenca)[2:7]}\nStatus: {status}')

            # checa se o tempo se esgotou e qual o tipo de ação se é 25 ou 5 minutos (pausa)
            if '00:00' == str(diferenca)[2:7]:
                if tipo == 'Pomo':
                    self.iniciarContagemPausa()
                else:
                    self.iniciarContagemPomo()

            # se o usuário solicitar então o programa para de executar, e zera a contagem até nova ordem
            if self.sinalParar:
                self.janela["-OUTPUT-"].update('25:00')
                break

if __name__ == '__main__':
    interface()