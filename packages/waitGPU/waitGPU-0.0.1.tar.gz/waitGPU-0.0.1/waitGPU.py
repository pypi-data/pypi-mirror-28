import os
import gpustat
import time

def util_sat(gpu, util): 
    """ Return true if the gpu utilization is at most util """
    return float(gpu.entry['utilization.gpu']) <= util

def mem_ratio_sat(gpu, mem_ratio): 
    """ Return true if the memory utilization is at most mem_ratio """
    r = float(gpu.entry['memory.used'])/float(gpu.entry['memory.total'])
    return r <= mem_ratio

def avail_mem_sat (gpu, mem): 
    """ Return true if there is at least mem available memory """
    avail_mem = float(gpu.entry['memory.total'])-float(gpu.entry['memory.used'])
    return mem <= avail_mem

def wait(utilization=None, memory_ratio=None, available_memory=None,
         interval=10):
    print("waitGPU: Waiting for the following conditions, checking every {} seconds. "
          .format(interval))
    conditions = []
    if utilization is not None: 
        conditions.append(lambda gpu: util_sat(gpu, utilization))
        print("waitGPU: utilization <= {}".format(utilization))
    if memory_ratio is not None: 
        conditions.append(lambda gpu: mem_ratio_sat(gpu, memory_ratio))
        print("waitGPU: memory_ratio <= {}".format(memory_ratio))
    if available_memory is not None: 
        conditions.append(lambda gpu: avail_mem_sat(gpu, available_memory))
        print("waitGPU: available_memory >= {}".format(available_memory))

    free_gpu_id = None
    while free_gpu_id is None: 
        stats = gpustat.GPUStatCollection.new_query()
        for gpu in stats: 
            if all(c(gpu) for c in conditions):
                free_gpu_id = int(gpu.entry['index'])
                break
        if free_gpu_id is None: 
            time.sleep(interval)

    print("waitGPU: Setting GPU to: {}".format(free_gpu_id))
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = str(free_gpu_id)
