# Batch Workflow Report

**Workflow**: AbacusBatchSubmitWorkChain<82698>
**Status**: Finished [301]
**Report generated**: 2026-06-10 03:55:20

---

## 1. Exit Code Summary

| Pseudo | BCC | FCC | Alpha-U | XO2 |
| --- | :---: | :---: | :---: | :---: |
| UO/hl-nr-pbe | [0](#child-82703) | [0](#child-82708) | [300](#child-82718) | [300](#child-82713) |
| UO/hl-fr-pz | [0](#child-82723) | [0](#child-82728) | [300](#child-82738) | [0](#child-82733) |

[⬇ Jump to child details](#2-child-workflow-details)

---

## 2. Child Workflow Details

### child-82703  <a id="child-82703"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `BCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82703> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82740> Finished [0]
    └── 🟢 [AbacusCalculation<82744>](#calc-82744) Finished [0]
```

- [AbacusCalculation<82744> details](#calc-82744)

---

### child-82708  <a id="child-82708"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `FCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82708> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82749> Finished [0]
    └── 🟢 [AbacusCalculation<82753>](#calc-82753) Finished [0]
```

- [AbacusCalculation<82753> details](#calc-82753)

---

### child-82718  <a id="child-82718"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `Alpha-U`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82718> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82766> Finished [0]
    ├── 🟡 [AbacusCalculation<82770>](#calc-82770) Finished [301]
    └── 🟡 [AbacusCalculation<82815>](#calc-82815) Finished [301]
```

- [AbacusCalculation<82770> details](#calc-82770)
- [AbacusCalculation<82815> details](#calc-82815)

---

### child-82713  <a id="child-82713"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `XO2`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82713> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82758> Finished [0]
    ├── 🟡 [AbacusCalculation<82762>](#calc-82762) Finished [301]
    └── 🟡 [AbacusCalculation<82810>](#calc-82810) Finished [301]
```

- [AbacusCalculation<82762> details](#calc-82762)
- [AbacusCalculation<82810> details](#calc-82810)

---

### child-82723  <a id="child-82723"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `BCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82723> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82774> Finished [0]
    └── 🟢 [AbacusCalculation<82778>](#calc-82778) Finished [0]
```

- [AbacusCalculation<82778> details](#calc-82778)

---

### child-82728  <a id="child-82728"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `FCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82728> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82783> Finished [0]
    └── 🟢 [AbacusCalculation<82787>](#calc-82787) Finished [0]
```

- [AbacusCalculation<82787> details](#calc-82787)

---

### child-82738  <a id="child-82738"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `Alpha-U`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82738> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82801> Finished [0]
    ├── 🟡 [AbacusCalculation<82805>](#calc-82805) Finished [301]
    └── 🟡 [AbacusCalculation<82820>](#calc-82820) Finished [301]
```

- [AbacusCalculation<82805> details](#calc-82805)
- [AbacusCalculation<82820> details](#calc-82820)

---

### child-82733  <a id="child-82733"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `XO2`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82733> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82792> Finished [0]
    └── 🟢 [AbacusCalculation<82796>](#calc-82796) Finished [0]
```

- [AbacusCalculation<82796> details](#calc-82796)

---

## 3. Calculation Details

### calc-82744  <a id="calc-82744"></a>

**AbacusCalculation <82744>**

[⬆ Back to child details](#child-82703)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342023` |
| Walltime | 00:09:03 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/2a/78/c743-d9da-4469-8798-2aa5512f594e` |

**Report Logs:**

```
2026-06-10 11:54:26 [37382 | REPORT]: [82703|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82744> iteration #1
```

---

### calc-82753  <a id="calc-82753"></a>

**AbacusCalculation <82753>**

[⬆ Back to child details](#child-82708)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342024` |
| Walltime | 00:58:40 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/ff/17/0855-e271-4093-8ac1-0ddb0168cd8f` |

**Report Logs:**

```
2026-06-10 11:54:28 [37383 | REPORT]: [82708|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82753> iteration #1
```

---

### calc-82770  <a id="calc-82770"></a>

**AbacusCalculation <82770>**

[⬆ Back to child details](#child-82718)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342025` |
| Walltime | 02:00:00 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/1d/ea/b2a4-5a04-4788-81f4-bc59f372a661` |

**Report Logs:**

```
2026-06-10 11:54:45 [37400 | REPORT]: [82718|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82770> failed but a handler dealt with the problem, restarting
2026-06-10 11:54:45 [37398 | REPORT]: [82718|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82770> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:32 [37385 | REPORT]: [82718|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82770> iteration #1
```

---

### calc-82815  <a id="calc-82815"></a>

**AbacusCalculation <82815>**

[⬆ Back to child details](#child-82718)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342025` |
| Walltime | 02:00:00 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/1d/ea/b2a4-5a04-4788-81f4-bc59f372a661` |

**Report Logs:**

```
2026-06-10 11:54:50 [37418 | REPORT]: [82718|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82815> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:54:50 [37416 | REPORT]: [82718|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82815> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:46 [37401 | REPORT]: [82718|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82815> iteration #2
```

---

### calc-82762  <a id="calc-82762"></a>

**AbacusCalculation <82762>**

[⬆ Back to child details](#child-82713)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342032` |
| Walltime | 02:00:20 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/21/7f/2811-32ca-4dcb-bdf0-7bc9721b0e31` |

**Report Logs:**

```
2026-06-10 11:54:44 [37396 | REPORT]: [82713|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82762> failed but a handler dealt with the problem, restarting
2026-06-10 11:54:44 [37394 | REPORT]: [82713|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82762> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:30 [37384 | REPORT]: [82713|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82762> iteration #1
```

---

### calc-82810  <a id="calc-82810"></a>

**AbacusCalculation <82810>**

[⬆ Back to child details](#child-82713)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342032` |
| Walltime | 02:00:20 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/21/7f/2811-32ca-4dcb-bdf0-7bc9721b0e31` |

**Report Logs:**

```
2026-06-10 11:54:50 [37414 | REPORT]: [82713|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82810> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:54:49 [37412 | REPORT]: [82713|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82810> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:45 [37397 | REPORT]: [82713|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82810> iteration #2
```

---

### calc-82778  <a id="calc-82778"></a>

**AbacusCalculation <82778>**

[⬆ Back to child details](#child-82723)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342026` |
| Walltime | 00:10:14 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/51/55/c04c-56b5-47b6-ad79-28a6a762bf3e` |

**Report Logs:**

```
2026-06-10 11:54:34 [37386 | REPORT]: [82723|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82778> iteration #1
```

---

### calc-82787  <a id="calc-82787"></a>

**AbacusCalculation <82787>**

[⬆ Back to child details](#child-82728)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342029` |
| Walltime | 00:42:44 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/3a/a0/1ef4-c61a-459a-b0ea-d8c062046698` |

**Report Logs:**

```
2026-06-10 11:54:36 [37387 | REPORT]: [82728|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82787> iteration #1
```

---

### calc-82805  <a id="calc-82805"></a>

**AbacusCalculation <82805>**

[⬆ Back to child details](#child-82738)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342031` |
| Walltime | 02:00:22 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/40/80/0203-37c0-44b6-adf3-1aa816398f1b` |

**Report Logs:**

```
2026-06-10 11:54:47 [37410 | REPORT]: [82738|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82805> failed but a handler dealt with the problem, restarting
2026-06-10 11:54:47 [37408 | REPORT]: [82738|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82805> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:39 [37389 | REPORT]: [82738|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82805> iteration #1
```

---

### calc-82820  <a id="calc-82820"></a>

**AbacusCalculation <82820>**

[⬆ Back to child details](#child-82738)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342031` |
| Walltime | 02:00:22 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/40/80/0203-37c0-44b6-adf3-1aa816398f1b` |

**Report Logs:**

```
2026-06-10 11:54:50 [37422 | REPORT]: [82738|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82820> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:54:50 [37420 | REPORT]: [82738|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82820> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:54:48 [37411 | REPORT]: [82738|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82820> iteration #2
```

---

### calc-82796  <a id="calc-82796"></a>

**AbacusCalculation <82796>**

[⬆ Back to child details](#child-82733)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342033` |
| Walltime | 01:27:05 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/3c/c0/1c70-ec27-4f4d-8879-16720c78b123` |

**Report Logs:**

```
2026-06-10 11:54:38 [37388 | REPORT]: [82733|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82796> iteration #1
```

---
