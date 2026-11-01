# Legacy task catalog: rules v2 / seed 0

This historical offline series is separate from the current 36-case benchmark.
See the [series guide](README.md) for its provenance and limitations.

Uppercase letters identify stations; lowercase letters identify material types. Entries to the right of each arrow specify slots 1, 2 and 3, not an execution order.
Types a-f are red, blue, green, orange, purple and cyan cubes; g-l are spheres in the same color order.
Each present station starts with three items of its corresponding type. Items of the same color and shape are interchangeable.
The 3-6-arm cases retain the agreed orders; 7-12-arm cases balance demand across minimum handover distances over the entire scene.
Complete seed-1 and seed-2 orders are under the corresponding environment in `configs/tasks/cube_transport`; see `references/summary.csv` for the summary.
This catalog is for human review. A policy should receive only its assigned task file at startup.

## Serial and parallel counts

A phase is pick-and-clear or place-and-clear. One station visit has two phases; h handovers require h+1 visits, so the total is 2×Σ(h+1) phases.
Serial execution performs one phase per round; parallel execution can perform several nonconflicting phases. Total work is unchanged. These counts are not MuJoCo integration steps, tool calls or elapsed seconds.
The checked parallel reference is a feasible upper bound. Optimality in this abstract model is proven only when it meets the fixed-route lower bound; otherwise the optimum lies between the lower bound and the reference.

| Arms | Serial phases | Parallel reference rounds | Fixed-route lower bound | Reference speedup |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 38 | 16 | 16 | 2.375 |
| 4 | 60 | 16 | 16 | 3.75 |
| 5 | 74 | 18 | 16 | 4.111 |
| 6 | 96 | 20 | 18 | 4.8 |
| 7 | 106 | 22 | 20 | 4.818 |
| 8 | 144 | 26 | 20 | 5.538 |
| 9 | 160 | 26 | 22 | 6.154 |
| 10 | 204 | 36 | 30 | 5.667 |
| 11 | 230 | 32 | 26 | 7.188 |
| 12 | 284 | 38 | 28 | 7.474 |

Below are the complete seed-0 orders and per-arm workloads, including relay work on the fixed reference routes.


## 3 arms: line-03-v2-seed0

```text
A ← a, c, c
B ← b, a, c
C ← a, b, b
```

Scene-wide minimum handovers → demand count: 0 → 2, 1 → 4, 2 → 3.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | red cube | green cube | green cube | 10 |
| B | blue cube | red cube | green cube | 16 |
| C | red cube | blue cube | blue cube | 12 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 4 arms: ring-04-v2-seed0

```text
A ← b, c, c
B ← b, d, d
C ← a, a, d
D ← a, b, c
```

Scene-wide minimum handovers → demand count: 0 → 1, 1 → 4, 2 → 7.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | blue cube | green cube | green cube | 16 |
| B | blue cube | orange cube | orange cube | 14 |
| C | red cube | red cube | orange cube | 14 |
| D | red cube | blue cube | green cube | 16 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 5 arms: ring-05-v2-seed0

```text
A ← b, d, e
B ← b, d, d
C ← a, a, e
D ← c, c, e
E ← a, b, c
```

Scene-wide minimum handovers → demand count: 0 → 1, 1 → 6, 2 → 8.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | blue cube | orange cube | purple cube | 14 |
| B | blue cube | orange cube | orange cube | 14 |
| C | red cube | red cube | purple cube | 16 |
| D | green cube | green cube | purple cube | 16 |
| E | red cube | blue cube | green cube | 14 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 6 arms: ring-06-v2-seed0

```text
A ← c, d, e
B ← a, a, c
C ← b, f, f
D ← b, d, e
E ← a, b, d
F ← c, e, f
```

Scene-wide minimum handovers → demand count: 0 → 2, 1 → 7, 2 → 4, 3 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | green cube | orange cube | purple cube | 16 |
| B | red cube | red cube | green cube | 18 |
| C | blue cube | cyan cube | cyan cube | 16 |
| D | blue cube | orange cube | purple cube | 14 |
| E | red cube | blue cube | orange cube | 16 |
| F | green cube | purple cube | cyan cube | 16 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 7 arms: ring-07-v2-seed0

```text
A ← a, e, g
B ← a, b, g
C ← a, c, f
D ← d, d, f
E ← b, c, f
F ← c, e, g
G ← b, d, e
```

Scene-wide minimum handovers → demand count: 0 → 5, 1 → 5, 2 → 6, 3 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | red cube | purple cube | red sphere | 14 |
| B | red cube | blue cube | red sphere | 12 |
| C | red cube | green cube | cyan cube | 12 |
| D | orange cube | orange cube | cyan cube | 16 |
| E | blue cube | green cube | cyan cube | 20 |
| F | green cube | purple cube | red sphere | 18 |
| G | blue cube | orange cube | purple cube | 14 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 8 arms: ring-08-v2-seed0

```text
A ← a, b, e
B ← b, c, g
C ← d, e, f
D ← d, h, h
E ← a, e, g
F ← c, f, h
G ← b, c, d
H ← a, f, g
```

Scene-wide minimum handovers → demand count: 0 → 5, 1 → 5, 2 → 4, 3 → 5, 4 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | red cube | blue cube | purple cube | 18 |
| B | blue cube | green cube | red sphere | 16 |
| C | orange cube | purple cube | cyan cube | 18 |
| D | orange cube | blue sphere | blue sphere | 20 |
| E | red cube | purple cube | red sphere | 18 |
| F | green cube | cyan cube | blue sphere | 18 |
| G | blue cube | green cube | orange cube | 18 |
| H | red cube | cyan cube | red sphere | 18 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 9 arms: ring-09-v2-seed0

```text
A ← a, c, f
B ← c, d, g
C ← c, f, h
D ← d, d, i
E ← b, b, i
F ← e, f, g
G ← a, e, i
H ← a, e, g
I ← b, h, h
```

Scene-wide minimum handovers → demand count: 0 → 5, 1 → 6, 2 → 6, 3 → 5, 4 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | red cube | green cube | cyan cube | 18 |
| B | green cube | orange cube | red sphere | 18 |
| C | green cube | cyan cube | blue sphere | 18 |
| D | orange cube | orange cube | green sphere | 14 |
| E | blue cube | blue cube | green sphere | 14 |
| F | purple cube | cyan cube | red sphere | 16 |
| G | red cube | purple cube | green sphere | 18 |
| H | red cube | purple cube | red sphere | 22 |
| I | blue cube | blue sphere | blue sphere | 22 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 10 arms: ring-10-v2-seed0

```text
A ← a, c, j
B ← a, b, c
C ← f, i, j
D ← f, h, i
E ← e, g, g
F ← b, f, i
G ← b, e, h
H ← c, d, e
I ← d, d, h
J ← a, g, j
```

Scene-wide minimum handovers → demand count: 0 → 5, 1 → 6, 2 → 5, 3 → 5, 4 → 4, 5 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | red cube | green cube | orange sphere | 16 |
| B | red cube | blue cube | green cube | 18 |
| C | cyan cube | green sphere | orange sphere | 18 |
| D | cyan cube | blue sphere | green sphere | 20 |
| E | purple cube | red sphere | red sphere | 28 |
| F | blue cube | cyan cube | green sphere | 30 |
| G | blue cube | purple cube | blue sphere | 26 |
| H | green cube | orange cube | purple cube | 20 |
| I | orange cube | orange cube | blue sphere | 14 |
| J | red cube | red sphere | orange sphere | 14 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 11 arms: ring-11-v2-seed0

```text
A ← f, g, j
B ← c, d, e
C ← b, c, g
D ← a, h, i
E ← d, e, j
F ← g, i, j
G ← b, c, f
H ← f, h, k
I ← a, e, i
J ← a, b, h
K ← d, k, k
```

Scene-wide minimum handovers → demand count: 0 → 6, 1 → 5, 2 → 5, 3 → 6, 4 → 6, 5 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | cyan cube | red sphere | orange sphere | 16 |
| B | green cube | orange cube | purple cube | 18 |
| C | blue cube | green cube | red sphere | 22 |
| D | red cube | blue sphere | green sphere | 22 |
| E | orange cube | purple cube | orange sphere | 22 |
| F | red sphere | green sphere | orange sphere | 26 |
| G | blue cube | green cube | cyan cube | 26 |
| H | cyan cube | blue sphere | purple sphere | 22 |
| I | red cube | purple cube | green sphere | 20 |
| J | red cube | blue cube | blue sphere | 18 |
| K | orange cube | purple sphere | purple sphere | 18 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.

## 12 arms: ring-12-v2-seed0

```text
A ← b, f, h
B ← g, h, l
C ← b, i, j
D ← b, c, g
E ← a, f, g
F ← e, f, l
G ← a, c, k
H ← e, e, h
I ← d, i, j
J ← a, d, l
K ← c, k, k
L ← d, i, j
```

Scene-wide minimum handovers → demand count: 0 → 5, 1 → 6, 2 → 5, 3 → 5, 4 → 5, 5 → 5, 6 → 5.

| Arm | Slot 1 | Slot 2 | Slot 3 | Reference phases for this arm |
| --- | --- | --- | --- | ---: |
| A | blue cube | cyan cube | blue sphere | 26 |
| B | red sphere | blue sphere | cyan sphere | 28 |
| C | blue cube | green sphere | orange sphere | 26 |
| D | blue cube | green cube | red sphere | 24 |
| E | red cube | cyan cube | red sphere | 28 |
| F | purple cube | cyan cube | cyan sphere | 28 |
| G | red cube | green cube | purple sphere | 20 |
| H | purple cube | purple cube | blue sphere | 16 |
| I | orange cube | green sphere | orange sphere | 18 |
| J | red cube | orange cube | cyan sphere | 22 |
| K | green cube | purple sphere | purple sphere | 24 |
| L | orange cube | green sphere | orange sphere | 24 |

Arm phase counts include relay work. Serial and parallel references perform the same total work; overlap and waiting differ.
