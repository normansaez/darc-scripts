import logging

CAMBIO = {"IZQUIERDA":"DERECHA","DERECHA":"IZQUIERDA"}
class DummyTest:
    def __init__(self):
        self.valid_init_range =  4
        self.valid_end_range  =  8
        self.full_range = 10
        self.dire = "DERECHA"
        self.cur_pos = 0
        self.cmd_pos = 0
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

    def move_motor_with_sensor(self,steps, dire):
        logging.info("moving: %d  to dir(%s)" % (steps, dire))

    def get_valid_steps(self, current_position, step):
        logging.info("cur_pos : %d" % current_position)
        cmd_position = current_position + step
        logging.info("cmd_pos : %d" % cmd_position)
        if cmd_position < self.valid_init_range:
            logging.error("cmd from %d --> %d" % (cmd_position, self.valid_init_range))
            cmd_position = self.valid_init_range
        if cmd_position > self.valid_end_range:
            logging.error("cmd from %d --> %d" % (cmd_position, self.valid_init_range))
            cmd_position = self.valid_init_range

        pasos = cmd_position - current_position
        if pasos > 0:
            logging.info("steps to cmd_pos: %d" % pasos)
            self.move_motor_with_sensor(pasos, self.dire)
        else:
            logging.info("steps to cmd_pos: %d" % pasos)
            self.dire = CAMBIO[self.dire]
            pasos = abs(pasos)
            self.move_motor_with_sensor(pasos, self.dire)
            self.dire = CAMBIO[self.dire]

        current_position = cmd_position
        return current_position, cmd_position

if __name__ == '__main__':
    dt = DummyTest()
    steps = 1
    for itera in range(0,10+1):
        logging.info("################################")
        logging.info("iter : %d" % itera)
        logging.info("dt.cur_pos: %d" % dt.cur_pos)
        dt.cur_pos, dt.cmd_pos = dt.get_valid_steps(dt.cur_pos, steps)
        logging.info("after steps ...")
        logging.info("dt.cur_pos: %d" % dt.cur_pos)
        logging.info("dt.cmd_pos: %d" % dt.cmd_pos)
