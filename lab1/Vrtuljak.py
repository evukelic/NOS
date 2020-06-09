import multiprocessing
import time
import random


def carousel():
    """
    Function which represents behaviour of carousel.
    """

    # queue for the requests from visitors to carousel
    request_queue = multiprocessing.Queue()

    # queue for the responses from carousel to visitors
    response_queue = multiprocessing.Queue()

    visitors_on_carousel = 0

    # create processes and give them function they'll execute
    for i in range(1, 9):
        multiprocessing.Process(target=ride_request, args=(request_queue, i, response_queue)).start()
    time.sleep(0.8)

    while request_queue.empty() is not True:
        # array for the id's of visitors which will be on the carousel
        ids = []
        # fill the carousel
        while visitors_on_carousel < 4:
            msg, p_id = request_queue.get()
            if msg == 'ride':
                ids.append(p_id)
                visitors_on_carousel += 1
                time.sleep(0.5)
                response_queue.put(('sit', p_id))

        if visitors_on_carousel == 4:
            time.sleep(0.5)
            print('\nPokrenuo vrtuljak!')
            time.sleep(random.uniform(1., 4.))
            print('Vrtuljak zaustavljen!\n')

            # empty the carousel
            for i in ids:
                response_queue.put(('out', i))

        visitors_on_carousel = 0


def ride_request(request, pid, response):
    """
    Function which represents visitors request for the ride.
    Visitor sends the request towards carousel via request queue, and waits for the response from response queue.
    :param request: queue of the request messages (from visitor to carousel)
    :param pid: visitor process id
    :param response: queue of the response messages (from carousel to visitor)
    """
    for n in range(1, 4):
        time.sleep(random.uniform(0.1, 3.))
        # put the ride request to the request queue for the current process
        request.put(('ride', pid))

        while True:
            # take one tuple (message, id) from the responses queue
            p_msg, p_i = response.get()
            if int(p_i) == int(pid) and p_msg == 'sit':
                print('Sjeo posjetitelj ' + str(pid))
            elif int(p_i) == int(pid) and p_msg == 'out':
                print('Sišao posjetitelj ' + str(pid))
                break
            else:
                # if id of response is not mine, put it back in queue and wait for correct one
                response.put((p_msg, p_i))

    print('Posjetitelj ' + str(pid) + ' završio!')


if __name__ == "__main__":
    carousel_process = multiprocessing.Process(target=carousel)
    carousel_process.start()
    carousel_process.join()

    print('\nVrtuljak završio!')
