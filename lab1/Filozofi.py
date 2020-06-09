import multiprocessing
import random
import time
import sys


def my_req_sent_before(my_clock, req_clock, my_id, req_id):
    """
    Helper function which determines which request is of higher priority.
    :return: True if the parent request is of higher priority, False otherwise.
    """
    if int(my_clock) == int(req_clock):
        return int(my_id) < int(req_id)
    return int(my_clock) < int(req_clock)


class Message:
    """
    Class Message represents one of the two types of messages that will be shared among processes - request or response.
    """

    def __init__(self, msg_name, process_id, t):
        """
        Initializes one Message object.
        :param msg_name: Name of the message (either 'request' or 'response')
        :param process_id: Id of a process that sends the Message
        :param t: Clock time in the message
        """
        self.name = msg_name
        self.process_id = process_id
        self.time = t

    def __str__(self):
        return self.name + ": (" + str(self.process_id) + ", " + str(self.time) + ")"


class Philosopher:
    """
    Class Philosopher represents one Philosopher process.
    Process communicates with other processes by sending messages through pipelines.
    """

    def __init__(self, pid, pipeline_connections_r, pipeline_connections_w):
        """
        Function which initializes an object.
        :param pid: Id of a process
        :param pipeline_connections_r: Pipelines from which process can read the messages
        :param pipeline_connections_w: Pipelines from which process can send the messages
        """
        # init a process and give it a function it will execute on start()
        self.process = multiprocessing.Process(target=self.manage_requests)
        # request message which is sent for entering critical section
        self.sent_request = None
        self.clock = random.randrange(1, len(pipeline_connections_r)*10)
        self.id = pid
        self.connections_r = pipeline_connections_r
        self.connections_w = pipeline_connections_w
        # number of responses for the sent request
        self.answers = 0
        # requests that need to be answered
        self.waiting_requests = {}

    def manage_requests(self):
        """
        Function which is executed when process starts. It sends request messages for the critical
        section, waits for the responses and sends responses for the waiting requests.
        """
        time.sleep(random.uniform(0.1, 3.))

        self.request_critical_section()
        self.wait_for_responses()
        self.send_queued_messages()

        time.sleep(random.uniform(0.1, 3.))

    def request_critical_section(self):
        """
        Function sends requests to the other processes for entering the critical section.
        """
        for connection, _id in self.connections_w:
            self.sent_request = Message('request', self.id, self.clock)
            print('Filozof ' + str(self.id) + ' šalje: ' + str(self.sent_request) + ' filozofu ' + str(_id))
            connection.send(self.sent_request)

    def enter_critical_section(self):
        """
        Function which runs when process is in the critical section.
        """
        print('\nFilozof ' + str(self.id) + ' je za stolom!\n')
        time.sleep(3)

    def send_queued_messages(self):
        """
        Function which sends response messages to the queued requests when the process leaves the critical
        section. Process sends responses in sorted order (by clock).
        """
        sorted_vals = sorted(self.waiting_requests.items(), key=lambda x: x[1].time)

        for connection, _id in self.connections_w:
            for pid, m in sorted_vals:
                if pid == _id:
                    connection.send(m)

    def tick(self, req_clock):
        """
        Function that represents one tick of a clock.
        :param req_clock: Clock of a process which sent the message
        :return: new value of the clock
        """
        if self.clock > req_clock:
            return self.clock + 1
        return req_clock + 1

    def wait_for_responses(self):
        """
        Waits for the responses for the sent request.
        If it meanwhile gets the request from another process, it either sends the response or puts
        the request in the waiting queue, following the Ricart-Agrawala Algorithm.
        """
        while self.answers != len(self.connections_r):
            for connection, _id in self.connections_r:
                msg = connection.recv()
                print('Filozof ' + str(self.id) + ' prima: ' + str(msg))
                if msg.name == 'response':
                    self.answers += 1
                    if self.answers == len(self.connections_r):
                        self.enter_critical_section()
                else:
                    if my_req_sent_before(self.sent_request.time, msg.time, self.id, msg.process_id):
                        if msg.process_id not in self.waiting_requests:
                            self.waiting_requests[msg.process_id] = []
                        self.waiting_requests[msg.process_id] = Message('response', self.id, msg.time)
                        self.clock = self.tick(msg.time)
                    else:
                        for con, _iid in self.connections_w:
                            if _iid == msg.process_id:
                                mess = Message('response', self.id, msg.time)
                                con.send(mess)
                                print('Filozof ' + str(self.id) + ' šalje: ' + str(mess) + ' filozofu ' + str(_iid))
                                self.clock = self.tick(msg.time)


def create_pipelines(num):
    """
    Function which creates one directional pipelines between processes.
    :param num: number of processes
    :return: two dictionaries of pipelines where keys are processes' ids
    """
    # connections made only for reading
    pipes_by_id_r = {}
    # connections made only for writing
    pipes_by_id_w = {}

    for id1 in range(1, num):
        if id1 not in pipes_by_id_r:
            pipes_by_id_r[id1] = []
        if id1 not in pipes_by_id_w:
            pipes_by_id_w[id1] = []
        for id2 in range(id1 + 1, num + 1):
            if id2 not in pipes_by_id_r:
                pipes_by_id_r[id2] = []
            if id2 not in pipes_by_id_w:
                pipes_by_id_w[id2] = []

            first_r, second_w = multiprocessing.Pipe()
            first_w, second_r = multiprocessing.Pipe()

            # for particular process id, value is tuple of connection object and id of other connected side
            pipes_by_id_r[id1].append((first_r, id2))
            pipes_by_id_r[id2].append((second_r, id1))
            pipes_by_id_w[id1].append((first_w, id2))
            pipes_by_id_w[id2].append((second_w, id1))

    return pipes_by_id_r, pipes_by_id_w


if __name__ == '__main__':
    try:
        n = int(sys.argv[1])
    except IndexError:
        print('Niste unijeli broj filozofa, broj će biti izabran nasumično.')
        n = random.randrange(3, 11)
        print('Izabrani broj je: ' + str(n) + '\n')

    if int(n) < 3 or int(n) > 10:
        print('Niste unijeli validan broj filozofa, broj će biti izabran nasumično.')
        n = random.randrange(3, 11)
        print('Izabrani broj je: ' + str(n) + '\n')

    pipelines_r, pipelines_w = create_pipelines(n)

    # create n Philosophers and start the processes
    for i in range(1, n+1):
        Philosopher(i, pipelines_r[i], pipelines_w[i]).process.start()
