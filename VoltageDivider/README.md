# python3

VoltageDivider is a program to receive configuration for a multi-cell Battery, the A2D specs anduse them to 
select the best resistors for the VoltageDividers to sample the voltage at each stage, where a stage is the cumulative of preceding cells in series.(eg: 4.2, 8.4, 12.6, 16.8, 21.0, 25.2  would be represented by 6 stages). The load resistors are in parallel with zener diodes to protect the microcontroller a2d inputs. Selected resistors are tested for dissipated power to ensure that the circuit does not self-distroy due to overheating. The Zener is also tested to prevent zener distruction due to
excessive spillage current. There are two input files: one for 3.3 volt system, and the second for a 5.0 volt system.
The program is extensible for any number of cells, and appears to work for various cell voltages.
