# waitGPU

A small Python library that waits for GPU conditions to be satisfied, and then
setting `CUDA_VISIBLE_DEVICES`
to the qualifying GPU on multi-GPU systems.

# Installation

`pip install waitGPU`

# Usage

 Use this library before any import that will use a GPU like `torch` or
 `tensorflow`.

```python
import waitGPU
waitGPU.wait(utilization=50, memory_ratio=0.5, available_memory=300,
             interval=10)
```
Specifying keyword arguments to `wait` will determine the criteria to wait for: 
+ `utilization` will wait until GPU utilization is at most the given value
+ `memory_ratio` will wait until the GPU memory utilization is at most the
  given value
+ `available_memory` will wait until the available memory is at least the
  given value
+ `interval` is the number of seconds to wait before checking conditions

# Dependencies

+ [Jongwook Choi's](https://wook.kr) [gpustat](https://github.com/wookayin/gpustat) library.

# Licensing

This code is in the public domain.
