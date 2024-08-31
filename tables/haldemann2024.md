| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| models_haldemann2024 | C0, C1, R0, R1, etc.  | Core mass fraction |
| T_out_haldemann2024 | 50, 300, 800, 1500, or 2000 | Outer boundary temperature (K) |
| colors_haldemann2024 | Any color | Colors of each model |

**Notes**: The pressure at which the integration of the internal structure was started was always set to 1 mbar. It is possible that for some combinations no transit radius is provided. This is the case if the radius of the planet is so big that the outermost layers would not be bound to the planet, for example,in the case of very small masses, high equilibrium temperatures and volatile rich compositions.

Below you can find all the possible models from Haldemann et al. (2024) available in *mr-plotter*. Table extracted from [https://github.com/mnijh/BICEPS_mass_radius](https://github.com/mnijh/BICEPS_mass_radius).

| Model | w<sub>Core</sub> | w<sub>Rock</sub> | w<sub>H<sub>2</sub>O</sub> | w<sub>H/He</sub> | x<sub>Fe,Core</sub> | x<sub>S,Core</sub> | x<sub>MgO,Mantle</sub> | x<sub>SiO<sub>2</sub>,Mantle</sub> | x<sub>FeO,Mantle</sub> |
| ----- | ---------------- | ---------------- | -------------------------- | ---------------- | ------------------- | ------------------ | ---------------------- | ---------------------------------- | ---------------------- |
| C0    | 1                | 0                | 0                          | 0                | 1                   | 0                  | N/A                    | N/A                                | N/A                    |
| C1    | 1                | 0                | 0                          | 0                | 0.87                | 0.13               | N/A                    | N/A                                | N/A                    |
| R0    | 0                | 1                | 0                          | 0                | N/A                 | N/A                | 1                      | 0                                  | 0                      |
| R1    | 0                | 1                | 0                          | 0                | N/A                 | N/A                | 0.5                    | 0.5                                | 0                      |
| R2    | 0                | 1                | 0                          | 0                | N/A                 | N/A                | 0.519                  | 0.423                              | 0.058                  |
| E0    | 0.32             | 0.68             | 0                          | 0                | 0.87                | 0.13               | 0.519                  | 0.423                              | 0.058                  |
| W0    | 0                | 0                | 1                          | 0                | N/A                 | N/A                | N/A                    | N/A                                | N/A                    |
| W1    | 0.3168           | 0.6732           | 0.01                       | 0                | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| W2    | 0.304            | 0.646            | 0.05                       | 0                | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| W3    | 0.288            | 0.612            | 0.1                        | 0                | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| W4    | 0.16             | 0.34             | 0.5                        | 0                | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| D0    | 0.319968         | 0.679932         | 0                          | 0.0001           | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| D1    | 0.31968          | 0.67932          | 0                          | 0.001            | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| D2    | 0.3168           | 0.6732           | 0                          | 0.01             | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| D3    | 0.288            | 0.612            | 0                          | 0.1              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| D4    | 0.256            | 0.544            | 0                          | 0.2              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N0    | 0.316768         | 0.673132         | 0.01                       | 0.0001           | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N1    | 0.31648          | 0.67252          | 0.01                       | 0.001            | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N2    | 0.3136           | 0.6664           | 0.01                       | 0.01             | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N3    | 0.2848           | 0.6052           | 0.01                       | 0.1              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N4    | 0.2528           | 0.5372           | 0.01                       | 0.2              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N5    | 0.287968         | 0.611932         | 0.1                        | 0.0001           | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N6    | 0.28768          | 0.61132          | 0.1                        | 0.001            | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N7    | 0.2848           | 0.6052           | 0.1                        | 0.01             | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N8    | 0.256            | 0.544            | 0.1                        | 0.1              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
| N9    | 0.224            | 0.476            | 0.1                        | 0.2              | 1                   | 0                  | 0.5                    | 0.5                                | 0                      |
