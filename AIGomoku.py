import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, make_response, redirect, url_for, jsonify

#승리판정 알고리즘 이상함
#리셋 기능 제작
#모델 선택 기능 제작
#ai vs ai 기능(희망 사항)

models = ["20201213_202430.h5","238d 32-64-128-64-32l 64e 512b model.h5"]

model = tf.keras.models.load_model(models[0])
w, h = 20, 20
isPlayerFirst = True
board = np.zeros([h, w], dtype=np.int8)

def predict(model, input_board):
    model_output = model.predict(board.reshape(1,h,w,1))
    model_output = model_output.reshape(h, w)
    input_board = board.copy()
    input_board[input_board == 1] = -1
    input_board = input_board.astype(model_output.dtype)
    model_output += input_board
    argMax = np.unravel_index(model_output.argmax(), model_output.shape)
    
    return argMax

def placeByAI(board):
    model_output = predict(model, board)
    board[model_output] = 1

    return board, model_output

def isWinSomeone(player, board): # 살짝 이상함
    placedPoints = np.where(board == player)

    for i in range(len(placedPoints[0])):
        y, x = placedPoints[0][i], placedPoints[1][i]

        if np.abs(np.sum(board[y,x:x+5])) == 5: return True# 상
        if np.abs(np.sum(board[y,x-4:x+1])) == 5: return True# 하
        if np.abs(np.sum(board[y:y+5,x])) == 5: return True# 우
        if np.abs(np.sum(board[y-4:y+1,x])) == 5: return True# 좌

        diagBoard = np.diag(board,k=x-y)
        flipDiagBoard = np.diag(np.fliplr(board),k=w-x-1-y)
        minxy = min(x,y)
        minwxy = min(w-x-1,y)

        if np.abs(np.sum(diagBoard[minxy-4:minxy+1])) == 5: return True# 좌상
        if np.abs(np.sum(diagBoard[minxy:minxy+5])) == 5: return True# 좌하
        if np.abs(np.sum(flipDiagBoard[minwxy-4:minwxy+1])) == 5: return True# 우상
        if np.abs(np.sum(flipDiagBoard[minwxy:minwxy+5])) == 5: return True# 우하

    return False
        


app = Flask(__name__)

app.secret_key = b'_5#877$&@89$ek+/]'

@app.route('/')
def home():
    return render_template('index.html',w=w,h=h)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'GET':
        infos = {'w' : w, 'h' : h, "models" : models}
        return jsonify(infos)
    if request.method == 'POST':
        print(request.get_json())
        return 'Sucesss', 200

@app.route('/placedByUser', methods=['GET', 'POST'])
def placedByUser():
    if request.method == 'GET':
        return 200
    if request.method == 'POST':
        global board
        requestedJson = request.get_json()
        board = requestedJson["board"]
        board = np.array(board)
        for i in range(w):
            board[i] = np.array(board[i])
        isWinUser = isWinSomeone(-1, board)
        isWinUserJson = {"isWin" : isWinUser}
        return jsonify(isWinUserJson)

@app.route('/placedByAI', methods=['GET', 'POST'])
def placedByAI():
    if request.method == 'GET':
        global board
        board, model_output = placeByAI(board)
        recommend_point = predict(model, board)
        recommend_point = [int(recommend_point[0]), int(recommend_point[1])]
        isWinAI = isWinSomeone(1, board)
        AIPlacementPoint = {'x' : int(model_output[1])+1, 'y' : int(model_output[0])+1, "isWin" : isWinAI, "recommend_point" : recommend_point}
        return jsonify(AIPlacementPoint)
    if request.method == 'POST':
        return "Success", 200

app.run()