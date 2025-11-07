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
def fingerUp(results):
    global fingers_left, fingers_right

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = hand_handedness.classification[0].label  # 'Left' ou 'Right'

            # Índices dos dedos (ponta, base)
            dedos = {
                "polegar": (4, 3),
                "indicador": (8, 6),
                "medio": (12, 10),
                "anelar": (16, 14),
                "mindinho": (20, 18)
            }

            status_dedos = []

            for i, (ponta, base) in enumerate(dedos.values()):
                if i == 0:  # polegar
                    if hand_label == "Right":
                        levantado = hand_landmarks.landmark[ponta].x < hand_landmarks.landmark[base].x
                    else:  # mão esquerda é espelhada
                        levantado = hand_landmarks.landmark[ponta].x > hand_landmarks.landmark[base].x
                else:  # demais dedos
                    levantado = hand_landmarks.landmark[ponta].y < hand_landmarks.landmark[base].y

                status_dedos.append(1 if levantado else 0)

            if hand_label == "Right":
                fingers_right = status_dedos
            else:
                fingers_left = status_dedos

def detectarGestos(gesto_ativo, imagem_gesto, cx_suave, cy_suave, fingers, alpha, cx, cy, image, w, h):
    gesto_detectado = -1

    # Verifica se o padrão de dedos coincide com algum gesto conhecido
    for i in range(linhas):
        if np.array_equal(gestos[i], fingers):
            gesto_detectado = i
            break

    # --- Se um gesto foi reconhecido ---
    if gesto_detectado != -1:
        # Se for um gesto novo, carrega uma nova imagem apenas 1x
        if gesto_detectado != gesto_ativo:
            gesto_ativo = gesto_detectado
            pasta = os.path.join(base_path, pasta_gestos[gesto_detectado])
            imagens = os.listdir(pasta)
            imagem_escolhida = random.choice(imagens)
            caminho_imagem = os.path.join(pasta, imagem_escolhida)
            img = cv2.imread(caminho_imagem)

            if img is not None:
                altura, largura = img.shape[:2]
                fator = 150 / max(altura, largura)
                imagem_gesto = cv2.resize(img, (int(largura * fator), int(altura * fator)))
                alpha = 1.0  # já aparece visível
            else:
                print(f"Erro ao abrir: {caminho_imagem}")

        # Atualiza posição suavemente (segue a mão)
        cx_suave = int(0.3 * cx_suave + 0.7 * cx)
        cy_suave = int(0.3 * cy_suave + 0.7 * cy)

        # Desenha imagem sobre a mão
        if imagem_gesto is not None:
            ih, iw, _ = imagem_gesto.shape
            offset = int(0.9 * ih) 
            x1, y1 = cx_suave - iw // 2, cy_suave - ih - offset
            x2, y2 = x1 + iw, y1 + ih

            # Corrige limites da tela
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h

            # Recalcula tamanho da imagem para caber dentro dos limites
            iw_corrigido, ih_corrigido = x2 - x1, y2 - y1
            if iw_corrigido > 0 and ih_corrigido > 0:
                imagem_redimensionada = cv2.resize(imagem_gesto, (iw_corrigido, ih_corrigido))
                overlay = image.copy()
                overlay[y1:y2, x1:x2] = imagem_redimensionada
                cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    else:
        # --- Nenhum gesto detectado ---
        if gesto_ativo != -1:
            alpha -= 0.1  # fade out
            if alpha <= 0:
                alpha = 0
                gesto_ativo = -1
                imagem_gesto = None

    return gesto_ativo, imagem_gesto, cx_suave, cy_suave, alpha


#Parametros mp
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
    
    gesto_ativo_esq = -1
    gesto_ativo_dir = -1
    imagem_gesto_esq = None
    imagem_gesto_dir = None
    alpha_esq = 0.0
    alpha_dir = 0.0
    cx_esq_suave, cy_esq_suave = 0, 0
    cx_dir_suave, cy_dir_suave = 0, 0

    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print("Falha na imagem")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Atualiza vetores de dedos
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingerUp(results)

                h, w, _ = image.shape
                label = hand_handedness.classification[0].label  # "Left" ou "Right"
                cx = int(hand_landmarks.landmark[0].x * w)
                cy = int(hand_landmarks.landmark[0].y * h)

                if label == 'Left':
                    gesto_ativo_esq, imagem_gesto_esq, cx_esq_suave, cy_esq_suave, alpha_esq = detectarGestos(
                        gesto_ativo_esq, imagem_gesto_esq, cx_esq_suave, cy_esq_suave,
                        fingers_left, alpha_esq, cx, cy, image, w, h)

                if label == 'Right':
                    gesto_ativo_dir, imagem_gesto_dir, cx_dir_suave, cy_dir_suave, alpha_dir = detectarGestos(
                        gesto_ativo_dir, imagem_gesto_dir, cx_dir_suave, cy_dir_suave,
                        fingers_right, alpha_dir, cx, cy, image, w, h)

        else:
            # Nenhuma mão detectada = esconde ambas
            for lado in ["esq", "dir"]:
                if lado == "esq" and gesto_ativo_esq != -1:
                    alpha_esq -= 0.1
                    if alpha_esq <= 0:
                        alpha_esq = 0
                        gesto_ativo_esq = -1
                        imagem_gesto_esq = None
                if lado == "dir" and gesto_ativo_dir != -1:
                    alpha_dir -= 0.1
                    if alpha_dir <= 0:
                        alpha_dir = 0
                        gesto_ativo_dir = -1
                        imagem_gesto_dir = None

        cv2.imshow('Detecção de mãos', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

print("fechando...")
cap.release()
cv2.destroyAllWindows()
