import cv2
import mediapipe as mp
import numpy as np

import random
import os

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

fingers_left = [0, 0, 0, 0, 0]
fingers_right = [0, 0, 0, 0, 0]

gestos = [
    [1, 1, 1, 1, 1], #New metal
    [1, 0, 0, 0, 0], #Jóinha
    [1, 1, 0, 0, 1], #Rock
    [0, 0, 1, 0, 0]  #Dedo do meio
]

# Caminho base onde estão as pastas
base_path = "./img"

# Lista com o nome das subpastas (cada gesto)
pasta_gestos = ["Nu_metal", "Joinha", "Rock", "Dedo_do_meio"]
gestos = np.array(gestos)
linhas, colunas = gestos.shape

if not cap.isOpened():
    print("Ocorreu um erro na inicialização, programa fechado!")
    exit()

print("Video iniciado")

#Função que atualiza dois vetores relacionados se o dedo x está levantado
#Exemplo de retorno: [1,0,0,0,0] = jóinha
def fingerUp():
    ponta = 4
    base = 1
    for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
        for i in range(5):
            if hand_handedness.classification[0].label == 'Right':
                if hand_landmarks.landmark[ponta] < hand_landmarks.landmark[base]:
                #armazena no vetor
                    fingers_right[i] = 1
                else:
                    fingers_right[i] = 0

            if hand_handedness.classification[0].label == 'Left':
                if hand_landmarks.landmark[ponta] < hand_landmarks.landmark[base]:
                # armazena no vetor
                    fingers_left[i] = 1
                else:
                    fingers_left[i] = 0

            ponta += 3
            base += 3


#Parametros mp
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence= 0.5,
    min_tracking_confidence= 0.5) as hands:
        
    while cap.isOpened():
        #começo da captura
        sucesso, frame = cap.read()
        if not sucesso:
            print("Falha na imagem")
            break
        
        #criação dos pontos
        image = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #ligação dos pontos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Detecção  de mãos', image)

        #Detecção de sinais
        #Por enquanto vê apenas gestos da mão esquerda
        fingerUp()
        for i in range(linhas):
            diferente = False
            for j in range(colunas):
                if gestos[i][j] != fingers_left[j]:
                    diferente = True
            if not diferente:
                # Encontrou o gesto correspondente!
                print(f"Gesto {i + 1} reconhecido")

                # Escolher uma imagem aleatória dentro da pasta correspondente
                pasta = os.path.join(base_path, pasta_gestos[i])
                imagens = os.listdir(pasta)
                imagem_escolhida = random.choice(imagens)

                caminho_imagem = os.path.join(pasta, imagem_escolhida)

                # Abrir e exibir
                img = cv2.imread(caminho_imagem)
                if img is not None:
                    cv2.imshow(f"Gesto {i + 1}", img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                else:
                    print(f"Erro ao abrir: {caminho_imagem}")

        if  cv2.waitKey(5) & 0xFF == 27:
            break
    
cap.release()
cv2.destroyAllWindows()