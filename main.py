import cv2
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Ocorreu um erro na inicialização, programa fechado!")
    exit()

print("Video iniciado")

#Parametros mp
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5 ) as hands:
        
    while cap.isOpened():
        #começo da captura
        sucesso, frame = cap.read()
        if not sucesso:
            print("Falha na imagem")
            break
        
        #criação dos pontos
        image = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        
        #ligação dos pontos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Detecção  de mãos', image)
        
        if  cv2.waitKey(5) & 0xFF == 27:
            break
    
cap.release()
cv2.destroyAllWindows()