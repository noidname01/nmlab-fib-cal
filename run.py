import os
from multiprocessing import Pool

processes = ["python3 ./gRPC/server.py", 
             "python3 ./rest/manage.py runserver 0.0.0.0:8000",]


def run_process(process):
    os.system(process)

if __name__ == '__main__':
    try:
        pool = Pool(processes=len(processes))
        pool.map(run_process, processes)
    except:
        os.system("bash terminate.sh")