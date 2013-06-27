import logging

class DummyTest:
    def __init__(self):
        self.valid_init_range =  4
        self.valid_end_range  =  8
        self.full_range = 10
        self.dire = 0
        self.cur_pos = 0
        self.cmd_pos = 0
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

    def move_motor_with_sensor(self,steps, dire):
        logging.info("moving: %d  to dir(%d)" % (steps, dire))

    def get_valid_steps(self, current_position, step):
        # set commanded position
        if current_position == 0 :
            cmd_position = self.valid_init_range + step
            self.move_motor_with_sensor(cmd_position, self.dire)
            return current_position, cmd_position
        else:
            cmd_position = current_position + step
        # try to move acording borders
        if cmd_position >= self.valid_init_range and cmd_position <= self.valid_end_range:
            logging.info("valid cmd_pos : %d" % cmd_position)
            current_position = cmd_position
            self.move_motor_with_sensor(step, self.dire)
        else:
            logging.error("NOT VALID cmd_pos : %d" % cmd_position)
            if cmd_position > self.valid_end_range:
                cmd_position = self.valid_init_range
                logging.error("back to init cmd_pos : %d" % cmd_position)
                self.move_motor_with_sensor(cmd_position, self.dire)
                current_position = cmd_position
                logging.error("current pos: %d" % current_position)
    
            if cmd_position < self.valid_init_range:
                cmd_position = self.valid_end_range
                logging.error("back to end cmd_pos : %d" % cmd_position)
                self.move_motor_with_sensor(cmd_position, self.dire)
                current_position = cmd_position
                logging.error("current pos: %d" % current_position)

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
