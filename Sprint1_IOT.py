import cv2
import mediapipe as mp
import numpy as np
import winsound 
import time
import csv
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Estilo dos Landmarks
estilo_conexoes = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)

# --- PARÂMETROS ---
LIMIAR_EAR_FECHADO = 0.23
LIMIAR_MAR_BOCEJO = 0.90
FRAMES_PARA_MICRO_SONO = 20
FRAMES_PARA_BOCEJO = 15
MAX_FADIGA = 100
score_fadiga = 0
fator_recuperacao = 0.1

# --- PREPARAÇÃO DO LOG ---
nome_arquivo = f"log_sessao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(nome_arquivo, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Evento", "Score_Fadiga", "EAR", "MAR"])

frames_olho_fechado = 0
frames_bocejo = 0
pontos_olho_ids = [33, 160, 158, 133, 153, 144]
pontos_boca_ids = [13, 14, 78, 308, 61, 291]

def calcular_distancia(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def registrar_log(evento, score, ear_val, mar_val):
    timestamp = datetime.now().strftime('%H:%M:%S')
    with open(nome_arquivo, mode='a', newline='') as file:
        writer_log = csv.writer(file)
        writer_log.writerow([timestamp, evento, int(score), f"{ear_val:.2f}", f"{mar_val:.2f}"])

# --- ESTILO DO TEXTO ---
def desenhar_texto_com_borda(img, texto, pos, tamanho=0.6, cor_texto=(255, 255, 255), grossura=1):
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, tamanho, (0, 0, 0), grossura + 2, cv2.LINE_AA)
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, tamanho, cor_texto, grossura, cv2.LINE_AA)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = face_mesh.process(rgb)
    h_img, w_img, _ = frame.shape

    if resultados.multi_face_landmarks:
        face_landmarks = resultados.multi_face_landmarks[0]
        pontos = face_landmarks.landmark

        # Visualização: Landmarks
        mp_draw.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face.FACEMESH_CONTOURS, 
            landmark_drawing_spec=None, 
            connection_drawing_spec=estilo_conexoes
        )

        # Cálculos
        v1 = calcular_distancia(pontos[pontos_olho_ids[1]], pontos[pontos_olho_ids[5]])
        v2 = calcular_distancia(pontos[pontos_olho_ids[2]], pontos[pontos_olho_ids[4]])
        h_olho = calcular_distancia(pontos[pontos_olho_ids[0]], pontos[pontos_olho_ids[3]])
        ear = (v1 + v2) / (2.0 * h_olho) if h_olho > 0 else 0

        v_boca = calcular_distancia(pontos[pontos_boca_ids[0]], pontos[pontos_boca_ids[1]])
        h_boca = calcular_distancia(pontos[pontos_boca_ids[2]], pontos[pontos_boca_ids[3]])
        mar = v_boca / h_boca if h_boca > 0 else 0

        # Lógica
        if ear <= LIMIAR_EAR_FECHADO:
            frames_olho_fechado += 1
            if frames_olho_fechado > FRAMES_PARA_MICRO_SONO:
                if frames_olho_fechado % 5 == 0:
                    score_fadiga = min(score_fadiga + 2, MAX_FADIGA)
                    registrar_log("MICRO_SONO", score_fadiga, ear, mar)
        else:
            frames_olho_fechado = 0

        if mar > LIMIAR_MAR_BOCEJO:
            frames_bocejo += 1
            if frames_bocejo > FRAMES_PARA_BOCEJO:
                if frames_bocejo % 10 == 0:
                    score_fadiga = min(score_fadiga + 5, MAX_FADIGA)
                    registrar_log("BOCEJO", score_fadiga, ear, mar)
        else:
            frames_bocejo = 0
            
        if frames_olho_fechado == 0 and frames_bocejo == 0 and score_fadiga > 0:
            score_fadiga -= fator_recuperacao

        # --- VISUALIZAÇÃO ---
        energia_avatar = int(MAX_FADIGA - score_fadiga)
        if energia_avatar > 70: cor_barra = (0, 255, 0)
        elif energia_avatar > 30: cor_barra = (0, 255, 255)
        else: cor_barra = (0, 0, 255)

        # Barra de Energia 
        cv2.rectangle(frame, (10, 40), (260, 70), (30, 30, 30), -1) 
        cv2.rectangle(frame, (10, 40), (10 + int(energia_avatar * 2.5), 70), cor_barra, -1)
        desenhar_texto_com_borda(frame, "ENERGIA AVATAR", (15, 62), tamanho=0.5)

        # Alerta
        if energia_avatar < 30:
            desenhar_texto_com_borda(frame, "ALERTA: FADIGA!", (10, 110), tamanho=1.0, cor_texto=(0, 0, 255), grossura=2)
            if int(time.time() * 10) % 10 == 0: 
                winsound.Beep(1000, 100)

        # DADOS TÉCNICOS 
        desenhar_texto_com_borda(frame, f"EAR: {ear:.2f} (Olhos)", (10, h_img - 30))
        desenhar_texto_com_borda(frame, f"MAR: {mar:.2f} (Boca)", (220, h_img - 30))

    cv2.imshow("MAP - IoT Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()