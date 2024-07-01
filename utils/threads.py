from threading import Thread, active_count


def run_thread(thread: Thread) -> None:
    if active_count() == 1:
        thread.start()
