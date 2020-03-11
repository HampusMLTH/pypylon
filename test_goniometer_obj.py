from goniometer_obj import GoniometerObject


def main():
    angle = 2
    go = GoniometerObject()
    print(go.stage_angle)
    print(go.angle_2_motorpos(angle, go.STAGE))
    go.stage_angle = angle
    print(go.stage_angle)
    print("done stage\n")
    
    print(go.sample_angle)
    print(go.angle_2_motorpos(angle, go.SAMPLE))
    go.sample_angle = angle
    print(go.sample_angle)
    print("done sample\n")
    
    print(go.led_angle)
    go.led_angle = -5
    print(go.led_angle)
    
if __name__ == '__main__':
    main()
    
