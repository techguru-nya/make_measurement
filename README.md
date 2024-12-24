# Measurement File (.cfg) Creation Tool
This project provides a tool for creating measurement files (`.cfg`) by processing signals from various sources. 

## Features
- Reads all signals from an A2L file.
- Removes unnecessary signals based on user-defined keywords.
- Adds required signals from a PLT file.

## Requirements
- Python
- JupyterLab

## How to Use
1. Open `main.ipynb`.
2. Set the paths for the following files in the notebook:
   - A2L file
   - PLT file
3. Define the keywords for removing unnecessary signals.
4. Run all cells in the notebook.

## Workflow
1. **Read A2L Signals**:  
   Extract all signals from the provided A2L file.
2. **Filter Signals**:  
   Remove unnecessary signals based on user-defined keywords.
3. **Add PLT Signals**:  
   Add additional required signals from the PLT file.
4. **Generate .cfg File**:  
   Compile the processed signals into a `.cfg` measurement file.

## Results
The tool generates a `.cfg` file with the finalized list of signals based on the filtering and addition criteria.
