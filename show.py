import os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout, \
    QWidget, QGroupBox, QGridLayout, QCheckBox, QDockWidget, QComboBox, QListWidgetItem, QListWidget
from PyQt5.QtCore import Qt, QSize
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image  # 用于加载纹理图像
import sys

# 光源位置和颜色
light_positions = [[0, 0, 4], [3, 3, 0]]
light_colors = [[1, 0, 0], [0, 0, 1]]

# 旋转角度
angle1 = 0
angle2 = 0
cube_angle = 0  # 立方体旋转角度
cone_angle = 0  # 圆锥旋转角度

# 几何体位置
sphere1_position = [2, 4, -2]
sphere2_position = [5, -1, 1]
cube_position = [-5, 1, 0]
cone_position = [0, 0, 0]

# 是否旋转几何体
rotate_sphere1 = True
rotate_sphere2 = True
rotate_cube = True
rotate_cone = True

# 当前纹理索引
sphere1_texture_index = 0
sphere2_texture_index = 0
cube_texture_index = 0
cone_texture_index = 0

class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0, 0, 0, 1)  # 设置背景色为黑色
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        glEnable(GL_LIGHTING)  # 启用光照#
        glEnable(GL_LIGHT0)  # 启用光源0#
        glEnable(GL_LIGHT1)  # 启用光源1#
        self.init_lighting()  # 初始化光照
        self.init_textures()  # 初始化纹理

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)  # 设置视口大小
        glMatrixMode(GL_PROJECTION)  # 设置投影矩阵模式
        glLoadIdentity()  # 重置投影矩阵
        gluPerspective(45, w / h, 0.1, 50)  # 设置透视投影
        glMatrixMode(GL_MODELVIEW)  # 设置模型视图矩阵模式

    def paintGL(self):
        global angle1, angle2, cube_angle,cone_angle
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 清除颜色和深度缓冲
        glLoadIdentity()  # 重置模型视图矩阵
        gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)  # 设置相机位置(10,10,10),目标点(0,0,0),相机的上方向为(0,1,0)Y方向

        glPushMatrix()  # 保存当前矩阵
        self.update_lighting()  # 更新光照
        self.draw_spheres()  # 绘制两个球体
        self.draw_cube()  # 绘制立方体
        self.draw_cone()  # 绘制圆锥体
        self.draw_light_sources()  # 绘制光源
        glPopMatrix()  # 恢复矩阵

        if rotate_sphere1:
            angle1 += 1.0
        if rotate_sphere2:
            angle2 += 1.0
        if rotate_cube:
            cube_angle += 1.0
        if rotate_cone:
            cone_angle += 1.0

        self.update()  # 请求更新绘制

    def init_lighting(self):  # 初始化光照
        # 环境光，glLightfv设置光源函数，GL_AMBIENT表示设置环境光参数，Alpha通道，表示不透明度
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.1, 0.1, 0.1, 1])
        # 光源衰减系数，glLightf，用于设置光源的浮点参数
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)#常量衰减系数，表示光源距离物体的距离不变时光照强度的衰减，光照强度不随距离变化
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)#线性衰减系数，表示光源距离物体的距离线性变化时光照强度的衰减，光源距离物体的距离每增加1单位，光照强度减少10%
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)#二次方衰减系数，表示光源距离物体的距离平方变化时光照强度的衰减,光源距离物体的距离平方每增加1单位，光照强度减少1%
        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.01)

    def init_textures(self):
        self.texture_ids = glGenTextures(6)  # 生成6个纹理ID

        # 第一个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[0])#二维纹理
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)#纹理的水平包裹方式为重复
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)#纹理的垂直包裹方式为重复
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)#纹理的放大过滤器为线性过滤（linear filter）
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)#纹理的缩小过滤器为线性过滤（linear filter）
        image1 = Image.open("line.jpg")
        image1 = image1.transpose(Image.FLIP_TOP_BOTTOM)#将图像上下翻转，因为 OpenGL 中的纹理坐标系的原点在左下角，而许多图像文件格式的原点在左上角
        img_data1 = image1.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image1.width, image1.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data1)

        # 第二个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[1])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        image2 = Image.open("moon.jpg")
        image2 = image2.transpose(Image.FLIP_TOP_BOTTOM)
        img_data2 = image2.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image2.width, image2.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data2)

        # 第三个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[2])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        image3 = Image.open("color.jpg")
        image3 = image3.transpose(Image.FLIP_TOP_BOTTOM)
        img_data3 = image3.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image3.width, image3.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data3)

        # 第四个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[3])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        image4 = Image.open("spot.jpg")
        image4 = image4.transpose(Image.FLIP_TOP_BOTTOM)
        img_data4 = image4.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image4.width, image4.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data4)

        # 第五个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[4])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        image5 = Image.open("leather.jpg")
        image5 = image5.transpose(Image.FLIP_TOP_BOTTOM)
        img_data5 = image5.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image5.width, image5.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data5)

        # 第六个纹理
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[5])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        image6 = Image.open("brush.jpg")
        image6 = image6.transpose(Image.FLIP_TOP_BOTTOM)
        img_data6 = image6.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image6.width, image6.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data6)

    def update_lighting(self):  # 更新光照
        global light_positions, light_colors
        glLightfv(GL_LIGHT0, GL_POSITION, light_positions[0] + [1])#构成齐次坐标，用于在 OpenGL 中表示位置。
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_colors[0] + [1])  # 漫反射，构成 RGBA 颜色
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_colors[0] + [1])  # 高光反射，构成 RGBA 颜色

        glLightfv(GL_LIGHT1, GL_POSITION, light_positions[1] + [1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_colors[1] + [1])
        glLightfv(GL_LIGHT1, GL_SPECULAR, light_colors[1] + [1])

    def draw_spheres(self):  # 两个球体的绘制
        global angle1, angle2, sphere1_position, sphere2_position
        # 球体细分数（越高越精细）
        slices = 40
        stacks = 40
        # 球体半径
        radius = 1.5

        # 第一个球体
        glPushMatrix()#保存当前矩阵状态
        glTranslatef(*sphere1_position)  # 移动第一个球体的位置
        glRotatef(angle1, 0, 1, 0)  # 绕Y轴旋转第一个球体
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[sphere1_texture_index])#绑定第一个球体使用的纹理。#
        glEnable(GL_TEXTURE_2D)#启用2D纹理#
        quadric = gluNewQuadric()#创建一个新的二次曲面对象，用于绘制球体
        gluQuadricTexture(quadric, GL_TRUE)#启用二次曲面的纹理映射#
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1, 1, 1, 1))  # 设置材质的环境光和漫反射颜色为白色，以便正确显示纹理。
        gluSphere(quadric, radius, slices, stacks)#绘制球体
        gluDeleteQuadric(quadric)#删除二次曲面对象
        glDisable(GL_TEXTURE_2D)#禁用2D纹理#
        glPopMatrix()#恢复之前保存的矩阵状态

        # 第二个球体
        glPushMatrix()
        glTranslatef(*sphere2_position)  # 移动第二个球体的位置
        glRotatef(angle2, 0, 1, 0)  # 绕Y轴旋转第二个球体
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[sphere2_texture_index])
        glEnable(GL_TEXTURE_2D)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1, 1, 1, 1))  # 将材质设置为白色以正确显示纹理
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def draw_cube(self):  # 立方体的绘制函数
        global cube_angle, cube_position
        # 立方体边长
        size = 1.5

        glPushMatrix()  # 保存当前矩阵状态
        glTranslatef(*cube_position)  # 移动立方体到指定位置
        glRotatef(cube_angle, 1, 1, 0)  # 绕向量 (1, 1, 0) 旋转立方体 cube_angle 角度
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[cube_texture_index])  # 绑定立方体的纹理
        glEnable(GL_TEXTURE_2D)  # 启用2D纹理
        glBegin(GL_QUADS)  # 开始绘制四边形

        # 定义前面顶点和纹理坐标
        glTexCoord2f(0, 0)#定义第一个顶点的纹理坐标 (0, 0)。这个坐标表示纹理图像的左下角。
        glVertex3f(-size, -size, size)#定义第一个顶点的三维坐标
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, size)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, size)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, size)

        # 定义后面顶点和纹理坐标
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, -size)
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, -size)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, -size)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, -size)

        # 定义左面顶点和纹理坐标
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, -size)
        glTexCoord2f(1, 0)
        glVertex3f(-size, -size, size)
        glTexCoord2f(1, 1)
        glVertex3f(-size, size, size)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, -size)

        # 定义右面顶点和纹理坐标
        glTexCoord2f(0, 0)
        glVertex3f(size, -size, -size)
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, size)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, size)
        glTexCoord2f(0, 1)
        glVertex3f(size, size, -size)

        # 定义顶面顶点和纹理坐标
        glTexCoord2f(0, 0)
        glVertex3f(-size, size, -size)
        glTexCoord2f(1, 0)
        glVertex3f(size, size, -size)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, size)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, size)

        # 定义底面顶点和纹理坐标
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, -size)
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, -size)
        glTexCoord2f(1, 1)
        glVertex3f(size, -size, size)
        glTexCoord2f(0, 1)
        glVertex3f(-size, -size, size)

        glEnd()  # 结束绘制四边形
        glDisable(GL_TEXTURE_2D)  # 禁用2D纹理
        glPopMatrix()  # 恢复之前保存的矩阵状态

    def draw_cone(self):
        global cone_angle, cone_position
        glPushMatrix()
        glTranslatef(*cone_position)  # 移动圆锥体位置
        glRotatef(cone_angle, 0, 0, 1)  # 旋转圆锥体
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[cone_texture_index])  # 绑定圆锥体的纹理
        glEnable(GL_TEXTURE_2D)  # 启用2D纹理
        quadric = gluNewQuadric()  # 创建一个新的二次曲面对象
        gluQuadricTexture(quadric, GL_TRUE)  # 为二次曲面对象启用纹理
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1, 1, 1, 1))  # 将材质设置为白色以正确显示纹理
        gluCylinder(quadric, 1.5, 0, 3, 32, 32)  # 底半径1.5，顶半径0，高3，32段和32堆
        gluDeleteQuadric(quadric)  # 删除二次曲面对象
        glDisable(GL_TEXTURE_2D)  # 禁用2D纹理
        glPopMatrix()  # 恢复之前保存的矩阵状态

    def draw_light_sources(self):  # 绘制光源函数
        global light_positions, light_colors
        glDisable(GL_LIGHTING)  # 禁用光照，以正确显示光源
        for i in range(2):
            glColor3fv(light_colors[i])  # 设置当前颜色为光源的颜色
            glPushMatrix()  # 保存当前矩阵状态
            glTranslatef(*light_positions[i])  # 移动到光源的位置
            gluSphere(gluNewQuadric(), 0.2, 20, 20)  # 绘制一个半径为0.2的球体，分段数为20
            glPopMatrix()  # 恢复之前保存的矩阵状态
        glEnable(GL_LIGHTING)  # 重新启用光照


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("计算机动画演示系统")
        self.setGeometry(100, 100, 1200, 900)

        self.opengl_widget = OpenGLWidget()
        self.setCentralWidget(self.opengl_widget)


        self.create_control_position()
        self.create_control_panel()
        self.create_image_list_panel()
        self.create_control_rotate()

    def create_control_position(self):
        control_widget = QWidget()
        control_layout = QVBoxLayout()

        # 光源位置控制
        light1_control_group = QGroupBox("光源1位置")
        light1_control_layout = QGridLayout()
        light1_control_group.setLayout(light1_control_layout)
        control_layout.addWidget(light1_control_group)

        for j in range(3):
            label = QLabel(f"光源 1 Axis {'XYZ'[j]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(light_positions[0][j])
            slider.valueChanged.connect(self.create_light_position_changed_callback(0, j))
            light1_control_layout.addWidget(label, j, 0)
            light1_control_layout.addWidget(slider, j, 1)

        light2_control_group = QGroupBox("光源2位置")
        light2_control_layout = QGridLayout()
        light2_control_group.setLayout(light2_control_layout)
        control_layout.addWidget(light2_control_group)

        for j in range(3):
            label = QLabel(f"光源 2 Axis {'XYZ'[j]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(light_positions[1][j])
            slider.valueChanged.connect(self.create_light_position_changed_callback(1, j))
            light2_control_layout.addWidget(label, 3+j, 0)
            light2_control_layout.addWidget(slider, 3+j, 1)


        # 几何体位置控制
        sphere1_control_group = QGroupBox("球体1位置控制")
        sphere1_control_layout = QGridLayout()
        sphere1_control_group.setLayout(sphere1_control_layout)
        control_layout.addWidget(sphere1_control_group)

        for i in range(3):
            label = QLabel(f"球体 1 Axis {'XYZ'[i]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(sphere1_position[i])
            slider.valueChanged.connect(self.create_sphere1_position_changed_callback(i))
            sphere1_control_layout.addWidget(label, i, 0)
            sphere1_control_layout.addWidget(slider, i, 1)

        sphere2_control_group = QGroupBox("球体2位置控制")
        sphere2_control_layout = QGridLayout()
        sphere2_control_group.setLayout(sphere2_control_layout)
        control_layout.addWidget(sphere2_control_group)

        for i in range(3):
            label = QLabel(f"球体 2 Axis {'XYZ'[i]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(sphere2_position[i])
            slider.valueChanged.connect(self.create_sphere2_position_changed_callback(i))
            sphere2_control_layout.addWidget(label, i + 3, 0)
            sphere2_control_layout.addWidget(slider, i + 3, 1)

        cube_control_group = QGroupBox("立方体位置")
        cube_control_layout = QGridLayout()
        cube_control_group.setLayout(cube_control_layout)
        control_layout.addWidget(cube_control_group)

        for i in range(3):
            label = QLabel(f"立方体 Axis {'XYZ'[i]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(cube_position[i])
            slider.valueChanged.connect(self.create_cube_position_changed_callback(i))
            cube_control_layout.addWidget(label, i, 0)
            cube_control_layout.addWidget(slider, i, 1)

        cone_control_group = QGroupBox("圆锥位置")
        cone_control_layout = QGridLayout()
        cone_control_group.setLayout(cone_control_layout)
        control_layout.addWidget(cone_control_group)

        for i in range(3):
            label = QLabel(f"圆锥 Axis {'XYZ'[i]}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(cone_position[i])
            slider.valueChanged.connect(self.create_cone_position_changed_callback(i))
            cone_control_layout.addWidget(label, i, 0)
            cone_control_layout.addWidget(slider, i, 1)

        control_widget.setLayout(control_layout)

        # 创建 QDockWidget 并将控制面板添加到其中
        dock_widget = QDockWidget("位置控制", self)
        dock_widget.setWidget(control_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)


    def create_control_rotate(self):
        # 添加复选框来控制旋转
        rotate_group = QGroupBox("是否旋转几何体")
        rotate_layout = QVBoxLayout()
        rotate_group.setLayout(rotate_layout)

        self.rotate_sphere1_checkbox = QCheckBox("旋转球体1")
        self.rotate_sphere1_checkbox.setChecked(rotate_sphere1)
        self.rotate_sphere1_checkbox.stateChanged.connect(self.rotate_sphere1_changed)
        rotate_layout.addWidget(self.rotate_sphere1_checkbox)

        self.rotate_sphere2_checkbox = QCheckBox("旋转球体2")
        self.rotate_sphere2_checkbox.setChecked(rotate_sphere2)
        self.rotate_sphere2_checkbox.stateChanged.connect(self.rotate_sphere2_changed)
        rotate_layout.addWidget(self.rotate_sphere2_checkbox)

        self.rotate_cube_checkbox = QCheckBox("旋转立方体")
        self.rotate_cube_checkbox.setChecked(rotate_cube)
        self.rotate_cube_checkbox.stateChanged.connect(self.rotate_cube_changed)
        rotate_layout.addWidget(self.rotate_cube_checkbox)

        self.rotate_cone_checkbox = QCheckBox("旋转圆锥")
        self.rotate_cone_checkbox.setChecked(rotate_cone)
        self.rotate_cone_checkbox.stateChanged.connect(self.rotate_cone_changed)
        rotate_layout.addWidget(self.rotate_cone_checkbox)

        # 创建 QDockWidget 并设置内容
        dock = QDockWidget("旋转控制", self)
        dock.setWidget(rotate_group)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)


    def rotate_sphere1_changed(self, state):
        global rotate_sphere1
        rotate_sphere1 = state == Qt.Checked

    def rotate_sphere2_changed(self, state):
        global rotate_sphere2
        rotate_sphere2 = state == Qt.Checked

    def rotate_cube_changed(self, state):
        global rotate_cube
        rotate_cube = state == Qt.Checked

    def rotate_cone_changed(self, state):
        global rotate_cone
        rotate_cone = state == Qt.Checked

    def create_light_position_changed_callback(self, light_index, axis_index):
        def callback(value):
            light_positions[light_index][axis_index] = value
        return callback

    def create_sphere1_position_changed_callback(self, axis_index):
        def callback(value):
            sphere1_position[axis_index] = value
        return callback

    def create_sphere2_position_changed_callback(self, axis_index):
        def callback(value):
            sphere2_position[axis_index] = value
        return callback

    def create_cube_position_changed_callback(self, axis_index):
        def callback(value):
            cube_position[axis_index] = value
        return callback

    def create_cone_position_changed_callback(self, axis_index):
        def callback(value):
            cone_position[axis_index] = value
        return callback

    def create_control_panel(self):
        control_panel = QDockWidget("几何体纹理选择", self)
        control_panel.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        controls = QWidget()
        control_panel.setWidget(controls)
        layout = QVBoxLayout()

        # 创建纹理选择组合框
        self.sphere1_texture_combo = self.create_texture_combo_box("球体1纹理", self.on_sphere1_texture_change)
        self.sphere2_texture_combo = self.create_texture_combo_box("球体2纹理", self.on_sphere2_texture_change)
        self.cube_texture_combo = self.create_texture_combo_box("立方体纹理", self.on_cube_texture_change)
        self.cone_texture_combo = self.create_texture_combo_box("圆锥纹理", self.on_cone_texture_change)

        layout.addWidget(self.sphere1_texture_combo)
        layout.addWidget(self.sphere2_texture_combo)
        layout.addWidget(self.cube_texture_combo)
        layout.addWidget(self.cone_texture_combo)

        controls.setLayout(layout)
        self.addDockWidget(Qt.RightDockWidgetArea, control_panel)


    def on_sphere1_texture_change(self, index):
        global sphere1_texture_index
        sphere1_texture_index = index

    def on_sphere2_texture_change(self, index):
        global sphere2_texture_index
        sphere2_texture_index = index

    def on_cube_texture_change(self, index):
        global cube_texture_index
        cube_texture_index = index

    def on_cone_texture_change(self, index):
        global cone_texture_index
        cone_texture_index = index

    def create_texture_combo_box(self, label_text, callback):
        group_box = QGroupBox(label_text)
        layout = QVBoxLayout()
        combo_box = QComboBox()
        combo_box.addItem("line")
        combo_box.addItem("moon")
        combo_box.addItem("color")
        combo_box.addItem("spot")
        combo_box.addItem("leather")
        combo_box.addItem("brush")
        combo_box.currentIndexChanged.connect(callback)
        layout.addWidget(combo_box)
        group_box.setLayout(layout)
        return group_box

    def on_sphere1_texture_change(self, index):
        global sphere1_texture_index
        sphere1_texture_index = index

    def on_sphere2_texture_change(self, index):
        global sphere2_texture_index
        sphere2_texture_index = index

    def on_cube_texture_change(self, index):
        global cube_texture_index
        cube_texture_index = index

    def on_cone_texture_change(self, index):
        global cone_texture_index
        cone_texture_index = index


    def create_image_list_panel(self):
        image_list_panel = QDockWidget("纹理一览", self)
        image_list_panel.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        images_widget = QWidget()
        image_list_panel.setWidget(images_widget)
        layout = QVBoxLayout()

        self.image_list_widget = QListWidget()
        self.image_preview_label = QLabel()

        self.image_list_widget.setIconSize(QSize(64, 64))
        self.image_list_widget.itemClicked.connect(self.on_image_selected)

        layout.addWidget(self.image_list_widget)
        layout.addWidget(self.image_preview_label)
        images_widget.setLayout(layout)

        self.addDockWidget(Qt.LeftDockWidgetArea, image_list_panel)

        self.load_images()

    def load_images(self):
        # 获取当前目录下的所有图片文件
        image_extensions = ['.jpg']
        image_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].lower() in image_extensions]

        for image_file in image_files:
            item = QListWidgetItem(image_file)
            item.setIcon(QIcon(image_file))
            self.image_list_widget.addItem(item)

    def on_image_selected(self, item):
        image_file = item.text()
        pixmap = QPixmap(image_file)
        self.image_preview_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
