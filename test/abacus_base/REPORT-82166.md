# Batch Workflow Report

**Workflow**: AbacusBatchSubmitWorkChain<82166>
**Status**: Finished [301]
**Report generated**: 2026-06-10 03:10:13

---

## 1. Exit Code Summary

| Pseudo | BCC | FCC | Alpha-U | XO2 |
| --- | :---: | :---: | :---: | :---: |
| UO/hl-nr-pbe | [0](#child-82171) | [0](#child-82176) | [300](#child-82186) | [300](#child-82181) |
| UO/hl-fr-pz | [0](#child-82191) | [0](#child-82196) | [300](#child-82206) | [0](#child-82201) |

[⬇ Jump to child details](#2-child-workflow-details)

---

## 2. Child Workflow Details

### child-82171  <a id="child-82171"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `BCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82171> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82208> Finished [0]
    └── 🟢 [AbacusCalculation<82212>](#calc-82212) Finished [0]
```

- [AbacusCalculation<82212> details](#calc-82212)

---

### child-82176  <a id="child-82176"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `FCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82176> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82217> Finished [0]
    └── 🟢 [AbacusCalculation<82221>](#calc-82221) Finished [0]
```

- [AbacusCalculation<82221> details](#calc-82221)

---

### child-82186  <a id="child-82186"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `Alpha-U`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82186> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82234> Finished [0]
    ├── 🟡 [AbacusCalculation<82238>](#calc-82238) Finished [301]
    └── 🟡 [AbacusCalculation<82283>](#calc-82283) Finished [301]
```

- [AbacusCalculation<82238> details](#calc-82238)
- [AbacusCalculation<82283> details](#calc-82283)

---

### child-82181  <a id="child-82181"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-nr-pbe`  |  **Proto**: `XO2`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82181> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82226> Finished [0]
    ├── 🟡 [AbacusCalculation<82230>](#calc-82230) Finished [301]
    └── 🟡 [AbacusCalculation<82278>](#calc-82278) Finished [301]
```

- [AbacusCalculation<82230> details](#calc-82230)
- [AbacusCalculation<82278> details](#calc-82278)

---

### child-82191  <a id="child-82191"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `BCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82191> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82242> Finished [0]
    └── 🟢 [AbacusCalculation<82246>](#calc-82246) Finished [0]
```

- [AbacusCalculation<82246> details](#calc-82246)

---

### child-82196  <a id="child-82196"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `FCC`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82196> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82251> Finished [0]
    └── 🟢 [AbacusCalculation<82255>](#calc-82255) Finished [0]
```

- [AbacusCalculation<82255> details](#calc-82255)

---

### child-82206  <a id="child-82206"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `Alpha-U`  |  **Exit**: `300`

```
🟡 AbacusBaseWorkChain<82206> Finished [300]
    ├── 🟢 create_kpoints_from_distance<82269> Finished [0]
    ├── 🟡 [AbacusCalculation<82273>](#calc-82273) Finished [301]
    └── 🟡 [AbacusCalculation<82288>](#calc-82288) Finished [301]
```

- [AbacusCalculation<82273> details](#calc-82273)
- [AbacusCalculation<82288> details](#calc-82288)

---

### child-82201  <a id="child-82201"></a>

[⬆ Back to exit code table](#1-exit-code-summary)

**Pseudo**: `UO/hl-fr-pz`  |  **Proto**: `XO2`  |  **Exit**: `0`

```
🟢 AbacusBaseWorkChain<82201> Finished [0]
    ├── 🟢 create_kpoints_from_distance<82260> Finished [0]
    └── 🟢 [AbacusCalculation<82264>](#calc-82264) Finished [0]
```

- [AbacusCalculation<82264> details](#calc-82264)

---

## 3. Calculation Details

### calc-82212  <a id="calc-82212"></a>

**AbacusCalculation <82212>**

[⬆ Back to child details](#child-82171)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342023` |
| Walltime | 00:09:03 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/2a/78/c743-d9da-4469-8798-2aa5512f594e` |

**Report Logs:**

```
2026-06-10 11:09:22 [37210 | REPORT]: [82171|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82212> iteration #1
```

---

### calc-82221  <a id="calc-82221"></a>

**AbacusCalculation <82221>**

[⬆ Back to child details](#child-82176)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342024` |
| Walltime | 00:58:40 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/ff/17/0855-e271-4093-8ac1-0ddb0168cd8f` |

**Report Logs:**

```
2026-06-10 11:09:24 [37211 | REPORT]: [82176|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82221> iteration #1
```

---

### calc-82238  <a id="calc-82238"></a>

**AbacusCalculation <82238>**

[⬆ Back to child details](#child-82186)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342025` |
| Walltime | 02:00:00 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/1d/ea/b2a4-5a04-4788-81f4-bc59f372a661` |

**Report Logs:**

```
2026-06-10 11:09:42 [37228 | REPORT]: [82186|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82238> failed but a handler dealt with the problem, restarting
2026-06-10 11:09:42 [37226 | REPORT]: [82186|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82238> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:28 [37213 | REPORT]: [82186|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82238> iteration #1
```

---

### calc-82283  <a id="calc-82283"></a>

**AbacusCalculation <82283>**

[⬆ Back to child details](#child-82186)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342025` |
| Walltime | 02:00:00 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/1d/ea/b2a4-5a04-4788-81f4-bc59f372a661` |

**Report Logs:**

```
2026-06-10 11:09:46 [37246 | REPORT]: [82186|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82283> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:09:46 [37244 | REPORT]: [82186|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82283> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:43 [37229 | REPORT]: [82186|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82283> iteration #2
```

---

### calc-82230  <a id="calc-82230"></a>

**AbacusCalculation <82230>**

[⬆ Back to child details](#child-82181)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342032` |
| Walltime | 02:00:20 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/21/7f/2811-32ca-4dcb-bdf0-7bc9721b0e31` |

**Report Logs:**

```
2026-06-10 11:09:40 [37224 | REPORT]: [82181|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82230> failed but a handler dealt with the problem, restarting
2026-06-10 11:09:40 [37222 | REPORT]: [82181|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82230> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:26 [37212 | REPORT]: [82181|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82230> iteration #1
```

---

### calc-82278  <a id="calc-82278"></a>

**AbacusCalculation <82278>**

[⬆ Back to child details](#child-82181)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342032` |
| Walltime | 02:00:20 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/21/7f/2811-32ca-4dcb-bdf0-7bc9721b0e31` |

**Report Logs:**

```
2026-06-10 11:09:46 [37242 | REPORT]: [82181|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82278> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:09:46 [37240 | REPORT]: [82181|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82278> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:41 [37225 | REPORT]: [82181|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82278> iteration #2
```

---

### calc-82246  <a id="calc-82246"></a>

**AbacusCalculation <82246>**

[⬆ Back to child details](#child-82191)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342026` |
| Walltime | 00:10:14 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/51/55/c04c-56b5-47b6-ad79-28a6a762bf3e` |

**Report Logs:**

```
2026-06-10 11:09:30 [37214 | REPORT]: [82191|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82246> iteration #1
```

---

### calc-82255  <a id="calc-82255"></a>

**AbacusCalculation <82255>**

[⬆ Back to child details](#child-82196)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342029` |
| Walltime | 00:42:44 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/3a/a0/1ef4-c61a-459a-b0ea-d8c062046698` |

**Report Logs:**

```
2026-06-10 11:09:32 [37215 | REPORT]: [82196|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82255> iteration #1
```

---

### calc-82273  <a id="calc-82273"></a>

**AbacusCalculation <82273>**

[⬆ Back to child details](#child-82206)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342031` |
| Walltime | 02:00:22 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/40/80/0203-37c0-44b6-adf3-1aa816398f1b` |

**Report Logs:**

```
2026-06-10 11:09:44 [37238 | REPORT]: [82206|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82273> failed but a handler dealt with the problem, restarting
2026-06-10 11:09:44 [37236 | REPORT]: [82206|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82273> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:36 [37217 | REPORT]: [82206|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82273> iteration #1
```

---

### calc-82288  <a id="calc-82288"></a>

**AbacusCalculation <82288>**

[⬆ Back to child details](#child-82206)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342031` |
| Walltime | 02:00:22 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/40/80/0203-37c0-44b6-adf3-1aa816398f1b` |

**Report Logs:**

```
2026-06-10 11:09:47 [37250 | REPORT]: [82206|AbacusBaseWorkChain|inspect_process]: AbacusCalculation<82288> failed but a handler detected an unrecoverable problem, aborting
2026-06-10 11:09:47 [37248 | REPORT]: [82206|AbacusBaseWorkChain|report_error_handled]: AbacusCalculation<82288> failed with exit status 301: Calculation did not complete successfully - 'Total Time' not found at end of running log.
2026-06-10 11:09:45 [37239 | REPORT]: [82206|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82288> iteration #2
```

---

### calc-82264  <a id="calc-82264"></a>

**AbacusCalculation <82264>**

[⬆ Back to child details](#child-82201)

| Property | Value |
| --- | --- |
| Scheduler JobID | `2342033` |
| Walltime | 01:27:05 |
| Remote Path | `/sh3/ysuanbase/home/yeesuan17910/aiida_data/yeesuan_0324/3c/c0/1c70-ec27-4f4d-8879-16720c78b123` |

**Report Logs:**

```
2026-06-10 11:09:34 [37216 | REPORT]: [82201|AbacusBaseWorkChain|run_process]: launching AbacusCalculation<82264> iteration #1
```

---
