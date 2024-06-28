from threading import Thread, active_count


def run_thread(thread: Thread) -> None:
    print(f"{active_count()=}")
    if active_count() == 1:
        thread.start()
