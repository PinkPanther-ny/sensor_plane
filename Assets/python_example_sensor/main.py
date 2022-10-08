import serial
import time
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import numpy as np
from threading import Thread


data = dict()

def update_data(ser):
    
    while True:
        buf = ser.read(18)
        assert(buf[:2] == b'\xa5\xa5')
        
        data.update({
            "X": twosComplement_hex(buf[2] | buf[3] << 8) / 100,
            "Y": twosComplement_hex(buf[4] | buf[5] << 8) / 100,
            "Z": twosComplement_hex(buf[6] | buf[7] << 8) / 100,

            "yaw_angle_velocity": twosComplement_hex(buf[8] | buf[9] << 8) / 100,
            "yaw_angle": twosComplement_hex(buf[10] | buf[11] << 8) / 100,
            "pitch_angle": twosComplement_hex(buf[12] | buf[13] << 8) / 100,
            "roll_angle": twosComplement_hex(buf[14] | buf[15] << 8) / 100,
            "checksum": (buf[16] | buf[17]) << 8
        })


def get_serial_port(name):
    ser = serial.Serial(
        port=name,
        baudrate=115200,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
    assert(ser.isOpen())
    print(f"Port {ser.name} initialized!")
    return ser

def drawText(screen, text, posx, posy, textHeight=48, fontColor=(0,0,0), backgroudColor=None):
    import pygame
    fontObj = pygame.font.SysFont('Corbel', textHeight)
    textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = (posx, posy)
    screen.blit(textSurfaceObj, textRectObj)
    
def twosComplement_hex(hexval):
    bits = 16
    # val = int(hexval, bits)
    val = hexval
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val



if __name__ == "__main__":
    
    data_thread = Thread(target = update_data, args=(get_serial_port("/dev/ttyUSB0"),))
    data_thread.daemon = True
    data_thread.start()
    
    pygame.init()
    width, height = (640, 480)
    screen = pygame.display.set_mode((width, height))
    screen_large = np.full((height, width, 3), 128, np.uint8)
    slider1 = Slider(screen, 15, 228, 200, 10, min=-180, max=180, step=0.1)
    slider2 = Slider(screen, 15, 273, 200, 10, min=-180, max=180, step=0.1)
    slider3 = Slider(screen, 15, 318, 200, 10, min=-180, max=180, step=0.1)
    slider4 = Slider(screen, 15, 363, 200, 10, min=-180, max=180, step=0.1)

    sliderX = Slider(screen, 300, 228, 200, 10, min=-20, max=20, step=0.1)
    sliderY = Slider(screen, 300, 273, 200, 10, min=-20, max=20, step=0.1)
    sliderZ = Slider(screen, 300, 318, 200, 10, min=-20, max=20, step=0.1)

    while True:
        
        surf = pygame.surfarray.make_surface(screen_large.transpose(1, 0, 2))
        screen.blit(surf, (0, 0))
        
        slider1.setValue(data["pitch_angle"])
        slider2.setValue(data["roll_angle"])
        slider3.setValue(data["yaw_angle"])
        slider4.setValue(data["yaw_angle_velocity"])
        drawText(screen, f"pitch_angle : {slider1.getValue()}", 15, 195, 26)
        drawText(screen, f"roll_angle : {slider2.getValue()}", 15, 245, 26)
        drawText(screen, f"yaw_angle : {slider3.getValue()}", 15, 295, 26)
        drawText(screen, f"yaw_angle_velocity : {slider4.getValue()}", 15, 340, 26)
                    
        sliderX.setValue(data["X"])
        sliderY.setValue(data["Y"])
        sliderZ.setValue(data["Z"])
        drawText(screen, f"X : {sliderX.getValue()}", 300, 195, 26)
        drawText(screen, f"Y : {sliderY.getValue()}", 300, 245, 26)
        drawText(screen, f"Z : {sliderZ.getValue()}", 300, 295, 26)
                    
        events = pygame.event.get()
        for event in events:
            # Close window to exit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.event.pump()
        pygame_widgets.update(events)
        pygame.display.update()
        # 100Hz
        
    pass