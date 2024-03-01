#Imports relevant modules.
import sys
import json
import math

#Global variables, including volatile memory consumption, carbon intensity, and power use effectiveness (PUE).
W_memory_per_GB = 0.3725  #Taken from GreenAlgorythms4HPC
g_per_kWh = 207.07 #UK SE Carbon grams per kWh taken from https://www.carbonfootprint.com/international_electricity_factors.html
pue = 1.28 #Power use effectiveness, specific to Sussex HPC architecture

#Use stdin if it's full.                                                   
if not sys.stdin.isatty():
    input_stream = sys.stdin

#We need the node info and CPU info (specific to Sussex HPC architecture).
with open("node_info.json", 'r') as fin:
    node_info = json.load(fin)
    
with open("cpu_info.json", 'r') as fin:
    cpu_info = json.load(fin)

#Go through the qacct input line by line grabbing job
#information to store in dictionary for output and calcs.
jobs = {}
task_id = "notset"
job_id = 0
hostname = None

#Calculate carbon emissions, multiplying energy usage by carbon intensity and PUE.
def calc_carbon_UK_in_g(energy, g_per_kWh=g_per_kWh, pue=pue):
    return energy * g_per_kWh * pue

#Calculate CPU energy usage, multiplying CPU time by TDP kw per core. Converted to kWH.
def calc_cpu_kWh(cpu,cpu_time):
    return cpu_time / 3600 * cpu["TDP"]/cpu["CPU"] / 1000

#Calculate memory energy usage, multiplying max memory used (rounded up) by volatile
#memory consumption and runtime. Converted to kWH.
def calc_mem_kWh(maxvmem, wallclock, W_memory_per_GB = W_memory_per_GB):
    return math.ceil(maxvmem) * W_memory_per_GB * wallclock / 3600 / 1000

#Iterates over each line for a given task.
for line in input_stream:

    #Pulls out job number, creates a new dictionary for it.
    if "jobnumber" in line:
        tmp = line.split()[1]
        if tmp!=job_id:
            job_id=tmp
            jobs[job_id]={}
        else:
            continue

    #Finds the node used in computing.
    elif "hostname" in line and "=" not in line:
        hostname=line.split()[1]

    #Finds the task ID, and creates a dictionary for it containing hostname.
    elif "taskid" in line and "pe" not in line:
        task_id = int(line.split()[1])
        jobs[job_id][task_id]={"host":hostname}

    #Finds the number of slots/CPUs used, adds to the dictionary.
    elif "slots" in line:
        jobs[job_id][task_id]["NUM_CPU"] = int(line.split()[1])

    #Finds the runtime of computing, adds it to the dictionary.
    elif "wallclock" in line and "ru_" not in line:
        wallclock = float(line.split()[1])
        jobs[job_id][task_id]["wallclock"] = wallclock

    #Pulls out requested RAM for this task.
    elif "hard_resources" in line:
        reqs = line.split()[1].split(",")
        RAM=None
        for res in reqs:
            if "h_vmem" in res:
                request = res.split("=")[1]
                if "G" in request:
                    RAM = float(request[:-1])
                elif "M" in request:
                    RAM = float(request[:-1])/1000
        jobs[job_id][task_id]["RAM"] = RAM

    #Finds CPU time for this task, adds it to the dictionary.
    elif "cpu" in line:
        cpu_time = float(line.split()[1])
        jobs[job_id][task_id]["cpu"] = cpu_time

        #Uses the node name for this job to find the CPU that has been used (contains TDP and CPU values).
        cpu = cpu_info[node_info[hostname]]

        #Uses this information in our CPU energy and emissions functions. 
        jobs[job_id][task_id]["cpu_kWh"] = calc_cpu_kWh(cpu, cpu_time)
        jobs[job_id][task_id]["cpu_gCO2"] = calc_carbon_UK_in_g(jobs[job_id][task_id]["cpu_kWh"])

    #Finds the maximum memory used throughout the task, adds it to the dictionary. Checks whether this
    #value is provided in GB or MB, and converts to GB if needed.
    elif "maxvmem" in line:
        if 'G' in line:
            maxvmem = float(line.split()[1][:-1])
        elif 'M' in line:
            maxvmem = float(line.split()[1][:-1])/1000
        else:
            maxvmem = float(line.split()[1][:-1])
        jobs[job_id][task_id]["maxvmem"] = maxvmem

        #Uses this value to calculate energy use and emissions for memory, using our functions.
        jobs[job_id][task_id]["mem_kWh"] = calc_mem_kWh(maxvmem, wallclock)
        jobs[job_id][task_id]["mem_gCO2"] = calc_carbon_UK_in_g(jobs[job_id][task_id]["mem_kWh"])

#Iterate through data and generates total energy and emissions values for each job/task.
for job_id in jobs.keys():
    print("Job ID: "+ job_id)
    for taskid in jobs[job_id].keys():
        print("\t"+str(taskid)+": ")
        jobs[job_id][taskid]["kWh"] = jobs[job_id][taskid]["cpu_kWh"]+jobs[job_id][taskid]["mem_kWh"]
        jobs[job_id][taskid]["gCO2"] = jobs[job_id][taskid]["cpu_gCO2"]+jobs[job_id][taskid]["mem_gCO2"]
        print("\t\t kWh: {:4f}".format(jobs[job_id][taskid]["kWh"]))
        print("\t\t gCO2: {:4f}".format(jobs[job_id][taskid]["gCO2"]))

#Saves out the output file.
with open("Job_JSONs/calc_carbon_"+str(job_id)+".json","w") as fout:
    json.dump(jobs,fout,indent=2)
