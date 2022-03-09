from copy import deepcopy
from math import floor

def tfm(pos):
    """Transforms pos=('letter',number) into board indices (y,x)"""
    x, y = pos
    pos_d = {list('abcdefgh')[i-1]:i for i in range(1,9)}
    return pos_d[x], y

def rev_tfm(pos):
    """Transforms board indices (y,x) into pos=('letter',number)"""
    y, x = pos
    pos_d = {i:list('abcdefgh')[i-1] for i in range(1,9)}
    return pos_d[y], x

def h_moves(bd,pos,rng=8):
    x, y = tfm(pos)
    pc = bd.get_fig(pos)
    bd = bd.get_board()
    mvs = set()
    
    free = True
    for i in range(1,rng+1):
        try:
            assert 0<x+i<9 and free
            if not isinstance(bd[y][x+i],Piece):
                mvs.add(rev_tfm((x+i,y)))
            elif pc.gblack() ^ bd[y][x+i].gblack():
                mvs.add(rev_tfm((x+i,y)))
                free = False
            else:
                free = False
        except AssertionError:
            pass
    free = True
    for i in range(-1,-rng-1,-1):
        try:
            assert 0<x+i<9 and free
            if not isinstance(bd[y][x+i],Piece):
                mvs.add(rev_tfm((x+i,y)))
            elif pc.gblack() ^ bd[y][x+i].gblack():
                mvs.add(rev_tfm((x+i,y)))
                free = False
            else:
                free = False
        except AssertionError:
            pass
    return mvs

def v_moves(bd,pos,rng=8):
    x, y = tfm(pos)
    pc = bd.get_fig(pos)
    bd = bd.get_board()
    mvs = set()
    
    free = True
    if not isinstance(pc,Pawn) or not pc.gblack():
        for i in range(1,rng+1):
            try:
                assert 0<y+i<9 and free
                if not isinstance(bd[y+i][x],Piece):
                    mvs.add(rev_tfm((x,y+i)))
                elif not isinstance(pc,Pawn) and pc.gblack() ^ bd[y+i][x].gblack():
                    mvs.add(rev_tfm((x,y+i)))
                    free = False
                else:
                    free = False
            except AssertionError:
                pass
    free = True
    if not isinstance(pc,Pawn) or pc.gblack():
        for i in range(-1,-rng-1,-1):
            try:
                assert 0<y+i<9 and free
                if not isinstance(bd[y+i][x],Piece):
                    mvs.add(rev_tfm((x,y+i)))
                elif not isinstance(pc,Pawn) and pc.black ^ bd[y+i][x].gblack():
                    mvs.add(rev_tfm((x,y+i)))
                    free = False
                else:
                    free = False
            except AssertionError:
                pass
    return mvs

def d_moves(bd,pos,rng=8):
    x, y = tfm(pos)
    pc = bd.get_fig(pos)
    bd = bd.get_board()
    mvs = set()
    
    free = True
    if not isinstance(pc,Pawn) or not pc.gblack():
        for i in range(1,rng+1):
            try:
                assert 0<x+i<9 and 0<y+i<9 and free
                if not isinstance(pc,Pawn) and not isinstance(bd[y+i][x+i],Piece):
                    mvs.add(rev_tfm((x+i,y+i)))
                elif isinstance(bd[y+i][x+i],Piece):
                    free = False
                    if pc.gblack() ^ bd[y+i][x+i].gblack():
                        mvs.add(rev_tfm((x+i,y+i)))
                else:
                    free = False
            except AssertionError:
                pass
        free = True
        for i in range(1,rng+1):
            try:
                assert 0<x-i<9 and 0<y+i<9 and free
                if not isinstance(pc,Pawn) and not isinstance(bd[y+i][x-i],Piece):
                    mvs.add(rev_tfm((x-i,y+i)))
                elif isinstance(bd[y+i][x-i],Piece):
                    free = False
                    if pc.gblack() ^ bd[y+i][x-i].gblack():
                        mvs.add(rev_tfm((x-i,y+i)))
                else:
                    free = False
            except AssertionError:
                pass
    free = True
    if not isinstance(pc,Pawn) or pc.gblack():
        for i in range(-1,-rng-1,-1):
            try:
                assert 0<x+i<9 and 0<y+i<9 and free
                if not isinstance(pc,Pawn) and not isinstance(bd[y+i][x+i],Piece):
                    mvs.add(rev_tfm((x+i,y+i)))
                elif isinstance(bd[y+i][x+i],Piece):
                    free = False
                    if pc.gblack() ^ bd[y+i][x+i].gblack():
                        mvs.add(rev_tfm((x+i,y+i)))
                else:
                    free = False
            except AssertionError:
                pass
        free = True
        for i in range(-1,-rng-1,-1):
            try:
                assert 0<x-i<9 and 0<y+i<9 and free
                if not isinstance(pc,Pawn) and not isinstance(bd[y+i][x-i],Piece):
                    mvs.add(rev_tfm((x-i,y+i)))
                elif isinstance(bd[y+i][x-i],Piece):
                    free = False
                    if pc.gblack() ^ bd[y+i][x-i].gblack():
                        mvs.add(rev_tfm((x-i,y+i)))
                else:
                    free = False
            except AssertionError:
                pass
    return mvs

def k_moves(bd,pos):
    x, y = tfm(pos)
    pc = bd.get_fig(pos)
    bd = bd.get_board()
    mvs = set()
    
    for i in [-1,1,-2,2]:
        for j in [-1,1,-2,2]:
            try:
                assert 0<x+i<9 and 0<y+j<9 and abs(i)!=abs(j)
                if not isinstance(bd[y+j][x+i],Piece):
                     mvs.add(rev_tfm((x+i,y+j)))
                elif pc.gblack() ^ bd[y+j][x+i].gblack():
                    mvs.add(rev_tfm((x+i,y+j)))
            except AssertionError:
                continue
    return mvs

class Piece():
    def __init__(self,pos,black=False,first=True):
        self.pos = rev_tfm(pos)
        self.black = black
        self.first = first
        
    def gblack(self):
        return self.black
    
    def gpos(self):
        return self.pos
    
    def nfirst(self):
        self.first = False
        
    def spos(self,pos):
        self.pos = pos
        
    def make_move(self,bd,move):
        gm = bd.get_board()
        x, y = tfm(self.gpos())
        x1, y1 = tfm(move)
        if move in self.moves(bd):
            gm[y][x], gm[y1][x1] = '*', gm[y][x]
            self.spos(rev_tfm((x1,y1)))
            bd.inc()
            bd.add_history()
        else:
            print("Вы ввели неправильный ход")
            return self.make_move(bd)
        if self.first:
            self.nfirst()
        return gm
    
class Pawn(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        
    def __repr__(self):
        if self.black:
            return 'p'
        return 'P'
    
    def moves(self,bd):
        pos = self.gpos()
        if self.first:
            return d_moves(bd,pos,rng=1)|v_moves(bd,pos,rng=2)
        return d_moves(bd,pos,rng=1)|v_moves(bd,pos,rng=1)

class Knight(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        
    def __repr__(self):
        if self.black:
            return 'n'
        return 'N'
    
    def moves(self,bd):
        pos = self.gpos()
        return k_moves(bd,pos)
    
class Bishop(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        
    def __repr__(self):
        if self.black:
            return 'b'
        return 'B'
    
    def moves(self,bd):
        pos = self.gpos()
        return d_moves(bd,pos)

class Rook(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        
    def __repr__(self):
        if self.black:
            return 'r'
        return 'R'
    
    def moves(self,bd):
        pos = self.gpos()
        return h_moves(bd,pos)|v_moves(bd,pos)
    
class King(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        self.rng = 1
        
    def __repr__(self):
        if self.black:
            return 'k'
        return 'K'
    
    def moves(self,bd):
        pos = self.gpos()
        return d_moves(bd,pos,rng=1)|v_moves(bd,pos,rng=1)|h_moves(bd,pos,rng=1)
    
class Queen(Piece):
    def __init__(self,pos,black=False):
        Piece.__init__(self,pos,black)
        
    def __repr__(self):
        if self.black:
            return 'q'
        return 'Q'
    
    def moves(self,bd):
        pos = self.gpos()
        return d_moves(bd,pos)|v_moves(bd,pos)|h_moves(bd,pos)

class Board():
    def __init__(self,bd,n,dop={}):
        self.bd = bd
        self.n = n
        history = {}
        history.update(dop)
        self.history = history
    
    def get_board(self):
        return self.bd
        
    def display_board(self):
        for i in range(9,-1,-1):
            print(*self.bd[i],sep=' ')
            
    def get_moves(self):
        return self.n
    
    def set_board(self,new):
        self.bd = new
        
    def get_fig(self,pos):
        x,y = tfm(pos)
        return self.bd[y][x]
    
    def inc(self):
        self.n += 1
        
    def add_history(self):
        if self.n == 1:
            al = list(' ABCDEFGH ')
            gm = [list(f'{i}********{i}') for i in range(1,9)]
            bd = [al,*gm,al]
            bd[2][1:9] = [Pawn((i,2)) for i in range(1,9)]
            bd[7][1:9] = [Pawn((i,7),black=True) for i in range(1,9)]
            bd[1][1], bd[1][8] = Rook((1,1)), Rook((8,1))
            bd[1][2], bd[1][7] = Knight((2,1)), Knight((7,1))
            bd[1][3], bd[1][6] = Bishop((3,1)), Bishop((6,1))
            bd[1][4], bd[1][5] = Queen((4,1)), King((5,1))
            bd[8][1], bd[8][8] = Rook((1,8),black=True), Rook((8,8),black=True)
            bd[8][2], bd[8][7] = Knight((2,8),black=True), Knight((7,8),black=True)
            bd[8][3], bd[8][6] = Bishop((3,8),black=True), Bishop((6,8),black=True)
            bd[8][4], bd[8][5] = Queen((4,8),black=True), King((5,8),black=True)
            self.history[0] = Board(bd,0)
        self.history[self.n] = Board(deepcopy(self.bd),self.n,dop=deepcopy(self.history))
        
    def back(self,k):
        return self.history[self.n-k]
    
    def twokings(self):
        n = 0
        bd = self.get_board()
        for row in bd:
            for column in row:
                if isinstance(column,King):
                    n += 1
        return not bool(n%2)
    
def form(inp=None):
    if inp is None:
        f = input()
    else:
        f = inp
    try:
        if f == 'назад':
            return
        assert len(f)==2 and f[0] in list('abcdefgh') and f[1] in list('12345678')
    except AssertionError:
        print("Вы неправильно ввели ход")
        return form()
    return f[0],int(f[1])

def winner(bd):
    n = bd.get_moves()
    if n%2:
        return 'Белые'
    return 'Черные'

def who_move(bd):
    n = bd.get_moves()
    if n%2:
        return True
    return False

def play_game(board=None,file=None):
    if board is None:
        al = list(' ABCDEFGH ')
        gm = [list(f'{i}********{i}') for i in range(1,9)]
        bd = [al,*gm,al]
        bd[2][1:9] = [Pawn((i,2)) for i in range(1,9)]
        bd[7][1:9] = [Pawn((i,7),black=True) for i in range(1,9)]
        bd[1][1], bd[1][8] = Rook((1,1)), Rook((8,1))
        bd[1][2], bd[1][7] = Knight((2,1)), Knight((7,1))
        bd[1][3], bd[1][6] = Bishop((3,1)), Bishop((6,1))
        bd[1][4], bd[1][5] = Queen((4,1)), King((5,1))
        bd[8][1], bd[8][8] = Rook((1,8),black=True), Rook((8,8),black=True)
        bd[8][2], bd[8][7] = Knight((2,8),black=True), Knight((7,8),black=True)
        bd[8][3], bd[8][6] = Bishop((3,8),black=True), Bishop((6,8),black=True)
        bd[8][4], bd[8][5] = Queen((4,8),black=True), King((5,8),black=True)
        bd = Board(bd,0)
    else:
        bd = Board(board.get_board(),board.n,dop=board.history)
    if file is not None:
        MOVES = file
        for line in MOVES:
            if len(line.split()[1:]) == 1:
                break
            white, black = line.split()[1:]
            frm, to = white.split('--')
            frm, to = form(inp=frm), form(inp=to)
            pc = bd.get_fig(frm)
            mvs = pc.moves(bd)
            bd.set_board(pc.make_move(bd,to))
            frm, to = black.split('--')
            frm, to = form(inp=frm), form(inp=to)
            pc = bd.get_fig(frm)
            mvs = pc.moves(bd)
            bd.set_board(pc.make_move(bd,to))
        return bd
    else:
        while bd.twokings(): 
            print('Какой фигурой вы хотите походить?')
            bd.display_board()
            
            frm = form()
            pc = bd.get_fig(frm)
            mvs = pc.moves(bd)
            
            if frm is None:
                bd = bd.back(1)
                continue
            
            while not mvs or pc.gblack() != who_move(bd):
                if not mvs:
                    print('У этой фигуры нет доступных ходов')
                if pc.gblack() != who_move(bd):
                    print('Выберите фигуру своего цвета')
                frm = form()
                pc = bd.get_fig(frm)
                mvs = pc.moves(bd)
            
            print('Куда вы хотите походить?')
            move = form()
            while move not in mvs:
                print('Некорректный ход')
                print('Какой ход вы хотите совершить?')
                move = form()
                
            bd.set_board(pc.make_move(bd,move))
            with open('/home/alik/chess/game_2','a') as fl:
                if bd.get_moves()/2 % 1 == 0:
                    fl.write(f'{frm[0]+str(frm[1])}--{move[0]+str(move[1])}\n')
                else:
                    fl.write(f'{bd.get_moves()//2+1}. {frm[0]+str(frm[1])}--{move[0]+str(move[1])} ')
                
        print(f'Поздравляем, {winner(bd)} победили')
        return bd
        
def watch_game(fl):
    bd = play_game(file=fl)
    n = bd.get_moves()
    k = 0
    bod = bd.back(n)
    bod.display_board()
    f = ''
    while f != 'стоп':
        try:
            f = input()
            if f == 'вперед':
                k += 1
                bod = bd.back(n-k)
                bod.display_board()
            if f == 'назад':
                k -= 1
                bod = bd.back(n-k)
                bod.display_board()
            if f == 'старт':
                bd = bd.back(n-k)
                play_game(board=bd)
        except KeyError:
            print('Игра закончилась')
            print('Чтобы остановить просмотр, напишите стоп')

if __name__ == '__main__':
    with open('/home/alik/chess/game_2','r') as fl:
       watch_game(fl)
    #play_game()