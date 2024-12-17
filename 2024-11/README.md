# November 2024: Beside the Point

## Overview

This Rust program runs a **Monte Carlo simulation** to determine the probability that randomly generated blue and red points have a **perpendicular bisector** that intersects the **closest side** to the blue point. The simulation is **multi-threaded** for efficiency, dividing the trials equally across threads. Results are logged to a file and displayed on the console, providing an estimated probability.


## Code Structure

The project consists of the following files:

- **`main.rs`**: The entry point for the program. It:
  - Parses input arguments.
  - Manages threading and workload distribution.
  - Aggregates results and calculates probabilities.
- **`lib.rs`**: Contains the core logic, including:
  - `has_solution`: Determines if the perpendicular bisector of two points intersects the closest side.
  - Additional supporting functions and structures.


## Usage

1. **Build the Project**  
   Ensure you have Rust installed. Compile the program using:
   ```bash
   cargo build --release
   ```

2. **Run the Simulation**  
   Execute the program with a single integer argument `n`, which determines the number of trials (`10^n`):
   ```bash
   ./target/release/<your_program_name> 6
   ```
   or more simply: 
   ```bash
   cargo run --release 6
   ```


   - Replace `6` with your desired exponent. For example:
     - `6` -> `1,000,000` iterations
     - `7` -> `10,000,000` iterations

3. **Output**  
   - The final **estimated probability** is printed to the console.  
   - Logs with detailed information are saved in the `log/` directory with a timestamped file name.

## Example Output

### Console Output:
```bash
0.4913861
```

### Log File Example (`log/2024-11-06T12:00:00.log`):
```
2024-11-06 12:00:00 INFO - Start
2024-11-06 12:00:00 INFO - Results 4913861
2024-11-06 12:00:00 INFO - Trials 10000000
2024-11-06 12:00:00 INFO - 0.4913861
```