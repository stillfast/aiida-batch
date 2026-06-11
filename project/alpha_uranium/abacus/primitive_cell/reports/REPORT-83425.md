# Batch Workflow Report

**Workflow**: AbacusBandBatchWorkChain<83425>
**Status**: Finished [0]
**Report generated**: 2026-06-11 03:51:57

---

## 1. Exit Code Summary

| Pseudo | Alpha-U |
| --- | :---: |
| sg15_sz | [0](#child-83428) |

[⬇ Jump to child details](#2-child-workflow-details)

---

## 2. Child Workflow Details

### child-83428  <a id="child-83428"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `sg15_sz`  |  **Proto**: `Alpha-U`  |  **Exit**: `0`

```
🟢 AbacusBandWorkChain<83428> Finished [0]
    ├── 🟢 seekpath_structure_analysis<83430> Finished [0]
    ├── 🟢 AbacusBaseWorkChain<83437> Finished [0]
    ├── 🟢 AbacusBaseWorkChain<83450> Finished [0]
    └── 🟢 AbacusBaseWorkChain<83455> Finished [0]
```

- [AbacusCalculation<83443> details](#calc-83443)
- [AbacusCalculation<83459> details](#calc-83459)
- [AbacusCalculation<83465> details](#calc-83465)

---

## 3. Calculation Details

### calc-83443  <a id="calc-83443"></a>

**AbacusCalculation <83443>**

[⬆ Back to child details](#child-83428)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361799` |
| Walltime | 00:07:54 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/cc/dc/4442-208f-4101-ab65-c1f9a6ca1262` |

**Report Logs:**

```
*** 83443 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 4 LOG MESSAGES:
+-> ERROR at 2026-06-11 11:36:49.620014+08:00
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 528, in _connect
 |     await options.waiter
 | asyncio.exceptions.CancelledError
 | 
 | During handling of the above exception, another exception occurred:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 456, in wait_for
 |     return fut.result()
 | asyncio.exceptions.CancelledError
 | 
 | The above exception was the direct cause of the following exception:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 207, in exponential_backoff_retry
 |     result = await coro()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/tasks.py", line 196, in do_update
 |     job_info = await cancellable.with_interrupt(update_request)
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 117, in with_interrupt
 |     result = await next(wait_iter)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 571, in _wait_for_one
 |     return f.result()  # May raise f.exception().
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 137, in _update_job_info
 |     self._jobs_cache = await self._get_jobs_from_scheduler()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 101, in _get_jobs_from_scheduler
 |     transport = await request
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/greenback/_impl.py", line 217, in _greenback_shim
 |     next_send = outcome.Value((yield next_yield))
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/transports.py", line 99, in do_open
 |     await transport.open_async()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/ssh_async.py", line 181, in open_async
 |     await self.async_backend.open()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/async_backend.py", line 234, in open
 |     self._conn = await asyncssh.connect(self.machine)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 9217, in connect
 |     return await asyncio.wait_for(
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 458, in wait_for
 |     raise exceptions.TimeoutError() from exc
 | asyncio.exceptions.TimeoutError
+-> ERROR at 2026-06-11 11:40:07.751724+08:00
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 528, in _connect
 |     await options.waiter
 | asyncio.exceptions.CancelledError
 | 
 | During handling of the above exception, another exception occurred:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 456, in wait_for
 |     return fut.result()
 | asyncio.exceptions.CancelledError
 | 
 | The above exception was the direct cause of the following exception:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 207, in exponential_backoff_retry
 |     result = await coro()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/tasks.py", line 196, in do_update
 |     job_info = await cancellable.with_interrupt(update_request)
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 117, in with_interrupt
 |     result = await next(wait_iter)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 571, in _wait_for_one
 |     return f.result()  # May raise f.exception().
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 137, in _update_job_info
 |     self._jobs_cache = await self._get_jobs_from_scheduler()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 101, in _get_jobs_from_scheduler
 |     transport = await request
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/greenback/_impl.py", line 217, in _greenback_shim
 |     next_send = outcome.Value((yield next_yield))
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/transports.py", line 99, in do_open
 |     await transport.open_async()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/ssh_async.py", line 181, in open_async
 |     await self.async_backend.open()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/async_backend.py", line 234, in open
 |     self._conn = await asyncssh.connect(self.machine)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 9217, in connect
 |     return await asyncio.wait_for(
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 458, in wait_for
 |     raise exceptions.TimeoutError() from exc
 | asyncio.exceptions.TimeoutError
+-> ERROR at 2026-06-11 11:41:07.809613+08:00
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 528, in _connect
 |     await options.waiter
 | asyncio.exceptions.CancelledError
 | 
 | During handling of the above exception, another exception occurred:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 456, in wait_for
 |     return fut.result()
 | asyncio.exceptions.CancelledError
 | 
 | The above exception was the direct cause of the following exception:
 | 
 | Traceback (most recent call last):
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 207, in exponential_backoff_retry
 |     result = await coro()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/tasks.py", line 196, in do_update
 |     job_info = await cancellable.with_interrupt(update_request)
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/utils.py", line 117, in with_interrupt
 |     result = await next(wait_iter)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 571, in _wait_for_one
 |     return f.result()  # May raise f.exception().
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 137, in _update_job_info
 |     self._jobs_cache = await self._get_jobs_from_scheduler()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/processes/calcjobs/manager.py", line 101, in _get_jobs_from_scheduler
 |     transport = await request
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/greenback/_impl.py", line 217, in _greenback_shim
 |     next_send = outcome.Value((yield next_yield))
 |   File "/home/liguozhou/install/aiida-core/src/aiida/engine/transports.py", line 99, in do_open
 |     await transport.open_async()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/ssh_async.py", line 181, in open_async
 |     await self.async_backend.open()
 |   File "/home/liguozhou/install/aiida-core/src/aiida/transports/plugins/async_backend.py", line 234, in open
 |     self._conn = await asyncssh.connect(self.machine)
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/site-packages/asyncssh/connection.py", line 9217, in connect
 |     return await asyncio.wait_for(
 |   File "/home/liguozhou/install/miniconda3/envs/aiida/lib/python3.10/asyncio/tasks.py", line 458, in wait_for
 |     raise exceptions.TimeoutError() from exc
 | asyncio.exceptions.TimeoutError
+-> WARNING at 2026-06-11 11:45:19.182657+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---

### calc-83459  <a id="calc-83459"></a>

**AbacusCalculation <83459>**

[⬆ Back to child details](#child-83428)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361867` |
| Walltime | 00:01:58 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/bb/6b/c4cd-12c6-4790-bd53-e86f01ccc4d7` |

**Report Logs:**

```
*** 83459 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 1 LOG MESSAGES:
+-> WARNING at 2026-06-11 11:49:41.998745+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---

### calc-83465  <a id="calc-83465"></a>

**AbacusCalculation <83465>**

[⬆ Back to child details](#child-83428)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361868` |
| Walltime | 00:03:58 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/10/d2/9f34-f648-4363-8304-caab56b4bd51` |

**Report Logs:**

```
*** 83465 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 1 LOG MESSAGES:
+-> WARNING at 2026-06-11 11:51:05.324639+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---
