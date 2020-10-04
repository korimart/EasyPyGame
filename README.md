# Dependencies

```
pip install pygame PyOpenGL PyOpenGL_accelerate pyglm pympler
```

# EasyPyGame 폴더

간단한 2d 엔진. 제공되는 기능은 다음과 같습니다.

- Input 편의 클래스

- 버튼과 텍스트박스 UI

- 리소스가 관리되는 단위인 Scene 제공

- Scene 안에 GameObject를 배치하면 Camera를 통해 렌더링

- 각 GameObject의 렌더링 방식을 지정할 수 있음 (싱글이미지, 애니메이션, 타일)

# Samples 폴더

EasyPyGame 엔진의 간단한 예제 몇개

# AddOn 폴더

BFS와 A* 알고리즘으로 길을 찾아 SimApp 로봇 시뮬레이터의 로봇 인터페이스로 로봇을 조작하는 플러그인

# SimApp 폴더

EasyPygame으로 만든 길찾기 로봇 시뮬레이터. 다음은 로봇의 규칙입니다.

- 로봇은 시계방향으로만 90도씩 회전할 수 있으며 앞으로만(칼이 가리키는 방향) 나아갈 수 있음.

- 로봇은 지형지물에 대한 사전정보가 없음.

- 초록색 화살표로 지정된 목표를 로봇은 전부 방문해야 함.

## 실행

```
python main.py
```

## 조작

B 지도 on/off

<> 속도조절

[] 카메라 거리 조절

## 예시 - 텍스트박스와 버튼

<img src="https://github.com/korimart/EasyPyGame/blob/master/1.gif" />

## 예시 - 길찾기

다음은 로봇이 Breadth First Search를 이용하여 경로를 찾는 과정(베이지색)과 찾은 경로(빨간색)을 보여줍니다.

<img src="https://github.com/korimart/EasyPyGame/blob/master/2.gif" />

## 예시 - 카메라 조작, 지형지물 드러내기, 속도조절

지형지물이 발견됨에 따라 경로가 수정되는 것을 볼 수 있습니다.

<img src="https://github.com/korimart/EasyPyGame/blob/master/3.gif" />
