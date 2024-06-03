import pyxel

KEY = [pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
D =   [[0,1],[0,-1],[1,0],[-1,0]  , [0,0]]
GPAD = [pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
LAXIS = [pyxel.GAMEPAD1_AXIS_LEFTY,pyxel.GAMEPAD1_AXIS_LEFTY,
         pyxel.GAMEPAD1_AXIS_LEFTX,pyxel.GAMEPAD1_AXIS_LEFTX]
LAXIS_RANGE = [[20000,36000],[-36000,-20000],[20000,36000],[-36000,-20000]]

START_STAGE=0
stars = []
g_objs = []
my_blasters = []
my_bombs = []
explo1s = []
explo2s = []
radars = []  #1台しか存在しないけど 
icbms = []  #1発しか存在しないけど
planes = []  #1機しか存在しないけど
paras = []  #1袋しか存在しないけど
packs = []  #1パックしか存在しないけど
tanks = []  #1両しか存在しないけど
missiles = []
carriers = []
balloons = []

class GroundObject():
    def __init__(self,type) -> None:
        #self.type = type
        self.is_active = True
        uvwhs = [
            [0,32,16,16,-20],[16,32,16,16,0],[32,32,16,16,0],
            [48,35,16,13,40],[66,37,12,11,0],[80,16,8,32,0]
        ]
        self.u = uvwhs[type][0]
        self.v = uvwhs[type][1]
        self.w = uvwhs[type][2]
        self.h = uvwhs[type][3]
        self.score = uvwhs[type][4]
        self.x = 240
        self.y = 200 - self.h
    def update(self):
        self.x -= 2
        if self.x < -64:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.u,self.v,self.w,self.h,6)

class Star():
    def __init__(self) -> None:
        self.x = pyxel.rndi(240,270)
        self.y = pyxel.rndi(0,190)
        self.cnt = pyxel.rndi(0,100)
        self.is_active = True
    def update(self):
        self.cnt += 1
        self.x -= 2
        if self.x < 0:
            self.is_active = False
    def draw(self):
        pyxel.pset(self.x,self.y,self.cnt//12%3*7)

class MyBlaster():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_active = True
    def update(self):
        self.x += 6
        if self.x > 260:
            self.is_active = False
    def draw(self):
        pyxel.rectb(self.x,self.y,12,1,9)

class MyBomb():
    def __init__(self,x,y,dx,dy) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.is_active = True
        self.cnt = 0
    def update(self):
        if self.cnt < 11:
            self.cnt += 1
            #self.x += self.dx
            self.y += self.dy
        self.x += self.dx
        self.y += 1.4
        if self.y > 192:
            self.is_active = False
    def draw(self):
        if self.cnt < 11:
            pyxel.blt(self.x,self.y,  0,  32,24, 8,8, 0)
        else:
            pyxel.blt(self.x,self.y,  0,  40,24, 8,8, 0)

class Explo1():  ### 自機の爆発エフェクト
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 24
        self.is_active = True
    def update(self):
        self.cnt -= 1
        self.x -= 2
        if self.cnt < 0:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y,  0,  self.cnt//4%3*16,80,  16,8, 0)

class Explo2():  ### 地上の物体の爆発エフェクト
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 24
        self.is_active = True
    def update(self):
        self.cnt -= 1
        self.x -= 2
        if self.cnt < 0:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y,  0,  self.cnt//4%3*8,88,  8,8, 0)

class Radar():
    def __init__(self) -> None:
        self.x = 240
        self.y = 200 - 12
        self.w = 11
        self.h = 12
        self.is_active = True
    def update(self):
        self.x -= 2
        if self.x < -12:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 3+pyxel.frame_count//12%2*16,52, 11,12, 0)

class Icbm():
    def __init__(self) -> None:
        self.x = 240
        self.y = 200 - 12
        self.w = 11
        self.h = 12
        self.is_active = True
    def update(self):
        self.x -= 2
        if self.x < -12:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 35+pyxel.frame_count//12%2*16,52, 11,12, 0)

class Plane():
    def __init__(self) -> None:
        self.x = pyxel.rndi(-300,-40)
        self.y = 20
        self.is_active = True
        self.is_droped = False
        self.drop_x = pyxel.rndi(140,200)
    def update(self):
        self.x += 1
        if not self.is_droped:
            if self.x > self.drop_x:
                paras.append(Para(self.x+8,self.y+8))
                self.is_droped = True
        if self.x > 250:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y,  0,  0,128, 24,8,  0)
class Para():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_active = True
        self.release_flag = False
    def update(self):
        if self.y < 60:
            self.x -= 0.2
            self.y += 1
        elif self.y < 192:
            self.x -= 2
            self.y += 1
        else:
            self.is_active = False
    def draw(self):
        if self.release_flag:
            h = 10
        else:
            h = 15
        if self.y < 30:
            pyxel.blt(self.x,self.y,  0,  0,141, 16,h,  0)
        else:
            pyxel.blt(self.x,self.y,  0,  16,141, 16,h,  0)
class Pack():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.explosion_flag = False
        self.is_active = True
    def update(self):
        self.y += 1
        self.x -= 0.2
        if self.y > 192:
            self.explosion_flag = True
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 3,152, 10,5, 0)

class Missile():
    def __init__(self) -> None:
        self.x = pyxel.rndi(240,300)
        self.y = pyxel.rndi(40,150)
        self.dy = pyxel.rndf(-0.1,0.1)
        self.is_active = True
    def update(self):
        self.x -= 4
        self.y += self.dy
        if self.x < -20:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 0,122, 16,5, 0)

class Carrier():
    def __init__(self) -> None:
        self.x = pyxel.rndi(240,260)
        self.y = pyxel.rndi(70,150)
        self.w = 24
        self.h = 9
        self.dx = pyxel.rndf(-1,-0.3)
        self.dy = pyxel.rndf(-0.1,0.1)
        self.cnt = pyxel.rndi(20,60)
        self.release_flag = False
        self.is_active = True
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.y = max(20,self.y)
        self.y = min(self.y,156)
        self.cnt -= 1
        if self.cnt < 0:
            self.dx = pyxel.rndf(-0.2,0.1)
            self.dy = pyxel.rndf(-0.1,0.1)
            self.cnt = pyxel.rndi(80,160)
            self.release_flag = True
        if self.x < 130:
            self.dx = pyxel.rndf(0.3,0.6)
            self.dy = pyxel.rndf(-0.1,0.1)
            self.cnt = pyxel.rndi(120,210)
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 0,162, self.w,self.h, 0)
class Balloon():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.dx = pyxel.rndi(-1,0)
        self.dy = pyxel.rndf(-0.2,0.2)
        self.w = 9
        self.h = 9
        self.cnt = pyxel.rndi(40,80)
        self.is_active = True
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.y = max(10,self.y)
        self.y = min(self.y,156)
        self.cnt -= 1
        if self.cnt < 0:
            self.dx = pyxel.rndi(-1,0)
            self.dy = pyxel.rndf(-0.6,0.6)
        if self.x < -10:
            self.is_active = False
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 0,96, 9,9, 0)

class MyShip():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_near_ground = False
        self.dxdy_flags = [False,False,False,False]
        self.is_active = True
        self.fuel_flag = True
    def update(self):
        if self.is_active:
            ### 地面の近くにいるかを判定してフラグ操作
            if self.y > 162:
                self.is_near_ground = True
            else:
                self.is_near_ground = False
        #else:
            #self.x = 10000
    def draw(self):
        if self.is_near_ground:
            pyxel.blt(self.x,self.y,  0, 24,16, 24,8, 0)
        else:
            pyxel.blt(self.x,self.y,  0, 0,16, 24,8, 0)
        if self.fuel_flag:
            pyxel.blt(self.x-8,self.y, 0,  pyxel.frame_count//3%3*8,24, 8,8, 0)
myship = MyShip(0,0)

class Tank():
    def __init__(self) -> None:
        self.x = 640
        self.y = 192
        self.is_active = True
        self.dash_cnt = 0
    def update(self):
        global myship
        if myship.x+16 < self.x:
            self.x -= 1
        else:
            self.x += 2
            self.dash_cnt = 10
        self.dash_cnt -= 1
        if self.dash_cnt > 0:
            self.x += (10-self.dash_cnt)
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 0,112, 16,8, 0)

class App():
    def __init__(self):
        pyxel.init(240,240,title="Stellar Blazer",fps=48)
        pyxel.load("sb.pyxres")
        self.mission_poss = [[0,248],[0,240],[0,232],[0,224]]
        self.init_game()
        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.stage_num = 0
        self.gameover_cnt = 0
        self.gameallclear_cnt = 0
        self.demomode_flag = True
        self.score = 0
        self.init_stage()

    def init_stage(self):
        global stars,g_objs,my_blasters,my_bombs,explo1s,explo2s,radars,icbms,planes,paras,packs,tanks,missiles,carriers,balloons
        self.stage_num += 1
        self.stage_cnt = 0
        self.fuel = 3000
        self.bomb = 30
        myship.is_active = False
        myship.x = -30
        myship.y = 64
        myship.is_near_ground = False
        self.stageclear_cnt = 0
        self.stagestart_cnt = 160
        stars = []
        g_objs = []
        my_blasters = []
        my_bombs = []
        explo1s = []
        explo2s = []
        radars = []
        icbms = []
        planes = []  #1機しか存在しないけど
        paras = []  #1袋しか存在しないけど
        packs = []  #1パックしか存在しないけど
        if self.stage_num == 2:
            tanks = [Tank()]
        else:
            tanks = []
        missiles = []
        carriers = []
        balloons = []

        if self.stage_num == 4:   ## 3面しかないよ！
            self.gameallclear_cnt = 480

    def update(self):
        ### ステージごとのカウンター
        self.stage_cnt += 1
        ### すべてのステージをクリアーしました！
        if self.gameallclear_cnt > 0:
            self.gameallclear_cnt -= 1
            if self.gameallclear_cnt == 0:
                self.init_game()
                return
        ### デモモード終了の判定
        if self.demomode_flag:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
                self.demomode_flag = False
                self.gameover_cnt = 0
                self.stage_num = START_STAGE
                pyxel.play(0,0)
                self.init_stage()
                return
        ### ステージ開始時　まったり登場シーンのカウントダウン
        if self.stagestart_cnt > 0:
            myship.x += 0.5
            self.stagestart_cnt -= 1
            if self.stagestart_cnt == 0:
                myship.is_active = True
        ### ゲームオーバー中のカウントダウン
        if self.gameover_cnt > 0:
            self.gameover_cnt -= 1
            if self.gameover_cnt == 0:
                self.init_game()
        ### ステージクリア時　飛び去るシーンのカウントダウン
        if self.stageclear_cnt > 0:
            myship.x += ( (250-self.stageclear_cnt) * 0.05)
            myship.y -= ( (250-self.stageclear_cnt) * 0.02)
            self.stageclear_cnt -= 1
            if self.stageclear_cnt == 0:
                self.init_stage()
        ### 自機関係の処理
        if myship.is_active: # and not self.demomode_flag:
            ### 燃料を減らす
            if not self.demomode_flag:
                self.fuel -= 1
            ### 自機の移動
            myship.dxdy_flags = [False,False,False,False]
            for i in range(4):
                if pyxel.btn(KEY[i]) or (pyxel.btnv(LAXIS[i]) > LAXIS_RANGE[i][0] and pyxel.btnv(LAXIS[i]) < LAXIS_RANGE[i][1]) or pyxel.btn(GPAD[i]):
                    myship.x += D[i][0] * 2
                    myship.y += D[i][1] * 2
                    myship.dxdy_flags[i] = True
            ### 自機を位置を移動範囲内に修正
            if myship.x < 0:
                myship.x = 0
            elif myship.x > 220:
                myship.x = 220
            if myship.y < 0:
                myship.y = 0
            ### 自機が地面に激突したかどうかの判定
            if myship.y > 192:
                myship.is_active = False
                pyxel.play(2,5)
                explo1s.append(Explo1(myship.x+12,192))
                myship.y = -10000
                self.gameover_cnt = 220
            ### 自機のブラスター発射／爆弾投下
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if myship.is_near_ground:
                    if self.bomb > 0:
                        self.bomb -= 1
                        dx = -0.8
                        dy = 0
                        bomb = MyBomb(myship.x+10,myship.y+4,  dx , dy )
                        if myship.dxdy_flags[0]:   #下
                            bomb.dy = 1
                        elif myship.dxdy_flags[1]: #上
                            bomb.dy = -1
                        if myship.dxdy_flags[2]:   #右
                            bomb.dx = 0.4
                        elif myship.dxdy_flags[3]: #左
                            bomb.dx = -2
                        pyxel.play(0,2)
                        my_bombs.append(bomb)
                else:
                    pyxel.play(0,1)
                    my_blasters.append(MyBlaster(myship.x+20,myship.y+4))
        ### 自機の更新
        myship.update()
        ### 点数の修正
        self.score = max(0,self.score)
        ### 燃料不足（FUEL）時の処理
        if self.fuel <= 0:
            self.fuel = 0
            myship.is_active = False
            myship.fuel_flag = False
            myship.y += 0.5
            if myship.y > 192:
                pyxel.play(2,5)
                explo1s.append(Explo1(myship.x+12,myship.y+2))
                myship.is_active = False
                myship.y = -10000
                self.gameover_cnt = 220
        ### 星の生成
        if pyxel.frame_count%30==0:
            stars.append(Star())
        ### 星の更新
        for star in reversed(stars):
            star.update()
            if star.is_active == False:
                stars.remove(star)
        ### 補給機の生成
        if self.stage_cnt%600==0:
            planes.append(Plane())
        ### 補給機の更新
        for plane in planes:
            plane.update()
            if plane.is_active == False:
                planes.remove(plane)
        ### パラシュートの更新
        for para in paras:
            para.update()
            ### パラシュートと自機との当たり判定
            if para.release_flag == False:
                if abs((para.x+6)-(myship.x+12)) < 18 and abs((para.y+6)-(myship.y+4)) < 10:
                    para.release_flag = True
                    if self.demomode_flag == False:
                        self.fuel = 3000
                        self.bomb = 30
                        myship.fuel_flag = True
                        myship.is_active = True
                        self.score += 100
                        pyxel.play(1,4)
            if para.is_active == False:
                paras.remove(para)
        ### 補給パックの更新
        for pack in packs:
            pack.update()
            ### 補給パックと自機との当たり判定
            if abs((pack.x+5)-(myship.x+12)) < 18 and abs((pack.y+3)-(myship.y+4)) < 7:
                if self.demomode_flag == False:
                    self.fuel = 3000
                    self.bomb = 30
                    myship.fuel_flag = True
                    myship.is_active = True
                    self.score += 100
                pack.is_active = False
                pyxel.play(1,4)
            ### 補給パックとレーダーとの当たり判定
            for radar in radars:
                if abs((pack.x+5)-(radar.x+6)) < 13 and abs((pack.y+3)-(radar.y+6)) < 9:
                    my_bombs.append(MyBomb(radar.x,radar.y,0,0))
                    pyxel.play(1,3)
            ### 補給パックと戦車との当たり判定
            for tank in tanks:
                if abs((pack.x+5)-(tank.x+8)) < 13 and abs((pack.y+3)-(tank.y+4)) < 7:
                    my_bombs.append(MyBomb(tank.x,tank.y,0,0))
                    pyxel.play(1,3)
            ### 補給パックとICBMとの当たり判定
            for icbm in icbms:
                if abs((pack.x+5)-(icbm.x+6)) < 13 and abs((pack.y+3)-(icbm.y+6)) < 9:
                    my_bombs.append(MyBomb(icbm.x,icbm.y,0,0))
                    pyxel.play(1,3)
            ### 補給パックと地上物との当たり判定（当たったら補給パックも消しちゃう）
            for obj in g_objs:
                if abs((pack.x+5)-(obj.x+obj.w/2)) < (5+obj.w/2) and abs((pack.y+3)-(obj.y+obj.h/2)) < (3+obj.h/2):
                    my_bombs.append(MyBomb(obj.x,obj.y,0,0))
                    pack.is_active = False
                    pyxel.play(1,3)
                    break
            ### 地面にぶつかって爆破する予告など
            if pack.explosion_flag:
                pyxel.play(2,6)
                explo2s.append(Explo2(pack.x,192))
            if pack.is_active == False:
                packs.remove(pack)
        ### ステージ1のレーダーを生成＆更新と削除
        if self.stage_num == 1:
            if self.stage_cnt > 1600 and pyxel.frame_count%680==0:
                radars.append(Radar())
            for radar in radars:
                radar.update()
                if radar.is_active == False:
                    radars.remove(radar)
        ### ステージ2の戦車の更新
        for tank in tanks:
            tank.update()
            ### 自機との当たり判定
            if abs((tank.x+8)-(myship.x+12))<20 and abs((tank.y+4)-(myship.y+4))<8:
                tank.is_active = False
                pyxel.play(2,5)
                explo1s.append(Explo1(myship.x+12,myship.y+2))
                myship.is_active = False
                myship.y = -10000
                self.gameover_cnt = 220
            if tank.is_active == False:
                tanks.remove(tank)
        ### ステージ2のミサイルの生成と更新
        if self.stage_num == 2:
            if self.stage_cnt > 140:
                if self.stage_cnt%17 == 0:
                    missiles.append(Missile())
            for missile in reversed(missiles):
                missile.update()
                ### 自機との当たり判定
                if self.stageclear_cnt==0:
                    if abs((missile.x+8)-(myship.x+12))<20 and abs((missile.y+4)-(myship.y+4))<8:
                        missile.is_active = False
                        pyxel.play(2,5)
                        explo1s.append(Explo1(myship.x+12,myship.y+2))
                        myship.is_active = False
                        myship.y = -10000
                        self.gameover_cnt = 220
                ### パラシュートとの当たり判定
                for para in paras:
                    if abs((para.x+6)-(missile.x+8))<14 and abs((para.y+5)-(missile.y+4))<12:
                        paras.remove(para)
                        packs.append(Pack(para.x+1,para.y+12))
                if missile.is_active == False:
                    missiles.remove(missile)
        ### ステージ3のICBMを生成＆更新と削除
        if self.stage_num == 3:
            if self.stage_cnt > 1400 and pyxel.frame_count%770==0:
                icbm = Icbm()
                icbms.append(icbm)
                gobj = GroundObject(5)
                gobj.x = icbm.x + pyxel.rndi(-32,64)
                g_objs.append(gobj)
            for icbm in icbms:
                icbm.update()
                if icbm.is_active == False:
                    icbms.remove(icbm)
        ### ステージ3の母艦の生成＆更新と削除
            if len(carriers) < 3:
                if self.stage_cnt > 300:
                    carriers.append(Carrier())
            for carr in reversed(carriers):
                carr.update()
                if carr.release_flag:
                    balloons.append(Balloon(carr.x-8,carr.y))
                    carr.release_flag = False
                ### 自機との当たり判定
                if self.stageclear_cnt == 0:
                    if abs((myship.x+12)-(carr.x+12))<24 and abs((myship.y+4)-(carr.y+4))<8:
                        carr.is_active = False
                        explo1s.append(Explo1(myship.x+12,myship.y+2))
                        myship.is_active = False
                        myship.y = -10000
                        self.gameover_cnt = 220
                if carr.is_active == False:
                    carriers.remove(carr)
        ### ステージ3の風船爆弾の更新と削除
            for balloon in reversed(balloons):
                balloon.update()
                ### 自機との当たり判定
                if self.stageclear_cnt == 0:
                    if abs((myship.x+12)-(balloon.x+4))<17 and abs((myship.y+4)-(balloon.y+4))<9:
                        balloon.is_active = False
                        pyxel.play(2,5)
                        explo1s.append(Explo1(myship.x+12,myship.y+2))
                        myship.is_active = False
                        myship.y = -10000
                        self.gameover_cnt = 220
                if balloon.is_active == False:
                    balloons.remove(balloon)
        ### ステージ1とステージ3の地上のオブジェクトを生成
        if self.stage_num == 1 or self.stage_num == 3:
            ### 地上のオブジェクトを生成
            if pyxel.frame_count%10==0 and pyxel.rndi(0,2)==0:
                g_objs.append(GroundObject( pyxel.rndi(0,5) )) 
            ### 地上のオブジェクトを更新
            for obj in reversed(g_objs):
                obj.update()
                if self.stageclear_cnt == 0:
                    if abs((obj.x+obj.w/2)-(myship.x+12))<(10+obj.w/2) and abs((obj.y+obj.h/2)-(myship.y+4))<(4+obj.h/2):
                        obj.is_active = False
                        pyxel.play(2,5)
                        explo1s.append(Explo1(myship.x+12,myship.y+2))
                        myship.is_active = False
                        myship.y = -10000
                        self.gameover_cnt = 220
                if obj.is_active == False:
                    g_objs.remove(obj)
        ### ブラスターの更新＆当たり判定
        for blaster in reversed(my_blasters):
            blaster.update()
            ###当たり判定
            for para in paras: ### ブラスターとパラシュートとの当たり判定
                if abs((para.x+6)-(blaster.x+10))<6 and abs((para.y+5)-(blaster.y))<7:
                    paras.remove(para)
                    packs.append(Pack(para.x+1,para.y+12))
            for missile in missiles: ### ブラスターとミサイルとの当たり判定
                if abs((missile.x+8)-(blaster.x+10))<13 and abs((missile.y+3)-(blaster.y))<4:
                    pyxel.play(1,7)
                    explo2s.append(Explo2(missile.x+6,missile.y))
                    missiles.remove(missile)
                    self.score += 80
                    blaster.is_active = False
                    break
            for carr in reversed(carriers): ### ブラスターと母艦との当たり判定
                if abs((carr.x+12)-(blaster.x+10))<20 and abs((carr.y+4)-(blaster.y))<4:
                    pyxel.play(1,7)
                    explo2s.append(Explo2(carr.x+6,carr.y))
                    carriers.remove(carr)
                    blaster.is_active = False
                    break
            for balloon in reversed(balloons): ### ブラスターと風船爆弾との当たり判定
                if abs((balloon.x+4)-(blaster.x+10))<15 and abs((balloon.y+4)-(blaster.y))<5:
                    pyxel.play(1,3)
                    explo2s.append(Explo2(balloon.x,balloon.y))
                    balloons.remove(balloon)
                    self.score += 20
                    blaster.is_active = False
                    break
            ### ブラスターの消去
            if blaster.is_active == False:
                my_blasters.remove(blaster)
        ### 爆弾の更新＆当たり判定
        for bomb in reversed(my_bombs):
            bomb.update()
            ###当たり判定
            for obj in reversed(g_objs): ### 地上オブジェクトとの当たり判定
                if abs((obj.x+obj.w/2)-(bomb.x+4))<(obj.w/2+4) and abs((obj.y+obj.h/2)-(bomb.y+4))<(obj.h/2):
                    self.score += obj.score
                    g_objs.remove(obj)
                    bomb.is_active = False
                    pyxel.play(1,3)
                    break
            for obj in radars: ### 1面のレーダー（破壊出来たら1面クリア！）
                if abs((obj.x+obj.w/2)-(bomb.x+4))<(obj.w/2+4) and abs((obj.y+obj.h/2)-(bomb.y+4))<(obj.h/2+4):
                    radars.remove(obj)
                    bomb.is_active = False
                    myship.is_active = False
                    self.stageclear_cnt = 260
                    pyxel.play(1,9)
                    pyxel.playm(0)
            for obj in tanks: ### 2面の戦車（破壊出来たら2面クリア！）
                if abs((obj.x+8)-(bomb.x+4))<12 and abs((obj.y+4)-(bomb.y+4))<8:
                    tanks.remove(tank)
                    self.score += 300
                    bomb.is_active = False
                    myship.is_active = False
                    self.stageclear_cnt = 260
                    pyxel.play(1,9)
                    pyxel.playm(0)
            for obj in icbms: ### 3面のICBM（破壊出来たら3面クリア！）
                if abs((obj.x+obj.w/2)-(bomb.x+4))<(obj.w/2+4) and abs((obj.y+obj.h/2)-(bomb.y+4))<(obj.h/2+4):
                    icbms.remove(obj)
                    bomb.is_active = False
                    myship.is_active = False
                    self.stageclear_cnt = 260
                    pyxel.play(1,9)
                    pyxel.playm(0)

            if bomb.is_active == False:
                pyxel.play(2,6)
                explo2s.append(Explo2(bomb.x+4,192))
                my_bombs.remove(bomb)
        ### 爆発エフェクトの更新
        for explo in reversed(explo1s):
            explo.update()
            if explo.is_active == False:
                explo1s.remove(explo)
        for explo in reversed(explo2s):
            explo.update()
            if explo.is_active == False:
                explo2s.remove(explo)

    def draw(self):
        ### すべてのステージをクリアーしました！
        if self.gameallclear_cnt > 0:
            pyxel.cls(0)
            pyxel.blt(0,0,  2,  0,0, 240,240, 0)
            return
        ### 黒い背景と地面の描画
        pyxel.cls(0)
        pyxel.bltm(0,200, 0, 0,0, 240,8, 0)
        ### ミッションの描画
        pyxel.blt(40,220, 0, self.mission_poss[self.stage_num-1][0],self.mission_poss[self.stage_num-1][1],200,8, 0)
        ### 星の描画
        for star in stars:
            star.draw()
        ### 補給機の描画
        for plane in planes:
            plane.draw()
        ### パラシュートの描画
        for para in paras:
            para.draw()
        ### 補給パックの描画
        for pack in packs:
            pack.draw()
        ### 地上のオブジェクトを描画
        for obj in reversed(g_objs):
            obj.draw()
        ### ステージ1のレーダーを描画
        for radar in radars:
            radar.draw()
        ### ステージ2の戦車の描画
        for tank in tanks:
            tank.draw()
        ### ステージ2のミサイルの描画
        for missile in missiles:
            missile.draw()
        ### ステージ3のICBMを描画
        for icbm in icbms:
            icbm.draw()
        ### ステージ3の母艦の描画
        for carr in reversed(carriers):
            carr.draw()
        ### ステージ3の風船爆弾の描画
        for balloon in reversed(balloons):
            balloon.draw()
        ### ブラスターを描画
        for blaster in reversed(my_blasters):
            blaster.draw()
        ### 爆弾を描画
        for bomb in reversed(my_bombs):
            bomb.draw()
        ### 爆発エフェクトの描画
        for explo in reversed(explo1s):
            explo.draw()
        for explo in reversed(explo2s):
            explo.draw()
        ### 自機の描画
        myship.draw()
        ### SCORE,FUEL,BOMBの描画
        pyxel.blt(10,8,    1,  0,176,  32,8,  0)
        for i in reversed(range(5)):
            pyxel.blt(43+(4-i)*6,8, 1, (self.score//(10**i))%10*8+1,200,  6,8,  0)
        pyxel.blt(96,8,  1,  0,184,  32,8,  0)
        for i in reversed(range(5)):
            pyxel.blt(122+(4-i)*6,8, 1, (self.fuel//(10**i))%10*8+1,200,  6,8,  0)
        pyxel.blt(178,8,  1,  0,192,  32,8,  0)
        for i in reversed(range(3)):
            pyxel.blt(212+(2-i)*6,8, 1, (self.bomb//(10**i))%10*8+1,200,  6,8,  0)
        ### ゲームオーバー画面の表示
        if self.gameover_cnt > 0 and not self.demomode_flag:
            #pyxel.text(100,100,"GAME OVER",8)
            pyxel.blt(70,100, 1, 0,160, 101,12, 0)
        ### デモモード時のタイトル描画
        if self.demomode_flag:
            pyxel.blt(54,70,  1,  0,72, 132,80, 0)
        ### ステージ開始時まったり登場シーンのメッセージ表示
        elif self.stagestart_cnt > 0:
            pyxel.text(100,100,"MISSION {}".format(self.stage_num),7)





        ###### デバッグ用 ###########################
        #pyxel.text(10,10, "LEFT X AXIS:{}".format(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)),7)
        #pyxel.text(10,20, "LEFT Y AXIS:{}".format(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)),7)
        #pyxel.text(10,40, "+ BUTTON  DOWN:{} UP:{} RIGHT:{} LEFT:{}".format(pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN),pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP),pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT),pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)),7)
        #pyxel.text(10,50, "self.bomb:{}".format(self.bomb),7)
        #pyxel.text(10,60, "self.stage_cnt:{}".format(self.stage_cnt),7)
        #pyxel.text(10,70, "len(planes):{}".format(len(planes)),7)
        #pyxel.text(10,80, "len(paras):{}".format(len(paras)),7)
        #pyxel.text(10,90, "len(packs):{}".format(len(packs)),7)
        #pyxel.text(10,30, "len(tanks):{}".format(len(tanks)),7)
        #pyxel.text(10,40, "len(missiles):{}".format(len(missiles)),7)

App()

