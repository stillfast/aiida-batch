# Batch Workflow Report

**Workflow**: AbacusBandBatchWorkChain<83396>
**Status**: Finished [0]
**Report generated**: 2026-06-11 03:52:03

---

## 1. Exit Code Summary

| Pseudo | Alpha-U |
| --- | :---: |
| sg15_sz | [0](#child-83399) |

[⬇ Jump to child details](#2-child-workflow-details)

---

## 2. Child Workflow Details

### child-83399  <a id="child-83399"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `sg15_sz`  |  **Proto**: `Alpha-U`  |  **Exit**: `0`

```
🟢 AbacusBandWorkChain<83399> Finished [0]
    ├── 🟢 seekpath_structure_analysis<83401> Finished [0]
    ├── 🟢 AbacusBaseWorkChain<83408> Finished [0]
    ├── 🟢 AbacusBaseWorkChain<83470> Finished [0]
    └── 🟢 AbacusBaseWorkChain<83475> Finished [0]
```

- [AbacusCalculation<83414> details](#calc-83414)
- [AbacusCalculation<83478> details](#calc-83478)
- [AbacusCalculation<83484> details](#calc-83484)

---

## 3. Calculation Details

### calc-83414  <a id="calc-83414"></a>

**AbacusCalculation <83414>**

[⬆ Back to child details](#child-83399)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361794` |
| Walltime | 00:08:35 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/a0/2f/fc7b-f353-4468-b631-2cee89fb5216` |

**Report Logs:**

```
*** 83414 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 4 LOG MESSAGES:
+-> ERROR at 2026-06-11 11:36:49.627079+08:00
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
+-> ERROR at 2026-06-11 11:40:07.759100+08:00
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
+-> ERROR at 2026-06-11 11:41:07.816558+08:00
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
+-> WARNING at 2026-06-11 11:45:24.641418+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---

### calc-83478  <a id="calc-83478"></a>

**AbacusCalculation <83478>**

[⬆ Back to child details](#child-83399)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361866` |
| Walltime | 00:01:58 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/44/44/0207-4f6b-431b-8ebf-d349fcb7dab5` |

**Report Logs:**

```
*** 83478 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 1 LOG MESSAGES:
+-> WARNING at 2026-06-11 11:49:43.798249+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---

### calc-83484  <a id="calc-83484"></a>

**AbacusCalculation <83484>**

[⬆ Back to child details](#child-83399)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2361869` |
| Walltime | 00:03:14 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/7f/6f/542b-b16c-44a4-b590-62ffe4170dbc` |

**Report Logs:**

```
*** 83484 [sg15_sz_Alpha-U]: None
*** (empty scheduler output file)
*** (empty scheduler errors file)
*** 1 LOG MESSAGES:
+-> WARNING at 2026-06-11 11:51:02.111834+08:00
 | The following expected files are missing: ['OUT.aiida/STRU_ION_D']
```

---
