# 1. Detection 만들기
#실제로 관절 위에 visualizing된 joint 객체 생성


import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils # drawing utilities - 포즈 시각화할 때 사용
mp_pose = mp.solutions.pose # pose 관련 model 임포트

# 웹캠 비디오 캡처를 위한 VideoCapture 객체 생성
cap = cv2.VideoCapture(0)

# Mediapipe의 Pose 모델 인스턴스 생성
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # 웹캠이 열려있는 동안 반복 실행
    while cap.isOpened():
        # 비디오 프레임 읽기
        ret, frame = cap.read()
        
        # 프레임을 RGB 색상 공간으로 변환
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Mediapipe Pose 모델을 이용하여 프레임 처리
        results = pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 검출된 포즈 랜드마크를 프레임에 그리기 (이미지, 조인트, 조인트커넥션)이 변수로 들어감
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),# joint 스타일
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=5) # joint line 스타일                      
                                 )
        
        # 처리된 프레임을 화면에 출력
        cv2.imshow('Mediapipe Feed', image)
        
        # 'q' 키를 누르면 반복 종료
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    # 비디오 캡처 객체와 창 닫기
    cap.release()
    cv2.destroyAllWindows()