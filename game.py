# coding: UTF-8
import tkinter
import random
from time import sleep 

# ループのインターバル時間
REFRESH = 30

class Othello:
    def __init__(self):
        self.board = Board()
        self.view = TkView(self.board)

        # プレイヤー先攻・後攻の辞書を定義する
        self.view.players = {}
    
    def play_game(self):

        global loop_count
        loop_count += 1
        # print("{}回目".format(loop_count))
        self.view.init_window()
        
        # 先攻・後攻の選択
        self.view.choice_attack()
        
        # ランダムプレーヤーのインスタンスを生成
        self.random = RandomPlayer(self.view)

        # 座標がキー、駒の状態を示す値をバリューとする辞書定義
        # (駒なし:0, 黒:1, 白:2)
        self.board.coord_to_piece = self.view.coord_to_piece 

        self.view_loop()
        self.hit_loop()
        self.view.mainloop()

    def view_loop(self):
            
            # # 検証用
            # self.view.players["first"] = "random"
            # self.view.players["second"] = "random_2"
            # self.view.players["wait"] = "ゲーム開始前"
            
            
            # if len(self.view.players) == 0:
            if "wait" not in self.view.players.keys():
                pass

            # ゲーム開始処理
            elif self.view.players[self.board.turn] == "ゲーム開始前":
                self.board.turn = "first"
                # tag情報を空にする   
                self.view.clicked_tag = "null"



            # humanのターンの時    
            elif self.view.players[self.board.turn] == "human" and self.view.set_flag == False:
                # 先攻後攻取得
                turn_num = self.board.turn
                if turn_num == "first":
                    piece_color = "Black piece"
                elif turn_num == "second":
                    piece_color = "White piece"
                else:
                    piece_color = ""        
                
                
                self.view.player_info = tkinter.Label(self.view.window, text='Turn of Human:  ' + piece_color, bg='#008080', fg='#000000', width=30)
                self.view.player_info.place(x=20, y=self.view.WINDOW_SIZE + 20)
                self.view.set_flag = True

            # randomのターンの時    
            elif self.view.players[self.board.turn] == "random" or self.view.players[self.board.turn] == "random_2" or self.view.players[self.board.turn] == "random_3" and self.view.set_flag == False:
                # 先攻後攻取得
                turn_num = self.board.turn
                if turn_num == "first":
                    piece_color = "Black piece"
                elif turn_num == "second":
                    piece_color = "White piece"
                else:
                    piece_color = ""  

                # player情報表示
                if self.view.players[self.board.turn] == "random":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(weak):  ' + piece_color, bg='#008080', fg='#000000', width=30)

                elif self.view.players[self.board.turn] == "random_2":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(little strong):  ' + piece_color, bg='#008080', fg='#000000', width=30)

                elif self.view.players[self.board.turn] == "random_3":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(strong):  ' + piece_color, bg='#008080', fg='#000000', width=30)
                
                self.view.player_info.place(x=20, y=self.view.WINDOW_SIZE + 20)
                self.view.set_flag = True
            
            # リスタート時にはループを抜ける
            if self.view.restart_flag:
                return
            else:    
                # ターン変更されるまで再帰処理               
                return self.view.window.after(REFRESH, self.view_loop)

    def hit_loop(self):
        
        # パスが連続した場合
        if self.board.finish_flag:
            pass
        else:         
            # ゲーム終了判断
            self.board.finish_game()
        
        # ゲームを終了フラグが立っていたらゲーム終了(ループぬける)
        if self.board.finish_flag:
            # 試合結果格納
            self.board.get_result(self.view)
            
            # 結果表示
            self.view.alert_finish(self.board)
            # print("game 終了")
            # リスタートするなら(ループ)
            if self.view.restart_flag:
                self.view.window.destroy()
                play_othello()

            # # 検証用    
            # self.view.window.destroy()
            # return

        # 手を打ったか、打っていないか判断,ゲーム終わっていないか判断
        if self.board.hit == False and self.board.finish_flag != True:
            # 可視化しているか確認
            if self.board.search_flag == False and self.board.turn != "wait":
                # 打てるマスの座標に色をつける
                self.search_avalable_cell()
                if len(self.board.search_hit_list_coord) != 0:
                    for cell in self.board.search_hit_list_coord:
                        # 可視化
                        self.view.draw_avalable_cell(cell)
            if self.view.clicked_tag != "null":
                

                # ゲーム開始しているか確認(human player)
                if self.board.turn != "wait" and self.view.players[self.board.turn] == "human":

                

                    # クリックされたtagから座標を検索
                    coord = self.view.tag_to_coord[self.view.clicked_tag]

                    # 駒が置けるマスか確認
                    self.board.check_avalable_hit(coord, self.view)
                    # 駒が置けるマスなら  
                    if self.board.avalable_hit:

                        # 置いた駒のデータ保存
                        self.board.dohit(coord)

                        # 駒をひっくり返す
                        self.board.reverse_piece(coord,self.view)

                        
                        # 置いた駒の点描
                        # 先攻なら黒駒
                        if self.board.turn == "first":
                            self.view.draw_piece_black(coord)

                        # 後攻なら白駒    
                        elif self.board.turn == "second":
                            self.view.draw_piece_white(coord)
                        
                        # tag情報を空にする   
                        self.view.clicked_tag = "null"

                        # 手を打ったことを変数に明記
                        self.board.hit = True
                        
                         # アラートがあればを削除
                        if self.view.alert_flag == True:
                            self.view.delete_alert()
                        else:
                            pass    
                        
                        # 可視化削除
                        if len(self.board.search_hit_list_coord) != 0:
                                for cell in self.board.search_hit_list_coord:
                                    # 可視化削除メソッド
                                    self.view.delete_avalable_cell(cell)

                        # ターン変更
                        self.board.change_turn()

                        if self.view.set_flag:
                            self.view.player_info.destroy()
                        self.view.set_flag = False
        
                    else:
                        self.view.alert_message_human()



                # ゲーム開始しているか確認(random player)         
            if self.board.turn != "wait" and self.view.players[self.board.turn] == "random":
                    self.random_hit_1()
            elif self.board.turn != "wait" and self.view.players[self.board.turn] == "random_2":
                    self.random_hit_2()   
            elif self.board.turn != "wait" and self.view.players[self.board.turn] == "random_3":
                    self.random_hit_3()

        
        return self.view.window.after(500, self.hit_loop)
        
    # 打てるマス検索
    def search_avalable_cell(self):
        # 初期化
        self.board.search_hit_list_coord = []
        self.board.search_hit_list_tag = []
        self.board.search_flag = True

        # 打てる手を保存したリストを生成(可視化用)
        self.random.search_hit(self.board)
        for tag in self.board.search_hit_list_tag:
            coord = self.view.tag_to_coord[tag]
            piece_count = self.board.coord_to_piece[coord]
            if piece_count == 0:
                self.board.search_hit_list_coord.append(coord) 

    # 打てるマス検索(コンピューター用)
    def random_avalable_cell(self):
        # 初期化
        self.board.random_hit_list_coord = []
        self.board.random_hit_list_tag = []
        
        # 打てる手を保存したリストを生成
        self.random.random_hit(self.board)
        for tag in self.board.random_hit_list_tag:
            coord = self.view.tag_to_coord[tag]
            piece_count = self.board.coord_to_piece[coord]
            if piece_count == 0:
                self.board.random_hit_list_coord.append(coord)  
    
    # コンピューター用(完全乱数)
    def random_hit_1(self):
        # 試行中メッセージ表示
        self.view.alert_message_random()
        # humanが打った後は待機時間を作り、盤面を表示する(すぐにコンピューターにいくと、自分が打ってどうなったかわかりにくい)
        # sleep(0.5)
        self.search_avalable_cell()
        self.random_avalable_cell()

        # 打てる手数を計算する 
        hit_count = len(self.board.random_hit_list_coord)

        # 乱数で手を選ぶ
        if hit_count == 0 and self.board.finish_flag == False:
            # パスアラート欲しかったらこれをコメントアウト解除
            # self.view.alert_pass()
            # お互い打つ手がなくなった時にゲーム終了する
            # (パスしたらフラグを立てる。パスが連続したら、ゲーム終了する)
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("手詰り")
                     
            self.board.change_turn()
            # self.view.set_flag = False    
        else:
            # お互い打つ手がなくなった時にゲーム終了する
            # (パスしたらフラグを立てる。パスが連続したら、ゲーム終了する)
            self.pass_count = 0

            if hit_count == 1:
                coord_list_idx = 0
            else:
                coord_list_idx = random.randint(0,hit_count-1)
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)

    # コンピューター用(少し強い)
    def random_hit_2(self):
        # 試行中メッセージ表示
        self.view.alert_message_random()
        # humanが打った後は待機時間を作り、盤面を表示する(すぐにコンピューターにいくと、自分が打ってどうなったかわかりにくい)
        # sleep(0.5)
        self.search_avalable_cell()
        self.random_avalable_cell()

        # 打てる手数を計算する 
        hit_count = len(self.board.random_hit_list_coord)

        # 乱数で手を選ぶ
        if hit_count == 0 and self.board.finish_flag == False:
            # パスアラート欲しかったらこれをコメントアウト解除
            # self.view.alert_pass()
            # お互い打つ手がなくなった時にゲーム終了する
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("手詰り")

            self.board.change_turn()
            # self.view.set_flag = False    
        else:
            # pass回数リセット
            self.pass_count = 0

            if hit_count == 1:
                coord_list_idx = 0
            else:
                for x in range(0,8,7):
                    for y in range(0,8,7):
                        for dx in range(-1,2,1):
                            for dy in range(-1,2,1):
                                around_tag = str(x+dx) + "_" + str(y+dy)
                                if around_tag != "0_0" and around_tag != "7_7" and around_tag != "7_0" and around_tag != "0_7":

                                    # 角周りを避ける
                                    for ran_coord in self.board.random_hit_list_coord:
                                        random_tag = self.view.coord_to_tag[ran_coord]
                                        
                                        if around_tag == random_tag and len(self.board.random_hit_list_coord) != 1:
                                            around_idx = self.board.random_hit_list_coord.index(ran_coord)
                                            self.board.random_hit_list_coord.pop(around_idx)
                
                # 打てる手数を計算する 
                hit_count = len(self.board.random_hit_list_coord)
                if hit_count == 1:
                    coord_list_idx = 0
                else:      
                    # 乱数で手を選ぶ
                    coord_list_idx = random.randint(0,hit_count-1)

                                   
                # 角をとれるならとる     
                for coord in self.board.random_hit_list_coord:
                    random_tag = self.view.coord_to_tag[coord]

                    # 角をとれるならとる
                    if random_tag == "0_0" or random_tag == "0_7" or random_tag == "7_0" or random_tag == "7_7":
                        coord_list_idx = self.board.random_hit_list_coord.index(coord)
                                       
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)

     # コンピューター用(強い)
    
    def random_hit_3(self):
        # 試行中メッセージ表示
        self.view.alert_message_random()
        # humanが打った後は待機時間を作り、盤面を表示する(すぐにコンピューターにいくと、自分が打ってどうなったかわかりにくい)
        # sleep(0.5)
        self.search_avalable_cell()
        self.random_avalable_cell()

        # 打てる手数を計算する 
        hit_count = len(self.board.random_hit_list_coord)

        # 乱数で手を選ぶ
        if hit_count == 0 and self.board.finish_flag == False:
            # パスアラート欲しかったらこれをコメントアウト解除
            # self.view.alert_pass()
            # お互い打つ手がなくなった時にゲーム終了する
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("手詰り")

            self.board.change_turn()
            # self.view.set_flag = False    
        else:
            if hit_count == 1:
                coord_list_idx = 0
            else:
                for x in range(0,8,7):
                    for y in range(0,8,7):
                        for dx in range(-1,2,1):
                            for dy in range(-1,2,1):
                                around_tag = str(x+dx) + "_" + str(y+dy)
                                if around_tag != "0_0" and around_tag != "7_7" and around_tag != "7_0" and around_tag != "0_7":

                                    # 角周りを避ける
                                    for ran_coord in self.board.random_hit_list_coord:
                                        random_tag = self.view.coord_to_tag[ran_coord]
                                        
                                        if around_tag == random_tag and len(self.board.random_hit_list_coord) != 1:
                                            around_idx = self.board.random_hit_list_coord.index(ran_coord)
                                            self.board.random_hit_list_coord.pop(around_idx)
                
                # 打てる手数を計算する 
                hit_count = len(self.board.random_hit_list_coord)
                if hit_count == 1:
                    coord_list_idx = 0
                else:
                    # 評価表を使った最善手の計算
                    max_eval_coord = ""
                    max_eval_score = -100000
                    for coord in self.board.random_hit_list_coord:
                        random_tag = self.view.coord_to_tag[coord]
                        random_evalvalue = self.board.tag_to_evalvalue[random_tag]
                        if random_evalvalue > max_eval_score:
                            max_eval_score = random_evalvalue
                            max_eval_coord = coord
                    coord_list_idx = self.board.random_hit_list_coord.index(max_eval_coord)


                                   
                # 角をとれるならとる     
                for coord in self.board.random_hit_list_coord:
                    random_tag = self.view.coord_to_tag[coord]

                    # 角をとれるならとる
                    if random_tag == "0_0" or random_tag == "0_7" or random_tag == "7_0" or random_tag == "7_7":
                        coord_list_idx = self.board.random_hit_list_coord.index(coord)
                                       
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)
    
    # random_hit共通処理
    def common_hit(self, coord):
        # 置いた駒のデータ保存
        self.board.dohit(coord)

        # 駒をひっくり返す
        self.board.reverse_piece(coord,self.view)

        # 置いた駒の点描
        # 先攻なら黒駒
        if self.board.turn == "first":
            self.view.draw_piece_black(coord)

        # 後攻なら白駒    
        elif self.board.turn == "second":
            self.view.draw_piece_white(coord)
            
        # 手を打ったことを変数に明記
        self.board.hit = True
        
        # アラートがあればを削除
        if self.view.alert_flag == True:                    
            self.view.delete_alert()
        else:
            pass    

        # 可視化削除
        if len(self.board.search_hit_list_coord) != 0:
                for cell in self.board.search_hit_list_coord:
                    # 可視化削除メソッド
                    self.view.delete_avalable_cell(cell)

        # ターン変更
        self.board.change_turn()
        
        self.view.set_flag = False                    

# オセロ盤面作成
class TkView:
    def __init__(self, board):

        # ウィンドウサイズ、セルサイズ、ウィンドウからのオフセット指定
        self.WINDOW_SIZE = 590
        self.CELL_SIZE = 70
        self.BOARD_OFFSET = 15
        
        # ターン表示用の変数
        self.set_flag = False

        # アラート表示用の変数
        self.alert_flag = False

        self.board = board

        self.restart_flag = False

        self.restart_flag_alert = False

        self.pass_flag_alert = False

    def init_window(self):
        self.window = tkinter.Tk()
        self.window.title("Othello")
        self.window.resizable(width=False, height=False)
        self.window.attributes("-topmost", True)

        # コンストラクタによりセットされた情報からキャンバスを作成
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.WINDOW_SIZE,
            height=self.WINDOW_SIZE  + 80
            )

        # キャンバス内に正方形を点描
        self.canvas.create_rectangle(
            0, 0, self.WINDOW_SIZE, self.WINDOW_SIZE, fill="green")

        # キャンバス内に情報表示用のスペースを作成
        self.canvas.create_rectangle(
            0, self.WINDOW_SIZE, self.WINDOW_SIZE, self.WINDOW_SIZE - self.BOARD_OFFSET + 100 , fill="white")

        # cellのtagを保存するリスト生成(1_2, 3_5など)
        self.cells_tag = []

        # tagがキー、座標がバリューの辞書定義
        self.tag_to_coord = {}

        # 座標がキー、tagがバリューの辞書定義
        self.coord_to_tag = {}

        # クリックされたtag保存変数
        self.clicked_tag = "null"

        # 座標がキー、駒の状態を示す値をバリューとする辞書定義
        # (駒なし:0, 黒:1, 白:2)
        self.coord_to_piece = {}

        # 座標保持用の変数(x軸用)
        i = 0
        for h in range(
                self.BOARD_OFFSET,
                self.WINDOW_SIZE -
                self.BOARD_OFFSET,
                self.CELL_SIZE):

            # 座標保持用の変数(y軸用)    
            j = 0
            for v in range(
                    self.BOARD_OFFSET,
                    self.WINDOW_SIZE -
                    self.BOARD_OFFSET,
                    self.CELL_SIZE):

                tag = "{}_{}".format(i, j)

                # x,y座標とセルサイズ指定により、オセロ盤を点描
                coord = (h, v, h + self.CELL_SIZE, v + self.CELL_SIZE)
                self.canvas.create_rectangle(*coord, fill="green", tags=tag)

                # リスト、辞書に情報を追加
                self.cells_tag.append(tag)
                self.tag_to_coord[tag] = coord
                self.coord_to_tag[coord] = tag

                # 初期駒の設置
                if j == 3 and i == 3 or j == 4 and i == 4:
                    # 黒駒
                    self.coord_to_piece[coord] = 1
                    self.canvas.create_oval(*coord, fill="black", tags=tag)

                elif j == 3 and i == 4 or j == 4 and i == 3:
                    # 白駒
                    self.coord_to_piece[coord] = 2
                    self.canvas.create_oval(*coord, fill="white", tags=tag)
  

                else:
                    # 駒情報を辞書に追加
                    # (最初は初期化)
                    self.coord_to_piece[coord] = 0

                # tagのｙ座標成分に+1
                j += 1

            # tagのx軸成分に+1    
            i += 1

        self.canvas.pack()
        
        # セルクリック時のイベント設定
        for tag in self.cells_tag:
            self.canvas.tag_bind(tag, "<ButtonPress-1>", self.check_click)

       # クリック判定(盤面)
    def check_click(self, event):
        # 存在する座標を生成
        for h in range(
                self.BOARD_OFFSET,
                self.WINDOW_SIZE -
                self.BOARD_OFFSET,
                self.CELL_SIZE):
            for v in range(
                    self.BOARD_OFFSET,
                    self.WINDOW_SIZE -
                    self.BOARD_OFFSET,
                    self.CELL_SIZE):
                coord = (h, v, h + self.CELL_SIZE, v + self.CELL_SIZE)
                # クリックされた場所がどのセルに当てはまるか検索する
                if h <= event.x <= h + self.CELL_SIZE and v <= event.y <= v + self.CELL_SIZE:
                    # クリックされたtag保存変数
                    self.clicked_tag = self.coord_to_tag[coord]
    
    # ゲームモードの選択
    def choice_attack(self):
        #モード選択ボタン配置
        self.describe = tkinter.Label(self.window, text='Mode', bg='#008080', fg='#000000', width=10)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        # mode_1 (human vs human)
        self.mode_1_button =  tkinter.Button(self.window, text='Human vs Human', bg='#008080', fg='#000000', width=20, command=self.mode_1_clicked)
        self.mode_1_button.place(x=20, y=self.WINDOW_SIZE + 50)

        # mode_2(human vs random)
        self.mode_2_button =  tkinter.Button(self.window, text='Human vs CPU', bg='#008080', fg='#000000', width=20, command=self.mode_2_clicked)
        self.mode_2_button.place(x=200, y=self.WINDOW_SIZE + 50)

        # mode_3(random vs random)
        self.mode_3_button =  tkinter.Button(self.window, text='CPU vs CPU', bg='#008080', fg='#000000', width=20, command=self.mode_3_clicked)
        self.mode_3_button.place(x=380, y=self.WINDOW_SIZE + 50)

    # mode_1クリック時(human vs human)
    def mode_1_clicked(self):
        # モード選択ボタンを削除
        self.mode_destory()

        self.players["first"] = "human"
        self.players["second"] = "human"
        self.players["wait"] = "ゲーム開始前"
    
    # mode_2クリック時(human vs random)
    def mode_2_clicked(self):

        # モード選択ボタン削除
        self.mode_destory()

        #  (先攻ボックス)
        self.before_button = tkinter.Button(self.window, text='Going first:Black piece', bg='#008080', fg='#000000', width=20, command=self.before_clicked)
        self.before_button.place(x=20, y=self.WINDOW_SIZE + 20)

        #  (後攻ボックス)
        self.after_button = tkinter.Button(self.window, text='Second attack:White piece', bg='#008080', fg='#000000', width=20, command=self.after_clicked)
        self.after_button.place(x=200, y=self.WINDOW_SIZE + 20)

    # mode_3クリック時(randmo vs random)
    def mode_3_clicked(self):

        # モード選択ボタンを削除
        self.mode_destory()

        self.describe = tkinter.Label(self.window, text='Choice strength(Going first)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        #  (先攻ボックス)
        self.before_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(0))
        self.before_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(1))
        self.before_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(2))
        self.before_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)

    # モード選択ボタン削除
    def mode_destory(self):
        self.mode_1_button.destroy()
        self.mode_2_button.destroy()
        self.mode_3_button.destroy()
        self.describe.destroy()

    # 先攻ボタンクリック時(human vs random)            
    def before_clicked(self):
        # ボタンクリック後、ボタンを削除
        self.before_button.destroy()
        self.after_button.destroy()
        self.players["first"] = "human"
        self.after_computer()

    # 後攻ボタンクリック時(human vs random)
    def after_clicked(self):
        # ボタンクリック後、ボタンを削除
        self.before_button.destroy()
        self.after_button.destroy()
        self.players["second"] = "human"
        self.before_computer()
    
    # 後攻ボタンクリック時(human vs random)
    def before_computer(self):
        # 表示削除
        self.describe.destroy()

        self.describe = tkinter.Label(self.window, text='Choice strength(Going first)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        #  (先攻ボックス)
        self.before_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(0))
        self.before_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(1))
        self.before_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(2))
        self.before_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)

    # 後攻ボタンクリック時(human vs random)
    def before_computer_clicked_human(self, id_num):
        if id_num == 0:
            self.players["first"] = "random"
        elif id_num == 1:
            self.players["first"] = "random_2"
        elif id_num == 2:
            self.players["first"] = "random_3"
        
        self.players["wait"] = "ゲーム開始前"
        self.before_computer_1.destroy()
        self.before_computer_2.destroy()
        self.before_computer_3.destroy()
        self.describe.destroy()

    # コンピューターの選択(先攻) tkinterのcommandの特質より関数をネストして使用
    def before_computer_clicked(self, id_num):        
        if id_num == 0:
            self.players["first"] = "random"

        elif id_num == 1:
            self.players["first"] = "random_2"
        
        elif id_num == 2:
            self.players["first"] = "random_3"
      
        self.before_computer_1.destroy()
        self.before_computer_2.destroy()
        self.before_computer_3.destroy()
        self.after_computer()

    def after_computer(self):
        # 表示削除
        self.describe.destroy()

        self.describe = tkinter.Label(self.window, text='Choice strength(second attack)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        #  (後攻ボックス)
        self.after_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(0))
        self.after_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.after_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(1))
        self.after_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
    
        self.after_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(2))
        self.after_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)
    
    # コンピューターの選択(後攻) tkinterのcommandの特質より関数をネストして使用
    def after_computer_clicked(self, id_num):
        if id_num == 0:
            self.players["second"] = "random"

        elif id_num == 1:
            self.players["second"] = "random_2"
        
        elif id_num == 2:
            self.players["second"] = "random_3"

        self.players["wait"] = "ゲーム開始前"
        self.after_computer_1.destroy()
        self.after_computer_2.destroy()
        self.after_computer_3.destroy()
        self.describe.destroy()

    # 駒が打たれた時の駒の点描(先攻の場合)
    def draw_piece_black(self, coord):
        tag = self.coord_to_tag[coord]
        self.canvas.create_oval(*coord, fill="black", tags=tag)

    # 駒が打たれた時の駒の点描(先攻の場合)
    def draw_piece_white(self, coord):
        tag = self.coord_to_tag[coord]
        self.canvas.create_oval(*coord, fill="white", tags=tag)

    # おけるマスの可視化
    def draw_avalable_cell(self,coord):
        tag = self.coord_to_tag[coord]
        tag = tag + "arc"
        self.canvas.create_oval(*coord,outline="red", tags=tag)

    # 可視化削除メソッド
    def delete_avalable_cell(self,coord):
        tag = self.coord_to_tag[coord]
        tag = tag + "arc"
        self.canvas.delete(tag)
            
    #置けない所がクリックされた場合(human plyaer)    
    def alert_message_human(self):
        # アラートが表示されていなければ
        if self.alert_flag == False:
            self.alert = tkinter.Label(self.window, text="Don't hit there", bg='#008080', fg='#000000', width=50)
            self.alert.place(x=200, y=self.WINDOW_SIZE + 20)
            
            # アラート表示に変更
            self.alert_flag = True

        else:
            pass

    #試行中のアラート(random plyaer)    
    def alert_message_random(self):
        # アラートが表示されていなければ
        if self.alert_flag == False:
            self.alert = tkinter.Label(self.window, text='Thinking', bg='#008080', fg='#000000', width=40)
            self.alert.place(x=250, y=self.WINDOW_SIZE + 20)
            
            # アラート表示に変更
            self.alert_flag = True
        else:
            pass

    # パスアラート(random player)
    def alert_pass(self):
        if self.pass_flag_alert == False:
            self.alert_pass_button = tkinter.Button(self.window, text='Pass your turn', bg='#008080', fg='#000000', width=20, command=self.turn_pass)
            self.pass_flag_alert = True
        self.alert_pass_button.place(x=200, y=self.WINDOW_SIZE + 50)
        # アラート表示に変更
        self.alert_flag = True

    # パス実行
    def turn_pass(self):
        self.alert_pass_button.destroy()
        self.alert_flag = False
        self.pass_flag_alert = False
        # ターン変更
        self.board.change_turn()

    # アラート削除メソッド
    def delete_alert(self):
        self.alert.destroy()
        self.alert_flag = False
    
    #ゲーム終了アラート   
    def alert_finish(self, board):
        black_count = board.result_count[0]
        white_count = board.result_count[1]
        
        self.alert = tkinter.Label(self.window, text='Finish game', bg='#008080', fg='#000000', width=40)
        if self.restart_flag_alert == False:
            self.alert_restart = tkinter.Button(self.window, text='Play again', bg='#008080', fg='#000000', width=20, command=self.restart_game)
            self.restart_flag_alert = True
        self.result = tkinter.Label(self.window, text="Going fisrt(Black piece):" + str(black_count) + "\n" + "Second attack(White piece):" + str(white_count), bg='#008080', fg='#000000', width=40)

        self.alert.place(x=250, y=self.WINDOW_SIZE + 20)
        self.alert_restart.place(x=20, y=self.WINDOW_SIZE + 50)
        self.result.place(x=250, y=self.WINDOW_SIZE + 40)
    
    # 再びゲームをする
    def restart_game(self):
        self.restart_flag = True

    def mainloop(self):
        self.window.mainloop()

# ゲームプレイヤーのクラスを定義する
class Player:
    def __init__(self, *args, **kargs):
        pass

    def __str__(self):
        return 'super player'

    def play(self, board):
        pass

# 人間のプレイヤー
class HumanPlayer(Player):
    def __init__(self, view):
        self.view = view

# コンピューターのプレイヤー
class RandomPlayer(Player):
    def __init__(self, view):
        self.view = view
        

    def random_hit(self, board):

        for x in range(0,8):
            for y in range(0,8):
                random_tag = str(x) + "_" + str(y)
                coord = self.view.tag_to_coord[random_tag]

                # 現在の情報
                piece_count = board.coord_to_piece[coord]

                # 置けるかどうか確認
                board.check_random_hit(coord, self.view)  
      
    def search_hit(self, board):

        for x in range(0,8):
            for y in range(0,8):
                random_tag = str(x) + "_" + str(y)
                coord = self.view.tag_to_coord[random_tag]

                # 置けるかどうか確認
                board.check_search_hit(coord, self.view)                      

# 盤面情報,ゲーム情報管理クラス   
class Board:
    def __init__(self):


        # ターン管理変数(first:先攻, second:後攻 wait:ゲーム前)
        self.turn = "wait"

        # ターン数カウント変数
        self.count = 0

        # 手を打ったかの変数
        self.hit = False

        # 置けるマスか判断
        self.avalable_hit = False

        #ひっくり返す時の終点を保存する辞書定義
        self.reverse_dic = {}

        # 先攻：1 後攻:2の辞書定義
        self.turn_to_piece = {}
        self.turn_to_piece["first"] = 1
        self.turn_to_piece["second"] = 2

        # ランダムに打つ時の打てる手リスト
        self.random_hit_list_tag = []
        self.random_hit_list_coord = []
        
        # 可視化用に打つ時の打てる手リスト
        self.search_hit_list_tag = []
        self.search_hit_list_coord = []

        # お互い打つ手がなくなった時にゲーム終了する
        self.pass_count = 0

        # ゲームを終了フラグ
        self.finish_flag = False 

        #ゲーム結果格納リスト
        self.result_count = []

        # 再びゲーム開始ボタンフラグ
        self.restart_flag = False

        # 可視化しているか確認フラグ
        self.search_flag = False

        # 評価表の辞書
        self.tag_to_evalvalue = {}
        self.tag_to_evalvalue["0_0"] = 30
        self.tag_to_evalvalue["0_1"] = -12
        self.tag_to_evalvalue["0_2"] = 0
        self.tag_to_evalvalue["0_3"] = -1
        self.tag_to_evalvalue["0_4"] = -1
        self.tag_to_evalvalue["0_5"] = 0
        self.tag_to_evalvalue["0_6"] = -12
        self.tag_to_evalvalue["0_7"] = 30
        self.tag_to_evalvalue["1_0"] = -12
        self.tag_to_evalvalue["1_1"] = -15
        self.tag_to_evalvalue["1_2"] = -3
        self.tag_to_evalvalue["1_3"] = -3
        self.tag_to_evalvalue["1_4"] = -3
        self.tag_to_evalvalue["1_5"] = -3
        self.tag_to_evalvalue["1_6"] = -15
        self.tag_to_evalvalue["1_7"] = -12
        self.tag_to_evalvalue["2_0"] = 0
        self.tag_to_evalvalue["2_1"] = -3
        self.tag_to_evalvalue["2_2"] = 0
        self.tag_to_evalvalue["2_3"] = -1
        self.tag_to_evalvalue["2_4"] = -1
        self.tag_to_evalvalue["2_5"] = 0
        self.tag_to_evalvalue["2_6"] = -3
        self.tag_to_evalvalue["2_7"] = 0
        self.tag_to_evalvalue["3_0"] = -1
        self.tag_to_evalvalue["3_1"] = -3
        self.tag_to_evalvalue["3_2"] = -1
        self.tag_to_evalvalue["3_3"] = -1
        self.tag_to_evalvalue["3_4"] = -1
        self.tag_to_evalvalue["3_5"] = -1
        self.tag_to_evalvalue["3_6"] = -3
        self.tag_to_evalvalue["3_7"] = -1
        self.tag_to_evalvalue["4_0"] = -1
        self.tag_to_evalvalue["4_1"] = -3
        self.tag_to_evalvalue["4_2"] = -1
        self.tag_to_evalvalue["4_3"] = -1
        self.tag_to_evalvalue["4_4"] = -1
        self.tag_to_evalvalue["4_5"] = -1
        self.tag_to_evalvalue["4_6"] = -3
        self.tag_to_evalvalue["4_7"] = -1
        self.tag_to_evalvalue["5_0"] = 0
        self.tag_to_evalvalue["5_1"] = -3
        self.tag_to_evalvalue["5_2"] = 0
        self.tag_to_evalvalue["5_3"] = -1
        self.tag_to_evalvalue["5_4"] = -1
        self.tag_to_evalvalue["5_5"] = 0
        self.tag_to_evalvalue["5_6"] = -3
        self.tag_to_evalvalue["5_7"] = 0
        self.tag_to_evalvalue["6_0"] = -12
        self.tag_to_evalvalue["6_1"] = -15
        self.tag_to_evalvalue["6_2"] = -3
        self.tag_to_evalvalue["6_3"] = -3
        self.tag_to_evalvalue["6_4"] = -3
        self.tag_to_evalvalue["6_5"] = -3
        self.tag_to_evalvalue["6_6"] = -15
        self.tag_to_evalvalue["6_7"] = -12
        self.tag_to_evalvalue["7_0"] = 30
        self.tag_to_evalvalue["7_1"] = -125
        self.tag_to_evalvalue["7_2"] = 0
        self.tag_to_evalvalue["7_3"] = -1
        self.tag_to_evalvalue["7_4"] = -1
        self.tag_to_evalvalue["7_5"] = 0
        self.tag_to_evalvalue["7_6"] = -12
        self.tag_to_evalvalue["7_7"] = 30

    # コマが置けるかどうかの判断
    def check_avalable_hit(self, coord, view):

        # 初期化
        x = 0
        y = 0
        # コマが置いてあるかどうか
        # (1)コマが置いていない場合
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                # (2)ひっくり返せる手であるか
                # クリックされた座標を確認する
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]

        # 置けるマスか判断
        self.check_piece_around(int(x), int(y), view)
       
    # コマが置けるかどうかの判断
    def check_random_hit(self, coord, view):

        # 初期化
        x = 0
        y = 0
        # コマが置いてあるかどうか
        # (1)コマが置いていない場合
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                # (2)ひっくり返せる手であるか
                # クリックされた座標を確認する
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]
                # 置けるマスか判断
                self.check_piece_around(int(x), int(y), view)

    # 可視化用メソッド
    def check_search_hit(self, coord, view):

        # 初期化
        x = 0
        y = 0
        # コマが置いてあるかどうか
        # (1)コマが置いていない場合
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                # (2)ひっくり返せる手であるか
                # クリックされた座標を確認する
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]
                # 置けるマスか判断
                self.check_search_around(int(x), int(y), view)

     # 周辺に自分の駒があるか確認するメソッド(選択マスの8方向)
    
    def check_search_around(self, x, y, view):


        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2
        else:
            my_color_num = 0    
  
        # 周辺8方向の座標で検索
        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                # 存在しないマスをはじく
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    # dx = 0 and dy = 0をはじく
                    if not (dx == 0 and dy == 0):

                        maked_tag = str(x + dx) + "_" + str(y + dy) 

                        # 周辺のマスの状態を確認する
                        # 調べるマスの状態取得
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
                                                
                        # 調べるマスに駒がないマス、もしくは自分の駒がある時は置けない
                        if piece_color_num == 0 :
                            pass
                        elif piece_color_num == my_color_num:
                            pass   

                            # 調べるマスに相手の駒がある場合    
                        elif piece_color_num != my_color_num:
                            hit_flag = self.check_search_around_2(x + dx, y + dy, dx, dy, view)


                            # ランダム用
                            if hit_flag:
                                self.search_hit_list_tag.append(str(x) + "_" + str(y))
    
      # 置ける可能性のあるマスの方向で検索                
    
    def check_search_around_2(self,x,y,dx,dy,view):
        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2
        else:
            my_color_num = 0    


        # 調べるマス取得
        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
  
            maked_tag = str(x + dx) + "_" + str(y + dy)
            # 取得マスの状態確認
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
            
            # 調べるマスに駒がないマス、もしくは自分の駒がある時は置けない
            if piece_color_num == 0 :
                pass

            # 調べたマスが自分の駒だったら                
            elif piece_color_num == my_color_num:
                return True

            # 調べるマスに相手の駒がある場合    
            elif piece_color_num != my_color_num:
                return self.check_search_around_2(x + dx, y + dy, dx, dy, view)
                
    # 周辺に自分の駒があるか確認するメソッド(選択マスの8方向)
    def check_piece_around(self, x, y, view):

        avalable_flag = False

        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2
        else:
            my_color_num = 0    
  
        # 周辺8方向の座標で検索
        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                # 存在しないマスをはじく
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    # dx = 0 and dy = 0をはじく
                    if not (dx == 0 and dy == 0):

                        maked_tag = str(x + dx) + "_" + str(y + dy) 

                        # 周辺のマスの状態を確認する
                        # 調べるマスの状態取得
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
                                                
                        # 調べるマスに駒がないマス、もしくは自分の駒がある時は置けない
                        if piece_color_num == 0 :
                            pass
                        elif piece_color_num == my_color_num:
                            pass   

                            # 調べるマスに相手の駒がある場合    
                        elif piece_color_num != my_color_num:
                            hit_flag = self.check_piece_around_2(x + dx, y + dy, dx, dy, view)

                            # ランダム用
                            if hit_flag:
                                self.random_hit_list_tag.append(str(x) + "_" + str(y))
                            

                else:
                    pass

    # 置ける可能性のあるマスの方向で検索                
    def check_piece_around_2(self,x,y,dx,dy,view):
        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2
        else:
            my_color_num = 0    


        # 調べるマス取得
        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
  
            maked_tag = str(x + dx) + "_" + str(y + dy)
            # 取得マスの状態確認
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
            
            # 調べるマスに駒がないマス、もしくは自分の駒がある時は置けない
            if piece_color_num == 0 :
                pass

            # 調べたマスが自分の駒だったら                
            elif piece_color_num == my_color_num:
                self.avalable_hit = True
                return True

            # 調べるマスに相手の駒がある場合    
            elif piece_color_num != my_color_num:
                return self.check_piece_around_2(x + dx, y + dy, dx, dy, view)
  
    def dohit(self, coord):
         
        # 先攻が打ったら
        if self.turn == "first":
            self.coord_to_piece[coord] = 1
            

        # 後攻が打ったら    
        else:
            self.coord_to_piece[coord] = 2
    
    # ひっくり返すメソッド
    def reverse_piece(self,coord,view):
        tag = view.coord_to_tag[coord]
        x = int(tag.split("_")[0])
        y = int(tag.split("_")[1])
        # ひっくり返す終点保存辞書生成
        self.reverse_piece_around(int(x), int(y), view)

        # 終点と方向からひっくり返す駒検索
        for finish_point, dx_dy in self.reverse_dic.items():

            # 増加方向
            dx = int(dx_dy.split("_")[0])
            dy = int(dx_dy.split("_")[1])
            
            # ひっくり返す終点
            finish_x = int(finish_point.split("_")[0])
            finish_y = int(finish_point.split("_")[1])
            
            # ひっくり返すマス
            reverse_x = x + dx
            reverse_y = y + dy

            # 終点まで検索
            count = 1
            while(reverse_x != finish_x or reverse_y != finish_y):
                reverse_x = x + dx * count
                reverse_y = y + dy * count
                reverse_tag = str(reverse_x) + "_" + str(reverse_y)

                # 駒をひっくり返す(データ上)
                self.coord_to_piece[view.tag_to_coord[reverse_tag]] = self.turn_to_piece[self.turn]
                
                # 駒をひっくり返す(表示上)
                if self.turn == "first":
                    view.draw_piece_black(view.tag_to_coord[reverse_tag])
                elif self.turn == "second":
                    view.draw_piece_white(view.tag_to_coord[reverse_tag])
                
                # 次の方向検索
                count += 1    
 
    # ひっくり返す駒があるか確認するメソッド(選択マスの8方向)
    def reverse_piece_around(self, x, y, view):
        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2
  
        # 周辺8方向の座標で検索
        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                # 存在しないマスをはじく
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    # dx = 0 and dy = 0をはじく
                    if not (dx == 0 and dy == 0):

                        maked_tag = str(x + dx) + "_" + str(y + dy) 

                        # 周辺のマスの状態を確認する
                        # 調べるマスの状態取得
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
                                                
                        # 調べるマスに相手の駒がある場合    
                        if piece_color_num != my_color_num and piece_color_num != 0:
                            self.reverse_piece_around_2(x + dx, y + dy, dx, dy, view)
                else:
                    pass    
    
     # ひっくり返すマスの方向で終点を検索                
    
    def reverse_piece_around_2(self,x,y,dx,dy,view):
        # 打ったプレーヤーの駒の色確認
        if self.turn == "first":
            # 黒色の場合
            my_color_num = 1
        elif self.turn == "second":
            # 白色の場合
            my_color_num = 2

        # 調べるマス取得
        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:

            maked_tag = str(x + dx) + "_" + str(y + dy) 
            # 取得マスの状態確認
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]

            # 調べたマスが自分の駒だったら                
            if piece_color_num == my_color_num:
                # ひっくり返す終点を保存する辞書にタグと方向を追加
                dx_dy = str(dx) + "_" + str(dy)
                self.reverse_dic[maked_tag] = dx_dy

            # 調べるマスに相手の駒がある場合    
            elif piece_color_num != my_color_num and piece_color_num != 0:
                return self.reverse_piece_around_2(x + dx, y + dy, dx, dy, view)

# ターン変更メソッド
    def change_turn(self):
        # 先攻から後攻へターン変更
        if self.turn == "first":
            self.turn = "second"
            
        # 後攻から先攻にターン変更    
        elif self.turn == "second":
            self.turn = "first"

        
        # 手を打ったかどうかフラグ初期化
        self.hit = False

        # 置けるマスがあるかどうかフラグ初期化 
        self.avalable_hit = False
        
        # 終点保存辞書初期化
        self.reverse_dic = {}
        
        # 可視化メソッド用フラグ
        self.search_flag = False

        # 書き込みフラグ
        self.result_write_flag = False

    # ゲーム終了判断メソッド
    def finish_game(self):
        finish_flag = True

        for count in self.coord_to_piece.values():
            # 空のマスがあるならFalse
            if count == 0:
                finish_flag = False

        # # 手詰まりならゲーム終了する
        # if self.pass_count == 2:
        #     finish_flag = True
        #     print("手詰まり finish_game")

        self.finish_flag = finish_flag

    # ゲーム結果取得メソッド
    def get_result(self,view):
        # 駒のカウント変数
        black_count = 0
        white_count = 0
 
        for piece in self.coord_to_piece.values():
            if piece == 1:
                black_count += 1
            elif piece == 2:
                white_count += 1
        
        # 結果をリストに格納し、セット
        result_count = [black_count,white_count]
        self.result_count = result_count
        
        first_player = view.players["first"]
        second_player = view.players["second"]
        
        result_message = "first: " + first_player + ": " + str(black_count) + ", "
        result_message += "second: " + second_player + ": " + str(white_count) + "\n"
        
        # # 検証用コード
        # if self.result_write_flag == False:
        #     # 結果書き込み
        #     with open("./result.txt", mode='a') as f:
        #         f.write(result_message)
        #     self.result_write_flag = True
        # return             

def play_othello():
    # オセロクラスのインスタンスを生成
    othello = Othello()

    # ゲームを開始する
    othello.play_game()

loop_count = 0
while(loop_count < 1):
    play_othello()



    


