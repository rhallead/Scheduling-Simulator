#!/usr/bin/env python3

import sys

# read job file
def read_job_file(file_path):
    jobs = []
    try:
        # read file_path and convert to 
        with open(file_path, 'r') as file:
            for line in file:
                arrival_time, run_time = map(int, line.strip().split())
                jobs.append((arrival_time, run_time))
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)
    return jobs

# First In First Out shceduler
def fifo_scheduler(jobs):
    # call function to print out job info? maybe?
    current_time = 0
    results = []
    # go through every job
    for job in jobs:
        run_time, arrival_time, pid = job
        if arrival_time > current_time:
            # update current time if necessary
            current_time = arrival_time
        # calculate turnaround time
        turnaround_time = current_time + run_time - arrival_time
        # calculate wait time
        wait_time = current_time - arrival_time
        results.append((turnaround_time, wait_time, pid))
        # increase current time
        current_time += run_time
    return results

# Shortest Remaining Time Next scheduler
def srtn_scheduler(jobs):
    current_time = 0
    results = []
    # store original run times!!
    run_times = {}
    for i in jobs:
        run_times[i[2]] = i[0]

    while jobs != []:
        available = []
        for job in jobs:
            # if arrival time is less than or equal to current_time
            if job[1] <= current_time:
                available.append(job)

        if available == []:
            # increase time and continue if no available jobs
            current_time += 1
            continue
        else:
            # sort by shortest run time
            available.sort(key=lambda x: x[0])
            # take shortest first available job
            process = list(available[0])
            # remove from available list
            copy_process = available.pop(0)
            current_time += 1
            # decrement remaining run time of process by 1
            process[0] -= 1
            jobs.remove(copy_process)
            # if remaining run time is now 0
            if process[0] == 0:
                # calculate turnaround and wait times
                # current time - arrival time
                turnaround_time = current_time - process[1]
                # turnaround - original run time
                wait_time = turnaround_time - run_times[process[2]]
                pid = process[2]
                results.append((turnaround_time, wait_time, pid))
                continue
            else:
                # if there is still run time, put job back on job list
                jobs.insert(0, process)
    return results

# Round Robin scheduler
def rr_scheduler(jobs, quantum):
    # jobs in format of (run time, arrival time, pid)
    current_time = 0
    results = []
    # set up run times for each process to save them somewhere
    run_times = {}
    for i in jobs:
        run_times[i[2]] = i[0]

    while jobs != []:
        available = []
        for job in jobs:
            # if arrival time less than or equal to current time 
            if job[1] <= current_time:
                available.append(job)
        # if no jobs are available, increase time by 1 and move on
        if available == []:
            current_time += 1
            continue

        else:
            # get first job
            process = list(available[0])
            copy_process = available.pop(0)
            jobs.remove(copy_process)
            # remaining runtime
            rem_runtime = process[0]
            # if runtime is less than or equal to quantum
            if rem_runtime <= quantum:
                # add remaining runtime to current time
                current_time += rem_runtime
                # calculate turnaround and wait times
                turnaround_time = current_time - process[1]
                wait_time = turnaround_time - run_times[process[2]]
                results.append((turnaround_time, wait_time, process[2]))
                continue
            # if remaining runtime is more than quantum
            else:
                # add quantum to current time
                current_time += quantum
                # subtract quantum from job's remaining runtime
                process[0] -= quantum
                # put process back on job list
                jobs.append(process)
    return results


# parse command line arguments
def parse_arguments():
    args = sys.argv[1:] 
    file_path = None
    algorithm = 'FIFO'  # default algorithm
    quantum = 1  # default quantum

    # Parse arguments
    if len(args) < 1 or len(args) > 5:
        print("Error: Wrong number of arguments")
        sys.exit(1)

    file_path = args[0]
    args = args[1:]

    while args:
        # check for -p
        if args[0] == '-p':
            if len(args) < 2:
                print("Error: Missing argument for '-p' option")
                sys.exit(1)
            algorithm = args[1]
            # return to default if given algorithm was wrong
            if algorithm not in ['FIFO', 'SRTN', 'RR']:
                algorithm = "FIFO"
            # update args 
            args = args[2:]
        # check for -q
        elif args[0] == '-q':
            if len(args) < 2:
                print("Error: Missing argument for '-q' option")
                sys.exit(1)
            try:
                # try to convert to integer
                quantum = int(args[1])
            except ValueError:
                print("Error: Quantum must be an integer")
                sys.exit(1)
            # check if quantum is valid
            if quantum <= 0:
                print("Error: Quantum must be a positive integer")
                sys.exit(1)
            # update args
            args = args[2:]
        # if anything else, error
        else:
            print("Error: Invalid argument:", args[0])
            sys.exit(1)

    return file_path, algorithm, quantum

# function to print results
def print_results(results, avg_turnaround, avg_wait):
    for i in results:
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (i[2], i[0], i[1]))
    print("Average -- Turnaround %3.2f  Wait %3.2f" % (avg_turnaround, avg_wait))


def main():
    # Parse command line arguments
    file_path, algorithm, quantum = parse_arguments()
    jobs = read_job_file(file_path)
    jobs = sorted(jobs, key=lambda x: x[1])
    # add pid to each job 
    jobs = [(job[0], job[1], idx) for idx, job in enumerate(jobs)]
    # jobs in format of (run time, arrival time, pid)

    if algorithm == "FIFO":
        results = fifo_scheduler(jobs)
    elif algorithm == "SRTN":
        results = srtn_scheduler(jobs)
    elif algorithm == "RR":
        results = rr_scheduler(jobs, quantum)
    
    # sort results based on ascending pid
    results = sorted(results, key=lambda x: x[2])

    # calculate avg turnaround time and wait time
    total_turnaround = 0
    total_wait = 0
    for i in results:
        total_turnaround += i[0]
        total_wait += i[1]
    avg_turnaround = total_turnaround / len(results)
    avg_wait = total_wait / len(results)

    # print results
    print_results(results, avg_turnaround, avg_wait)

if __name__ == "__main__":
    main()
