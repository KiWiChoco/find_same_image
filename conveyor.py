# -*- coding: utf-8 -*-

from tkinter import *
import random

class Conveyor(Frame):
    def __init__(self, master, picture, width):
        super(Conveyor, self).__init__()
        self.image_number_list = [] # 셔플된 이미지의 번호를 저장하기 위한 리스트. 13개
        self.labels = [] # 컨베이어 frame에 추가되는 이미지 label 위젯의 리스트
        self.master = master # 컨베이어 frame의 parent 설정
        self.width = width # 메인 테이블의 가로 길이. = 4
        self.n = width*(width-1)+1 # 컨베이어에 넣을 이미지의 수. = 13
        self.picture = picture # app에서 생성한 이미지 받아와서 저장 -> 모든 이미지
        self.image_flags = list(False for i in range(self.width*self.width)) # 이미지가 컨베이어에 올라갔는지 아닌지 체크하기 위한 리스트. 초기 세팅은 모두 FALSE.

        self.conveyor_canvas2 = Canvas(self, width=50, height=30)
        self.cur2 = self.conveyor_canvas2.create_text(25, 15, font="Times 12 bold", text="FINAL", fill="red")
        self.conveyor_canvas2.grid(row=0, column=self.n-1)

        self.conveyor_canvas = Canvas(self, width=30, height=30) # 현재 위치 표시를 위한 캔버스 위젯 생성

        # 컨베이어에 올릴 이미지 셔플링
        self.random_shuffle()

        # 셔플 결과대로 이미지 label 생성하여 리스트에 저장
        for i in range(0, self.n):
            self.labels.append(Label(self, image=self.picture[self.image_number_list[i]]))
            self.image_flags[self.image_number_list[i]] = True

        # 현재 index 설정 = 시작 위치 설정
        self.cur_idx = int(self.n/self.width*(self.width-1))

        # 현재 이미지 설정 = 시작 이미지 설정
        # 선택한 이미지와 비교 목적으로 저장
        self.cur_image = self.picture.index(self.picture[self.image_number_list[self.cur_idx]])

        # TODO
        # 캔버스 세팅
        self.cur = self.conveyor_canvas.create_polygon([(0, 5), (30, 5), (15, 25)], fill='yellow', width=1, outline="black")
        self.conveyor_canvas.grid(row=0, column=self.cur_idx)

        for i in range(self.n):
            self.labels[i].grid(row=1, column=i)

    # 이미지 셔플 함수
    def random_shuffle(self):
        self.image_number_list = random.sample(range(self.width*self.width), self.n)

    # TODO
    # 선택한 그림이 현재 위치의 그림과 일치하는 경우
    def correct_match(self):
        # 마지막 이미지를 찾은 경우
        if self.cur_idx == self.n-1:
            self.master.quit_game(win=True)
        else:
            # 현재 위치가 컨베이어의 가장 우측 도형을 지목할 때
            # FINAL 글씨를 가리지 않도록 도형 수정
            if self.cur_idx == self.n-2:
                self.conveyor_canvas2.delete(self.cur2)
            self.cur_idx += 1
            self.conveyor_canvas.grid(row=0, column=self.cur_idx)


    # TODO
    # 선택한 그림이 현재 위치의 그림과 일치하지 않는 경우
    def wrong_match(self):
        # 마지막 기회에서 틀린 경우
        if(self.cur_idx == 0):
            self.master.quit_game(win=False)
        else:
            if self.cur_idx == self.n - 1:
                self.cur2 = self.conveyor_canvas2.create_text(25, 15, font="Times 12 bold", text="FINAL", fill="red")
                self.conveyor_canvas2.grid(row=0, column=12)
            self.cur_idx -= 1
            self.conveyor_canvas.grid(row=0, column=self.cur_idx)

            # 새 이미지 추가
            while True:
                new_image = random.randint(0, self.width*self.width-1)
                if new_image not in self.image_number_list:
                    break

            # 기존 이미지 좌측으로 한 칸씩 이동
            # label.config(parameter = configuration) 기존의 label 위젯 변경 가능
            for i in range(0, self.n-1):
                self.labels[i].config(image=self.picture[self.image_number_list[i+1]])
                self.image_number_list[i] = self.image_number_list[i+1]

            # 새 이미지 추가
            self.image_number_list[self.n-1] = new_image
            self.labels[self.n-1].config(image=self.picture[self.image_number_list[self.n-1]])
