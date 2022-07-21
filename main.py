import PySimpleGUI as sg, random
import numpy as np
from random import randint

class Board:
    score = 0
    mask_rate = 0.7 #DEFAULT_MASK_RATE = 0.7 - % Ячеек, которые нужно скрыть
    size = 3
    lang = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37']
    #solution = [] - Создается в def createSolution(self)
    #puzzle = [] - Создается в def createPuzzle(self)

    def createSolution(self):                                               #Функция для создания нашей матрицы решения
        '''Функция для создания нашей матрицы решения'''                                              
        size = self.size
        self.solution = np.zeros((size*size, size*size), np.int)            #Создает матрицу nxn, заполненную нулями
        for i in range(size*size):                                          #Создаем типовой массив для нашего судоку
            for j in range(size*size):
                self.solution[i, j] = (i*size + i/size + j) % (size*size) + 1
    
    def createPuzzle(self):                                                 #Функция для создания самого судоку на основе решения (solution)   
        '''Функция для создания самого судоку на основе решения (solution)'''
        self.puzzle = self.solution.copy()
        self.puzzle[np.random.choice([True, False], size=self.solution.shape, p=[self.mask_rate, 1 - self.mask_rate])] = 0
    
    def translate(self):                                                    #Функция перевода на другой алфавит
        '''Функция перевода на другой алфавит'''
        size = self.size
        solutionABC = [[''] * size*size for i in range(size*size)]          #Создаем пустой массив solutionABC
        puzzleABC = [[''] * size*size for i in range(size*size)]            #Создаем пустой массив puzzleABC
        for i in range(size*size):
            for j in range(size*size):
                solutionABC[i][j] = self.lang[self.solution[i, j]]          #Записываем переведенный символ в solutionABC
                puzzleABC[i][j] = self.lang[self.puzzle[i, j]]              #Записываем переведенный символ в puzzleABC
        self.solution = solutionABC.copy()                                  #Копируем переведенный массив в исходный
        self.puzzle = puzzleABC.copy()                                      #Копируем переведенный массив в исходный
    
    def transpositing(self):                                                #Функция транспонирования матрицы решения
        '''Функция транспонирования матрицы решения'''
        self.solution = np.array(list(map(list, zip(*self.solution))))
    

    def row_swap(self):                                                     #Функция рандомной замены местами двух строк внутри блока
        '''Функция рандомной замены местами двух строк внутри блока'''
        size = self.size
        for i in range(0, size*size, size):                                 #Проходит по всем блокам в матрице 1 раз
            r, c = randint(i, i+size-1), randint(i, i+size-1)               #Выбирает два рандомных индекса строк в блоке
            a = np.array(self.solution[c])                                  #Замена двух строк с использованием дополнительной переменной
            self.solution[c] = self.solution[r]                             #Кортежная замена не возможна, так как solution это 
            self.solution[r] = a                                            #list в numpy - отдельный объект со своими свойствами - не обычный list
    
    def row_box_swap(self):                                                 #Функция рандомной замены местами двух блоков судоку
        '''Функция рандомной замены местами двух блоков судоку'''
        size = self.size
        for i in range(0, size*size, size):                                 #Проходит по всем блокам в матрице 1 раз
            j = randint(0, size-1)*size                                     #Выбираем блок от первого до n-ного, * size - получаем индекс первого элемента в блоке
            for k in range(size):                                           #Проходит по всем строкам в блоке
                arr = np.array(self.solution[i+k])                          #Замена строк блока i на строку блока j n раз, n = size
                self.solution[i+k] = self.solution[j+k]
                self.solution[j+k] = arr
    
def create_and_show_puzzle(window, board):                            
    '''Фунция для создания готового решения поля судоку и вывода в окно'''
    generate_sudoku(board)                                                  #Вызываем фунцию для создания готового решения поля судоку 
    for r, row in enumerate(board.puzzle):                                  #Заполняем все ячейки на нашем поле судоку puzzle, созданном на основе solution
        for c, col in enumerate(row):
            window[r, c].update(board.puzzle[r][c] if board.puzzle[r][c] else '', background_color=sg.theme_input_background_color()) 

def generate_sudoku(board):                                                 #Функция полной генерации судоку
       '''Функция полной генерации судоку'''
       board.createSolution()
       mix(board)
       board.createPuzzle()
       board.translate()

def mix(board):                                                             #Функция рандомного перемешивания solution (решения)
    '''Функция рандомного перемешивания solution (решения)'''
    for i in range(randint(0, board.size**2)): board.row_swap()             #Рандомно перемешивает строки
    for i in range(randint(0, board.size**2)): board.row_box_swap()         #Рандомно перемешивает блоки
    board.transpositing()                                                   #Транспонируем матрицу решений чтобы столбцы стали строками
    for i in range(randint(0, board.size**2)): board.row_swap()             #Делаем то же самое
    for i in range(randint(0, board.size**2)): board.row_box_swap()
    board.transpositing()                                                   #Транспонируем матрицу обратно


def check_progress(window, board):
    '''Функция check_progress, проверяет решение'''
    solved = True                                                           #Флаг для проверки, решил ли пользователь судоку
    for r, row in enumerate(board.solution):                                #Проходит по всем значениям solution (решения)
        for c, col in enumerate(row):
            value = window[r, c].get()                                      #Берет текущее значение из ячейки
            if value:                                                       #Если в ячейке что-то есть
                if value != board.solution[r][c]:                           #Если значение не соответствует верному, выделяем красным
                    window[r, c].update(background_color='red')
                    solved = False                                          #Убираем флаг
                else:
                    window[r, c].update(background_color=sg.theme_input_background_color()) #Иначе возвращаем нормальный цвет фона
            else:
                solved = False                                              #Убираем флаг
                window[r, c].update(background_color='yellow')              #Если значения просто нет, красим в желтый
    return solved

def window_create(board):                                                   #Функция создания окна
    
    size = board.size
    window = sg.Window(
        'Судоку', [[sg.T('Размер доски:'), sg.B('2x2'), sg.B('3x3'), sg.B('4x4'), sg.B('5x5'), sg.B('6x6')], ] + 
        [[sg.T('Сложность:'), sg.B('Элементарно'), sg.B('Легко'), sg.B('Средне'), sg.B('Боль'), sg.B('До смерти')], ] +
        [[sg.T('Алфавит доски:'), sg.B('Числа'), sg.B('Ru'), sg.B('En'), sg.B('Свой')],] + 
        [[sg.Frame('', [[sg.I(random.randint(1, board.size*size), justification='r', size=(size, 1), enable_events=True,
        key=(fr * size + r, fc * size + c)) for c in range(size)] for r in range(size)]) for fc in range(size)] for fr in range(size)] +[[sg.B('Решение'), sg.B('Проверка'), sg.B('Подсказка'), sg.B('Новая игра'), 
        sg.T('Счет побед: ' + str(board.score), key='-SCORE-')], ], finalize=True
         )    
    return window

def main(mask_rate):
    board = Board()                                                         #Создаем переменную нашего класса - доску
    window = window_create(board)                                           #Создаем окно

    create_and_show_puzzle(window, board)                                   #Создаем судоку и вписываем его в наше окно
    check_showing = False
    while True:                                                             #Бесконечный цикл
        event, values = window.read()                                       #Считывание данных с окна
        if event == sg.WIN_CLOSED:                                          #Если окно закрыли
            break

        if event == 'Решение':                                              #Если была нажата кнопка Solve
            for r, row in enumerate(board.solution):
                for c, col in enumerate(row):
                    window[r, c].update(board.solution[r][c], background_color=sg.theme_input_background_color())
                    
        elif event == 'Проверка':                                           #Если была нажата кнопка Check
            check_showing = True
            solved = check_progress(window, board)
            if solved:
                board.score += 1
                window['-SCORE-'].update('Счет побед: ' + str(board.score))
                sg.popup('Поздравляем! Вы решили судоку правильно.')

        elif event == 'Подсказка':                                          #Если была нажата кнопка Hint
            elem = window.find_element_with_focus()
            try:
                elem.update(board.solution[elem.Key[0]][elem.Key[1]], background_color=sg.theme_input_background_color())
            except:
                pass                                                        #Скорее всего, потому что элемент ввода не имеет фокуса

        elif event == 'Новая игра':                                         #Если была нажата кнопка New Game
            create_and_show_puzzle(window, board)
        
        elif event == '2x2' and len(board.lang) > 4:                        #Если была нажата кнопка 2x2
            window.close()
            board.size = 2
            window = window_create(board)
            create_and_show_puzzle(window, board)
            check_showing = False
        
        elif event == '3x3' and len(board.lang) > 9:                        #Если была нажата кнопка 3x3
            window.close()
            board.size = 3
            window = window_create(board)
            create_and_show_puzzle(window, board)
            check_showing = False
        
        elif event == '4x4'and len(board.lang) > 16:                        #Если была нажата кнопка 4x4
            window.close()
            board.size = 4
            window = window_create(board)
            create_and_show_puzzle(window, board)
            check_showing = False
        
        elif event == '5x5'and len(board.lang) > 25:                        #Если была нажата кнопка 5x5
            window.close()
            board.size = 5
            window = window_create(board)
            create_and_show_puzzle(window, board)
            check_showing = False

        elif event == '6x6'and len(board.lang) > 36:                        #Если была нажата кнопка 5x5
            window.close()
            board.size = 6
            window = window_create(board)
            create_and_show_puzzle(window, board)
            check_showing = False

        elif event == 'Числа':                                              #Если был выбран алфавит Numbers
            board.lang = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37']
            create_and_show_puzzle(window, board)

        elif event == 'Ru':                                                 #Если был выбран алфавит Ru
            board.lang = ['', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            create_and_show_puzzle(window, board)

        elif event == 'En':                                                 #Если был выбран алфавит En
            board.lang = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
            create_and_show_puzzle(window, board)

        elif event == 'Свой':                                               #Если был выбран алфавит Custom, создаю новое окно custom
            custom = sg.Window('Судоку', [[sg.T('Напишите алфавит через пробел:')], ] + [[sg.In('', size=(30, 2), key='-LANG-')],] + [[sg.B('Продолжить'), sg.B('Отмена')], ], finalize=True)
            while True:
                event_custom, _ = custom.read()
                if event_custom == sg.WIN_CLOSED:                           #Если окно закрыли
                    break
                if event_custom == 'Продолжить':                            #Если пользователь нажал кнопку Continue
                    if len(custom['-LANG-'].get().split(' ')) >= board.size**2: #Проверка на размер введенного алфавита
                        board.lang = custom['-LANG-'].get().split(' ')      #Если проверка пройдена, тогда составляем алфавит
                        board.lang.insert(0, '')                            #Добавляем в начало алфавита пустой элемент (нужен для puzzle)
                        custom.close()
                        create_and_show_puzzle(window, board)               #Составляем новое судоку для нового алфавита
                        break                                               
                    else:                                                   #Если алфавит меньше размера доски, выводит сообщение об ошибке и возвращает обратно 
                        zhulik = sg.Window('Судоку', [[sg.T('Вы ввели алфавит меньше размера поля судоку(')], ] + [[sg.B('Продолжить')], ], finalize=True)
                        while True:
                            event_zhulik, _ = zhulik.read()
                            if event_zhulik == sg.WIN_CLOSED:               #Если окно закрыли
                                break
                            if event_zhulik == 'Продолжить':
                                zhulik.close()
                                break
                if event_custom == 'Отмена':
                    custom.close()
                    break

        elif event == 'Элементарно':                                        #Если была выбрана сложность Элементарно
            board.mask_rate = 0.01
            create_and_show_puzzle(window, board)

        elif event == 'Легко':                                              #Если была выбрана сложность Easy
            board.mask_rate = 0.1
            create_and_show_puzzle(window, board)

        elif event == 'Средне':                                             #Если была выбрана сложность Medium
            board.mask_rate = 0.3
            create_and_show_puzzle(window, board)

        elif event == 'Боль':                                               #Если была выбрана сложность Pain and suffering
            board.mask_rate = 0.5
            create_and_show_puzzle(window, board)
        
        elif event == 'До смерти':                                          #Если была выбрана сложность To death
            board.mask_rate = 0.7
            create_and_show_puzzle(window, board)
        
        elif check_showing:                                                 #Если было введено значение, меняем цвета на поле на обычные
            check_showing = False
            for r, row in enumerate(board.solution):
                for c, col in enumerate(row):
                    window[r, c].update(background_color=sg.theme_input_background_color())
    window.close()

if __name__ == "__main__":
    DEFAULT_MASK_RATE = 0.7                                                 # % Ячеек, которые нужно скрыть
    main(DEFAULT_MASK_RATE)