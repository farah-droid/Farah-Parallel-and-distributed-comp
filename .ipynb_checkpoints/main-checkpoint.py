from tasks import power
from dispatch_tasks import dispatch

if __name__ == "__main__":
    results= dispatch()
    print(results[:10])